# -*- coding: utf-8 -*-
"""Resumo do vortices_sotavento.py: vortices resolvidos (>= 4 km2) e persistentes (>= 3 saidas) a 5,5 km e a janela do
anfiteatro a 6 e 7 km ASL. Uso: python3 resumo_vortices.py <prefixo>.json"""
import json, sys
J = json.load(open(sys.argv[1]))
print("UTC   Fr   | resolvidos (>=4 km2) a 5,5 km: orog/conv | persistentes orog (>=3 saidas): zeta/f, area, dist | anf a 6 km (cob, zeta/f, conv, w) | anf a 7 km (zeta/f, conv, w)")
for s in J["saidas"]:
    n = s["niveis"]["5500"]; v = n["vortices"]
    res = [r for r in v if r["area_km2"] >= 4]
    per = [r for r in res if r["tipo"] == "orografico" and r.get("persist", 1) >= 3]
    a6 = s["niveis"]["6000"]["anfiteatro"]; a7 = s["niveis"]["7000"]["anfiteatro"]
    f = lambda a, k, m=1: ("%+6.1f" % (m * a[k])) if a[k] is not None else "   -  "
    print("%5.1f %4.2f | %2d / %2d | %s | %3.0f%% %s %s %s | %s %s %s" % (s["hora_utc"] % 24, s["Fr"] or 0,
          sum(r["tipo"] == "orografico" for r in res), sum(r["tipo"] == "convectivo" for r in res),
          ("; ".join("%+.0ff %.1fkm2 %.1fkm" % (r["zeta_f"], r["area_km2"], r["dist_anf_km"]) for r in per[:2]) or "-").ljust(44),
          100 * a6["cobertura"], f(a6, "zeta_f"), f(a6, "delta_1e4", -1), f(a6, "w"), f(a7, "zeta_f"), f(a7, "delta_1e4", -1), f(a7, "w")))
