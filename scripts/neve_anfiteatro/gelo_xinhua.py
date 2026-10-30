# -*- coding: utf-8 -*-
"""
De onde saiu o gelo que aparece no quadro do Xinhua Video (copia do video de drone de Hei Mu, 26/08/2026).

No quadro, uma faixa branca desce de uma frente de gelo no alto de um paredao ate a nuvem de poeira. Este script
procura essa frente no Sentinel-2 L2A e no GLO-30:

* cenas limpas antes (12/08 e 24/08/2026) e depois (27/08 e 18/10/2026) do colapso, em torno do ponto do drone;
* gelo/neve antes (NDSI > 0,4 e NIR > 0,2) e o que deixou de ser gelo depois;
* frentes de gelo: borda de gelo com encosta > 40 graus logo abaixo (geleira suspensa sobre o paredao).

Uso: python gelo_xinhua.py baixa      (Planetary Computer; grava data/processed/gelo_xinhua/s2_*.npz)
     python gelo_xinhua.py analisa
"""
import json
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
SAIDA = os.path.join(RAIZ, "data", "processed", "gelo_xinhua")
TILE = os.path.join(RAIZ, "cluster", "wrf_lhende", "d04", "glo30_3s", "00001-00540.00001-00480")
S0, W0, RES, NX, NY = 28.08, 85.30, 3.0 / 3600.0, 540, 480
AOI = (85.48, 28.255, 85.575, 28.33)
P = (28.293985, 85.523964)
PETLEY = (28.2921, 85.5271)
VORTICE_E = (28.270, 85.535)
CICATRIZ = [(85.5225, 28.2830), (85.5300, 28.2870), (85.5300, 28.2950)]
DATAS = ["2026-08-12", "2026-08-24", "2026-08-27", "2026-10-18"]
BANDAS = ["B02", "B03", "B04", "B08", "B11", "SCL"]


def baixa():
    from shapely.geometry import box
    from comum import stac_busca, pc_assina, ler_janela, reamostra_para, PC
    os.makedirs(SAIDA, exist_ok=True)
    g = box(*AOI)
    for d in DATAS:
        it = stac_busca(PC, ["sentinel-2-l2a"], list(AOI), d + "T00:00:00Z/" + d + "T23:59:59Z")
        for item in it:
            nome = item["id"]
            f = os.path.join(SAIDA, "s2_%s.npz" % nome)
            if os.path.exists(f):
                continue
            a11, tr, crs, _ = ler_janela(pc_assina(item["assets"]["B11"]["href"]), g, folga_m=0)
            out = {}
            for b in BANDAS:
                a, t, c, _ = ler_janela(pc_assina(item["assets"][b]["href"]), g, folga_m=0)
                out[b] = a.astype(np.float32) if t == tr else reamostra_para(a, t, c, a11.shape, tr, crs,
                                                                            "nearest" if b == "SCL" else "average")
            for b in BANDAS[:-1]:
                out[b] = ((out[b] - 1000.0) / 10000.0).astype(np.float32)
            np.savez_compressed(f, transform=np.array(tr)[:6], crs=str(crs), datetime=item["properties"]["datetime"], **out)
            print("gravado", nome, a11.shape)


def cenas():
    fs = sorted(f for f in os.listdir(SAIDA) if f.startswith("s2_") and f.endswith(".npz"))
    return [(f, np.load(os.path.join(SAIDA, f))) for f in fs]


def dem():
    z = np.fromfile(TILE, ">i2").reshape(NY, NX).astype(float)        # linha 0 = sul
    lat = S0 + (np.arange(NY) + 0.5) * RES; lon = W0 + (np.arange(NX) + 0.5) * RES
    return lat, lon, z


def na_grade(d, lat, lon, z):
    """GLO-30 e lat/lon nos pixels de 20 m da cena"""
    from pyproj import Transformer
    from scipy.interpolate import RegularGridInterpolator
    a, b, c, dd, e, f = d["transform"]
    ny, nx = d["B11"].shape
    X = c + a * (np.arange(nx) + 0.5); Y = f + e * (np.arange(ny) + 0.5)
    XX, YY = np.meshgrid(X, Y)
    lo, la = Transformer.from_crs(str(d["crs"]), 4326, always_xy=True).transform(XX, YY)
    zz = RegularGridInterpolator((lat, lon), z, bounds_error=False)(np.c_[la.ravel(), lo.ravel()]).reshape(la.shape)
    return la, lo, zz, XX, YY


def classes(d):
    g, n, s = d["B03"], d["B08"], d["B11"]
    ndsi = (g - s) / np.maximum(g + s, 1e-3)
    nuvem = np.isin(d["SCL"], [0, 3, 8, 9, 10])
    gelo = (ndsi > 0.4) & (n > 0.20) & ~nuvem
    return ndsi, nuvem, gelo


