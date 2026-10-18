# -*- coding: utf-8 -*-
"""
O que sao os pixels dos maiores aglomerados de "perda" (analise_pares.py)? Para cada aquisicao, classifica
esses pixels pela refletancia (Sentinel-2 L2A, Earth Search, 20 m):
  neve   verde > 0,11 e NDSI > 0,42                      (claro no verde, escuro no SWIR)
  nuvem  verde > 0,35 e SWIR > 0,25 e NDSI <= 0,42        (claro nos dois: nuvem/nevoa nao mascarada pela SCL)
  rocha  verde <= 0,35 e NDSI <= 0,42 (inclui detrito, gelo sujo)
  escuro verde <= 0,11 (sombra)
  mascarado (SCL estrita)
Grava diag_aglomerados.json e um painel em falsa cor (B11, B8A, B04) ampliado sobre os aglomerados.
Uso: python diag_aglomerados.py <dir_dados> <saida.png>
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402
import serie_multifonte as S  # noqa: E402

ACQ = [("2026-08-12", "S2C"), ("2026-08-24", "S2B"), ("2026-08-24", "S2A"), ("2026-08-27", "S2B"), ("2026-09-01", None), ("2026-09-21", None), ("2026-10-18", None)]
AGS = {"C 12/08>27/08": "E_C_12ago_27ago_S2C_S2B", "A 12/08>24/08 (S2A)": "E_A_12ago_24ago_S2C_S2A",
       "B 24/08>27/08 mesma orbita": "E_B_24ago_27ago_S2A_S2B", "Z falsa perda 15 min": "E_Z_24ago_S2B_S2A_15min_S2B_S2A"}


def main(d, png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import rasterio
    from rasterio.windows import from_bounds
    regs = S.regioes(d)
    from shapely.ops import unary_union
    geom = unary_union(list(regs.values())).envelope
    its = S.it_s2es(geom)
    ags = {k: np.load(os.path.join(d, "aglomerado_%s.npy" % v)) for k, v in AGS.items() if os.path.exists(os.path.join(d, "aglomerado_%s.npy" % v))}
    res = {}
    fig, axs = plt.subplots(1, len(ACQ), figsize=(3.2 * len(ACQ), 3.9))
    cores = {"C 12/08>27/08": "red", "A 12/08>24/08 (S2A)": "orange", "B 24/08>27/08 mesma orbita": "magenta", "Z falsa perda 15 min": "cyan"}
    for c, (dt, sat) in enumerate(ACQ):
        cand = [i for i in its if i["properties"]["datetime"][:10] == dt and (sat is None or i["id"].startswith(sat))]
        if not cand:
            continue
        it = cand[0]
        verde, swir, scl, T, crs, meta = S.cena_s2es(it, geom)
        ie, ib = S.inval_scl(scl, verde)
        with np.errstate(invalid="ignore", divide="ignore"):
            nd = (verde - swir) / (verde + swir)
        cls = np.full(verde.shape, "rocha", dtype=object)
        cls[(verde > 0.35) & (swir > 0.25) & (nd <= 0.42)] = "nuvem"
        cls[(verde > 0.11) & (nd > 0.42)] = "neve"
        cls[verde <= 0.11] = "escuro"
        cls[ie] = "mascarado"
        k = "%s_%s" % (dt, it["id"][:3]); res[k] = {}
        for nome, m in ags.items():
            if m.shape != verde.shape:
                continue
            v, n = np.unique(cls[m], return_counts=True)
            res[k][nome] = {"n_px": int(m.sum()), **{str(a): round(float(b / m.sum()), 3) for a, b in zip(v, n)},
                            "verde_med": round(float(np.nanmedian(verde[m])), 3), "swir_med": round(float(np.nanmedian(swir[m])), 3)}
        # falsa cor ampliada (B11, B8A, B04) na grade de 20 m
        a = it["assets"]
        b, T2, crs2, _ = S.ler_bandas({"swir": a["swir16"]["href"], "nir": a["nir08"]["href"], "red": a["red"]["href"]}, "swir", geom)
        fc = np.dstack([b["swir"], b["nir"], b["red"]]).astype(float) * 1e-4
        fc = np.clip(fc / 0.8, 0, 1)
        allm = np.zeros(verde.shape, bool)
        for m in ags.values():
            if m.shape == verde.shape:
                allm |= m
        jj, ii = np.where(allm)
        jc = comum.mascara(regs["anfiteatro"], verde.shape, T, crs)
        from pyproj import Transformer
        cx, cy = Transformer.from_crs(4326, crs, always_xy=True).transform(*comum.COLAPSO)
        ci, cj = (cx - T.c) / T.a, (cy - T.f) / T.e
        j0, j1 = min(jj.min(), int(cj)) - 25, max(jj.max(), int(cj)) + 25; i0, i1 = min(ii.min(), int(ci)) - 25, max(ii.max(), int(ci)) + 25
        ax = axs[c]
        ax.imshow(fc[j0:j1, i0:i1], extent=(i0, i1, j1, j0))
        ax.contour(np.arange(verde.shape[1]), np.arange(verde.shape[0]), jc.astype(float), levels=[0.5], colors="yellow", linewidths=0.8)
        for nome, m in ags.items():
            if m.shape == verde.shape:
                ax.contour(np.arange(verde.shape[1]), np.arange(verde.shape[0]), m.astype(float), levels=[0.5], colors=cores[nome], linewidths=1.0)
        ax.plot(ci, cj, "x", c="red", ms=9, mew=2)
        ax.set_xlim(i0, i1); ax.set_ylim(j1, j0); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title("%s %s" % (dt, it["id"][:3]), fontsize=9)
        print(k, json.dumps(res[k], ensure_ascii=False))
    fig.suptitle("Falsa cor B11-B8A-B04 (neve = ciano/azul; nuvem = branca; rocha = marrom/rosa), 20 m. Contornos: maiores aglomerados de perda — "
                 "C 12/08>27/08 vermelho, A 12/08>24/08 laranja, B 24/08>27/08 mesma órbita magenta, falsa perda em 15 min ciano", fontsize=8.5)
    fig.tight_layout(); fig.savefig(png, dpi=130)
    json.dump(res, open(os.path.join(d, "diag_aglomerados.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
