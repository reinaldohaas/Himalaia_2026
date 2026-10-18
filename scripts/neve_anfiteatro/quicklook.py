# -*- coding: utf-8 -*-
"""
Recortes em cor verdadeira (TCI 10 m do Sentinel-2 L2A, Earth Search) do anfiteatro nas datas que decidem a
mudanca em torno do colapso, com o contorno do anfiteatro, o ponto de colapso e os maiores aglomerados de perda
(analise_pares.py). Linha de baixo: classe neve/gelo (NDSI > 0,42) usada nos pares; cinza = nao observado.
Uso: python quicklook.py <dir_dados> <saida.png>
"""
import json
import os
import sys
from datetime import datetime

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402
import serie_multifonte as S  # noqa: E402

DATAS = [("2026-08-12", "S2C"), ("2026-08-24", "S2B"), ("2026-08-24", "S2A"), ("2026-08-27", "S2B"), ("2026-09-21", None), ("2026-10-18", None)]


def main(d, png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import rasterio
    from rasterio.windows import from_bounds
    from shapely.geometry import shape
    from pyproj import Transformer
    an = shape(json.load(open(os.path.join(d, "anfiteatro.geojson")))["features"][0]["geometry"])
    its = S.it_s2es(an.buffer(0.01).envelope)
    z = np.load(os.path.join(d, "mascaras_s2es.npz"))
    tr = Transformer.from_crs(4326, 32645, always_xy=True)
    ax_, ay_ = tr.transform(*an.exterior.xy) if an.geom_type == "Polygon" else tr.transform(*max(an.geoms, key=lambda g: g.area).exterior.xy)
    cx, cy = tr.transform(*comum.COLAPSO)
    x0, x1 = min(ax_) - 400, max(ax_) + 400; y0, y1 = min(ay_) - 400, max(ay_) + 400
    ags = {}
    for f in os.listdir(d):
        if f.startswith("aglomerado_") and f.endswith(".npy"):
            ags[f[11:-4]] = np.load(os.path.join(d, f))
    regT = None
    for k in z.files:
        if k.endswith("__T"):
            regT = z[k]; break
    fig, axs = plt.subplots(2, len(DATAS), figsize=(3.3 * len(DATAS), 7.2))
    for c, (dt, sat) in enumerate(DATAS):
        cand = [i for i in its if i["properties"]["datetime"][:10] == dt and (sat is None or i["id"].startswith(sat))]
        a0, a1 = axs[0, c], axs[1, c]
        if not cand:
            a0.set_title("%s %s: sem cena" % (dt, sat or "")); continue
        it = cand[0]
        with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
            with rasterio.open(it["assets"]["visual"]["href"]) as s:
                w = from_bounds(x0, y0, x1, y1, s.transform).round_offsets().round_lengths()
                rgb = s.read(window=w, boundless=True).transpose(1, 2, 0)
        ext = (x0, x1, y0, y1)
        a0.imshow(rgb, extent=ext)
        a0.plot(ax_, ay_, "-", c="yellow", lw=0.9); a0.plot(cx, cy, "x", c="red", ms=9, mew=2)
        a0.set_title("%s %s" % (dt, it["id"][:3]), fontsize=9)
        # classe neve das aquisicoes do dia
        kk = [k for k in z.files if k.endswith("__ndsiE") and k.split("_")[2] == dt.replace("-", "") and k.startswith(it["id"][:3])]
        if kk:
            nd = z[kk[0]].astype(float); T = z[kk[0][:-7] + "__T"]
            gx = T[2] + T[0] * (np.arange(nd.shape[1]) + 0.5); gy = T[5] + T[4] * (np.arange(nd.shape[0]) + 0.5)
            cl = np.where(np.isfinite(nd), (nd > 0.42).astype(float), np.nan)
            a1.imshow(np.where(np.isfinite(cl), np.nan, 1), extent=(gx[0], gx[-1], gy[-1], gy[0]), cmap="Greys", vmin=0, vmax=2.5)
            a1.imshow(cl, extent=(gx[0], gx[-1], gy[-1], gy[0]), cmap="Blues", vmin=-0.3, vmax=1.1)
            for nome, cor in (("E_C_12ago_27ago_S2C_S2B", "red"), ("E_A_12ago_24ago_S2C_S2A", "orange"), ("E_B_24ago_27ago_S2A_S2B", "magenta"), ("E_Z_24ago_S2B_S2A_15min_S2B_S2A", "cyan")):
                if nome in ags and ags[nome].shape == nd.shape:
                    for ax in (a0, a1):
                        ax.contour(gx, gy, ags[nome].astype(float), levels=[0.5], colors=cor, linewidths=1.0)
        a1.plot(ax_, ay_, "-", c="k", lw=0.8); a1.plot(cx, cy, "x", c="red", ms=9, mew=2)
        for ax in (a0, a1):
            ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_xticks([]); ax.set_yticks([])
    axs[1, 0].set_ylabel("neve/gelo (NDSI>0,42)\nsó SCL: azul escuro = neve, claro = sem neve, cinza = nuvem", fontsize=8)
    fig.suptitle("Anfiteatro do Lhende Khola (3,41 km², amarelo) — x vermelho = ponto de colapso (85,515E 28,271N)\n"
                 "contornos: maior aglomerado de perda 12/08>27/08 (vermelho), 12/08>24/08 (laranja), 24/08>27/08 mesma orbita (magenta), falsa perda em 15 min 24/08 S2B>S2A (ciano)", fontsize=10)
    fig.tight_layout(); fig.savefig(png, dpi=130)
    print("ok", png)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
