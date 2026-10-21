# -*- coding: utf-8 -*-
"""
O "lago temporario" do segundo deslizamento (USGS us7000tc90, 28,3281 N 85,4798 E) no Sentinel-1 RTC (gamma0 VV),
que ve atraves de nuvem e cobre a janela de 26/08 a 08/09/2026 sem imagem optica.

Agua parada = superficie lisa = queda forte de VV. Pixel de agua nova: VV antes > -15 dB (nao era sombra de relevo nem
agua), VV depois < -18 dB e queda > 5 dB, na mesma orbita. Ruido: o mesmo teste num par de antes do evento.
Regioes: ate 2 km do ponto do tc90; vale do Lhende Khola (28,30-28,36 N, 85,45-85,52 E); e o deposito do Sentinel-2.
Saidas em data/processed/cicatriz_lago/ (s1_lago.json, s1_lago.png).
"""
import json
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from comum import stac_busca, pc_assina, ler_janela, reamostra_para, PC

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
SAIDA = os.path.join(RAIZ, "data", "processed", "cicatriz_lago")
TC90 = (85.4798, 28.3281)
# por orbita relativa: (ruido_antes, antes, [depois...])
ORBITAS = {121: ("2026-08-07", "2026-08-19", ["2026-08-31", "2026-09-12"]),
           19: ("2026-08-12", "2026-08-24", ["2026-09-05", "2026-09-17"]),
           85: ("2026-08-04", "2026-08-16", ["2026-08-28", "2026-09-09"])}


def main():
    from affine import Affine
    from rasterio.crs import CRS
    from shapely.geometry import box, Point
    from shapely import vectorized
    from pyproj import Transformer
    m = np.load(os.path.join(SAIDA, "mascaras.npz"))
    dep = m["deposito"].astype(bool)
    tr = Affine.from_gdal(*m["transform"]); crs = CRS.from_user_input(str(m["crs"]))
    H, W = dep.shape
    xs = tr.c + tr.a * (np.arange(W) + 0.5); ys = tr.f + tr.e * (np.arange(H) + 0.5)
    X, Y = np.meshgrid(xs, ys)
    t = Transformer.from_crs(4326, crs, always_xy=True)
    perto = vectorized.contains(Point(*t.transform(*TC90)).buffer(2000.0), X, Y)
    xb0, yb0 = t.transform(85.45, 28.30); xb1, yb1 = t.transform(85.52, 28.36)
    vale = (X >= min(xb0, xb1)) & (X <= max(xb0, xb1)) & (Y >= min(yb0, yb1)) & (Y <= max(yb0, yb1))
    geom = box(85.44, 28.23, 85.61, 28.37)
    it = stac_busca(PC, ["sentinel-1-rtc"], [85.46, 28.31, 85.50, 28.345], "2026-08-01/2026-09-20")
    por = {}
    for f in it:
        p = f["properties"]
        por[(p["sat:relative_orbit"], p["datetime"][:10])] = f
    px = abs(tr.a * tr.e) / 1e4
    cache = {}

    def vv(orb, dt):
        k = (orb, dt)
        if k not in cache:
            f = por.get(k)
            if f is None:
                cache[k] = None
            else:
                a, ta, ca, nd = ler_janela(pc_assina(f["assets"]["vv"]["href"], "sentinel-1-rtc"), geom, folga_m=0)
                a = a.astype(np.float32); a[(a <= 0) | ~np.isfinite(a)] = np.nan
                r = reamostra_para(np.nan_to_num(a, nan=0.0), ta, ca, (H, W), tr, crs, "average")
                r[r <= 0] = np.nan
                cache[k] = 10 * np.log10(r)
        return cache[k]

    def maior(mk):
        from scipy import ndimage
        lab, n = ndimage.label(mk, structure=np.ones((3, 3)))
        return float(ndimage.sum(mk, lab, range(1, n + 1)).max()) if n else 0.0

    def agua_nova(a, b):
        return (a > -15) & (b < -18) & (a - b > 5)

    res = {"criterio": "VV antes > -15 dB, VV depois < -18 dB, queda > 5 dB (mesma orbita)", "pares": []}
    mapas = []
    for orb, (r0, a0, depois) in ORBITAS.items():
        A0, A = vv(orb, r0), vv(orb, a0)
        if A is None:
            continue
        for rot, (x, y) in [("ruido " + r0 + " > " + a0, (A0, A))] + [(a0 + " > " + d, (A, vv(orb, d))) for d in depois]:
            if x is None or y is None:
                res["pares"].append({"orbita": orb, "par": rot, "sem": True}); continue
            w = agua_nova(x, y)
            ent = {"orbita": orb, "par": rot, "agua_nova_perto_tc90_ha": round(float((w & perto).sum() * px), 2),
                   "agua_nova_vale_ha": round(float((w & vale).sum() * px), 2),
                   "agua_nova_sobre_deposito_ha": round(float((w & dep).sum() * px), 2),
                   "dVV_mediana_deposito_dB": round(float(np.nanmedian((y - x)[dep])), 1),
                   "maior_mancha_perto_tc90_ha": round(maior(w & perto) * px, 2)}
            res["pares"].append(ent); print(ent, flush=True)
            if not rot.startswith("ruido"):
                mapas.append((orb, rot, x, y, w))
    json.dump(res, open(os.path.join(SAIDA, "s1_lago.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    figura(mapas, dep, X, Y, t)


def figura(mapas, dep, X, Y, t):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ext = (X.min(), X.max(), Y.min(), Y.max())
    n = len(mapas)
    fig, axs = plt.subplots(2, n, figsize=(3.6 * n, 7), sharex=True, sharey=True)
    axs = np.array(axs).reshape(2, n)
    xt, yt = t.transform(*TC90)
    for j, (orb, rot, a, b, w) in enumerate(mapas):
        h = axs[0, j].imshow(b - a, extent=ext, origin="upper", cmap="RdBu_r", vmin=-8, vmax=8, interpolation="nearest")
        axs[0, j].set_title("orb %d  %s\ndVV (dB)" % (orb, rot), fontsize=7)
        axs[1, j].imshow(b, extent=ext, origin="upper", cmap="gray", vmin=-22, vmax=2, interpolation="nearest")
        axs[1, j].imshow(np.ma.masked_where(~w, w), extent=ext, origin="upper", cmap="cool", interpolation="nearest")
        axs[1, j].set_title("VV depois (dB); agua nova em magenta", fontsize=7)
        for ax in axs[:, j]:
            ax.contour(X, Y, dep.astype(float), [0.5], colors="y", linewidths=0.6)
            ax.plot(xt, yt, "c^", ms=8, mec="k"); ax.set_xticks([]); ax.set_yticks([])
    fig.colorbar(h, ax=axs[0, :], shrink=0.8, label="dVV (dB)")
    fig.suptitle("Sentinel-1 RTC: agua nova depois do evento? (triangulo: us7000tc90; amarelo: deposito do Sentinel-2)", fontsize=9)
    fig.savefig(os.path.join(SAIDA, "s1_lago.png"), dpi=120)
    print(os.path.join(SAIDA, "s1_lago.png"))


if __name__ == "__main__":
    main()
