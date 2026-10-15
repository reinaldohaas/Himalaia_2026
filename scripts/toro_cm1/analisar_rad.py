# -*- coding: utf-8 -*-
"""Analise das rodadas com radiacao e fluxos (rad_06utc, rad_12utc). Saida a cada 30 min; eixo em hora UTC de 25/08."""
import json, os, sys
import numpy as np
_trapz = getattr(np, "trapezoid", None) or np.trapz   # numpy < 2.0 nao tem trapezoid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grads

SP = os.path.dirname(os.path.abspath(__file__))
ZBASE, DX, TAP, ANF = 3000.0, 500.0, 1800.0, 1.5
RUNS = {"rad_06utc": 6.0, "rad_12utc": 12.0}


def um(run, h0):
    d = os.path.join(SP, run)
    s, dd = grads.ler(os.path.join(d, "cm1out_s.ctl"),
                      ["rain", "zs", "zhval", "th", "prs", "rho", "qc", "qr", "qi", "qs", "qg", "cci", "qv",
                       "uinterp", "vinterp", "winterp", "hfx", "qfx", "tsk", "lwp", "cwp", "gsw", "lu"])
    st, _ = grads.stats(os.path.join(d, "cm1out_stats.ctl"))
    x = dd["xdef"]; X, Y = np.meshgrid(x, x)
    anf = (abs(X) <= ANF) & (abs(Y) <= ANF)
    zs = s["zs"][0, 0] + ZBASE; zh = s["zhval"] + ZBASE
    T = s["th"] * (s["prs"] / 1e5) ** 0.2857
    frio = T < 273.15; misto = frio & (T > 235.15)
    liq = (s["qc"] + s["qr"]) * s["rho"]; slw = np.where(frio, liq, 0.0)
    gelo = (s["qi"] + s["qs"] + s["qg"]) * s["rho"]
    nt = slw.shape[0]; hh = h0 + np.arange(nt) * TAP / 3600.
    dz = np.clip(np.gradient(zh, axis=1), 1, None)
    slw_col = np.nansum(slw * dz, axis=1); liq_col = np.nansum(liq * dz, axis=1); gelo_col = np.nansum(gelo * dz, axis=1)
    gy, gx = np.gradient(zs, DX); tana = np.hypot(gx, gy)
    vh0 = np.hypot(s["uinterp"][:, 0], s["vinterp"][:, 0])
    dep = slw[:, 0] * vh0 * tana * DX * DX
    dep_anf = np.nansum(np.where(anf, dep, 0), axis=(1, 2))
    w = s["winterp"]
    m_anf = lambda a: np.nanmean(np.where(anf, a, np.nan), axis=(1, 2))
    # topo de nuvem: maior z com (qc+qi+qs) > 0.01 g/kg
    cond = (s["qc"] + s["qi"] + s["qs"]) > 1e-5
    ztop = np.where(cond.any(axis=1), np.nanmax(np.where(cond, zh, np.nan), axis=1), np.nan)
    o = dict(
        hora_utc=hh.tolist(), nt=int(nt),
        wmax_stats=st["wmax"].tolist(), wmax=np.nanmax(w, axis=(1, 2, 3)).tolist(),
        wmax_anf=np.nanmax(np.where(anf[None, None], w, -99), axis=(1, 2, 3)).tolist(),
        liq_kt=(np.nansum(liq_col, axis=(1, 2)) * DX * DX / 1e6).tolist(),
        slw_kt=(np.nansum(slw_col, axis=(1, 2)) * DX * DX / 1e6).tolist(),
        gelo_kt=(np.nansum(gelo_col, axis=(1, 2)) * DX * DX / 1e6).tolist(),
        slw_anf_t=(np.nansum(np.where(anf, slw_col, 0), axis=(1, 2)) * DX * DX / 1e3).tolist(),
        lwc_sr_max=(np.nanmax(slw, axis=(1, 2, 3)) * 1e3).tolist(),
        lwc_sr_anf_max=(np.nanmax(np.where(anf[None, None], slw, 0), axis=(1, 2, 3)) * 1e3).tolist(),
        icnc_max=(np.nanmax(np.where(misto, s["cci"] * s["rho"], 0), axis=(1, 2, 3)) / 1e3).tolist(),
        rain_max=np.nanmax(s["rain"][:, 0] * 10, axis=(1, 2)).tolist(),
        rain_anf=m_anf(s["rain"][:, 0] * 10).tolist(),
        rain_media=np.nanmean(s["rain"][:, 0] * 10, axis=(1, 2)).tolist(),
        hfx_dom=np.nanmean(s["hfx"][:, 0], axis=(1, 2)).tolist(), hfx_anf=m_anf(s["hfx"][:, 0]).tolist(),
        tsk_anf=(m_anf(s["tsk"][:, 0]) - 273.15).tolist(), gsw_dom=np.nanmean(s["gsw"][:, 0], axis=(1, 2)).tolist(),
        ztop_max=np.nanmax(ztop, axis=(1, 2)).tolist(),
        area_nuvem_km2=(cond.any(axis=1).sum(axis=(1, 2)) * 0.25).tolist(),
        dep_anf_kg_s=dep_anf.tolist(),
        dep_anf_m3=float(_trapz(dep_anf, hh * 3600) / 1000.0) if nt > 1 else 0.0,
        dep_dom_m3=float(_trapz(np.nansum(dep, axis=(1, 2)), hh * 3600) / 1000.0) if nt > 1 else 0.0,
    )
    for nome, a in [("slw_col", slw_col), ("liq_col", liq_col), ("gelo_col", gelo_col), ("rain", s["rain"][:, 0] * 10)]:
        np.save(os.path.join(d, "campo_%s.npy" % nome), a.astype(np.float32))
    return o


if __name__ == "__main__":
    R = {}
    for run, h0 in RUNS.items():
        try:
            R[run] = o = um(run, h0)
        except Exception as e:
            print(run, "ERRO", e); continue
        print("== %s  (%d saidas, ate %.1f UTC)" % (run, o["nt"], o["hora_utc"][-1]))
        print(" hora  wmax  w_anf  liq(kt) SLW(kt) gelo(kt) SLWanf(t) LWCsr  ICNC/L  chuvaMx chuvaAnf  hfx_dom hfx_anf tsk_anf ztop  nuvem_km2")
        for k in range(o["nt"]):
            print(" %5.1f %5.2f %5.2f %8.1f %7.1f %8.1f %8.1f %6.2f %7.1f %7.2f %7.3f %8.0f %7.0f %7.1f %5.0f %7.1f" % (
                o["hora_utc"][k] % 24, o["wmax"][k], o["wmax_anf"][k], o["liq_kt"][k], o["slw_kt"][k], o["gelo_kt"][k],
                o["slw_anf_t"][k], o["lwc_sr_max"][k], o["icnc_max"][k], o["rain_max"][k], o["rain_anf"][k],
                o["hfx_dom"][k], o["hfx_anf"][k], o["tsk_anf"][k], np.nan_to_num(o["ztop_max"][k]), o["area_nuvem_km2"][k]))
        print(" deposicao por impacto (E=1): anfiteatro %.0f m3, dominio %.0f m3" % (o["dep_anf_m3"], o["dep_dom_m3"]))
    json.dump(R, open(os.path.join(SP, "cm1_rad_resultados.json"), "w"), indent=1)
