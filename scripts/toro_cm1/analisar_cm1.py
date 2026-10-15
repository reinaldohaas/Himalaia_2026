# -*- coding: utf-8 -*-
"""Compara as 8 execucoes do toro-CM1 (4 sondagens x 2 microfisicas)."""
import json
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grads

SP = os.path.dirname(os.path.abspath(__file__))
SNDS = ["WK", "pre", "pico", "pre_colapso"]
MPS = ["morrison", "nssl"]
DX = DY = 500.0
DZ = 300.0
VOL = DX * DY * DZ
AREA = 20 * 20 * DX * DY


def um(run):
    d = os.path.join(SP, run)
    st, ds = grads.stats(os.path.join(d, "cm1out_stats.ctl"))
    s, dd = grads.ler(os.path.join(d, "cm1out_s.ctl"),
                      ["rain", "prate", "th", "prs", "rho", "qc", "qr", "qi", "qs", "qg", "cci", "nci", "ccw", "cape", "pwat"])
    ni = s["cci"] if "cci" in s else s["nci"]           # NSSL: cci ; Morrison: nci  (por kg)
    if "ccw" in s:
        ccw = s["ccw"]
    else:                                               # Morrison: Nc fixo = ndcnst (cm-3)
        ccw = 1000.0e6 / s["rho"]
    T = s["th"] * (s["prs"] / 1e5) ** 0.2857
    frio = T < 273.15
    liq = s["qc"] + s["qr"]
    slw = np.where(frio, liq, 0.0)                         # kg/kg super-resfriada
    slw_massa = np.nansum(s["rho"] * slw * VOL, axis=(1, 2, 3))   # kg no dominio, por tempo
    slw_lwc_max = np.nanmax(s["rho"] * slw, axis=(1, 2, 3)) * 1e3  # g/m3
    gelo = s["qi"] + s["qs"] + s["qg"]
    gelo_massa = np.nansum(s["rho"] * gelo * VOL, axis=(1, 2, 3))
    misto = frio & (T > 235.15)                             # fase mista 0 a -38 C
    cci_max = np.nanmax(np.where(misto, ni * s["rho"], 0), axis=(1, 2, 3)) / 1e3   # por litro
    # diametro medio de gotícula onde qc > 0.01 g/kg (so faz sentido com ccw prognostico)
    m = s["qc"] > 1e-5
    with np.errstate(all="ignore"):
        dm = np.where(m & (ccw > 1e3), (6 * s["qc"] / (np.pi * 1000.0 * ccw)) ** (1 / 3.), np.nan) * 1e6
    dm_sr = np.where(frio, dm, np.nan)
    rain = s["rain"][:, 0] * 10.0                          # cm -> mm
    prate = s["prate"][:, 0] * 3600.0                      # kg/m2/s -> mm/h
    t = np.arange(rain.shape[0]) * 300.0
    out = dict(
        t_min=(t / 60).tolist(),
        wmax=st["wmax"].tolist(),
        prate_max=np.nanmax(prate, axis=(1, 2)).tolist(),
        rain_media=np.nanmean(rain, axis=(1, 2)).tolist(),
        rain_max=np.nanmax(rain, axis=(1, 2)).tolist(),
        slw_massa_t=(slw_massa / 1e6).tolist(),           # kt
        slw_lwc_max=slw_lwc_max.tolist(),
        gelo_massa_t=(gelo_massa / 1e6).tolist(),
        cci_max_L=cci_max.tolist(),
        cape0=float(np.nanmean(s["cape"][0])), pwat0=float(np.nanmean(s["pwat"][0]) * 1000),
        dm_sr_med=float(np.nanmedian(dm_sr)) if np.isfinite(dm_sr).any() else None,
        dm_sr_p10=float(np.nanpercentile(dm_sr, 10)) if np.isfinite(dm_sr).any() else None,
        dm_sr_p90=float(np.nanpercentile(dm_sr, 90)) if np.isfinite(dm_sr).any() else None,
        nt=int(rain.shape[0]),
    )
    out["vol_chuva_m3"] = out["rain_media"][-1] / 1000.0 * AREA
    return out


if __name__ == "__main__":
    R = {}
    print("%-22s %3s %6s %8s %7s %7s %8s %7s %8s %9s %10s" % (
        "execucao", "nt", "wmax", "prateMx", "chuvaMd", "chuvaMx", "SLWmax", "LWCmx", "geloMx", "ICNCmx/L", "Dgota(p50)"))
    for snd in SNDS:
        for mp in MPS:
            run = "run_%s_%s" % (snd, mp)
            try:
                o = um(run)
            except Exception as e:
                print("%-22s  ERRO %s" % (run, e)); continue
            R[run] = o
            dm = "%.1f um" % o["dm_sr_med"] if o["dm_sr_med"] else "  --"
            print("%-22s %3d %6.1f %8.1f %7.2f %7.1f %8.1f %7.2f %8.1f %9.1f %10s" % (
                run, o["nt"], max(o["wmax"]), max(o["prate_max"]), o["rain_media"][-1], o["rain_max"][-1],
                max(o["slw_massa_t"]), max(o["slw_lwc_max"]), max(o["gelo_massa_t"]), max(o["cci_max_L"]), dm))
    print("\nunidades: wmax m/s | prateMx mm/h | chuva mm (media e max no dominio 10x10 km, t=120 min) |"
          " SLW kt (agua liquida T<0C no dominio) | LWCmx g/m3 | gelo kt | ICNC por litro na fase mista (0 a -38 C) | D gota um")
    json.dump(R, open(os.path.join(SP, "cm1_resultados.json"), "w"), indent=1)
