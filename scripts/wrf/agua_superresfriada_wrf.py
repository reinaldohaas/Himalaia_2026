# -*- coding: utf-8 -*-
"""
Agua super-resfriada e gelo em suspensao no WRF de 27 h (recortes do vlab: recorte_gelo_d03.nc, recorte_gelo_d02.nc).

Para cada saida e regiao: massa (kg) e coluna (kg/m2) de agua liquida super-resfriada (QCLOUD + QRAIN com T < 0 C),
so de nuvem super-resfriada (QCLOUD, T < 0), de graupel + granizo, e do condensado total; maximos de razao de
mistura (g/kg), temperatura media ponderada pela massa da agua super-resfriada, w maximo e minimo.
Regioes: anfiteatro (poligono do GLO-30), raio de 10 e 30 km do ponto USGS (d03); caixa inteira do recorte e raio de
50 km da conveccao noturna do WRF (27,7 N; 84,9 E) no d02. Densidade: p = P + PB; T = (T' + 300) (p/1e5)^0,2857;
rho = p / (Rd T (1 + 0,61 qv)); espessura das camadas pelo geopotencial (PH + PHB)/g nos niveis w.
Uso: python agua_superresfriada_wrf.py <recorte_d03.nc> <recorte_d02.nc> <anfiteatro.geojson> <saida_prefixo>
"""
import json
import sys

import numpy as np

SITIO = (28.271, 85.515)
CONV = (27.7, 84.9)
ALVO_KG = 1.42e10


def regioes_mask(lat, lon, an):
    from shapely import vectorized
    d = np.hypot((lat - SITIO[0]) * 111.32, (lon - SITIO[1]) * 111.32 * np.cos(np.radians(SITIO[0])))
    dc = np.hypot((lat - CONV[0]) * 111.32, (lon - CONV[1]) * 111.32 * np.cos(np.radians(CONV[0])))
    return {"anfiteatro": vectorized.contains(an, lon, lat), "r10km": d < 10, "r30km": d < 30, "r100km": d < 100,
            "conv_r50km": dc < 50, "dominio": np.ones(lat.shape, bool)}


def processa(arq, an, regs_quero, dx_km):
    import netCDF4
    out = []
    with netCDF4.Dataset(arq) as f:
        T = ["".join(t.astype(str)) if hasattr(t, "astype") else str(t) for t in f.variables["Times"][:]]
        T = [b"".join(t).decode() if isinstance(t, (bytes, np.ndarray)) and not isinstance(t, str) else t for t in f.variables["Times"][:]]
        lat = f.variables["XLAT"][0]; lon = f.variables["XLONG"][0]
        R = regioes_mask(np.asarray(lat), np.asarray(lon), an)
        R = {k: v for k, v in R.items() if k in regs_quero}
        A = (dx_km * 1000.0) ** 2
        for k in range(len(T)):
            p = f.variables["P"][k] + f.variables["PB"][k]
            th = f.variables["T"][k] + 300.0
            tk = th * (p / 1e5) ** 0.2857
            qv = f.variables["QVAPOR"][k]
            rho = p / (287.04 * tk * (1 + 0.61 * qv))
            z = (f.variables["PH"][k] + f.variables["PHB"][k]) / 9.81
            dz = np.diff(z, axis=0)
            m = rho * dz * A                                   # massa de ar por celula (kg)
            qc = f.variables["QCLOUD"][k]; qr = f.variables["QRAIN"][k]
            qg = f.variables["QGRAUP"][k]; qh = f.variables["QHAIL"][k]
            qi = f.variables["QICE"][k]; qs = f.variables["QSNOW"][k]
            frio = tk < 273.15
            slw = (qc + qr) * frio; slc = qc * frio; gh = qg + qh
            tot = qc + qr + qg + qh + qi + qs
            w = f.variables["W"][k]; wm = 0.5 * (w[1:] + w[:-1])
            t0 = T[k] if isinstance(T[k], str) else str(T[k])
            reg = {}
            for nome, mk in R.items():
                if not mk.any():
                    continue
                M = lambda q: float((q * m)[:, mk].sum())
                area = mk.sum() * A
                ms = M(slw)
                reg[nome] = {"area_km2": round(area / 1e6, 1),
                             "slw_kg": ms, "slw_coluna_kgm2": round(ms / area, 3), "slc_kg": M(slc),
                             "graupel_granizo_kg": M(gh), "gh_coluna_kgm2": round(M(gh) / area, 3),
                             "condensado_total_kg": M(tot), "tot_coluna_kgm2": round(M(tot) / area, 3),
                             "qslw_max_gkg": round(float(slw[:, mk].max() * 1e3), 3), "qgh_max_gkg": round(float(gh[:, mk].max() * 1e3), 3),
                             "T_slw_C": round(float((tk[:, mk] * slw[:, mk] * m[:, mk]).sum() / max((slw[:, mk] * m[:, mk]).sum(), 1e-12) - 273.15), 1) if ms > 0 else None,
                             "w_max": round(float(wm[:, mk].max()), 1), "w_min": round(float(wm[:, mk].min()), 1)}
            out.append({"utc": t0, "regioes": reg})
            r = reg.get("anfiteatro") or reg.get("conv_r50km")
            print(t0, " | ".join("%s: SLW %.2e kg (%.2f kg/m2, Tm %s C, max %.2f g/kg) GH %.2e kg tot %.2e kg w %+.0f/%+.0f" % (
                n, v["slw_kg"], v["slw_coluna_kgm2"], v["T_slw_C"], v["qslw_max_gkg"], v["graupel_granizo_kg"], v["condensado_total_kg"], v["w_max"], v["w_min"])
                for n, v in reg.items() if n in ("anfiteatro", "r30km", "conv_r50km", "dominio")), flush=True)
    return out


def main(d03, d02, anj, pref):
    from shapely.geometry import shape
    an = shape(json.load(open(anj))["features"][0]["geometry"])
    print("=== d03 (1 km)")
    r3 = processa(d03, an, ("anfiteatro", "r10km", "r30km", "conv_r50km", "dominio"), 1.0)
    print("=== d02 (3 km)")
    r2 = processa(d02, an, ("r30km", "r100km", "conv_r50km", "dominio"), 3.0)
    res = {"alvo_kg": ALVO_KG, "d03": r3, "d02": r2}
    def mx(lst, reg, campo):
        v = [(x["regioes"][reg][campo], x["utc"]) for x in lst if reg in x["regioes"]]
        return max(v) if v else None
    res["maximos"] = {"d03": {reg: {c: mx(r3, reg, c) for c in ("slw_kg", "graupel_granizo_kg", "condensado_total_kg")} for reg in ("anfiteatro", "r10km", "r30km", "conv_r50km", "dominio")},
                      "d02": {reg: {c: mx(r2, reg, c) for c in ("slw_kg", "graupel_granizo_kg", "condensado_total_kg")} for reg in ("r30km", "r100km", "conv_r50km", "dominio")}}
    json.dump(res, open(pref + ".json", "w"), indent=1, default=str)
    print(json.dumps(res["maximos"], indent=1, default=str))


if __name__ == "__main__":
    main(*sys.argv[1:5])
