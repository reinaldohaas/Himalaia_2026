# -*- coding: utf-8 -*-
"""
Ponto indicado pelo pesquisador (24/10/2026) como o lugar que o drone de Hei Mu ve no instante do colapso e onde o
granizo teria se acumulado: 28,293985 N, 85,523964 E. Relevo do GLO-30 a 3" (tile do d04, cluster/wrf_lhende/d04/glo30_3s).
Calcula: cota, declividade e orientacao no ponto; distancias a cicatriz (Adhikari et al.), ao "ponto de colapso" antigo
(USGS 28,271/85,515), ao centro do vortice do experimento E e a maior mancha de perda de gelo do Sentinel-2; o caminho de
maior declive a partir do ponto (para onde escorre o que se acumula ali) e a area a montante (de onde pode vir o que
escorrega para o ponto), com a hipsometria dessa area.
Saida: data/processed/ponto_drone/ponto_drone.json e .png
"""
import json
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..", "..")
TILE = os.path.join(RAIZ, "cluster", "wrf_lhende", "d04", "glo30_3s", "00001-00540.00001-00480")
SAIDA = os.path.join(RAIZ, "data", "processed", "ponto_drone")
S0, W0, RES, NX, NY = 28.08, 85.30, 3.0 / 3600.0, 540, 480

P = (28.293985, 85.523964)
REF = {
    "cicatriz_Adhikari_1": (28.2830, 85.5225), "cicatriz_Adhikari_2": (28.2870, 85.5300),
    "cicatriz_Adhikari_3": (28.2950, 85.5300),
    "colapso_USGS_tbwb": (28.271, 85.515), "vortice_E": (28.270, 85.535),
    "maior_perda_gelo_S2": (28.293, 85.5288), "exutorio_anfiteatro": (28.285, 85.51306),
    "sondagem_CM1": (28.2849, 85.5132),
    "ruptura_Petley": (28.2921, 85.5271),
}


def km(a, b):
    return np.hypot((a[0] - b[0]) * 111.32, (a[1] - b[1]) * 111.32 * np.cos(np.radians(28.29)))


