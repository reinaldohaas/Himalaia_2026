# -*- coding: utf-8 -*-
"""
Area de mudanca robusta do Sentinel-1 a leste do exutorio do anfiteatro (queda e aumento de retroespalhamento em
>= 2 das 3 geometrias, a <= 7 km do exutorio): recorte do dVV medio, cor verdadeira e falsa cor (B11-B8A-B04)
do Sentinel-2 antes (12/08) e depois (cenas limpas de setembro/outubro), com contornos das manchas do radar e
a fracao de neve (NDSI > 0,42, mascara espectral) dentro de cada mancha por data.
Uso: python candidato_fonte.py <dir_dados> <saida.png>
"""
import json
import os
import sys
from datetime import datetime

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402
import serie_multifonte as S  # noqa: E402

C = datetime(2026, 8, 26, 2, 52)
EXU = (85.5131, 28.2850)
DATAS = [("2026-08-12", "S2C"), ("2026-08-24", "S2A"), ("2026-09-28", None), ("2026-10-18", None)]


def f5(db):
    from scipy.ndimage import uniform_filter
    lin = np.where(np.isfinite(db), 10 ** (db / 10), 0); w = np.isfinite(db).astype(float)
    m = uniform_filter(lin, 5) / np.maximum(uniform_filter(w, 5), 1e-6)
    return np.where(w > 0, 10 * np.log10(np.maximum(m, 1e-6)), np.nan)


