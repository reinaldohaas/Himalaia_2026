# -*- coding: utf-8 -*-
"""
Precipitacao solida acumulada no solo (WRF d03, 1 km) nas rodadas A, B, C e D, para a hipotese revisada de 22/10/2026:
a massa densa teria se acumulado no chao das encostas altas e escorregado ate a zona da ruptura.
Le recorte_solo_d03.nc (RAINNC, SNOWNC, GRAUPELNC, HAILNC em mm; SNOW em kg/m2; SNOWH em m) de saida/wrf_lhende/toro_X/graupel/.
Regioes: anfiteatro (poligono GLO-30); encostas altas (HGT >= 6000 m) na caixa dos flancos norte do Langtang Lirung e
do Tsangbu Ri (85,48-85,58 E, 28,24-28,30 N); zona da cicatriz (ate 1 km da linha de campo de Adhikari et al. 2026).
Periodos: 17:00 -> 01:30 (antes da nucleacao no nucleo) e 17:00 -> 02:45 (antes da ruptura, 02:52:16).
Uso: python acumulado_solo.py <dir_saida_wrf_lhende> <anfiteatro.geojson> <saida.json>
"""
import json
import os
import sys

import numpy as np

CAIXA = (85.48, 28.24, 85.58, 28.30)
CICATRIZ = [(85.5225, 28.2830), (85.5300, 28.2870), (85.5300, 28.2950)]
SITIO = (28.271, 85.515)


def main(base, geo, saida):
    import netCDF4
    from shapely.geometry import shape, LineString, Point
    from shapely import contains_xy
    an = shape(json.load(open(geo, encoding="utf-8"))["features"][0]["geometry"])
    cic = LineString(CICATRIZ)
    res = {}
    for X in "ABCD":
        arq = os.path.join(base, "toro_" + X, "graupel", "recorte_solo_d03.nc")
        if not os.path.exists(arq):
            print(X, "sem recorte"); continue
        with netCDF4.Dataset(arq) as f:
            T = [b"".join(t).decode()[:16] for t in f.variables["Times"][:]]
            lat = np.asarray(f.variables["XLAT"][0]); lon = np.asarray(f.variables["XLONG"][0])
            hgt = np.asarray(f.variables["HGT"][0])
            V = {v: np.asarray(f.variables[v][:]) for v in ("RAINNC", "SNOWNC", "GRAUPELNC", "HAILNC", "SNOW", "SNOWH")}
        kx = np.cos(np.radians(SITIO[0]))
        # distancia a cicatriz em km (aproximacao plana local)
        dc = np.array([[cic.distance(Point(lo * kx, la)) for lo, la in zip(rl, rb)] for rl, rb in zip(lon, lat)]) * 111.32 \
            if False else None
        L = LineString([(x * kx, y) for x, y in CICATRIZ])
        dc = np.vectorize(lambda lo, la: L.distance(Point(lo * kx, la)))(lon, lat) * 111.32
        reg = {"anfiteatro": contains_xy(an, lon, lat),
               "encostas_altas_6km": (lon >= CAIXA[0]) & (lon <= CAIXA[2]) & (lat >= CAIXA[1]) & (lat <= CAIXA[3]) & (hgt >= 6000),
               "cicatriz_1km": dc <= 1.0}
        i17 = T.index("2026-08-25_17:00"); i130 = T.index("2026-08-26_01:30"); i245 = T.index("2026-08-26_02:45")
        out = {}
        for nome, m in reg.items():
            e = {"pontos_1km2": int(m.sum()), "cota_media_m": round(float(hgt[m].mean()), 0)}
            for rot, i1 in (("ate_0130", i130), ("ate_0245", i245)):
                d = {v: V[v][i1] - V[v][i17] for v in ("RAINNC", "SNOWNC", "GRAUPELNC", "HAILNC")}
                solido = d["SNOWNC"] + d["GRAUPELNC"] + d["HAILNC"]
                e[rot] = {"total_mm_media": round(float(d["RAINNC"][m].mean()), 2),
                          "solido_mm_media": round(float(solido[m].mean()), 2),
                          "solido_mm_max": round(float(solido[m].max()), 2),
                          "graupel_granizo_mm_media": round(float((d["GRAUPELNC"] + d["HAILNC"])[m].mean()), 3),
                          "massa_solida_kg": round(float(solido[m].sum() * 1e6), 0),          # 1 mm sobre 1 km2 = 1e6 kg
                          "dSWE_kg_m2_media": round(float((V["SNOW"][i1] - V["SNOW"][i17])[m].mean()), 2)}
            out[nome] = e
        res[X] = out
        print(X, json.dumps(out, ensure_ascii=False))
    json.dump(res, open(saida, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(*sys.argv[1:4])
