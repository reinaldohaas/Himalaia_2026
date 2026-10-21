# -*- coding: utf-8 -*-
"""
Mapas da fase do topo perto do anfiteatro (Himawari-9 B07 + B13, 10 min), a partir dos arquivos baixados por
fase_topo_10min.py. Para cada horario: T13 (cinza) e, onde o topo esta abaixo de 0 C (T13 < 273 K), a refletancia
em 3,9 um r39 (cor): r39 alta = gotas de agua no topo (super-resfriadas, se T13 < 273 K); r39 baixa = gelo ou neve.
Posicoes aparentes (sem paralaxe); a seta marca o deslocamento para um topo a 8 km.

Uso: python mapa_fase_topo.py [dir_bruto] [dir_saida] [HHMM,HHMM,...]
"""
import glob
import json
import os
import sys
from datetime import datetime, timedelta

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import ahi_hsd as hsd
from fase_topo_10min import planck, zenite_solar, aparente, SITIO

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
BRUTO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "data", "raw", "himawari_10min")
SAIDA = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "data", "processed", "himawari_fase_topo")
HORAS = (sys.argv[3].split(",") if len(sys.argv) > 3 else
         ["0030", "0100", "0130", "0150", "0210", "0230", "0250", "0300", "0320"])   # nao ha varredura as 02:40
EN = os.environ.get("FIG_LANG", "pt") == "en"
DG = 0.01
lat = np.arange(28.95, 27.6, -DG)
lon = np.arange(84.85, 86.35, DG)
LON, LAT = np.meshgrid(lon, lat)
KX = 111.32 * np.cos(np.radians(SITIO[0]))


def amostra(s, campo):
    c, l = hsd.ll2cl(LAT, LON, s["sub_lon"], s["cfac"], s["lfac"], s["coff"], s["loff"])
    ci = np.rint(c).astype(int) - 1
    li = np.rint(l).astype(int) - 1 - (s["lin0"] - 1)
    out = np.full(LAT.shape, np.nan, np.float64)
    m = (li >= 0) & (li < s[campo].shape[0]) & (ci >= 0) & (ci < s[campo].shape[1])
    out[m] = s[campo][li[m], ci[m]]
    return out


def main():
    anf = None
    p = os.path.join(RAIZ, "data", "processed", "neve_anfiteatro", "anfiteatro.geojson")
    if os.path.exists(p):
        anf = np.array(json.load(open(p, encoding="utf-8"))["features"][0]["geometry"]["coordinates"][0])
    n = len(HORAS)
    nc = 3
    fig, axs = plt.subplots((n + nc - 1) // nc, nc, figsize=(4.0 * nc, 3.7 * ((n + nc - 1) // nc)), sharex=True, sharey=True)
    for ax, hh in zip(axs.ravel(), HORAS):
        dia = "20260825" if hh >= "1200" else "20260826"
        a7 = glob.glob(os.path.join(BRUTO, "HS_H09_%s_%s_B07_*" % (dia, hh)))
        a13 = glob.glob(os.path.join(BRUTO, "HS_H09_%s_%s_B13_*" % (dia, hh)))
        if not a7 or not a13:
            ax.set_title(hh + " sem dados"); continue
        s7, s13 = hsd.ler_segmento(a7[0]), hsd.ler_segmento(a13[0])
        t = datetime(2026, 8, int(dia[6:]), int(hh[:2]), int(hh[2:]))
        sza = zenite_solar(t, LAT, LON)
        T = amostra(s13, "tb"); L = amostra(s7, "rad")
        e39 = np.pi * planck(s7["lambda_um"], 5772.0) * (6.957e8 / 1.496e11) ** 2 / 1.0105 ** 2
        Be = planck(s7["lambda_um"], T)
        r39 = (L - Be) / (e39 * np.cos(np.radians(np.minimum(sza, 89))) / np.pi - Be)
        ax.pcolormesh(lon, lat, T, cmap="gray_r", vmin=210, vmax=295, shading="auto")
        rr = np.where(T < 273, r39, np.nan)
        pc = ax.pcolormesh(lon, lat, rr, cmap="turbo", vmin=0, vmax=0.25, shading="auto", alpha=0.85)
        if anf is not None:
            ax.fill(anf[:, 0], anf[:, 1], color="m", zorder=5)
        ax.plot(SITIO[1], SITIO[0], "m*", ms=9, zorder=6)
        for r in (10, 30):
            th = np.linspace(0, 2 * np.pi, 120)
            ax.plot(SITIO[1] + r / KX * np.sin(th), SITIO[0] + r / 111.32 * np.cos(th), "m:", lw=0.7)
        la8, lo8 = aparente(8, s13["sub_lon"])
        ax.annotate("", xy=(lo8, la8), xytext=(SITIO[1], SITIO[0]), arrowprops=dict(arrowstyle="->", color="m", lw=1.2))
        npt = (t + timedelta(hours=5, minutes=45)).strftime("%H:%M")
        ax.set_title("%s:%s UTC (%s NPT), sza %.0f" % (hh[:2], hh[2:], npt, float(zenite_solar(t, *SITIO))), fontsize=8)
        ax.set_aspect(1 / np.cos(np.radians(SITIO[0])))
    for ax in axs.ravel()[n:]:
        ax.axis("off")
    cb = fig.colorbar(pc, ax=axs, shrink=0.8)
    if EN:
        cb.set_label(r"3.9-$\mu$m reflectance where T13 < 273 K (high: water; low: ice or snow)")
        fig.suptitle("Himawari-9 cloud-top phase near the Lhende amphitheatre, 26 August 2026 (apparent positions; arrow: "
                     "parallax of a top at 8 km; rings 10 and 30 km)", fontsize=9)
    else:
        cb.set_label("refletancia em 3,9 um onde T13 < 273 K (alta = agua; baixa = gelo/neve)")
        fig.suptitle("Himawari-9: fase do topo perto do anfiteatro de Lhende, 26/08/2026 (posicao aparente; seta: paralaxe de um topo a 8 km; aneis 10/30 km)", fontsize=9)
    os.makedirs(SAIDA, exist_ok=True)
    out = os.path.join(SAIDA, "mapa_fase_topo%s.png" % ("_en" if EN else ""))
    fig.savefig(out, dpi=130)
    print(out)


if __name__ == "__main__":
    main()
