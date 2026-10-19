# -*- coding: utf-8 -*-
"""
Figure: WRF (ERA5-driven, 3-km d02) against Himawari-9 for the convective system of 25-26 Aug 2026.
Row 1: Himawari B13 Tb at 12:00, 18:00, 22:00 and 02:50 UTC (213 K contour); row 2: WRF outgoing long-wave radiation
at the same times (120 W m-2 contour); both with the observed track and the site. Row 3: area of the tracked observed
system (< 213 K), of the largest WRF object (< 120 W m-2) within 600 km of the site, and of cold cloud within 150 km
of the site in each (Himawari < 213 K; WRF < 120 W m-2).
Usage: python fig_wrf_himawari.py <dir_hsd> <wrfaux_d02.nc> <trajetoria.json> <diag_mcs_d02.json> <out.png> [pt|en]
"""
import glob
import json
import os
import sys
from datetime import datetime

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "himawari"))
import trajetoria_sistema as T  # noqa: E402

TEMPOS = ["2026-08-25_12:00", "2026-08-25_18:00", "2026-08-25_22:00", "2026-08-26_02:50"]
BOX = (25.8, 32.0, 82.7, 93.3)
TXT = {"en": {"tb": "Himawari-9 B13 Tb (K)", "olr": "WRF OLR (W m$^{-2}$)",
              "obs": "observed system (< 213 K)", "wrf": "largest WRF object (< 120 W m$^{-2}$)", "him150": "Himawari < 213 K within 150 km of site",
              "wrf150": "WRF < 120 W m$^{-2}$ within 150 km of site", "area": "area (10$^3$ km$^2$)", "utc": "UTC, 25-26 August 2026", "col": "collapse",
              "sem": "WRF output at 02:30"},
       "pt": {"tb": "Himawari-9 B13, Tb (K)", "olr": "WRF, OLR (W m$^{-2}$)",
              "obs": "sistema observado (< 213 K)", "wrf": "maior objeto do WRF (< 120 W m$^{-2}$)", "him150": "Himawari < 213 K a até 150 km do sítio",
              "wrf150": "WRF < 120 W m$^{-2}$ a até 150 km do sítio", "area": "área (10$^3$ km$^2$)", "utc": "UTC, 25-26 de agosto de 2026", "col": "colapso",
              "sem": "saída do WRF às 02:30"}}