def main(d, png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.ndimage import label
    from rasterio.transform import Affine
    from rasterio.crs import CRS
    from rasterio.warp import reproject, Resampling
    from rasterio.features import shapes
    from pyproj import Transformer
    from shapely.geometry import shape, box, mapping
    from shapely.ops import unary_union
    z = np.load(os.path.join(d, "cubos_s1.npz")); orbs = {}
    for k in z.files:
        if k.endswith("__vv"):
            o, dt = k.split("__")[:2]
            orbs.setdefault(o, []).append((datetime.strptime(dt, "%Y-%m-%dT%H%M%S"), z[k].astype(np.float32), z[k[:-4] + "__T"]))
    crs = CRS.from_epsg(32645); ref = None; acc = []
    for o, l in sorted(orbs.items()):
        l.sort(key=lambda x: x[0])
        for (ta, a, T), (tb, b, _) in zip(l[:-1], l[1:]):
            if ta < C < tb:
                dd = (f5(b) - f5(a)).astype(np.float32); Ta = Affine(*T[:6])
                if ref is None:
                    ref = (Ta, dd.shape); acc.append(dd)
                else:
                    r = np.full(ref[1], np.nan, np.float32)
                    reproject(dd, r, src_transform=Ta, src_crs=crs, dst_transform=ref[0], dst_crs=crs, resampling=Resampling.bilinear, src_nodata=np.nan, dst_nodata=np.nan)
                    acc.append(r)
    acc = np.array(acc); T, shp = ref; med = np.nanmean(acc, 0)
    sob = (acc > 3).sum(0) >= 2; des = (acc < -3).sum(0) >= 2
    tf = Transformer.from_crs(4326, 32645, always_xy=True); ti = Transformer.from_crs(32645, 4326, always_xy=True)
    ex, ey = tf.transform(*EXU)
    jj, ii = np.mgrid[0:shp[0], 0:shp[1]]; gx = T.c + T.a * (ii + 0.5); gy = T.f + T.e * (jj + 0.5)
    perto = np.hypot(gx - ex, gy - ey) < 3500
    # mancha de queda principal e aumentos vizinhos (> 3 ha), poligonos em EPSG:4326
    polis = {}
    for nome, m in (("queda", des & perto), ("aumento", sob & perto)):
        lab, n = label(m, structure=np.ones((3, 3)))
        tam = np.bincount(lab.ravel())[1:] * abs(T.a * T.e) / 1e4
        gs = []
        for k in np.where(tam > 3)[0]:
            q = (lab == k + 1).astype(np.uint8)
            g = unary_union([shape(s) for s, v in shapes(q, mask=q.astype(bool), transform=T) if v == 1])
            from shapely.ops import transform as shtr
            gs.append((float(tam[k]), shtr(lambda x, y, z=None: ti.transform(x, y), g)))
        polis[nome] = gs
    allg = unary_union([g for v in polis.values() for _, g in v])
    caixa = allg.buffer(0.006).envelope
    # optico
    its = S.it_s2es(caixa)
    res = {"manchas": {n: [{"ha": round(a, 1), "centro": [round(g.centroid.x, 4), round(g.centroid.y, 4)]} for a, g in v] for n, v in polis.items()}, "neve": {}}
    fig, axs = plt.subplots(2, len(DATAS) + 1, figsize=(3.6 * (len(DATAS) + 1), 7.4))
    x0, y0, x1, y1 = caixa.bounds
    X0, Y0 = tf.transform(x0, y0); X1, Y1 = tf.transform(x1, y1)
    ax = axs[0, 0]
    ax.imshow(med, extent=(T.c, T.c + T.a * shp[1], T.f + T.e * shp[0], T.f), cmap="RdBu", vmin=-6, vmax=6)
    ax.set_title("S1: ΔVV médio (3 geometrias)", fontsize=9)
    axs[1, 0].axis("off")
    an = shape(json.load(open(os.path.join(d, "anfiteatro.geojson")))["features"][0]["geometry"])
    ga = an if an.geom_type == "Polygon" else max(an.geoms, key=lambda x: x.area)
    axx, axy = tf.transform(*ga.exterior.xy)
    def contornos(a):
        for nome, cor in (("queda", "red"), ("aumento", "blue")):
            for _, g in polis[nome]:
                gg = g if g.geom_type == "Polygon" else max(g.geoms, key=lambda x: x.area)
                px, py = tf.transform(*gg.exterior.xy); a.plot(px, py, "-", c=cor, lw=1.1)
        a.plot(axx, axy, "-", c="yellow", lw=0.9); a.plot(ex, ey, "o", c="k", mfc="yellow", ms=6)
        a.set_xlim(X0, X1); a.set_ylim(Y0, Y1); a.set_xticks([]); a.set_yticks([])
    contornos(ax)
    import rasterio
    from rasterio.windows import from_bounds
    for c, (dt, sat) in enumerate(DATAS, start=1):
        cand = [i for i in its if i["properties"]["datetime"][:10] == dt and (sat is None or i["id"].startswith(sat))]
        if not cand:
            continue
        it = cand[0]
        with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
            with rasterio.open(it["assets"]["visual"]["href"]) as s:
                w = from_bounds(X0, Y0, X1, Y1, s.transform).round_offsets().round_lengths()
                rgb = s.read(window=w, boundless=True).transpose(1, 2, 0)
        axs[0, c].imshow(rgb, extent=(X0, X1, Y0, Y1)); axs[0, c].set_title("%s %s cor verdadeira" % (dt, it["id"][:3]), fontsize=9)
        verde, swir, scl, Ts, crs2, meta = S.cena_s2es(it, caixa)
        a = it["assets"]
        b, T2, _, _ = S.ler_bandas({"swir": a["swir16"]["href"], "nir": a["nir08"]["href"], "red": a["red"]["href"]}, "swir", caixa)
        fc = np.clip(np.dstack([b["swir"], b["nir"], b["red"]]).astype(float) * 1e-4 / 0.8, 0, 1)
        axs[1, c].imshow(fc, extent=(T2.c, T2.c + T2.a * fc.shape[1], T2.f + T2.e * fc.shape[0], T2.f)); axs[1, c].set_title("falsa cor B11-B8A-B04", fontsize=9)
        ie, ib = S.inval_scl(scl, verde)
        with np.errstate(invalid="ignore", divide="ignore"):
            nd = (verde - swir) / (verde + swir)
        ies = ie | ((verde > 0.35) & (swir > 0.25) & ~(nd > 0.42)) | (verde <= 0.11)
        res["neve"][dt] = {}
        for nome in ("queda", "aumento"):
            for k, (ha, g) in enumerate(polis[nome]):
                m = comum.mascara(g, verde.shape, Ts, crs2); ok = m & ~ies & np.isfinite(nd)
                res["neve"][dt]["%s_%d_%.0fha" % (nome, k, ha)] = {"frac_obs": round(float(ok.sum() / max(m.sum(), 1)), 2),
                                                                   "frac_neve": round(float((nd[ok] > 0.42).mean()), 2) if ok.sum() > 10 else None,
                                                                   "verde_med": round(float(np.nanmedian(verde[m])), 3), "swir_med": round(float(np.nanmedian(swir[m])), 3)}
        for a_ in (axs[0, c], axs[1, c]):
            contornos(a_)
    fig.suptitle("Mudança robusta do Sentinel-1 a leste do exutório (círculo amarelo; contorno amarelo = anfiteatro): vermelho = queda > 3 dB, azul = aumento > 3 dB "
                 "em ≥ 2 das 3 geometrias", fontsize=9.5)
    fig.tight_layout(); __import__('figlang').prepara(fig); fig.savefig(__import__('figlang').caminho(png), dpi=130)
    json.dump(res, open(os.path.join(d, "candidato_fonte.json"), "w"), indent=1)
    json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"tipo": n, "ha": round(a, 1)}, "geometry": mapping(g)} for n, v in polis.items() for a, g in v]},
              open(os.path.join(d, "manchas_s1_exutorio.geojson"), "w"))
    print(json.dumps(res, indent=0)[:3000])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
