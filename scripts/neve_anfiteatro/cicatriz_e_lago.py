# -*- coding: utf-8 -*-
"""
Cicatriz da ruptura do Tsangbu Ri e o "lago temporario" do segundo deslizamento (USGS us7000tc90), no Sentinel-2 L2A.

* Pares na mesma epoca do ano e na mesma orbita relativa (passagem das ~04:47 UTC): outubro de 2025 (antes) e
  outubro de 2026 (depois). Assim a iluminacao e a neve sazonal sao as mesmas, e o par de 2025 entre si da o ruido.
* Cicatriz: pixels que eram neve/gelo nas duas cenas de antes e deixaram de ser nas duas de depois, a ate 2 km da
  cicatriz verificada em campo (Adhikari et al. 2026, Fig. 2). Tambem o inverso (rocha que virou neve/detrito claro).
* Lago: agua (NDSI = MNDWI > 0,1 com NIR baixo) no vale do Lhende Khola em torno do ponto do us7000tc90
  (28,3281 N, 85,4798 E), em todas as cenas pouco nubladas de ago-out de 2026 e de outubro de 2025.
Saidas em data/processed/cicatriz_lago/.
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
AOI = (85.45, 28.24, 85.60, 28.36)
CICATRIZ = [(85.5225, 28.2830), (85.5300, 28.2870), (85.5300, 28.2950)]   # lida na Fig. 2 de Adhikari et al.
TC90 = (85.4798, 28.3281)
ANTES = ["2025-10-13", "2025-10-18"]
DEPOIS = ["2026-10-13", "2026-10-18"]
BANDAS = ["B02", "B03", "B04", "B08", "B11", "B12", "SCL"]


def itens(datas="2025-10-01/2026-10-20"):
    it = stac_busca(PC, ["sentinel-2-l2a"], list(AOI), datas, {"eo:cloud_cover": {"lt": 70}})
    return [f for f in it if f["properties"]["datetime"][11:13] == "04" and f["properties"]["datetime"][14:16] in ("46", "47", "48")]


def le(item, geom):
    """todas as bandas na grade de 20 m do B11"""
    a11, tr, crs, _ = ler_janela(pc_assina(item["assets"]["B11"]["href"]), geom, folga_m=0)
    out = {}
    for b in BANDAS:
        a, t, c, _ = ler_janela(pc_assina(item["assets"][b]["href"]), geom, folga_m=0)
        out[b] = a.astype(np.float32) if (t == tr) else reamostra_para(a, t, c, a11.shape, tr, crs,
                                                                     "nearest" if b == "SCL" else "average")
    for b in BANDAS[:-1]:
        out[b] = (out[b] - 1000.0) / 10000.0 if item["properties"]["datetime"] >= "2022-01-25" else out[b] / 10000.0
    return out, tr, crs


def classes(d):
    g, n, s = d["B03"], d["B08"], d["B11"]
    ndsi = (g - s) / np.maximum(g + s, 1e-3)
    nuvem = np.isin(d["SCL"], [3, 8, 9, 10]) | (d["SCL"] == 0)
    neve = (ndsi > 0.4) & (n > 0.20) & ~nuvem
    ndwi = (g - n) / np.maximum(g + n, 1e-3)
    agua = (ndwi > 0.15) & (n < 0.12) & (s < 0.04) & (d["B12"] < 0.03) & (g > 0.03) & ~nuvem & (d["SCL"] != 2)
    nao_neve = (ndsi < 0.2) & ~nuvem
    return ndsi, nuvem, neve, agua, nao_neve


def main():
    from shapely.geometry import box, LineString, Point
    from pyproj import Transformer
    os.makedirs(SAIDA, exist_ok=True)
    geom = box(*AOI)
    todos = itens()
    por_data = {}
    for f in todos:
        por_data.setdefault(f["properties"]["datetime"][:10], f)
    print("cenas da passagem das 04:47:", ", ".join(sorted(por_data)))
    dados = {}
    for dt in sorted(set(ANTES + DEPOIS) | {k for k in por_data if k >= "2026-08-01"}):
        if dt not in por_data:
            print(dt, "sem cena"); continue
        d, tr, crs = le(por_data[dt], geom)
        dados[dt] = d
        print(dt, "lida", d["B11"].shape, flush=True)
    # grade e distancias
    H, W = dados[ANTES[0]]["B11"].shape
    xs = tr.c + tr.a * (np.arange(W) + 0.5); ys = tr.f + tr.e * (np.arange(H) + 0.5)
    X, Y = np.meshgrid(xs, ys)
    t = Transformer.from_crs(4326, crs, always_xy=True)
    cic = LineString([t.transform(*p) for p in CICATRIZ])
    from shapely import vectorized
    perto = vectorized.contains(cic.buffer(2000.0), X, Y)
    px = abs(tr.a * tr.e) / 1e4       # ha por pixel
    C = {k: classes(v) for k, v in dados.items()}

    def mudanca(a_lst, d_lst):
        validos = np.ones((H, W), bool); era = np.ones((H, W), bool); virou = np.ones((H, W), bool)
        era_r = np.ones((H, W), bool); virou_n = np.ones((H, W), bool)
        for k in a_lst:
            _, nu, ne, _, nn = C[k]; validos &= ~nu; era &= ne; era_r &= nn
        for k in d_lst:
            _, nu, ne, _, nn = C[k]; validos &= ~nu; virou &= nn; virou_n &= ne
        perda = era & virou & validos & perto
        ganho = era_r & virou_n & validos & perto
        return perda, ganho, (validos & perto).sum() * px
    perda, ganho, val = mudanca(ANTES, DEPOIS)
    perda0, ganho0, val0 = mudanca([ANTES[0]], [ANTES[1]])           # ruido: 2025 contra 2025
    res = {"pares": {"antes": ANTES, "depois": DEPOIS},
           "area_valida_ha": round(float(val), 1),
           "neve_gelo_para_nao_neve_ha": round(float(perda.sum() * px), 1),
           "nao_neve_para_neve_ha": round(float(ganho.sum() * px), 1),
           "ruido_2025_perda_ha": round(float(perda0.sum() * px), 1), "ruido_2025_ganho_ha": round(float(ganho0.sum() * px), 1)}
    # maior mancha contigua de perda e sua cota
    from scipy import ndimage
    lab, n = ndimage.label(perda)
    if n:
        tam = ndimage.sum(perda, lab, range(1, n + 1)); k = int(np.argmax(tam)) + 1
        m = lab == k
        ti = Transformer.from_crs(crs, 4326, always_xy=True)
        lo, la = ti.transform(X[m].mean(), Y[m].mean())
        res["maior_mancha_perda"] = {"ha": round(float(m.sum() * px), 1), "lat": round(la, 4), "lon": round(lo, 4)}
    # lago: agua a ate 1,5 km do ponto do tc90 e ao longo do vale (caixa 28,30-28,36 N, 85,45-85,52 E)
    p90 = Point(*t.transform(*TC90))
    perto90 = vectorized.contains(p90.buffer(1500.0), X, Y)
    xb0, yb0 = t.transform(85.45, 28.30); xb1, yb1 = t.transform(85.52, 28.36)
    vale = (X >= min(xb0, xb1)) & (X <= max(xb0, xb1)) & (Y >= min(yb0, yb1)) & (Y <= max(yb0, yb1))
    serie = []
    for k in sorted(C):
        _, nu, _, ag, _ = C[k]
        serie.append({"data": k, "nuvem_perto_tc90_%": round(float(100 * (nu & perto90).sum() / perto90.sum()), 0),
                      "agua_perto_tc90_ha": round(float((ag & perto90).sum() * px), 2),
                      "nuvem_vale_%": round(float(100 * (nu & vale).sum() / vale.sum()), 0),
                      "agua_vale_ha": round(float((ag & vale).sum() * px), 2)})
    res["lago"] = serie
    # deposito: vegetado ou neve nas duas cenas de antes e solo exposto/detrito nas duas de depois (AOI inteira);
    # ruido pelo mesmo teste entre as duas cenas de 2025
    def deposito(a_lst, d_lst):
        ok = np.ones((H, W), bool); era = np.ones((H, W), bool); virou = np.ones((H, W), bool)
        for k in a_lst:
            d = dados[k]; nd = (d["B08"] - d["B04"]) / np.maximum(d["B08"] + d["B04"], 1e-3)
            ok &= ~C[k][1]; era &= (nd > 0.3)            # so vegetacao antes: a neve sazonal entra como ruido
        for k in d_lst:
            d = dados[k]; nd = (d["B08"] - d["B04"]) / np.maximum(d["B08"] + d["B04"], 1e-3)
            ok &= ~C[k][1]; virou &= (nd < 0.15) & (C[k][0] < 0.2) & (d["B04"] > 0.08)
        return era & virou & ok
    def manchas(m, ha_min=5):
        lab, n = ndimage.label(m, structure=np.ones((3, 3)))
        if not n:
            return np.zeros_like(m)
        tam = ndimage.sum(m, lab, range(1, n + 1))
        return np.isin(lab, 1 + np.where(tam * px >= ha_min)[0])
    def maior(m):
        lab, n = ndimage.label(m, structure=np.ones((3, 3)))
        return float(ndimage.sum(m, lab, range(1, n + 1)).max()) if n else 0.0
    dep = deposito(ANTES, DEPOIS); dep0 = deposito([ANTES[0]], [ANTES[1]])
    grandes, grandes0 = manchas(dep), manchas(dep0)
    lab, n = ndimage.label(grandes, structure=np.ones((3, 3)))
    tam = ndimage.sum(grandes, lab, range(1, n + 1)) if n else np.array([0])
    res["deposito"] = {"ha_total": round(float(dep.sum() * px), 1), "ha_em_manchas_ge_5ha": round(float(grandes.sum() * px), 1),
                       "maior_mancha_ha": round(float(tam.max() * px), 1),
                       "ruido_2025_ha_total": round(float(dep0.sum() * px), 1),
                       "ruido_2025_ha_em_manchas_ge_5ha": round(float(grandes0.sum() * px), 1),
                       "ruido_2025_maior_mancha_ha": round(maior(grandes0) * px, 1)}
    _, _, _, agP, _ = C[DEPOIS[1]]; _, _, _, agA, _ = C[ANTES[0]]
    res["agua_sobre_deposito_ha"] = round(float((agP & grandes).sum() * px), 2)
    np.savez_compressed(os.path.join(SAIDA, "mascaras.npz"), deposito=grandes, perda=perda, ganho=ganho,
                        agua_depois=agP, agua_antes=agA, transform=np.array(tr.to_gdal()), crs=str(crs))
    json.dump(res, open(os.path.join(SAIDA, "cicatriz_lago.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))
    figura(dados, C, perda, ganho, tr, crs, X, Y, t, cic, p90, grandes, agP, agA)


def figura(dados, C, perda, ganho, tr, crs, X, Y, t, cic, p90, dep, agP, agA):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ext = (X.min(), X.max(), Y.min(), Y.max())

    def rgb(d):   # falsa cor SWIR2 / NIR / vermelho: neve ciano, rocha marrom, agua escura
        a = np.dstack([d["B12"], d["B08"], d["B04"]])
        return np.clip(a / 0.6, 0, 1)
    fig, axs = plt.subplots(1, 3, figsize=(16, 5.6), sharex=True, sharey=True)
    for ax, k, tit in [(axs[0], ANTES[1], "antes " + ANTES[1]), (axs[1], DEPOIS[1], "depois " + DEPOIS[1])]:
        ax.imshow(rgb(dados[k]), extent=ext, origin="upper")
        ax.set_title(tit + " (B12/B8/B4)", fontsize=9)
    axs[2].imshow(rgb(dados[DEPOIS[1]]) * 0.5, extent=ext, origin="upper")
    cod = np.zeros(perda.shape, np.int8)
    cod[dep] = 3; cod[perda] = 1; cod[ganho] = 2; cod[agA] = 5; cod[agP] = 4
    m = np.ma.masked_where(cod == 0, cod)
    axs[2].imshow(m, extent=ext, origin="upper", interpolation="nearest",
                  cmap=matplotlib.colors.ListedColormap(["red", "yellow", "orange", "blue", "white"]), vmin=0.5, vmax=5.5)
    axs[2].set_title("laranja: deposito novo; vermelho/amarelo: neve perdida/ganha (2 km da cicatriz);\n"
                     "azul: agua em out/2026; branco: agua em out/2025", fontsize=8)
    for ax in axs:
        xx, yy = cic.xy; ax.plot(xx, yy, "m-", lw=2)
        ax.plot(*p90.coords[0], "c^", ms=9, mec="k")
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Sentinel-2 L2A: cicatriz do Tsangbu Ri (linha magenta, Adhikari et al. Fig. 2) e ponto do 2o deslizamento "
                 "(triangulo, USGS us7000tc90); out/2025 x out/2026, mesma orbita", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(SAIDA, "cicatriz_lago.png"), dpi=130)
    print(os.path.join(SAIDA, "cicatriz_lago.png"))


if __name__ == "__main__":
    main()
