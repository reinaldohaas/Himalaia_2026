# -*- coding: utf-8 -*-
"""
Analise das rodadas do toro-CM1 com terreno GLO-30 (ter_<sondagem>_nssl).

Anfiteatro = janela de 3 x 3 km centrada no ponto de colapso (85,515 E; 28,271 N), que e a celula
central do dominio (x = y = 0).

Cota superior de deposicao por impacto na encosta (riming), por celula e por saida:
    D = rho * q_l(T<0) * |V_h| * tan(alfa) * E * A * dt
  q_l   : agua liquida (nuvem+chuva) no 1o nivel do modelo acima do solo, so se T < 0 C
  |V_h| : vento horizontal no mesmo nivel
  tan(alfa) * A : projecao vertical da encosta da celula (area que o vento "ve")
  E = 1 (eficiencia de coleta maxima) -> LIMITE SUPERIOR
"""
import json
import os
import sys
import numpy as np
_trapz = getattr(np, "trapezoid", None) or np.trapz   # numpy < 2.0 nao tem trapezoid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grads

SP = os.path.dirname(os.path.abspath(__file__))
ZBASE = 3000.0
DX = 500.0
TAPFRQ = 900.0
ANF = 1.5           # semi-largura da janela do anfiteatro (km)


def um(run):
    d = os.path.join(SP, run)
    s, dd = grads.ler(os.path.join(d, "cm1out_s.ctl"),
                      ["rain", "zs", "zhval", "th", "prs", "rho", "qc", "qr", "qi", "qs", "qg", "cci",
                       "uinterp", "vinterp", "winterp"])
    st, _ = grads.stats(os.path.join(d, "cm1out_stats.ctl"))
    x = dd["xdef"]; y = dd["ydef"]
    X, Y = np.meshgrid(x, y)
    anf = (abs(X) <= ANF) & (abs(Y) <= ANF)
    zs = s["zs"][0, 0] + ZBASE                                   # m ASL
    zh = s["zhval"] + ZBASE                                      # (nt,nz,ny,nx) m ASL
    T = s["th"] * (s["prs"] / 1e5) ** 0.2857
    frio = T < 273.15
    misto = frio & (T > 235.15)
    liq = (s["qc"] + s["qr"]) * s["rho"]                         # kg/m3
    slw = np.where(frio, liq, 0.0)
    nt = slw.shape[0]
    t = np.arange(nt) * TAPFRQ / 60.
    dz = np.diff(np.concatenate([np.zeros_like(zh[:, :1]), (zh[:, 1:] + zh[:, :-1]) / 2,
                                 zh[:, -1:] + (zh[:, -1:] - zh[:, -2:-1]) / 2], axis=1), axis=1)
    dz = np.clip(dz, 1, None)
    slw_col = np.nansum(slw * dz, axis=1)                        # kg/m2 por coluna
    gy, gx = np.gradient(zs, DX)
    tana = np.hypot(gx, gy)
    vh0 = np.hypot(s["uinterp"][:, 0], s["vinterp"][:, 0])
    dep = slw[:, 0] * vh0 * tana * DX * DX                      # kg/s por celula (E=1)
    dep_anf = np.nansum(np.where(anf, dep, 0), axis=(1, 2))      # kg/s no anfiteatro
    # integracao trapezoidal no tempo -> m3 de agua
    dep_anf_m3 = float(_trapz(dep_anf, t * 60) / 1000.0) if nt > 1 else 0.0
    dep_dom_m3 = float(_trapz(np.nansum(dep, axis=(1, 2)), t * 60) / 1000.0) if nt > 1 else 0.0
    w = s["winterp"]
    w_anf = np.nanmax(np.where(anf[None, None], w, -99), axis=(1, 2, 3))
    rain = s["rain"][:, 0] * 10.0                                # mm
    ni = np.where(misto, s["cci"] * s["rho"], 0) / 1e3           # L-1
    out = dict(
        t_min=t.tolist(), nt=int(nt),
        wmax_stats=st["wmax"].tolist(),
        wmax=np.nanmax(w, axis=(1, 2, 3)).tolist(),
        wmax_anf=w_anf.tolist(),
        slw_massa_kt=(np.nansum(slw_col, axis=(1, 2)) * DX * DX / 1e6).tolist(),
        slw_massa_anf_t=(np.nansum(np.where(anf, slw_col, 0), axis=(1, 2)) * DX * DX / 1e3).tolist(),
        lwc_sr_max=(np.nanmax(slw, axis=(1, 2, 3)) * 1e3).tolist(),
        lwc_sr_anf_max=(np.nanmax(np.where(anf[None, None], slw, 0), axis=(1, 2, 3)) * 1e3).tolist(),
        icnc_max=np.nanmax(ni, axis=(1, 2, 3)).tolist(),
        rain_max=np.nanmax(rain, axis=(1, 2)).tolist(),
        rain_anf_media=np.nanmean(np.where(anf, rain, np.nan), axis=(1, 2)).tolist(),
        vh0_anf_med=np.nanmean(np.where(anf, vh0, np.nan), axis=(1, 2)).tolist(),
        dep_anf_kg_s=dep_anf.tolist(), dep_anf_m3=dep_anf_m3, dep_dom_m3=dep_dom_m3,
        zs_anf=[float(zs[anf].min()), float(zs[anf].max())],
        tana_anf_med=float(np.degrees(np.arctan(np.mean(tana[anf])))),
    )
    np.save(os.path.join(d, "campos_slw_col.npy"), slw_col.astype(np.float32))
    np.save(os.path.join(d, "campos_w.npy"), w.astype(np.float32))
    np.save(os.path.join(d, "campos_zh.npy"), zh.astype(np.float32))
    np.save(os.path.join(d, "campos_slw.npy"), slw.astype(np.float32))
    np.save(os.path.join(d, "campos_zs.npy"), zs.astype(np.float32))
    return out


if __name__ == "__main__":
    R = {}
    for t in ["pre", "pico", "pre_colapso"]:
        run = "ter_%s_nssl" % t
        try:
            R[run] = um(run)
        except Exception as e:
            print(run, "ERRO", e); continue
        o = R[run]
        print("%-22s nt=%d  wmax=%.2f  w_anf=%.2f  SLW dominio max=%.1f kt  SLW anf max=%.1f t  LWC_sr max=%.2f (anf %.2f) g/m3"
              "  ICNC max=%.1f/L  chuva max=%.2f mm (anf %.3f)  |V| anf ~%.1f m/s  deposicao E=1: anf %.0f m3, dominio %.0f m3"
              % (run, o["nt"], max(o["wmax_stats"]), max(o["wmax_anf"]), max(o["slw_massa_kt"]), max(o["slw_massa_anf_t"]),
                 max(o["lwc_sr_max"]), max(o["lwc_sr_anf_max"]), max(o["icnc_max"]), max(o["rain_max"]),
                 np.nanmax(o["rain_anf_media"]), np.nanmean(o["vh0_anf_med"]), o["dep_anf_m3"], o["dep_dom_m3"]))
    json.dump(R, open(os.path.join(SP, "cm1_terreno_resultados.json"), "w"), indent=1)