def main():
    os.makedirs(SAIDA, exist_ok=True)
    z = np.fromfile(TILE, ">i2").reshape(NY, NX).astype(float)      # linha 0 = sul
    lat = S0 + (np.arange(NY) + 0.5) * RES; lon = W0 + (np.arange(NX) + 0.5) * RES
    dy = RES * 111320.0; dx = dy * np.cos(np.radians(28.29))
    gy, gx = np.gradient(z, dy, dx)
    decl = np.degrees(np.arctan(np.hypot(gx, gy)))
    orient = (np.degrees(np.arctan2(-gx, -gy)) + 360) % 360        # direcao para onde a encosta desce (0 = N)
    ij = lambda la, lo: (int((la - S0) / RES), int((lo - W0) / RES))
    j0, i0 = ij(*P)
    r = {"ponto": {"lat": P[0], "lon": P[1], "cota_m": z[j0, i0], "declividade_graus": round(decl[j0, i0], 1),
                   "desce_para_graus": round(orient[j0, i0]), "cota_max_300m": z[j0-4:j0+5, i0-4:i0+5].max(),
                   "declividade_media_300m": round(decl[j0-4:j0+5, i0-4:i0+5].mean(), 1)}}
    r["distancias_km"] = {k: round(km(P, v), 2) for k, v in REF.items()}
    r["cotas_ref_m"] = {k: z[ij(*v)] for k, v in REF.items()}
    jm, im = np.unravel_index(np.argmax(z), z.shape)
    r["cume_tile"] = {"lat": round(lat[jm], 4), "lon": round(lon[im], 4), "cota_m": z[jm, im], "dist_km": round(km(P, (lat[jm], lon[im])), 2)}

    # caminho de maior declive (D8) a partir do ponto
    viz = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    dist = lambda a, b: np.hypot(a * dy, b * dx)
    cam = [(j0, i0)]
    while len(cam) < 2000:
        j, i = cam[-1]
        if not (0 < j < NY - 1 and 0 < i < NX - 1): break
        q = [((z[j, i] - z[j + a, i + b]) / dist(a, b), j + a, i + b) for a, b in viz]
        s, jn, inn = max(q)
        if s <= 0: break
        cam.append((jn, inn))
    comp = np.cumsum([0] + [dist(cam[k + 1][0] - cam[k][0], cam[k + 1][1] - cam[k][1]) for k in range(len(cam) - 1)])
    marcos = []
    for k in range(0, len(cam), max(1, len(cam) // 25)):
        j, i = cam[k]; marcos.append({"s_km": round(comp[k] / 1e3, 2), "lat": round(lat[j], 4), "lon": round(lon[i], 4), "cota_m": z[j, i]})
    j, i = cam[-1]; marcos.append({"s_km": round(comp[-1] / 1e3, 2), "lat": round(lat[j], 4), "lon": round(lon[i], 4), "cota_m": z[j, i]})
    r["caminho_descida"] = marcos

    # area a montante do ponto (todas as celulas cujo caminho D8 passa a ate 1 celula do ponto)
    ordem = np.argsort(z, axis=None)[::-1]
    dest = -np.ones(z.size, int)
    zz = z.ravel()
    for n in ordem:
        j, i = divmod(n, NX)
        if not (0 < j < NY - 1 and 0 < i < NX - 1): continue
        best, bn = 0.0, -1
        for a, b in viz:
            s = (z[j, i] - z[j + a, i + b]) / dist(a, b)
            if s > best: best, bn = s, (j + a) * NX + (i + b)
        dest[n] = bn
    alvo = np.zeros(z.size, bool)
    for a in (-1, 0, 1):
        for b in (-1, 0, 1): alvo[(j0 + a) * NX + i0 + b] = True
    mont = alvo.copy()
    # propaga: uma celula esta a montante se o seu destino esta a montante; processar das mais baixas para as mais altas
    for n in ordem[::-1]:
        d = dest[n]
        if d >= 0 and mont[d]: mont[n] = True
    m2 = mont.reshape(z.shape)
    a_cel = dx * dy / 1e6
    r["refs_na_area_montante"] = {k: bool(m2[ij(*v)]) for k, v in REF.items()}
    zm = z[m2]
    r["area_montante"] = {"km2": round(m2.sum() * a_cel, 3), "cota_max_m": zm.max(), "cota_mediana_m": float(np.median(zm)),
                          "km2_acima_6000": round((zm >= 6000).sum() * a_cel, 3), "km2_acima_5500": round((zm >= 5500).sum() * a_cel, 3),
                          "declividade_media": round(decl[m2].mean(), 1),
                          "faixas_500m_km2": {"%d-%d" % (c, c + 500): round(((zm >= c) & (zm < c + 500)).sum() * a_cel, 3) for c in range(4000, 7500, 500)}}
    np.savez_compressed(os.path.join(SAIDA, "bacia_ponto.npz"), mascara=m2, lat=lat, lon=lon)
    json.dump(r, open(os.path.join(SAIDA, "ponto_drone.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    print(json.dumps(r, ensure_ascii=False, indent=1, default=float))

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    js = slice(ij(28.22, 0)[0], ij(28.34, 0)[0]); is_ = slice(ij(0, 85.47)[1], ij(0, 85.58)[1])
    fig, ax = plt.subplots(figsize=(7.5, 7))
    ext = [lon[is_][0], lon[is_][-1], lat[js][0], lat[js][-1]]
    sh = np.clip(np.cos(np.radians(decl)) , 0, 1)
    ax.imshow(z[js, is_], origin="lower", extent=ext, cmap="terrain", vmin=2500, vmax=7300, alpha=0.9)
    cs = ax.contour(lon[is_], lat[js], z[js, is_], levels=range(3000, 7500, 500), colors="k", linewidths=0.4)
    # (clabel derruba o matplotlib deste ambiente no Windows)
    ax.contour(lon, lat, m2.astype(float), levels=[0.5], colors="m", linewidths=1.5)
    cy = [lat[c[0]] for c in cam]; cx = [lon[c[1]] for c in cam]; ax.plot(cx, cy, "b-", lw=1.5, label="maior declive a partir do ponto")
    ax.plot([v[1] for k, v in REF.items() if k.startswith("cic")], [v[0] for k, v in REF.items() if k.startswith("cic")], "r-", lw=2.5, label="cicatriz (Adhikari et al.)")
    ax.plot(P[1], P[0], "y*", ms=16, mec="k", label="ponto do drone (pesquisador)")
    for k, mk in (("colapso_USGS_tbwb", "rx"), ("vortice_E", "co"), ("maior_perda_gelo_S2", "ks"), ("exutorio_anfiteatro", "g^")):
        ax.plot(REF[k][1], REF[k][0], mk, ms=8, label=k)
    ax.plot(lon[im], lat[jm], "w^", mec="k", ms=9, label="cume (%.0f m)" % z[jm, im])
    ax.set_xlim(ext[:2]); ax.set_ylim(ext[2:]); ax.set_aspect(1 / np.cos(np.radians(28.29)))
    ax.legend(fontsize=6.5, loc="lower left"); ax.set_title("Ponto do drone, cicatriz e area a montante (magenta) - GLO-30 3\"", fontsize=9)
    fig.savefig(os.path.join(SAIDA, "ponto_drone.png"), dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    main()
