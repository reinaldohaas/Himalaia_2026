# -*- coding: utf-8 -*-
"""
Neve ou nuvem na mancha clara do Langtang Lirung (B03 de 26/08 mais claro que o de 25/08, 00:50-02:30 UTC)?
Himawari-9 B05 (1,6 um, 2 km) com B03 (0,64 um, 500 m, levado a ~2 km) e B13 (10,4 um, 2 km), ortorretificados
com o GLO-30 (deslocamento de paralaxe na cota do chao), 26/08 e 25/08, 00:00-03:00 UTC.

Em 1,6 um a neve e o gelo absorvem: neve tem B03 alto e B05 baixo (NDSI = (B03 - B05)/(B03 + B05) ~ 0,6-0,9);
nuvem de agua tem os dois altos (NDSI ~ 0-0,2); nuvem de gelo fica no meio (NDSI ~ 0,3-0,5) e e fria no B13.
Neve no chao a 5-6,5 km de manha tem B13 perto de 265-280 K; topo de nuvem de gelo, bem abaixo de 250 K.
Ressalva: o pixel de 2 km mistura neve, rocha e sombra; o NDSI de um pixel misto cai.

Regioes (na grade do B03 ortorretificado):
  mancha = celulas acima de 5 km com B03(26) - B03(25) > 0,25 na media de 00:50-02:30
  neve_25 = celulas acima de 6 km com B03(25) > 0,6 na media de 00:50-02:30 (neve antiga do macico, controle)
  bacia = bacia do ponto do drone (ponto_drone.py)
Uso: python b05_neve_nuvem.py [dir_bruto_b05] [dir_bruto_b13]
Saidas em data/processed/himawari_b03/: b05_neve_nuvem.txt, b05_neve_nuvem.json, b05_neve_nuvem.png
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import ahi_hsd as hsd

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
B05 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "data", "raw", "himawari_b05")
B13 = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "data", "raw", "himawari_10min")
D = os.path.join(RAIZ, "data", "processed", "himawari_b03")
BUCKET = "https://noaa-himawari9.s3.amazonaws.com"
P = (28.293985, 85.523964)


def baixar(t, banda, pasta):
    os.makedirs(pasta, exist_ok=True)
    nome = "HS_H09_%s_%s_FLDK_R20_S0310.DAT.bz2" % (t.strftime("%Y%m%d_%H%M"), banda)
    dst = os.path.join(pasta, nome)
    if not os.path.exists(dst):
        urllib.request.urlretrieve("%s/AHI-L1b-FLDK/%s/%s" % (BUCKET, t.strftime("%Y/%m/%d/%H%M"), nome), dst + ".part")
        os.replace(dst + ".part", dst)
    return dst


def zenite(t, lat, lon):
    n = t.timetuple().tm_yday
    g = 2 * np.pi / 365 * (n - 1 + (t.hour - 12) / 24)
    dec = 0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g) + 0.000907 * np.sin(2 * g)
    eqt = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g) - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    hs = np.radians(((t.hour * 60 + t.minute + eqt + 4 * lon) / 4) - 180)
    la = np.radians(lat)
    return np.degrees(np.arccos(np.sin(la) * np.sin(dec) + np.cos(la) * np.cos(dec) * np.cos(hs)))


def aparente(la0, lo0, h, sub):
    la, lo = la0, lo0
    for _ in range(10):
        tl, to = hsd.paralaxe(la, lo, h, sub)
        la, lo = la - (tl - la0), lo - (to - lo0)
    return la, lo


def amostra(s, campo, la, lo):
    c, l = hsd.ll2cl(la, lo, s["sub_lon"], s["cfac"], s["lfac"], s["coff"], s["loff"])
    i = np.rint(l).astype(int) - 1 - (s["lin0"] - 1); j = np.rint(c).astype(int) - 1
    out = np.full(np.shape(la), np.nan)
    ok = (i >= 0) & (i < campo.shape[0]) & (j >= 0) & (j < campo.shape[1])
    out[ok] = campo[i[ok], j[ok]]
    return out


def suaviza(a, n):
    """media movel n x n ignorando NaN (B03 de 500 m levado a ~2 km)"""
    v = np.nan_to_num(a); w = np.isfinite(a).astype(float)
    k = np.ones(n) / n
    f = lambda x: np.apply_along_axis(lambda r: np.convolve(r, k, "same"), 1, np.apply_along_axis(lambda c: np.convolve(c, k, "same"), 0, x))
    with np.errstate(invalid="ignore"):
        return f(v) / f(w)


def main():
    a26, a25 = np.load(os.path.join(D, "b03_orto.npz")), np.load(os.path.join(D, "b03_orto_20260825.npz"))
    lat, lon, Z = a26["lat"], a26["lon"], a26["Z"]
    LON, LAT = np.meshgrid(lon, lat)
    bac = np.load(os.path.join(RAIZ, "data", "processed", "ponto_drone", "bacia_ponto.npz"))
    r = bac["lat"][1] - bac["lat"][0]
    mb = bac["mascara"][((LAT - bac["lat"][0]) / r).round().astype(int), ((LON - bac["lon"][0]) / r).round().astype(int)]
    janela = [k for k in a26.files if k.startswith("t") and "0050" <= k[1:] <= "0230" and k in a25.files]
    d_med = np.nanmean([a26[k] - a25[k] for k in janela], axis=0)
    r25 = np.nanmean([a25[k] for k in janela], axis=0)
    mancha = (Z > 5.0) & (d_med > 0.25)
    neve25 = (Z > 6.0) & (r25 > 0.6)
    regioes = {"mancha": mancha, "neve_25": neve25, "bacia": mb}
    print("celulas: " + ", ".join("%s %d (%.1f km2)" % (k, v.sum(), v.sum() * 0.2 * 0.2 * np.cos(np.radians(28.29)) * 1.11 ** 2) for k, v in regioes.items()))

    res, figs = {}, {}
    for dia in ("20260826", "20260825"):
        a = a26 if dia.endswith("26") else a25
        t0 = datetime.strptime(dia, "%Y%m%d")
        for m in range(0, 181, 10):
            t = t0 + timedelta(minutes=m); k = "t" + t.strftime("%H%M")
            if k not in a.files:
                continue
            try:
                s5, s13 = hsd.ler_segmento(baixar(t, "B05", B05)), hsd.ler_segmento(baixar(t, "B13", B13))
            except Exception as e:
                print(t, "sem dados:", e, flush=True)
                continue
            sza = float(zenite(t, *P))
            d = (np.array(aparente(P[0], P[1], 5.0, s5["sub_lon"])) - np.array(P)) / 5.0
            la_ap, lo_ap = LAT + Z * d[0], LON + Z * d[1]
            r5 = amostra(s5, s5["rad"].astype(np.float64) * s5["c_albedo"], la_ap, lo_ap) / np.cos(np.radians(min(sza, 88.0)))
            t13 = amostra(s13, s13["tb"].astype(np.float64), la_ap, lo_ap)
            r3 = suaviza(a[k].astype(np.float64), 10)
            ndsi = (r3 - r5) / (r3 + r5)
            ent = {"sza": round(sza, 1)}
            for nome, mk in regioes.items():
                ent[nome] = {"B03": round(float(np.nanmean(r3[mk])), 3), "B05": round(float(np.nanmean(r5[mk])), 3),
                             "NDSI": round(float(np.nanmean(ndsi[mk])), 3), "T13": round(float(np.nanmean(t13[mk])), 1)}
            res.setdefault(dia, {})[t.strftime("%H:%M")] = ent
            if dia.endswith("26") and t.strftime("%H%M") in ("0100", "0150", "0230"):
                figs[t.strftime("%H:%M")] = (r3, r5, ndsi, t13)
            print(dia, t.strftime("%H:%M"), " | ".join("%s B03 %.2f B05 %.2f NDSI %.2f T13 %.0f" % (n, e["B03"], e["B05"], e["NDSI"], e["T13"])
                                                    for n, e in ent.items() if n != "sza"), flush=True)

    lin = ["# Himawari-9, ortorretificado: B03 (levado a ~2 km), B05 (1,6 um), NDSI = (B03-B05)/(B03+B05), T13 (K)",
           "# mancha = mais clara no B03 de 26/08 que no de 25/08 (00:50-02:30, acima de 5 km); neve_25 = neve antiga do macico (>6 km);",
           "# bacia = bacia do ponto do drone. Neve: NDSI ~0,6-0,9 e T13 ~265-280 K; nuvem de agua: NDSI ~0-0,2; nuvem de gelo: NDSI ~0,3-0,5 e T13 < 250 K",
           "dia      UTC   sza  | mancha: B03  B05  NDSI  T13 | neve_25: B03  B05  NDSI  T13 | bacia: B03  B05  NDSI  T13"]
    for dia, hs in res.items():
        for h, e in hs.items():
            lin.append("%s %s %5.1f | " % (dia, h, e["sza"]) + " | ".join("%5.2f %5.2f %5.2f %5.0f" % (e[n]["B03"], e[n]["B05"], e[n]["NDSI"], e[n]["T13"])
                                                                          for n in ("mancha", "neve_25", "bacia")))
    txt = "\n".join(lin) + "\n"
    open(os.path.join(D, "b05_neve_nuvem.txt"), "w", encoding="utf-8").write(txt)
    json.dump(res, open(os.path.join(D, "b05_neve_nuvem.json"), "w", encoding="utf-8"), indent=1)
    print(txt)

    fig, axs = plt.subplots(len(figs), 4, figsize=(14, 3.4 * len(figs)), squeeze=False)
    ext = [lon[0], lon[-1], lat[-1], lat[0]]
    for row, (h, (r3, r5, ndsi, t13)) in zip(axs, figs.items()):
        for ax, campo, tit, cm, vv in zip(row, (r3, r5, ndsi, t13), ("B03 (~2 km)", "B05 1,6 um", "NDSI", "T13 (K)"),
                                          ("gray", "gray", "RdBu", "inferno"), ((0, 1), (0, 0.6), (-0.6, 0.9), (220, 290))):
            im = ax.imshow(campo, extent=ext, cmap=cm, vmin=vv[0], vmax=vv[1], interpolation="nearest")
            ax.contour(lon, lat, mancha.astype(float), levels=[0.5], colors="lime", linewidths=1.2)
            ax.contour(lon, lat, neve25.astype(float), levels=[0.5], colors="c", linewidths=1.0)
            ax.contour(lon, lat, mb.astype(float), levels=[0.5], colors="m", linewidths=1.2)
            ax.contour(lon, lat, Z, levels=[5, 6, 7], colors="k", linewidths=0.3)
            ax.plot(P[1], P[0], "y*", ms=9, mec="k")
            ax.set_title("26/08 %s UTC - %s" % (h, tit), fontsize=8); ax.tick_params(labelsize=6)
            ax.set_aspect(1 / np.cos(np.radians(P[0])))
            fig.colorbar(im, ax=ax, shrink=0.7)
    fig.suptitle("Himawari-9 ortorretificado, 26/08/2026. Verde = mancha mais clara que em 25/08 (B03); ciano = neve antiga do macico (>6 km, 25/08);\n"
                 "magenta = bacia do ponto do drone (estrela). Neve: B05 baixo, NDSI alto, T13 ~265-280 K; nuvem de agua: B05 alto, NDSI baixo", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(D, "b05_neve_nuvem.png"), dpi=120)


if __name__ == "__main__":
    main()
