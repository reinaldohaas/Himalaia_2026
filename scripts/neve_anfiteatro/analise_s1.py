# -*- coding: utf-8 -*-
"""
Sentinel-1 RTC (gamma0 VV, 10 m; independente de nuvem): mudanca de retroespalhamento nos pares de 12 dias da
mesma orbita. Os tres pares que contem o colapso (26/08 02:52 UTC) sao comparados com os pares sem evento da
mesma orbita (01/07 a 18/10), no anfiteatro e nos controles.

Filtro: media 5 x 5 pixels (50 m) em potencia linear antes da diferenca (reduz o speckle).
Metricas por regiao: fracao da area com dVV > +3 dB (aumento: superficie mais rugosa/seca, ex. deposito ou gelo
exposto) e < -3 dB (queda: neve molhada, superficie lisa); o par do evento e expresso em desvios-padrao da
distribuicao dos pares de referencia da mesma orbita. Pixels que mudam em >= 2 das 3 geometrias = mudanca robusta.
Uso: python analise_s1.py <dir_dados> <saida.png>
"""
import json
import os
import sys
from datetime import datetime

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402
import serie_multifonte as S  # noqa: E402

COLAPSO_T = datetime(2026, 8, 26, 2, 52)
LIM_DB = 3.0


def main(d, png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.ndimage import uniform_filter
    from rasterio.transform import Affine
    from rasterio.crs import CRS
    z = np.load(os.path.join(d, "cubos_s1.npz"))
    regs = S.regioes(d, corredor=True)
    orbs = {}
    for k in z.files:
        if k.endswith("__vv"):
            orb, dt = k.split("__")[:2]
            orbs.setdefault(orb, []).append((datetime.strptime(dt, "%Y-%m-%dT%H%M%S"), z[k].astype(np.float32), z[k[:-4] + "__T"]))
    crs = CRS.from_epsg(32645)
    out = {"pares": [], "evento": {}}
    mapas = {}
    for orb, l in sorted(orbs.items()):
        l.sort(key=lambda x: x[0])
        T0 = l[0][2]; shp = l[0][1].shape
        if any(x[1].shape != shp or not np.allclose(x[2], T0) for x in l):
            print("aviso: grades diferentes na orbita", orb)
        T = Affine(*T0[:6]); A = abs(T.a * T.e)
        masks = {k: comum.mascara(g, shp, T, crs) for k, g in regs.items()}
        filt = []
        for t, db, _ in l:
            lin = np.where(np.isfinite(db), 10 ** (db / 10.0), 0.0); w = np.isfinite(db).astype(float)
            m = uniform_filter(lin, 5) / np.maximum(uniform_filter(w, 5), 1e-6)
            filt.append((t, np.where(w > 0, 10 * np.log10(np.maximum(m, 1e-6)), np.nan)))
        for (ta, a), (tb, b) in zip(filt[:-1], filt[1:]):
            dd = b - a
            r = {"orbita": orb, "a": str(ta), "b": str(tb), "evento": bool(ta < COLAPSO_T < tb)}
            for k, m in masks.items():
                ok = m & np.isfinite(dd)
                r[k] = {"sobe": float((dd[ok] > LIM_DB).mean()), "desce": float((dd[ok] < -LIM_DB).mean()), "mediana_db": float(np.median(dd[ok]))}
            out["pares"].append(r)
            if r["evento"]:
                mapas[orb] = (dd, T, masks)
    for orb in sorted(orbs):
        ref = [p for p in out["pares"] if p["orbita"] == orb and not p["evento"]]
        ev = [p for p in out["pares"] if p["orbita"] == orb and p["evento"]]
        if not ev:
            continue
        ev = ev[0]; e = {"a": ev["a"], "b": ev["b"]}
        for k in regs:
            for q in ("sobe", "desce", "mediana_db"):
                v = np.array([p[k][q] for p in ref])
                e["%s_%s" % (k, q)] = round(ev[k][q], 4)
                e["%s_%s_ref_media" % (k, q)] = round(float(v.mean()), 4)
                e["%s_%s_ref_dp" % (k, q)] = round(float(v.std()), 4)
                e["%s_%s_z" % (k, q)] = round(float((ev[k][q] - v.mean()) / v.std()), 2) if v.std() > 0 else None
        e["n_ref"] = len(ref)
        out["evento"][orb] = e
        print(orb, "%s -> %s" % (ev["a"][:10], ev["b"][:10]), "| anf sobe %.3f (ref %.3f+-%.3f, z %s) desce %.3f (ref %.3f+-%.3f, z %s) | alto_fora sobe z %s desce z %s" % (
            e["anfiteatro_sobe"], e["anfiteatro_sobe_ref_media"], e["anfiteatro_sobe_ref_dp"], e["anfiteatro_sobe_z"],
            e["anfiteatro_desce"], e["anfiteatro_desce_ref_media"], e["anfiteatro_desce_ref_dp"], e["anfiteatro_desce_z"],
            e["alto_fora_sobe_z"], e["alto_fora_desce_z"]))
    # mudanca robusta: >= 2 das 3 geometrias, reamostradas para a grade da primeira
    from rasterio.warp import reproject, Resampling
    ks = sorted(mapas)
    if len(ks) >= 2:
        d0, T0, m0 = mapas[ks[0]]
        sobe = np.zeros(d0.shape); desce = np.zeros(d0.shape)
        for k in ks:
            dd, T, _ = mapas[k]
            r = np.full(d0.shape, np.nan, np.float32)
            reproject(dd.astype(np.float32), r, src_transform=T, src_crs=crs, dst_transform=T0, dst_crs=crs, resampling=Resampling.bilinear, src_nodata=np.nan, dst_nodata=np.nan)
            sobe += (r > LIM_DB); desce += (r < -LIM_DB)
        A0 = abs(T0.a * T0.e)
        for k, m in m0.items():
            out.setdefault("robusto", {})[k] = {"sobe_2de3_ha": round(float((m & (sobe >= 2)).sum() * A0 / 1e4), 2),
                                                 "desce_2de3_ha": round(float((m & (desce >= 2)).sum() * A0 / 1e4), 2),
                                                 "area_ha": round(float(m.sum() * A0 / 1e4), 1)}
        print("robusto (>= 2 de 3 geometrias):", out["robusto"])
        fig, axs = plt.subplots(1, len(ks) + 1, figsize=(4.2 * (len(ks) + 1), 4.4))
        from pyproj import Transformer
        cx, cy = Transformer.from_crs(4326, crs, always_xy=True).transform(*comum.COLAPSO)
        for c, k in enumerate(ks + ["robusto"]):
            ax = axs[c]
            if k == "robusto":
                im = np.where(sobe >= 2, 1.0, np.where(desce >= 2, -1.0, 0.0)); T = T0; m = m0["anfiteatro"]
                ax.imshow(im, cmap="bwr_r", vmin=-1.5, vmax=1.5, extent=(T.c, T.c + T.a * im.shape[1], T.f + T.e * im.shape[0], T.f))
                ax.set_title(">= 2 de 3 geometrias: azul sobe > 3 dB, vermelho desce", fontsize=8)
            else:
                dd, T, mm = mapas[k]; m = mm["anfiteatro"]
                h = ax.imshow(dd, cmap="RdBu", vmin=-6, vmax=6, extent=(T.c, T.c + T.a * dd.shape[1], T.f + T.e * dd.shape[0], T.f))
                e = out["evento"][k]; ax.set_title("%s  %s > %s  dVV (dB)" % (k, e["a"][5:10], e["b"][5:10]), fontsize=8)
            ax.contour(np.linspace(T.c, T.c + T.a * m.shape[1], m.shape[1]), np.linspace(T.f, T.f + T.e * m.shape[0], m.shape[0]), m.astype(float), levels=[0.5], colors="k", linewidths=0.8)
            ax.plot(cx, cy, "x", c="lime", ms=9, mew=2); ax.set_xticks([]); ax.set_yticks([])
        fig.colorbar(h, ax=axs[:len(ks)], shrink=0.7, label="dVV (dB)")
        fig.suptitle("Sentinel-1D RTC, pares de 12 dias que contêm o colapso (x verde); contorno = anfiteatro", fontsize=10)
        fig.savefig(png, dpi=120)
    json.dump(out, open(os.path.join(d, "analise_s1.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
