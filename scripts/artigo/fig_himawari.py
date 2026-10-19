# -*- coding: utf-8 -*-
"""
Figure for the paper: the mesoscale convective system of 25-26 Aug 2026 in Himawari-9 AHI band 13.
(a-d) Tb maps at 12:00, 18:00, 22:00 and 02:50 UTC with the 213 K contour, the parallax-corrected track and the
site; (e) area of the tracked system (< 213 K) and its distance to the site; (f) Tb over the site.
Reads the cached segment-3 HSD files (scripts/himawari/trajetoria_sistema.py) and trajetoria.json.
Usage: python fig_himawari.py <dir_hsd> <trajetoria.json> <out.png>
"""
import glob
import json
import os
import sys
from datetime import datetime

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "himawari"))
import ahi_hsd as hsd  # noqa: E402
import trajetoria_sistema as T  # noqa: E402

TEMPOS = ["20260825_1200", "20260825_1800", "20260825_2200", "20260826_0250"]
BOX = (25.5, 32.0, 83.0, 92.5)


def main(dhsd, traj, png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    lat = np.arange(BOX[1], BOX[0] - 1e-9, -0.04); lon = np.arange(BOX[2], BOX[3] + 1e-9, 0.04)
    reg = json.load(open(traj))["registros"]
    tr = [(r["sistema"]["lon"], r["sistema"]["lat"], r["utc"]) for r in reg if r["sistema"]]
    fig = plt.figure(figsize=(7.2, 8.6))
    gs = GridSpec(3, 2, figure=fig, height_ratios=[1, 1, 0.95], hspace=0.28, wspace=0.12)
    for k, tt in enumerate(TEMPOS):
        arqs = sorted(glob.glob(os.path.join(dhsd, "HS_H09_%s_B13_FLDK_R20_S*.DAT*" % tt)))
        tb, s0 = T.reamostra(arqs, lat, lon)
        ax = fig.add_subplot(gs[k // 2, k % 2])
        pc = ax.pcolormesh(lon, lat, tb, cmap="gray_r", vmin=190, vmax=300, shading="auto", rasterized=True)
        ax.contour(lon, lat, tb, levels=[213], colors="red", linewidths=0.6)
        ax.plot([p[0] for p in tr], [p[1] for p in tr], "-", c="orange", lw=1.3)
        tnow = datetime.strptime(tt, "%Y%m%d_%H%M")
        cur = [p for p in tr if datetime.strptime(p[2], "%Y-%m-%dT%H:%MZ") == tnow]
        if cur:
            ax.plot(cur[0][0], cur[0][1], "o", mfc="orange", mec="k", ms=6)
        ax.plot(T.SITIO[1], T.SITIO[0], "*", c="cyan", mec="k", ms=12)
        ax.set_xlim(BOX[2], BOX[3]); ax.set_ylim(BOX[0], BOX[1]); ax.set_aspect(1 / np.cos(np.radians(28.5)))
        ax.text(0.02, 0.96, "abcd"[k], transform=ax.transAxes, fontweight="bold", va="top", color="w", fontsize=11)
        ax.text(0.98, 0.04, tnow.strftime("%d Aug %H:%M UTC"), transform=ax.transAxes, ha="right", color="w", fontsize=8.5)
        ax.tick_params(labelsize=7.5)
        if k % 2:
            ax.set_yticklabels([])
        if k < 2:
            ax.set_xticklabels([])
    cb = fig.colorbar(pc, ax=fig.axes[:4], shrink=0.75, pad=0.02); cb.set_label("B13 brightness temperature (K)", fontsize=8); cb.ax.tick_params(labelsize=7.5)
    ax = fig.add_subplot(gs[2, :])
    t = [datetime.strptime(r["utc"], "%Y-%m-%dT%H:%MZ") for r in reg]
    h = np.array([(x - datetime(2026, 8, 25)).total_seconds() / 3600 for x in t])
    area = np.array([r["sistema"]["area_km2"] / 1e3 if r["sistema"] else np.nan for r in reg])
    dist = np.array([r["sistema"]["dist_sitio_km"] if r["sistema"] else np.nan for r in reg])
    tbs = np.array([r["tb_sitio"] for r in reg])
    ax.plot(h, area, "-o", c="k", ms=3, lw=1.2, label="system area < 213 K (10$^3$ km$^2$)")
    ax.set_ylabel("area (10$^3$ km$^2$)", fontsize=8.5)
    ax2 = ax.twinx(); ax2.plot(h, dist, "-s", c="tab:orange", ms=3, lw=1.2, label="distance to site (km)")
    ax2.set_ylabel("distance to site (km)", fontsize=8.5, color="tab:orange")
    ax3 = ax.twinx(); ax3.spines.right.set_position(("axes", 1.13)); ax3.plot(h, tbs, ":", c="tab:blue", lw=1.3)
    ax3.set_ylabel("Tb at site (K)", fontsize=8.5, color="tab:blue")
    ax.axvline(24 + 2 + 52 / 60, c="r", lw=0.9); ax.text(26.9, ax.get_ylim()[1] * 0.9, "collapse", color="r", fontsize=8, ha="right")
    ax.set_xticks(range(9, 28, 3)); ax.set_xticklabels(["%02d" % (x % 24) for x in range(9, 28, 3)])
    ax.set_xlabel("UTC, 25-26 August 2026", fontsize=8.5); ax.grid(alpha=0.3)
    for a in (ax, ax2, ax3):
        a.tick_params(labelsize=7.5)
    ax.text(0.01, 0.95, "e", transform=ax.transAxes, fontweight="bold", va="top", fontsize=11)
    fig.savefig(png, dpi=220, bbox_inches="tight")
    print("ok", png)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
