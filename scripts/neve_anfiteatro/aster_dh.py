# -*- coding: utf-8 -*-
"""
Variacao de altitude da cicatriz do Tsangbu Ri e do deposito, com o ASTER AST14DEM (30 m) contra o Copernicus GLO-30.

* DEMs ASTER: 16/06/2026 e 11/07/2026 (antes; controle de ruido) e 30/08/2026 (duas cenas, 4 dias depois do evento).
* Tudo na grade de 20 m de cicatriz_e_lago.py (UTM 45N), para usar a mascara do deposito do Sentinel-2.
* Alinhamento: deslocamento horizontal (busca em grade de +-90 m) e vertical (mediana) que minimizam a dispersao de dh
  no terreno estavel (fora do deposito + 300 m, fora de 2,5 km da cicatriz, declividade < 30 graus).
* Nuvens: o AST14DEM poe a nuvem no lugar do terreno. Pixels com |dh| > 4 NMAD + 30 m no terreno estavel ou
  |dh| > 150 m em qualquer lugar sao descartados, e a fracao descartada e informada.
Uso: python aster_dh.py [dir_aster]
"""
import glob
import json
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from comum import stac_busca, pc_assina, ler_janela, reamostra_para, PC

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
ASTER = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "data", "raw", "aster")
SAIDA = os.path.join(RAIZ, "data", "processed", "cicatriz_lago")
CICATRIZ = [(85.5225, 28.2830), (85.5300, 28.2870), (85.5300, 28.2950)]
DEMS = {"2026-06-16": "AST14DEM_00406162026032757", "2026-07-11": "AST14DEM_00407112026032205",
        "2026-08-30a": "AST14DEM_00408302026030907", "2026-08-30b": "AST14DEM_00408302026030916"}


def nmad(x):
    x = x[np.isfinite(x)]
    return 1.4826 * np.median(np.abs(x - np.median(x))) if x.size else np.nan


