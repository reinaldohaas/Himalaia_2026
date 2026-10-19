# -*- coding: utf-8 -*-
"""
Linha de neve (cota em que a fracao de neve/gelo, NDSI > 0,42, cruza 50 %) por cena, na janela inteira do
anfiteatro + controles (~12 x 9 km), em faixas de 100 m de cota do GLO-30, so nos pixels observados.
Tambem: cota dos pixels que ganharam e perderam neve nos pares do evento e no par de 15 min (ruido).
Fontes: s2es, s2pc, s2l1c; mascaras espectral e estrita. Uma faixa so conta com >= 200 pixels observados.
Uso: python linha_de_neve.py <dir_dados> <saida.png>
"""
import json
import os
import sys
from datetime import datetime

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

COLAPSO_T = datetime(2026, 8, 26, 2, 52)
FAIXAS = np.arange(3000, 7300, 100)


def dem_na_grade(T, shp):
    from rasterio.transform import Affine
    from rasterio.crs import CRS
    from shapely.geometry import box
    from pyproj import Transformer
    it = comum.stac_busca(comum.PC, ["cop-dem-glo-30"], [85.40, 28.18, 85.65, 28.38], "2000-01-01/2030-01-01")[0]
    href = comum.pc_assina(it["assets"]["data"]["href"])
    Ta = Affine(*T[:6]); crs = CRS.from_epsg(32645)
    x0, y1 = Ta.c, Ta.f; x1, y0 = Ta.c + Ta.a * shp[1], Ta.f + Ta.e * shp[0]
    lon, lat = Transformer.from_crs(32645, 4326, always_xy=True).transform([x0, x1, x0, x1], [y0, y0, y1, y1])
    z, Tz, cz, nd = comum.ler_janela(href, box(min(lon), min(lat), max(lon), max(lat)), folga_m=500)
    return comum.reamostra_para(z, Tz, cz, shp, Ta, crs, metodo="bilinear")


def linha(nd, zz, lim=0.42):
    ok = np.isfinite(nd)
    f, n = [], []
    for z0 in FAIXAS:
        m = ok & (zz >= z0) & (zz < z0 + 100)
        n.append(int(m.sum())); f.append(float((nd[m] > lim).mean()) if m.sum() >= 200 else np.nan)
    f = np.array(f)
    # menor cota acima da qual a fracao fica >= 0,5 em todas as faixas validas seguintes (ignora rochedos isolados no alto)
    v = np.where(np.isfinite(f))[0]
    if len(v) < 5:
        return None, f
    for k in v:
        if np.nanmin(f[k:]) >= 0.5 or (np.nanmean(f[k:] >= 0.5) >= 0.8 and f[k] >= 0.5):
            if k == v[0]:
                return None, f      # ja coberto na faixa mais baixa observada: linha abaixo da janela observada
            # interpolacao linear entre a faixa anterior valida e esta
            kp = v[v < k][-1]
            z = FAIXAS[kp] + 50 + (0.5 - f[kp]) / (f[k] - f[kp]) * (FAIXAS[k] - FAIXAS[kp]) if f[k] != f[kp] else FAIXAS[k] + 50
            return float(z), f
    return None, f


