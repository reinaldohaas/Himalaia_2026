# -*- coding: utf-8 -*-
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grads
SP = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(SP, "cm1_rad_resultados.json")))
COR = {"rad_06utc": "#d95f02", "rad_12utc": "#1b9e77"}
ROT = {"rad_06utc": "início 25/08 06 UTC (meio-dia local)", "rad_12utc": "início 25/08 12 UTC (pôr do sol)"}
x = np.arange(80) * 0.5 - 19.75
fig = plt.figure(figsize=(16, 10.5))
# serie
P = [("slw_anf_t", "água líq. T<0 °C sobre o anfiteatro 3×3 km (t)", "linear"),
     ("lwc_sr_max", "LWC super-resfriado máx no domínio (g/m³)", "linear"),
     ("rain_anf", "precipitação acumulada sobre o anfiteatro (mm)", "linear"),
     ("hfx_anf", "calor sensível sobre o anfiteatro (W/m²)", "linear"),
     ("ztop_max", "topo de nuvem máx (m ASL)", "linear"),
     ("icnc_max", "cristais máx, fase mista (L⁻¹)", "symlog")]
for n, (k, tit, esc) in enumerate(P):
    a = fig.add_subplot(3, 3, n + 1)
    for run, o in R.items():
        h = np.array(o["hora_utc"])
        a.plot(h, np.nan_to_num(o[k]), color=COR[run], lw=1.7, label=ROT[run])
    a.axvline(24 + 2 + 52 / 60, color="k", ls="--", lw=1); a.text(24 + 2.9, a.get_ylim()[1] * .9, " colapso", fontsize=8)
    a.axvspan(18, 21, color="0.85", zorder=0)
    a.set_title(tit, fontsize=9); a.grid(alpha=.3); a.set_xlim(6, 27.2)
    a.set_xticks(range(6, 28, 3)); a.set_xticklabels(["%02d" % (h % 24) for h in range(6, 28, 3)]); a.set_xlabel("hora UTC (25→26/08)")
    if esc == "symlog": a.set_yscale("symlog", linthresh=10)
    if n == 0: a.legend(fontsize=8, loc="upper right")
# mapas: chuva acumulada (06 utc) e SLW coluna max noturna (12 utc); corte no colapso (12 utc)
zs = np.load(os.path.join(SP, "terreno", "zs_modelo_asl.npy"))
r6 = np.load(os.path.join(SP, "rad_06utc", "campo_rain.npy"))
a = fig.add_subplot(3, 3, 7)
im = a.pcolormesh(x, x, r6[-1], cmap="YlGnBu", shading="auto"); plt.colorbar(im, ax=a, shrink=.85)
a.contour(x, x, zs, np.arange(3500, 7000, 500), colors="k", linewidths=.4); a.plot(0, 0, "r*", ms=11)
a.add_patch(plt.Rectangle((-1.5, -1.5), 3, 3, fill=False, ec="r")); a.set_aspect("equal")
a.set_title("início 06 UTC: precipitação acumulada até %02.0f UTC (mm)" % (R["rad_06utc"]["hora_utc"][-1] % 24), fontsize=9)
s12 = np.load(os.path.join(SP, "rad_12utc", "campo_slw_col.npy"))
a = fig.add_subplot(3, 3, 8)
k = int(np.argmin(abs(np.array(R["rad_12utc"]["hora_utc"]) - (24 + 2.833))))
im = a.pcolormesh(x, x, s12[k] * 1e3, cmap="Blues", shading="auto"); plt.colorbar(im, ax=a, shrink=.85)
a.contour(x, x, zs, np.arange(3500, 7000, 500), colors="k", linewidths=.4); a.plot(0, 0, "r*", ms=11)
a.add_patch(plt.Rectangle((-1.5, -1.5), 3, 3, fill=False, ec="r")); a.set_aspect("equal")
a.set_title("início 12 UTC: água líq. T<0 °C na coluna às %02.1f UTC (g/m²)" % (R["rad_12utc"]["hora_utc"][k] % 24), fontsize=9)
s, d = grads.ler(os.path.join(SP, "rad_12utc", "cm1out_s.ctl"), ["zhval", "th", "prs", "rho", "qc", "qr"])
zh = s["zhval"][k] + 3000; T = s["th"][k] * (s["prs"][k] / 1e5) ** .2857 - 273.15; lwc = (s["qc"][k] + s["qr"][k]) * s["rho"][k] * 1e3
a = fig.add_subplot(3, 3, 9); ic = 39
Y = np.broadcast_to(x[None, :], zh[:, :, ic].shape)
im = a.pcolormesh(Y, zh[:, :, ic] / 1000, lwc[:, :, ic], cmap="Blues", shading="auto", vmin=0); plt.colorbar(im, ax=a, shrink=.85)
a.contour(Y, zh[:, :, ic] / 1000, T[:, :, ic], [0], colors="r", linestyles="--")
a.fill_between(x, 3, zs[:, ic] / 1000, color="0.45"); a.set_ylim(3, 8); a.axvline(0, color="r", lw=.6, ls=":")
a.set_title("início 12 UTC: corte S–N em x=0 às %02.1f UTC — LWC (g/m³), 0 °C" % (R["rad_12utc"]["hora_utc"][k] % 24), fontsize=9)
a.set_xlabel("y (km)"); a.set_ylabel("z (km ASL)")
fig.suptitle("toro-CM1 + terreno GLO-30 + radiação RRTMG + fluxos de superfície (MM5/slab) + uso do solo WorldCover — Lhende Khola, 25–26/08/2026",
             fontsize=11)
fig.tight_layout(rect=[0, 0, 1, .96]); fig.savefig(sys.argv[1], dpi=110); print("figura:", sys.argv[1])
