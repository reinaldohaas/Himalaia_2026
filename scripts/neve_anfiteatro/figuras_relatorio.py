# -*- coding: utf-8 -*-
"""
Figuras do relatorio multifonte:
  serie_fontes.png        fracao de neve/gelo (NDSI > 0,42) nos pixels observados do anfiteatro, por fonte,
                          cenas com >= 50 % do anfiteatro observado; Landsat/HLS marcados quando > 10 % dos pixels
                          observados tem SWIR negativo (correcao atmosferica fisicamente impossivel)
  mapa_s1_corredor.png    dVV medio das tres geometrias do Sentinel-1 nos pares que contem o colapso, com o
                          anfiteatro, o talvegue (marcas a cada 5 km) e o ponto de colapso
Uso: python figuras_relatorio.py <dir_dados>
"""
import json
import os
import sys
from datetime import datetime

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

COLAPSO_T = datetime(2026, 8, 26, 2, 52)


def serie(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    est = [("s2es", "Sentinel-2 L2A (Earth Search)", "o", "tab:blue", "espectral"),
           ("s2pc", "Sentinel-2 L2A (Planetary Computer)", "s", "tab:cyan", "espectral"),
           ("s2l1c", "Sentinel-2 L1C (topo da atmosfera)", "^", "tab:purple", "espectral"),
           ("hlss", "HLS S30 (LaSRC)", "D", "tab:olive", "estrita"),
           ("ls", "Landsat 8/9 C2 L2 (LaSRC)", "v", "tab:brown", "estrita"),
           ("modis", "MODIS MOD/MYD10A1 500 m", ".", "0.55", None)]
    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    for f, rot, mk, c, mas in est:
        p = os.path.join(d, "serie_%s.json" % f)
        if not os.path.exists(p):
            continue
        xs, ys, ruins = [], [], []
        for r in json.load(open(p)):
            if "erro" in r:
                continue
            a = r["regioes"]["anfiteatro"]
            e = a if mas is None else a.get(mas, a["estrita"])
            if (e.get("frac_obs") or 0) < 0.5 or e.get("frac_neve_42") is None:
                continue
            t = datetime.strptime(r["datetime"][:19], "%Y-%m-%dT%H:%M:%S")
            ruim = (e.get("frac_swir_neg") or 0) > 0.10
            (ruins if ruim else xs).append(t) if False else None
            if ruim:
                ruins.append((t, e["frac_neve_42"]))
            else:
                xs.append(t); ys.append(e["frac_neve_42"])
        ax.plot(xs, ys, mk, c=c, ms=4 if mk == "." else 6, mfc="none" if mk in "s^Dv" else c, label=rot, alpha=0.9 if mk != "." else 0.6)
        if ruins:
            ax.plot([x[0] for x in ruins], [x[1] for x in ruins], mk, c="red", ms=7, mfc="none", mew=1.4)
    ax.plot([], [], "o", c="red", mfc="none", label="Landsat/HLS com SWIR < 0 em > 10 % dos pixels (rejeitado)")
    ax.axvline(COLAPSO_T, c="r", lw=1); ax.text(COLAPSO_T, 1.02, " colapso 26/08 02:52", color="r", fontsize=8, va="bottom")
    ax.set_ylim(-0.03, 1.08); ax.set_ylabel("fração de neve/gelo nos pixels\nobservados do anfiteatro (NDSI > 0,42)")
    ax.grid(alpha=0.3); ax.legend(fontsize=7.5, ncol=2, loc="lower left")
    ax.set_title("Anfiteatro do Lhende Khola (3,41 km²): seis fontes, 01/07 a 18/10/2026 — cenas com ≥ 50 % do anfiteatro observado", fontsize=10)
    fig.autofmt_xdate(); fig.tight_layout(); __import__('figlang').prepara(fig); fig.savefig(__import__('figlang').caminho(os.path.join(d, "serie_fontes.png")), dpi=130)


def mapa(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.ndimage import uniform_filter
    from rasterio.transform import Affine
    from rasterio.crs import CRS
    from rasterio.warp import reproject, Resampling
    from pyproj import Transformer
    from shapely.geometry import shape
    z = np.load(os.path.join(d, "cubos_s1.npz"))
    orbs = {}
    for k in z.files:
        if k.endswith("__vv"):
            orb, dt = k.split("__")[:2]
            orbs.setdefault(orb, []).append((datetime.strptime(dt, "%Y-%m-%dT%H%M%S"), z[k].astype(np.float32), z[k[:-4] + "__T"]))
    crs = CRS.from_epsg(32645); ref = None; acc = []
    for orb, l in sorted(orbs.items()):
        l.sort(key=lambda x: x[0])
        for (ta, a, T), (tb, b, _) in zip(l[:-1], l[1:]):
            if ta < COLAPSO_T < tb:
                f = []
                for db in (a, b):
                    lin = np.where(np.isfinite(db), 10 ** (db / 10.0), 0.0); w = np.isfinite(db).astype(float)
                    m = uniform_filter(lin, 5) / np.maximum(uniform_filter(w, 5), 1e-6)
                    f.append(np.where(w > 0, 10 * np.log10(np.maximum(m, 1e-6)), np.nan))
                dd = (f[1] - f[0]).astype(np.float32)
                Ta = Affine(*T[:6])
                if ref is None:
                    ref = (Ta, dd.shape)
                    acc.append(dd)
                else:
                    r = np.full(ref[1], np.nan, np.float32)
                    reproject(dd, r, src_transform=Ta, src_crs=crs, dst_transform=ref[0], dst_crs=crs, resampling=Resampling.bilinear, src_nodata=np.nan, dst_nodata=np.nan)
                    acc.append(r)
    med = np.nanmean(np.array(acc), 0)
    T, shp = ref
    ext = (T.c, T.c + T.a * shp[1], T.f + T.e * shp[0], T.f)
    tr = Transformer.from_crs(4326, 32645, always_xy=True)
    an = shape(json.load(open(os.path.join(d, "anfiteatro.geojson")))["features"][0]["geometry"])
    g = an if an.geom_type == "Polygon" else max(an.geoms, key=lambda x: x.area)
    ax_, ay_ = tr.transform(*g.exterior.xy)
    tal = [f for f in json.load(open(os.path.join(d, "corredor.geojson")))["features"] if f["properties"]["nome"] == "talvegue_completo"][0]
    xy = np.array(tal["geometry"]["coordinates"]); dist = np.array(tal["properties"]["dist_m"])
    tx, ty = tr.transform(xy[:, 0], xy[:, 1])
    cx, cy = tr.transform(*comum.COLAPSO)
    fig, ax = plt.subplots(figsize=(11, 6.2))
    h = ax.imshow(med, extent=ext, cmap="RdBu", vmin=-5, vmax=5)
    ax.plot(ax_, ay_, "-", c="k", lw=1.0); ax.plot(tx, ty, "-", c="0.15", lw=0.7, alpha=0.8)
    for km in (5, 10, 15, 20, 25):
        k = int(np.argmin(abs(dist - km * 1000))); ax.plot(tx[k], ty[k], "o", c="k", ms=3); ax.text(tx[k], ty[k] + 300, "%d km" % km, fontsize=8, ha="center")
    ax.plot(cx, cy, "x", c="lime", ms=10, mew=2.5)
    ax.text(cx + 400, cy, "ponto de colapso", fontsize=8, color="darkgreen")
    ax.set_xlim(min(tx) - 2500, max(max(tx), max(ax_)) + 2500); ax.set_ylim(min(min(ty), min(ay_)) - 2000, max(ty) + 2500)
    ax.set_xticks([]); ax.set_yticks([])
    fig.colorbar(h, ax=ax, shrink=0.8, label="ΔVV médio das 3 geometrias (dB), pares de 12 dias com o colapso")
    ax.set_title("Sentinel-1D RTC: mudança de retroespalhamento entre ~16–24/08 e ~28/08–05/09 (azul = aumento)\n"
                 "contorno preto = anfiteatro (3,41 km²); linha = talvegue do Lhende Khola a partir do ponto de colapso", fontsize=9.5)
    fig.tight_layout(); __import__('figlang').prepara(fig); fig.savefig(__import__('figlang').caminho(os.path.join(d, "mapa_s1_corredor.png")), dpi=130)


if __name__ == "__main__":
    serie(sys.argv[1]); mapa(sys.argv[1]); print("ok")