def main(d, png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    res = {"linha": [], "cota_mudanca": {}}
    zz = None
    for f in ("s2es", "s2pc", "s2l1c"):
        z = np.load(os.path.join(d, "mascaras_%s.npz" % f))
        serie = {r["id"]: r for r in json.load(open(os.path.join(d, "serie_%s.json" % f))) if "erro" not in r}
        for suf, mas in (("__ndsi", "espectral"), ("__ndsiE", "estrita")):
            for k in z.files:
                if not k.endswith(suf):
                    continue
                i = k[:-len(suf)]
                if zz is None:
                    zz = dem_na_grade(z[i + "__T"], z[k].shape)
                nd = z[k].astype(np.float32)
                obs = float(np.isfinite(nd).mean())
                L, fr = linha(nd, zz)
                res["linha"].append({"fonte": f, "mascara": mas, "id": i, "datetime": serie[i]["datetime"], "frac_obs_janela": round(obs, 3),
                                     "linha_neve_m": None if L is None else round(L)})
    # cota dos ganhos e perdas (s2es, mascara espectral) nos pares do evento e no par de 15 min
    z = np.load(os.path.join(d, "mascaras_s2es.npz"))
    cen = {}
    for k in z.files:
        if k.endswith("__ndsi"):
            i = k[:-6]; t = json.load(open(os.path.join(d, "serie_s2es.json")))
    ser = {r["id"]: r for r in t if "erro" not in r}
    for k in z.files:
        if k.endswith("__ndsi"):
            i = k[:-6]; cen.setdefault((ser[i]["datetime"][:10], i[:3]), []).append(z[k].astype(np.float32))
    cen = {kk: (v[0] if len(v) == 1 else np.where(np.isfinite(v[0]), v[0], v[1])) for kk, v in cen.items()}
    anf = z["regiao__anfiteatro"]
    PARES = {"Z_15min_24ago_S2B>S2A": (("2026-08-24", "S2B"), ("2026-08-24", "S2A")),
             "B_24ago_S2A>27ago_S2B": (("2026-08-24", "S2A"), ("2026-08-27", "S2B")),
             "B_24ago_S2B>27ago_S2B": (("2026-08-24", "S2B"), ("2026-08-27", "S2B")),
             "A_12ago_S2C>24ago_S2A": (("2026-08-12", "S2C"), ("2026-08-24", "S2A"))}
    for nome, (ka, kb) in PARES.items():
        a, b = cen[ka], cen[kb]; ok = np.isfinite(a) & np.isfinite(b)
        g = ok & (a <= 0.42) & (b > 0.42); p = ok & (a > 0.42) & (b <= 0.42)
        r = {}
        for reg, m in (("janela", np.ones_like(anf, bool)), ("anfiteatro", anf)):
            r[reg] = {"ganho_ha": round(float((g & m).sum() * 0.04), 1), "perda_ha": round(float((p & m).sum() * 0.04), 1),
                      "comum_ha": round(float((ok & m).sum() * 0.04), 1),
                      "ganho_cota_p10_p50_p90": [round(float(x)) for x in np.percentile(zz[g & m], [10, 50, 90])] if (g & m).sum() > 20 else None,
                      "perda_cota_p10_p50_p90": [round(float(x)) for x in np.percentile(zz[p & m], [10, 50, 90])] if (p & m).sum() > 20 else None}
        res["cota_mudanca"][nome] = r
        print(nome, json.dumps(r))
    json.dump(res, open(os.path.join(d, "linha_de_neve.json"), "w"), indent=1)
    fig, ax = plt.subplots(figsize=(11, 4.6))
    est = {("s2es", "espectral"): ("o", "tab:blue"), ("s2pc", "espectral"): ("s", "tab:cyan"), ("s2l1c", "espectral"): ("^", "tab:purple"),
           ("s2es", "estrita"): ("x", "tab:gray")}
    for (f, m), (mk, c) in est.items():
        pts = [(datetime.strptime(x["datetime"][:19], "%Y-%m-%dT%H:%M:%S"), x["linha_neve_m"]) for x in res["linha"]
               if x["fonte"] == f and x["mascara"] == m and x["linha_neve_m"] and x["frac_obs_janela"] >= 0.3]
        if pts:
            ax.plot([p[0] for p in pts], [p[1] for p in pts], mk, c=c, ms=6 if mk != "x" else 5, mfc="none" if mk in "s^" else None,
                    label="%s, máscara %s" % (f, m))
    ax.axvline(COLAPSO_T, c="r", lw=1); ax.text(COLAPSO_T, ax.get_ylim()[1], " colapso", color="r", fontsize=8, va="top")
    ax.set_ylabel("linha de neve (m)\n(fração de neve = 50 %)"); ax.legend(fontsize=8); ax.grid(alpha=0.3)
    ax.set_title("Linha de neve na janela do anfiteatro (~12 × 9 km), Sentinel-2, cenas com ≥ 30 % da janela observada", fontsize=10)
    fig.autofmt_xdate(); fig.tight_layout(); __import__('figlang').prepara(fig); fig.savefig(__import__('figlang').caminho(png), dpi=130)
    for x in res["linha"]:
        if x["fonte"] == "s2es" and x["mascara"] == "espectral" and x["frac_obs_janela"] >= 0.3:
            print(x["datetime"][:16], x["id"][:3], "obs %.2f" % x["frac_obs_janela"], "linha", x["linha_neve_m"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
