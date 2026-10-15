# -*- coding: utf-8 -*-
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grads

SP = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(SP, "cm1_terreno_resultados.json")))
saida = sys.argv[1]
ROT = {"pre": "ERA5 25/08 12 UTC", "pico": "ERA5 25/08 18 UTC", "pre_colapso": "ERA5 26/08 00 UTC"}
COR = {"pre": "#d95f02", "pico": "#1b9e77", "pre_colapso": "#7570b3"}
x = np.arange(80) * 0.5 - 19.75
fig = plt.figure(figsize=(16, 10))
for i, t in enumerate(["pre", "pico", "pre_colapso"]):
    s, d = grads.ler(os.path.join(SP, "ter_%s_nssl" % t, "cm1out_s.ctl"),
                     ["zs", "zhval", "th", "prs", "rho", "qc", "qr", "qv", "winterp"])
    zs = s["zs"][0, 0] + 3000; zh = s["zhval"] + 3000
    T = s["th"] * (s["prs"] / 1e5) ** 0.2857 - 273.15
    lwc = (s["qc"] + s["qr"]) * s["rho"] * 1e3
    es = 6.112 * np.exp(17.67 * T / (T + 243.5)); ur = s["qv"] / (0.622 * es / (s["prs"] / 100 - es)) * 100
    dz = np.gradient(zh, axis=1)
    col = np.nansum(lwc * dz, axis=1)                      # g/m2
    a = fig.add_subplot(3, 3, i + 1)
    im = a.pcolormesh(x, x, col.max(axis=0), cmap="Blues", shading="auto", vmin=0, vmax=max(col.max(), 1))
    a.contour(x, x, zs, np.arange(3500, 7000, 500), colors="k", linewidths=.5)
    a.plot(0, 0, "r*", ms=11); a.add_patch(plt.Rectangle((-1.5, -1.5), 3, 3, fill=False, ec="r", lw=1))
    a.set_title("%s — água líquida na coluna, máx em 3 h (g/m²)" % ROT[t], fontsize=9)
    a.set_aspect("equal"); plt.colorbar(im, ax=a, shrink=.85)
    k = s["zhval"].shape[0] - 1
    if col.max() > 0:
        k = int(np.argmax(col.max(axis=(1, 2))))
    ic = 39
    a = fig.add_subplot(3, 3, 4 + i)
    Y = np.broadcast_to(x[None, :], zh[k, :, :, ic].shape); Z = zh[k, :, :, ic] / 1000
    im = a.pcolormesh(Y, Z, ur[k, :, :, ic], cmap="YlGnBu", shading="auto", vmin=40, vmax=100)
    a.contour(Y, Z, lwc[k, :, :, ic], [0.01], colors="m", linewidths=1.4)
    a.contour(Y, Z, T[k, :, :, ic], [0], colors="r", linewidths=1.2, linestyles="--")
    a.contour(Y, Z, s["winterp"][k, :, :, ic], [-.5, .5, 1], colors=["b", "k", "k"], linewidths=.6)
    a.fill_between(x, 3, zs[:, ic] / 1000, color="0.45"); a.set_ylim(3, 10); a.axvline(0, color="r", lw=.6, ls=":")
    a.set_title("corte S–N em x=0, t=%d min: UR (%%), nuvem (magenta), 0 °C (vermelho), w ±0,5 m/s" % (k * 15), fontsize=8)
    a.set_xlabel("y (km, sul → norte)"); a.set_ylabel("z (km ASL)"); plt.colorbar(im, ax=a, shrink=.85)
for j, (k, tit) in enumerate([("wmax_stats", "w máx no domínio (m/s)"), ("wmax_anf", "w máx sobre o anfiteatro 3×3 km (m/s)"),
                              ("rain_max", "precipitação acumulada máx (mm)")]):
    a = fig.add_subplot(3, 3, 7 + j)
    for t in ["pre", "pico", "pre_colapso"]:
        o = R["ter_%s_nssl" % t]
        a.plot(np.linspace(0, 180, len(o[k])), o[k], color=COR[t], lw=1.6, label=ROT[t])
    a.set_title(tit, fontsize=9); a.set_xlabel("min"); a.grid(alpha=.3)
    if j == 0: a.legend(fontsize=8)
fig.suptitle("toro-CM1 com terreno Copernicus GLO-30 (40×40 km, Δx=500 m, sem bolha, NSSL+SIP, 3 h) — sondagem ERA5 hidrostaticamente consistente",
             fontsize=11)
fig.tight_layout(rect=[0, 0, 1, .96]); fig.savefig(saida, dpi=110); print("figura:", saida)
