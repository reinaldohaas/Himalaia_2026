# -*- coding: utf-8 -*-
"""
Diferenca de refletancia B03 (Himawari-9, 500 m, ortorretificada) entre 26/08/2026 e o dia anterior, no mesmo horario
(00:00-03:00 UTC). No mesmo horario a geometria do sol e do satelite e praticamente a mesma (a declinacao muda
~0,4 grau), entao o relevo e as sombras se cancelam e sobra o que mudou: nuvem, nevoeiro, neve ou granizo novos.

Iluminacao: cos(i) = cos(sza) cos(s) + sin(sza) sin(s) cos(az_sol - aspecto), do GLO-30. Celulas com cos(i) < 0,1
estao na sombra propria (ou quase) e nao dizem nada sobre o chao.

Entradas: b03_orto.npz e b03_orto_20260825.npz (b03_ponto_drone.py), bacia_ponto.npz (ponto_drone.py).
Saidas: b03_diferenca.png, b03_diferenca.txt
"""
import os
import sys
from datetime import datetime, timedelta

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
D = os.path.join(RAIZ, "data", "processed", "himawari_b03")
P = (28.293985, 85.523964)
CICATRIZ = [(28.2830, 85.5225), (28.2870, 85.5300), (28.2950, 85.5300)]


def sol(t, lat, lon):
    """zenite e azimute (graus, a partir do N, horario) do sol"""
    n = t.timetuple().tm_yday
    g = 2 * np.pi / 365 * (n - 1 + (t.hour - 12) / 24)
    dec = 0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g) + 0.000907 * np.sin(2 * g)
    eqt = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g) - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    hs = np.radians(((t.hour * 60 + t.minute + eqt + 4 * lon) / 4) - 180)
    la = np.radians(lat)
    cz = np.sin(la) * np.sin(dec) + np.cos(la) * np.cos(dec) * np.cos(hs)
    z = np.arccos(cz)
    az = np.degrees(np.arctan2(-np.sin(hs) * np.cos(dec), np.cos(la) * np.sin(dec) - np.sin(la) * np.cos(dec) * np.cos(hs))) % 360
    return np.degrees(z), az


def main():
    a, b = np.load(os.path.join(D, "b03_orto.npz")), np.load(os.path.join(D, "b03_orto_20260825.npz"))
    lat, lon, Z = a["lat"], a["lon"], a["Z"]
    bac = np.load(os.path.join(RAIZ, "data", "processed", "ponto_drone", "bacia_ponto.npz"))
    r = bac["lat"][1] - bac["lat"][0]
    LON, LAT = np.meshgrid(lon, lat)
    mb = bac["mascara"][((LAT - bac["lat"][0]) / r).round().astype(int), ((LON - bac["lon"][0]) / r).round().astype(int)]
    # declividade e aspecto na grade do B03
    dy = abs(lat[1] - lat[0]) * 111320.0; dx = abs(lon[1] - lon[0]) * 111320.0 * np.cos(np.radians(P[0]))
    gy, gx = np.gradient(Z * 1000.0, -dy, dx)                    # lat decresce com a linha
    s = np.arctan(np.hypot(gx, gy)); asp = (np.degrees(np.arctan2(-gx, -gy)) + 360) % 360
    hs = sorted(k for k in a.files if k.startswith("t") and k in b.files)
    lin = ["# B03 26/08 - 25/08 no mesmo horario (refletancia/cos(sza)); bacia do ponto do drone (1,19 km2) e disco de 3 km",
           "# frac_iluminada = fracao da bacia com cos(i) >= 0,1",
           "UTC   sza  az_sol | bacia: r26   r25   dif  frac_ilum | dif so iluminada | disco 3 km: dif | vale < 4 km: dif"]
    paineis = []
    disco = np.hypot((LAT - P[0]) * 111.32, (LON - P[1]) * 111.32 * np.cos(np.radians(P[0]))) <= 3.0
    vale = Z < 4.0
    for k in hs:
        t = datetime(2026, 8, 26, int(k[1:3]), int(k[3:5]))
        sza, az = sol(t, *P)
        ci = np.cos(np.radians(sza)) * np.cos(s) + np.sin(np.radians(sza)) * np.sin(s) * np.cos(np.radians(az - asp))
        d = a[k] - b[k]
        il = mb & (ci >= 0.1)
        lin.append("%s %5.1f %5.0f | %6.3f %6.3f %6.3f  %4.2f | %6.3f | %6.3f | %6.3f" % (
            t.strftime("%H:%M"), sza, az, np.nanmean(a[k][mb]), np.nanmean(b[k][mb]), np.nanmean(d[mb]), il.sum() / mb.sum(),
            np.nanmean(d[il]) if il.any() else np.nan, np.nanmean(d[disco]), np.nanmean(d[vale])))
        paineis.append((t, sza, d, ci))
    txt = "\n".join(lin) + "\n"
    open(os.path.join(D, "b03_diferenca.txt"), "w", encoding="utf-8").write(txt)
    print(txt)

    n = len(paineis); nc = 5; nl = int(np.ceil(n / nc))
    fig, axs = plt.subplots(nl, nc, figsize=(3.3 * nc, 3.4 * nl))
    for ax in axs.ravel()[n:]:
        ax.axis("off")
    ext = [lon[0], lon[-1], lat[-1], lat[0]]
    for ax, (t, sza, d, ci) in zip(axs.ravel(), paineis):
        im = ax.imshow(d, extent=ext, cmap="RdBu_r", vmin=-0.5, vmax=0.5, interpolation="nearest")
        ax.contourf(lon, lat, (ci < 0.1).astype(float), levels=[0.5, 1.5], colors="none", hatches=["...."])
        ax.contour(lon, lat, Z, levels=[4, 5, 6, 7], colors="k", linewidths=0.3)
        ax.contour(lon, lat, mb.astype(float), levels=[0.5], colors="m", linewidths=1.2)
        ax.plot([c[1] for c in CICATRIZ], [c[0] for c in CICATRIZ], "g-", lw=1.5)
        ax.plot(P[1], P[0], "y*", ms=9, mec="k")
        ax.set_title("%s UTC (%s NPT) sza %.0f" % (t.strftime("%H:%M"), (t + timedelta(hours=5, minutes=45)).strftime("%H:%M"), sza), fontsize=8)
        ax.set_aspect(1 / np.cos(np.radians(P[0]))); ax.tick_params(labelsize=6)
    fig.colorbar(im, ax=axs.ravel().tolist(), shrink=0.5, label="refletancia 26/08 - 25/08")
    fig.suptitle("Himawari-9 B03 ortorretificado: 26/08 menos 25/08 no mesmo horario. Vermelho = mais claro no dia 26 (nuvem, nevoeiro, neve, granizo);\n"
                 "pontilhado = sombra propria do relevo (cos i < 0,1); magenta = bacia do ponto do drone; verde = cicatriz; curvas de 4-7 km", fontsize=9)
    fig.savefig(os.path.join(D, "b03_diferenca.png"), dpi=130, bbox_inches="tight")


if __name__ == "__main__":
    main()