def main():
    import rasterio
    from affine import Affine
    from rasterio.crs import CRS
    from shapely.geometry import box, LineString
    from shapely import vectorized
    from pyproj import Transformer
    from scipy import ndimage
    m = np.load(os.path.join(SAIDA, "mascaras.npz"))
    dep = m["deposito"].astype(bool)
    tr = Affine.from_gdal(*m["transform"]); crs = CRS.from_user_input(str(m["crs"]))
    H, W = dep.shape
    xs = tr.c + tr.a * (np.arange(W) + 0.5); ys = tr.f + tr.e * (np.arange(H) + 0.5)
    X, Y = np.meshgrid(xs, ys)
    t = Transformer.from_crs(4326, crs, always_xy=True); ti = Transformer.from_crs(crs, 4326, always_xy=True)
    cic = LineString([t.transform(*p) for p in CICATRIZ])
    zona_cic = vectorized.contains(cic.buffer(600.0), X, Y) & ~dep        # cicatriz e entorno imediato
    longe_cic = ~vectorized.contains(cic.buffer(2500.0), X, Y)
    dep_folga = ndimage.binary_dilation(dep, iterations=15)               # 300 m
    lo0, la0 = ti.transform(X.min(), Y.max()); lo1, la1 = ti.transform(X.max(), Y.min())
    geom = box(min(lo0, lo1), min(la0, la1), max(lo0, lo1), max(la0, la1))
    it = stac_busca(PC, ["cop-dem-glo-30"], list(geom.bounds), "2000-01-01/2030-01-01")
    glo = np.zeros((H, W), np.float32); cnt = np.zeros((H, W), np.float32)
    for f in it:
        a, ta, ca, nd = ler_janela(pc_assina(f["assets"]["data"]["href"], "cop-dem-glo-30"), geom, folga_m=500)
        r = reamostra_para(a, ta, ca, (H, W), tr, crs, "bilinear")
        ok = r > 100
        glo[ok] += r[ok]; cnt[ok] += 1
    glo = np.where(cnt > 0, glo / np.maximum(cnt, 1), np.nan)
    gy, gx = np.gradient(glo, abs(tr.e), tr.a)
    decl = np.degrees(np.arctan(np.hypot(gx, gy)))
    estavel = longe_cic & ~dep_folga & (decl < 30) & np.isfinite(glo)
    px = abs(tr.a * tr.e)
    res = {"grade_m": abs(tr.a), "area_deposito_km2": round(float(dep.sum() * px / 1e6), 2),
           "area_zona_cicatriz_km2": round(float(zona_cic.sum() * px / 1e6), 2), "dems": {}}
    mapas = {}
    for nome, pref in DEMS.items():
        arqs = glob.glob(os.path.join(ASTER, pref + "*.tif"))
        if not arqs:
            print(nome, "sem arquivo"); continue
        with rasterio.open(arqs[0]) as s:
            a = s.read(1).astype(np.float32); ta, ca = s.transform, s.crs
        a[(a < 100) | (a > 9000)] = np.nan
        melhor = None
        for dx in range(-90, 91, 15):
            for dy in range(-90, 91, 15):
                tt = Affine(ta.a, ta.b, ta.c + dx, ta.d, ta.e, ta.f + dy)
                r = reamostra_para(np.nan_to_num(a, nan=-32768), tt, ca, (H, W), tr, crs, "bilinear")
                r[r < 100] = np.nan
                dh = r - glo
                s_ = dh[estavel & np.isfinite(dh) & (np.abs(dh) < 150)]
                if s_.size < 2000:
                    continue
                q = nmad(s_)
                if melhor is None or q < melhor[0]:
                    melhor = (q, dx, dy, float(np.median(s_)), dh)
        if melhor is None:
            print(nome, "sem sobreposicao util"); continue
        q, dx, dy, off, dh = melhor
        dh = dh - off
        valido = np.isfinite(dh) & (np.abs(dh) < 150)
        lim = 4 * q + 30
        ruim_est = estavel & valido & (np.abs(dh) > lim)
        dh[~valido] = np.nan
        dh[ruim_est] = np.nan
        mapas[nome] = dh

        def resumo(msk):
            v = dh[msk]; ok = np.isfinite(v)
            if ok.sum() < 20:
                return {"cobertura_%": round(100 * ok.mean(), 0) if msk.sum() else 0}
            return {"cobertura_%": round(float(100 * ok.mean()), 0), "mediana_m": round(float(np.nanmedian(v)), 1),
                    "media_m": round(float(np.nanmean(v)), 1), "nmad_m": round(float(nmad(v)), 1),
                    "volume_Mm3_area_valida": round(float(np.nansum(v) * px / 1e6), 1),
                    "volume_Mm3_extrapolado": round(float(np.nanmean(v) * msk.sum() * px / 1e6), 1)}
        res["dems"][nome] = {"deslocamento_m": [dx, dy], "offset_vertical_m": round(off, 1),
                             "nmad_estavel_m": round(float(q), 1),
                             "estavel_cobertura_%": round(float(100 * np.isfinite(dh[estavel]).mean()), 0),
                             "deposito": resumo(dep), "zona_cicatriz": resumo(zona_cic)}
        print(nome, json.dumps(res["dems"][nome], ensure_ascii=False), flush=True)
    json.dump(res, open(os.path.join(SAIDA, "aster_dh.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    figura(mapas, dep, cic, X, Y)


def figura(mapas, dep, cic, X, Y):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ext = (X.min(), X.max(), Y.min(), Y.max())
    ks = list(mapas)
    fig, axs = plt.subplots(1, len(ks), figsize=(5 * len(ks), 5.2), sharex=True, sharey=True)
    axs = np.atleast_1d(axs)
    for ax, k in zip(axs, ks):
        im = ax.imshow(mapas[k], extent=ext, origin="upper", cmap="RdBu", vmin=-80, vmax=80, interpolation="nearest")
        ax.contour(X, Y, dep.astype(float), [0.5], colors="k", linewidths=0.7)
        xx, yy = cic.xy; ax.plot(xx, yy, "m-", lw=2)
        ax.set_title("ASTER %s - GLO-30" % k, fontsize=9); ax.set_xticks([]); ax.set_yticks([])
    fig.colorbar(im, ax=axs, shrink=0.8, label="dh (m): azul = ganho, vermelho = perda")
    fig.suptitle("Variacao de altitude (ASTER AST14DEM alinhado ao GLO-30); contorno preto: deposito do Sentinel-2; "
                 "magenta: cicatriz (Adhikari et al.)", fontsize=10)
    fig.savefig(os.path.join(SAIDA, "aster_dh.png"), dpi=120)
    print(os.path.join(SAIDA, "aster_dh.png"))


if __name__ == "__main__":
    main()