def main(dhsd, aux, traj, diag, png, lang="en"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    import netCDF4
    L = TXT[lang]
    reg = json.load(open(traj))["registros"]
    tr = [(r["sistema"]["lon"], r["sistema"]["lat"]) for r in reg if r["sistema"]]
    lat = np.arange(BOX[1], BOX[0] - 1e-9, -0.04); lon = np.arange(BOX[2], BOX[3] + 1e-9, 0.04)
    with netCDF4.Dataset(aux) as f:
        wt = [b"".join(t).decode()[:16] for t in f.variables["Times"][:]]
        wla = f.variables["XLAT"][0]; wlo = f.variables["XLONG"][0]; olr = f.variables["OLR"][:]
    fig = plt.figure(figsize=(11, 8.4))
    gs = GridSpec(3, 4, figure=fig, height_ratios=[1, 1, 0.9], hspace=0.22, wspace=0.08)
    for c, t in enumerate(TEMPOS):
        tt = datetime.strptime(t, "%Y-%m-%d_%H:%M")
        arqs = sorted(glob.glob(os.path.join(dhsd, "HS_H09_%s_B13_FLDK_R20_S*.DAT*" % tt.strftime("%Y%m%d_%H%M"))))
        tb, _ = T.reamostra(arqs, lat, lon)
        a = fig.add_subplot(gs[0, c])
        p1 = a.pcolormesh(lon, lat, tb, cmap="gray_r", vmin=190, vmax=300, shading="auto", rasterized=True)
        a.contour(lon, lat, tb, levels=[213], colors="red", linewidths=0.5)
        b = fig.add_subplot(gs[1, c])
        k = wt.index(t) if t in wt else wt.index("2026-08-26_02:30")
        p2 = b.pcolormesh(wlo, wla, olr[k], cmap="gray", vmin=80, vmax=320, shading="auto", rasterized=True)
        b.contour(wlo, wla, olr[k], levels=[120], colors="red", linewidths=0.5)
        if t not in wt:
            b.text(0.98, 0.15, L["sem"], transform=b.transAxes, ha="right", color="w", fontsize=7)
        for ax in (a, b):
            ax.plot([p[0] for p in tr], [p[1] for p in tr], "-", c="orange", lw=1.1)
            ax.plot(T.SITIO[1], T.SITIO[0], "*", c="cyan", mec="k", ms=10)
            ax.set_xlim(BOX[2], BOX[3]); ax.set_ylim(BOX[0], BOX[1]); ax.set_aspect(1 / np.cos(np.radians(29)))
            ax.tick_params(labelsize=6.5)
            if c:
                ax.set_yticklabels([])
        a.set_xticklabels([])
        a.set_title(tt.strftime("%d/%m %H:%M UTC") if lang == "pt" else tt.strftime("%d Aug %H:%M UTC"), fontsize=8.5)
        a.text(0.03, 0.95, "abcd"[c], transform=a.transAxes, color="w", fontweight="bold", va="top")
        b.text(0.03, 0.95, "efgh"[c], transform=b.transAxes, color="w", fontweight="bold", va="top")
    cb1 = fig.colorbar(p1, ax=fig.axes[0:8:2], shrink=0.85, pad=0.01); cb1.set_label(L["tb"], fontsize=7); cb1.ax.tick_params(labelsize=6.5)
    cb2 = fig.colorbar(p2, ax=fig.axes[1:8:2], shrink=0.85, pad=0.01); cb2.set_label(L["olr"], fontsize=7); cb2.ax.tick_params(labelsize=6.5)
    ax = fig.add_subplot(gs[2, :])
    hora = lambda s: (datetime.strptime(s[:16], "%Y-%m-%dT%H:%M" if "T" in s else "%Y-%m-%d_%H:%M") - datetime(2026, 8, 25)).total_seconds() / 3600
    hh = [hora(r["utc"]) for r in reg]
    ax.plot(hh, [r["sistema"]["area_km2"] / 1e3 if r["sistema"] else np.nan for r in reg], "-o", c="k", ms=3, lw=1.2, label=L["obs"])
    ax.plot(hh, [r["area213_150km"] / 1e3 for r in reg], ":", c="k", lw=1.2, label=L["him150"])
    dg = json.load(open(diag))["linhas"]
    hw = [hora(l["utc"]) for l in dg]
    ax.plot(hw, [l["wrf"]["area_km2"] / 1e3 if l["wrf"] else np.nan for l in dg], "-s", c="tab:red", ms=2.5, lw=1.1, label=L["wrf"])
    # WRF cold area within 150 km of the site
    d = np.hypot((wla - T.SITIO[0]) * 111.32, (wlo - T.SITIO[1]) * 111.32 * np.cos(np.radians(T.SITIO[0])))
    a150 = [(np.nan if olr[k].max() <= 0 else float(((olr[k] < 120) & (d < 150)).sum() * 9.0) / 1e3) for k in range(len(wt))]
    ax.plot([hora(t) for t in wt], a150, ":", c="tab:red", lw=1.3, label=L["wrf150"])
    ax.axvline(24 + 2 + 52 / 60, c="r", lw=0.9)
    ax.set_yscale("log"); ax.set_ylim(0.1, 300); ax.set_xlim(0, 27)
    ax.set_xticks(range(0, 28, 3)); ax.set_xticklabels(["%02d" % (x % 24) for x in range(0, 28, 3)], fontsize=7.5)
    ax.tick_params(labelsize=7.5); ax.set_ylabel(L["area"], fontsize=8); ax.set_xlabel(L["utc"], fontsize=8)
    ax.legend(fontsize=7, ncol=2, loc="upper right"); ax.grid(alpha=0.3, which="both")
    ax.text(0.005, 0.95, "i", transform=ax.transAxes, fontweight="bold", va="top")
    fig.savefig(png, dpi=200, bbox_inches="tight")
    print("ok", png)


if __name__ == "__main__":
    main(*sys.argv[1:6], *(sys.argv[6:7] or ["en"]))
