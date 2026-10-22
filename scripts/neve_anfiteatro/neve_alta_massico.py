# -*- coding: utf-8 -*-
"""
Mudanca de neve/gelo nas encostas altas do macico (Langtang Lirung e Tsangbu Ri), por faixa de altitude, entre
outubro de 2025 e outubro de 2026 (Sentinel-2, mesma orbita), com o par de 2025 como ruido.
Teste da hipotese do pesquisador (22/10/2026): a massa densa se acumulou no alto e escorregou ate a zona de ruptura.
Uma massa grande descendo do cume deixaria trilha: neve/gelo -> rocha ou rocha -> neve/detrito nas faixas altas.
Usa as mascaras e a grade de cicatriz_e_lago.py (mesmas cenas) e o GLO-30.
Saidas: data/processed/cicatriz_lago/neve_alta<sufixo>.json e .png
Uso: python neve_alta_massico.py [antes1,antes2 depois1,depois2 ruido_a,ruido_b sufixo]
  padrao: out/2025 x out/2026, ruido 13/10/2025 x 18/10/2025
"""
import json
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from comum import stac_busca, pc_assina, ler_janela, reamostra_para, PC
import cicatriz_e_lago as cl

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
SAIDA = os.path.join(RAIZ, "data", "processed", "cicatriz_lago")
FAIXAS = [(3500, 4500), (4500, 5000), (5000, 5500), (5500, 6000), (6000, 6500), (6500, 7300)]
CAIXA = (85.48, 28.24, 85.58, 28.30)    # flancos norte do Langtang Lirung e do Tsangbu Ri, acima da cicatriz


def main():
    if len(sys.argv) > 4:
        antes, depois = sys.argv[1].split(","), sys.argv[2].split(",")
        ruido, suf = sys.argv[3].split(","), sys.argv[4]
    else:
        antes, depois, ruido, suf = cl.ANTES, cl.DEPOIS, [cl.ANTES[0], cl.ANTES[1]], ""
    from shapely.geometry import box
    from pyproj import Transformer
    geom = box(*cl.AOI)
    todos = cl.itens("2025-07-01/2026-10-20")
    por = {}
    for f in todos:
        por.setdefault(f["properties"]["datetime"][:10], f)
    dados = {}
    for dt in sorted(set(antes + depois + ruido)):
        d, tr, crs = cl.le(por[dt], geom); dados[dt] = d
    C = {k: cl.classes(v) for k, v in dados.items()}
    H, W = dados[antes[0]]["B11"].shape
    glo = np.full((H, W), np.nan, np.float32)
    for f in stac_busca(PC, ["cop-dem-glo-30"], list(cl.AOI), "2000-01-01/2030-01-01"):
        a, ta, ca, nd = ler_janela(pc_assina(f["assets"]["data"]["href"], "cop-dem-glo-30"), geom, folga_m=500)
        r = reamostra_para(a, ta, ca, (H, W), tr, crs, "bilinear"); glo = np.where(r > 100, r, glo)
    xs = tr.c + tr.a * (np.arange(W) + 0.5); ys = tr.f + tr.e * (np.arange(H) + 0.5)
    X, Y = np.meshgrid(xs, ys)
    t = Transformer.from_crs(4326, crs, always_xy=True)
    x0, y0 = t.transform(CAIXA[0], CAIXA[1]); x1, y1 = t.transform(CAIXA[2], CAIXA[3])
    cx = (X >= min(x0, x1)) & (X <= max(x0, x1)) & (Y >= min(y0, y1)) & (Y <= max(y0, y1))
    px = abs(tr.a * tr.e) / 1e4

    def teste(a_lst, d_lst):
        ok = np.ones((H, W), bool); era_n = np.ones((H, W), bool); era_r = np.ones((H, W), bool)
        vir_r = np.ones((H, W), bool); vir_n = np.ones((H, W), bool)
        for k in a_lst:
            _, nu, ne, _, nn = C[k]; ok &= ~nu; era_n &= ne; era_r &= nn
        for k in d_lst:
            _, nu, ne, _, nn = C[k]; ok &= ~nu; vir_r &= nn; vir_n &= ne
        return ok, era_n & vir_r & ok, era_r & vir_n & ok
    ok, perda, ganho = teste(antes, depois)
    ok0, perda0, ganho0 = teste([ruido[0]], [ruido[1]])
    res = []
    for z0, z1 in FAIXAS:
        m = cx & (glo >= z0) & (glo < z1)
        res.append({"faixa_m": [z0, z1], "area_ha": round(float(m.sum() * px), 0),
                    "valida_%": round(float(100 * (ok & m).sum() / max(m.sum(), 1)), 0),
                    "neve_para_rocha_ha": round(float((perda & m).sum() * px), 1),
                    "rocha_para_neve_ha": round(float((ganho & m).sum() * px), 1),
                    "ruido_perda_ha": round(float((perda0 & m).sum() * px), 1),
                    "ruido_ganho_ha": round(float((ganho0 & m).sum() * px), 1)})
        print(res[-1], flush=True)
    json.dump({"caixa": CAIXA, "antes": antes, "depois": depois, "ruido": ruido, "faixas": res},
              open(os.path.join(SAIDA, "neve_alta%s.json" % suf), "w", encoding="utf-8"), indent=1)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ext = (X.min(), X.max(), Y.min(), Y.max())
    fig, axs = plt.subplots(1, 2, figsize=(13, 6), sharex=True, sharey=True)
    for ax, k in zip(axs, (antes[-1], depois[0])):
        d = dados[k]
        ax.imshow(np.clip(np.dstack([d["B12"], d["B08"], d["B04"]]) / 0.6, 0, 1), extent=ext, origin="upper")
        ax.contour(X, Y, glo, [5000, 6000, 7000], colors=["w", "y", "orange"], linewidths=0.6)
        ax.set_title(k + " (B12/B8/B4); contornos 5, 6 e 7 km", fontsize=9)
    cod = np.zeros((H, W), np.int8); cod[perda & cx] = 1; cod[ganho & cx] = 2
    axs[1].imshow(np.ma.masked_where(cod == 0, cod), extent=ext, origin="upper", interpolation="nearest",
                  cmap=matplotlib.colors.ListedColormap(["red", "yellow"]), vmin=0.5, vmax=2.5)
    for ax in axs:
        ax.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], "c--", lw=0.8)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Encostas altas do macico (caixa ciano): vermelho neve/gelo -> rocha, amarelo rocha -> neve/detrito claro "
                 "(antes %s x depois %s; ruido %s)" % (",".join(antes), ",".join(depois), ">".join(ruido)), fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(SAIDA, "neve_alta%s.png" % suf), dpi=120)
    print(os.path.join(SAIDA, "neve_alta%s.png" % suf))


if __name__ == "__main__":
    main()
