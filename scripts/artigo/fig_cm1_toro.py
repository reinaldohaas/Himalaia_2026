# -*- coding: utf-8 -*-
"""
Figure for the paper: CM1 anti-scavenging (Tinsley-type) experiments over the Lhende Khola amphitheatre,
18 UTC 25 Aug -> 03 UTC 26 Aug 2026, from the diagnostics in data/processed/toro_cm1/toro_exp_20261018/diag_*.json
(cluster/diag_toro.py). Panels: (a) supercooled liquid water over the amphitheatre; (b) rain rate over the
amphitheatre; (c) equivalent IR cloud-top temperature over the site against Himawari-9 B13.
Usage: python fig_cm1_toro.py <out.png>
"""
import json
import os
import sys

import numpy as np

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "processed", "toro_cm1", "toro_exp_20261018")
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "processed", "himawari_trajetoria", "trajetoria.txt")
RUNS = [("diag_rad_06utc_hib16x7.json", "control", "k", "-"),
        ("diag_toro_A.json", "suppression everywhere", "tab:orange", "-"),
        ("diag_toro_Ag.json", "suppression where no graupel", "tab:blue", "-"),
        ("diag_toro_Ag_vort.json", "  + imposed vortex", "tab:blue", "--"),
        ("diag_toro_Ag_gelo10.json", "  + ice seeding (10x)", "tab:purple", "-"),
        ("diag_toro_Ag_lev.json", "  + forced ascent 1 m/s", "tab:green", "-")]


def horas(h):
    return np.where(h < 6, h + 24, h)


def main(png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(3, 1, figsize=(7.2, 8.0), sharex=True)
    for f, lab, c, ls in RUNS:
        p = os.path.join(D, f)
        if not os.path.exists(p):
            continue
        s = json.load(open(p))["saidas"]
        h = horas(np.array([x["hora_utc"] for x in s]))
        m = h >= 18
        ax[0].plot(h[m], np.array([x["slw_t"] for x in s])[m] / 1e3, ls, c=c, lw=1.4, label=lab)
        ax[1].plot(h[m], np.array([x["taxa_mmh"] for x in s])[m], ls, c=c, lw=1.4)
        ax[2].plot(h[m], np.array([x["tb_sitio"] for x in s])[m], ls, c=c, lw=1.4)
    # Himawari-9 B13 over the site
    th, tb = [], []
    for l in open(H, encoding="utf-8"):
        if l.startswith("2026-08-"):
            hh = int(l[11:13]) + int(l[14:16]) / 60.0
            hh = hh + 24 if l.startswith("2026-08-26") else hh
            if hh >= 18:
                th.append(hh); tb.append(float(l.split()[1]))
    ax[2].plot(th, tb, "o", c="tab:red", ms=4, label="Himawari-9 B13 (observed)")
    for a in ax:
        a.axvline(24 + 2 + 52 / 60, c="r", lw=0.9, alpha=0.7)
        a.grid(alpha=0.3)
    ax[0].set_ylabel("supercooled liquid\nover amphitheatre (kt)")
    ax[1].set_ylabel("rain rate over\namphitheatre (mm h$^{-1}$)")
    ax[2].set_ylabel("cloud-top / surface\ntemperature at site (K)")
    ax[0].legend(fontsize=7.5, loc="upper left", ncol=2)
    ax[2].legend(fontsize=7.5, loc="lower left")
    ax[0].text(26.9, ax[0].get_ylim()[1] * 0.92, " collapse", color="r", fontsize=8)
    ax[2].set_xticks(range(18, 28)); ax[2].set_xticklabels(["%02d" % (x % 24) for x in range(18, 28)])
    ax[2].set_xlabel("UTC, 25-26 August 2026")
    for a, t in zip(ax, "abc"):
        a.text(0.005, 0.97, t, transform=a.transAxes, fontweight="bold", va="top", fontsize=11)
    fig.tight_layout(); fig.savefig(png, dpi=200)
    print("ok", png)


if __name__ == "__main__":
    main(sys.argv[1])