def analisa():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy import ndimage
    lat, lon, z = dem()
    cs = cenas()
    ref = cs[0][1]
    la, lo, zz, XX, YY = na_grade(ref, lat, lon, z)
    dy, dx = np.gradient(zz, 20.0, 20.0)
    decl = np.degrees(np.arctan(np.hypot(dx, dy)))
    perto = np.hypot((la - P[0]) * 111.32, (lo - P[1]) * 111.32 * np.cos(np.radians(P[0]))) < 2.5
    r = {"cenas": []}
    por_data = {}
    for f, d in cs:
        if d["B11"].shape != ref["B11"].shape or not np.allclose(d["transform"], ref["transform"]):
            continue
        ndsi, nuvem, gelo = classes(d)
        nf = float(nuvem[perto].mean())
        r["cenas"].append({"id": f[3:-4], "datetime": str(d["datetime"]), "nuvem_ate_2_5km": round(nf, 2),
                           "gelo_ate_2_5km_ha": round(float((gelo & perto).sum()) * 0.04, 1)})
        dia = str(d["datetime"])[:10]
        if dia not in por_data or nf < por_data[dia][0]:
            por_data[dia] = (nf, d, gelo, nuvem)
    antes = [por_data[k] for k in ("2026-08-12", "2026-08-24") if k in por_data]
    depois = [por_data[k] for k in ("2026-08-27", "2026-10-18") if k in por_data]
    # gelo antes em pelo menos uma cena limpa antes, e nao-gelo (limpo) em todas as cenas limpas depois
    g_antes = np.zeros_like(zz, bool)
    for _, d, g, nv in antes:
        g_antes |= g
    sem_depois = np.ones_like(zz, bool); visto = np.zeros_like(zz, bool)
    for _, d, g, nv in depois:
        ndsi, nuvem, _ = classes(d)
        sem_depois &= (ndsi < 0.2) | nuvem
        visto |= ~nuvem
    perdeu = g_antes & sem_depois & visto & perto
    lab, n = ndimage.label(perdeu)
    manchas = []
    for k in range(1, n + 1):
        m = lab == k
        if m.sum() < 5:
            continue
        manchas.append({"ha": round(m.sum() * 0.04, 1), "lat": round(float(la[m].mean()), 4), "lon": round(float(lo[m].mean()), 4),
                        "cota_min_m": round(float(zz[m].min())), "cota_max_m": round(float(zz[m].max())),
                        "decl_media_graus": round(float(decl[m].mean()), 1)})
    manchas.sort(key=lambda m: -m["ha"])
    r["perda_de_gelo_24ago_para_27ago_18out"] = manchas[:10]
    # frentes de gelo: borda inferior do gelo de 24/08 com paredao (> 40 graus) logo abaixo, acima de 4,8 km
    g24 = por_data.get("2026-08-24", antes[-1])[2]
    borda = g24 & ~ndimage.binary_erosion(g24)
    abaixo = ndimage.maximum_filter(decl * ~g24, size=5) > 40
    frente = borda & abaixo & perto & (zz > 4800)
    lab, n = ndimage.label(ndimage.binary_dilation(frente, iterations=2))
    fr = []
    for k in range(1, n + 1):
        m = (lab == k) & frente
        if m.sum() < 8:
            continue
        fr.append({"pixels": int(m.sum()), "comprimento_km": round(m.sum() * 0.02, 2), "lat": round(float(la[m].mean()), 4),
                   "lon": round(float(lo[m].mean()), 4), "cota_media_m": round(float(zz[m].mean())),
                   "dist_ponto_drone_km": round(float(np.hypot((la[m].mean() - P[0]) * 111.32, (lo[m].mean() - P[1]) * 98.0)), 2)})
    fr.sort(key=lambda m: -m["pixels"])
    r["frentes_de_gelo_24ago"] = fr[:12]
    json.dump(r, open(os.path.join(SAIDA, "gelo_xinhua.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(r, indent=1, ensure_ascii=False))

    # figura: RGB antes e depois, perda de gelo, frentes, relevo
    rgb = lambda d: np.clip(np.dstack([d["B04"], d["B03"], d["B02"]]) * 2.2, 0, 1)
    ext = [lo.min(), lo.max(), la.min(), la.max()]
    pares = [("2026-08-24", "24/08 (antes)"), ("2026-08-27", "27/08 (depois)"), ("2026-10-18", "18/10")]
    fig, axs = plt.subplots(1, 4, figsize=(22, 6.2))
    for ax, (k, t) in zip(axs, pares):
        if k not in por_data:
            ax.axis("off"); continue
        ax.imshow(rgb(por_data[k][1]), extent=ext, origin="upper")
        ax.set_title("Sentinel-2 " + t, fontsize=10)
    ax = axs[3]
    ax.imshow(rgb(por_data.get("2026-08-24", antes[-1])[1]) * 0.6, extent=ext, origin="upper")
    ax.contour(lo, la, perdeu.astype(float), [0.5], colors="r", linewidths=1.2)
    ax.contour(lo, la, frente.astype(float), [0.5], colors="cyan", linewidths=1.0)
    ax.set_title("vermelho: gelo em 24/08 que sumiu depois\nciano: frentes de gelo sobre paredao > 40 graus", fontsize=9)
    for a in axs:
        a.contour(lo, la, zz, levels=np.arange(3500, 7500, 250), colors="k", linewidths=0.3, alpha=0.5)
        a.contour(lo, la, zz, levels=[5000, 6000], colors="y", linewidths=0.8)
        a.plot(*zip(*CICATRIZ), "m-", lw=2)
        a.plot(P[1], P[0], "*", color="yellow", ms=13, mec="k")
        a.plot(PETLEY[1], PETLEY[0], "o", color="orange", ms=6, mec="k")
        a.plot(VORTICE_E[1], VORTICE_E[0], "x", color="w", ms=9, mew=2)
        a.set_xlim(85.495, 85.56); a.set_ylim(28.265, 28.315)
        a.set_aspect(1 / np.cos(np.radians(P[0]))); a.tick_params(labelsize=7)
    fig.suptitle("Frente de gelo do quadro do Xinhua: estrela = ponto do drone; magenta = cicatriz (Adhikari et al.); "
                 "laranja = Petley; x = vortice do experimento E; curvas a cada 250 m (amarelo: 5 e 6 km)", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(SAIDA, "gelo_xinhua_mapa.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    modo = sys.argv[1]
    if modo == "baixa":
        baixa()
    elif modo == "analisa":
        analisa()
