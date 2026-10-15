# -*- coding: utf-8 -*-
import json
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SP = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(SP, "cm1_resultados.json")))
saida = sys.argv[1]
COR = {"WK": "#444444", "pre": "#d95f02", "pico": "#1b9e77", "pre_colapso": "#7570b3"}
ROT = {"WK": "Weisman-Klemp (controle toro-CM1)", "pre": "ERA5 25/08 12 UTC",
       "pico": "ERA5 25/08 18 UTC", "pre_colapso": "ERA5 26/08 00 UTC (3 h antes)"}
PAIN = [("wmax", "w máx (m/s)"), ("prate_max", "taxa de precipitação máx (mm/h)"),
        ("rain_max", "chuva acumulada máx (mm)"), ("slw_lwc_max", "LWC super-resfriado máx (g/m³)"),
        ("slw_massa_t", "água líquida T<0 °C no domínio (kt)"), ("cci_max_L", "cristais de gelo máx, fase mista 0 a −38 °C (L⁻¹)")]
fig, ax = plt.subplots(2, 3, figsize=(15, 8.2))
for a, (k, tit) in zip(ax.flat, PAIN):
    for run, o in R.items():
        snd, mp = run[4:].rsplit("_", 1)
        a.plot(np.linspace(0, 120, len(o[k])), o[k], color=COR[snd], ls="-" if mp == "morrison" else "--", lw=1.6,
               label="%s · %s" % (ROT[snd], "Morrison" if mp == "morrison" else "NSSL+SIP"))
    a.set_title(tit, fontsize=10); a.set_xlabel("min"); a.grid(alpha=.3)
    if k == "cci_max_L":
        a.set_yscale("symlog", linthresh=1)
ax[0, 0].legend(fontsize=7, loc="upper right")
fig.suptitle("toro-CM1 (CM1 r21.1, 10×10 km, Δx=500 m, bolha +3 K) — sondagem idealizada × sondagem real ERA5 do Lhende Khola (solo 4.010 m)",
             fontsize=11)
fig.tight_layout(rect=[0, 0, 1, .96]); fig.savefig(saida, dpi=130)
print("figura:", saida)
