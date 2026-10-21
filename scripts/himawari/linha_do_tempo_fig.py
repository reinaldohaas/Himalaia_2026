# -*- coding: utf-8 -*-
"""
Figura da linha do tempo de 25/08 12 UTC a 26/08 07 UTC: nuvem (Himawari-9), eventos sismicos e cheia, com as fases
da hipotese do pesquisador. Usa:
  * area < 213 K a ate 150 km do sitio (trajetoria.txt, a cada 30 min);
  * Tb do topo sobre o sitio com a paralaxe invertida para um topo a 10 km (B13; a cada 30 min ate 22:00 e a cada
    10 min depois), calculada aqui com ahi_hsd e fase_topo_10min.aparente;
  * eventos de LINHA_DO_TEMPO_EVENTO_26AGO2026.md.
Uso: python linha_do_tempo_fig.py [dir_b13_30min] [dir_10min] [trajetoria.txt]
"""
import glob
import os
import sys
from datetime import datetime

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import ahi_hsd as hsd
from fase_topo_10min import aparente

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
B30 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "data", "raw", "himawari_b13")
B10 = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "data", "raw", "himawari_10min")
TRAJ = sys.argv[3] if len(sys.argv) > 3 else os.path.join(RAIZ, "data", "processed", "himawari_trajetoria", "trajetoria.txt")
SAIDA = os.path.join(RAIZ, "data", "processed", "linha_do_tempo")
T0 = datetime(2026, 8, 25, 0, 0)


def horas(t):
    return (t - T0).total_seconds() / 3600.0


def tb_sitio(arq, h=10.0):
    s = hsd.ler_segmento(arq)
    la, lo = aparente(h, s["sub_lon"])
    c, l = hsd.ll2cl(np.array([la]), np.array([lo]), s["sub_lon"], s["cfac"], s["lfac"], s["coff"], s["loff"])
    i, j = int(np.rint(l[0])) - 1 - (s["lin0"] - 1), int(np.rint(c[0])) - 1
    return float(np.nanmin(s["tb"][i - 1:i + 2, j - 1:j + 2]))


def main():
    os.makedirs(SAIDA, exist_ok=True)
    serie = {}
    for d, padrao in ((B30, "HS_H09_2026082*_B13_*"), (B10, "HS_H09_2026082*_B13_*")):
        for a in sorted(glob.glob(os.path.join(d, padrao))):
            b = os.path.basename(a)
            t = datetime.strptime(b[7:20], "%Y%m%d_%H%M")
            if t >= datetime(2026, 8, 25, 12):
                serie[t] = tb_sitio(a)
    area = []
    for ln in open(TRAJ, encoding="utf-8"):
        if ln.startswith("2026-"):
            p = ln.split()
            area.append((datetime.strptime(p[0], "%Y-%m-%dT%H:%MZ"), float(p[2])))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(12, 8.2), sharex=True, gridspec_kw={"height_ratios": [1.1, 1.1, 1.3]})
    x = [horas(t) for t, _ in area]
    a1.fill_between(x, [v / 1e3 for _, v in area], color="0.6", step="mid")
    a1.set_ylabel("conveccao profunda\n(< 213 K, ate 150 km)\n10³ km²", fontsize=8)
    a1.set_title("Linha do tempo, 25/08 12 UTC a 26/08 07 UTC (Himawari-9; USGS; Adhikari et al. 2026; NDRRMA/KP; CCTV)", fontsize=10)
    ts = sorted(serie)
    a2.plot([horas(t) for t in ts], [serie[t] for t in ts], "k.-", ms=3)
    a2.axhline(273, color="0.5", lw=0.6, ls=":")
    a2.invert_yaxis()
    a2.set_ylabel("topo sobre o sitio\nTb (K), paralaxe\ninvertida (10 km)", fontsize=8)
    a2.text(horas(datetime(2026, 8, 25, 12, 10)), 274, "273 K: terreno ou nuvem baixa", fontsize=7, color="0.4", va="top")
    a2.set_ylim(285, 210)
    ev = [(datetime(2026, 8, 26, 2, 35, 12), "ML 2,5 (~10 km SSE)", "orange"),
          (datetime(2026, 8, 26, 2, 52, 16), "ruptura Tsangbu Ri (Ms 5,2)", "red"),
          (datetime(2026, 8, 26, 2, 59), "cheia no porto de Kyirong", "blue"),
          (datetime(2026, 8, 26, 3, 15), "Bhote Koshi sobe (FFD)", "blue"),
          (datetime(2026, 8, 26, 4, 43), "Galchhi", "blue"),
          (datetime(2026, 8, 26, 6, 0, 35), "2o deslizamento (Ms 4,2, 7 km NNW)", "red")]
    for k, (t, rot, cor) in enumerate(ev):
        for ax in (a1, a2, a3):
            ax.axvline(horas(t), color=cor, lw=0.9, alpha=0.7)
        a3.text(horas(t) + 0.04, 0.95 - 0.12 * k, rot, color=cor, fontsize=7.5, va="top", transform=a3.get_xaxis_transform())
    fases = [(17.5, 22.0, 0.0, "1. reservatorio?\nnuvem espessa sobre o sitio,\n~5 mm de chuva (IMERG)", "#d0e4f5"),
             (22.0, 25.0, 0.0, "2a. a conveccao profunda\nperto do sitio colapsa\n(22 -> 01 UTC)", "#f5e0c8"),
             (24.0, 25.4, 0.34, "2b. o topo sobre o sitio\ndesce ao terreno\n(00 -> 01:20 UTC)", "#f5c8c8"),
             (25.4, 26.87, 0.0, "3. espera\n~1,5 h", "#e8e8e8"),
             (26.87, 30.0, 0.0, "4. ruptura e cheia\n5. 2o deslizamento", "#f0d0f0")]
    for x0, x1, y0, rot, cor in fases:
        a3.axvspan(x0, x1, ymin=y0, ymax=y0 + 0.30, color=cor)
        a3.text((x0 + x1) / 2, y0 + 0.15, rot, ha="center", va="center", fontsize=7, transform=a3.get_xaxis_transform())
    a3.set_yticks([]); a3.set_ylabel("eventos e\nfases da hipotese", fontsize=8)
    tk = list(range(12, 32, 2))
    a3.set_xticks(tk); a3.set_xticklabels(["%02d" % (h % 24) for h in tk])
    a3.set_xlim(12, 31); a3.set_xlabel("UTC (25/08 -> 26/08); NPT = UTC + 5:45; hora de Pequim = UTC + 8")
    fig.tight_layout()
    out = os.path.join(SAIDA, "linha_do_tempo.png")
    fig.savefig(out, dpi=130)
    print(out)


if __name__ == "__main__":
    main()
