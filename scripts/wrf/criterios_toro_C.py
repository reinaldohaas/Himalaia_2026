# -*- coding: utf-8 -*-
"""
Criterios pre-registrados do experimento C (scripts/toro_wrf/LEIA-ME_toro_wrf.md, "Experimento C"), com B e A como
comparacao, a partir dos recortes do vlab (d03, 1 km):
  recorte_vortice_d03.nc (so C; 23:00-03:00; U, V, W, QNICE, ...), recorte_gelo_d03.nc (A, B, C; 17:00-03:00),
  wrfaux_d03 (RAINNC, OLR; a cada 15 min).
1. Vortice: vento tangencial maximo e vorticidade relativa maxima entre 2 e 6 km acima do terreno, ate 10 km do centro,
   as 01:30 e 02:30 (so C).
2. Reservatorio no nucleo antes de 01:30: agua super-resfriada (QCLOUD + QRAIN com T < 0 C) ate 5 e ate 30 km;
   ascendente maxima ate 5 km.
3. Nucleacao depois de 01:30: QNICE (so C), massa de gelo (QICE + QSNOW + QGRAUP + QHAIL) ate 5 km; congelamento
   estimado pela variacao da massa de gelo na coluna ate 5 km (sem descontar adveccao) e o calor latente L_f x massa.
4. Liberacao 01:30-03:00: chuva (RAINNC) sobre o anfiteatro e volume ate 30 km; maior taxa em 15 min; descendente minima.
5. OLR sobre o sitio as 02:45.
Uso: python criterios_toro_C.py <dir_C> <dir_B> <dir_A> <anfiteatro.geojson> <saida.json>
  cada dir_X (saida/wrf_lhende/toro_X do Drive) tem wrfaux_d03* e, em graupel/, recorte_gelo_d03.nc;
  dir_C tem tambem recorte_vortice_d03.nc
"""
import glob
import json
import os
import sys

import numpy as np

SITIO = (28.271, 85.515)
G, RD, LF = 9.81, 287.05, 3.34e5


def nomes_tempo(f):
    return [b"".join(t).decode() for t in f.variables["Times"][:]]


def geometria(f):
    lat = np.asarray(f.variables["XLAT"][0]); lon = np.asarray(f.variables["XLONG"][0])
    kx = 111.32 * np.cos(np.radians(SITIO[0]))
    x = (lon - SITIO[1]) * kx; y = (lat - SITIO[0]) * 111.32
    return lat, lon, x, y, np.hypot(x, y)


def estado(f, k):
    """densidade, T (K), altura acima do terreno (m) e espessura das camadas (m), na grade de massa"""
    p = f.variables["P"][k] + f.variables["PB"][k]
    th = f.variables["T"][k] + 300.0
    T = th * (p / 1e5) ** 0.2857
    qv = f.variables["QVAPOR"][k] if "QVAPOR" in f.variables else 0.0
    rho = p / (RD * T * (1 + 0.61 * qv))
    zw = (f.variables["PH"][k] + f.variables["PHB"][k]) / G
    dz = np.diff(zw, axis=0)
    zm = 0.5 * (zw[1:] + zw[:-1]) - f.variables["HGT"][0][None]
    return np.asarray(rho), np.asarray(T), np.asarray(zm), np.asarray(dz)


def massa(q, rho, dz, msk, A=1e6):
    return float(np.sum((q * rho * dz)[:, msk]) * A)


def gelo_total(f, k):
    s = 0.0
    for v in ("QICE", "QSNOW", "QGRAUP", "QHAIL"):
        if v in f.variables:
            s = s + np.asarray(f.variables[v][k])
    return s


def analisa_gelo(arq, rot):
    import netCDF4
    out = {}
    with netCDF4.Dataset(arq) as f:
        T_ = nomes_tempo(f); lat, lon, x, y, r = geometria(f)
        n5, n30 = r <= 5, r <= 30
        for k, t in enumerate(T_):
            hh = t[11:16]
            if t[:10] == "2026-08-25" and hh < "23:00":
                continue
            rho, T, zm, dz = estado(f, k)
            slw = (np.asarray(f.variables["QCLOUD"][k]) + np.asarray(f.variables["QRAIN"][k])) * (T < 273.15)
            ice = gelo_total(f, k)
            w = np.asarray(f.variables["W"][k]); wm = 0.5 * (w[1:] + w[:-1])
            out[t[:16]] = {"slw_r5_kg": massa(slw, rho, dz, n5), "slw_r30_kg": massa(slw, rho, dz, n30),
                           "gelo_r5_kg": massa(ice, rho, dz, n5), "gelo_r30_kg": massa(ice, rho, dz, n30),
                           "w_max_r5": float(wm[:, n5].max()), "w_min_r5": float(wm[:, n5].min()),
                           "w_min_r30": float(wm[:, n30].min())}
    print(rot, "gelo lido:", len(out), "horarios", flush=True)
    return out


def analisa_vortice(arq):
    import netCDF4
    out = {}
    with netCDF4.Dataset(arq) as f:
        T_ = nomes_tempo(f); lat, lon, x, y, r = geometria(f)
        for k, t in enumerate(T_):
            rho, T, zm, dz = estado(f, k)
            u = np.asarray(f.variables["U"][k]); v = np.asarray(f.variables["V"][k])
            u = 0.5 * (u[..., 1:] + u[..., :-1]); v = 0.5 * (v[:, 1:] + v[:, :-1])
            vt = (x * v - y * u) / np.maximum(r, 0.5)                     # ciclonico (anti-horario) positivo
            dvdx = np.gradient(v, axis=2) / 1000.0; dudy = np.gradient(u, axis=1) / 1000.0
            zeta = dvdx - dudy
            camada = (zm >= 2000) & (zm <= 6000) & (r <= 10)[None]
            qn = np.asarray(f.variables["QNICE"][k])
            n5 = r <= 5
            out[t[:16]] = {"vt_max_2_6km_r10": float(vt[camada].max()), "zeta_max_2_6km_r10": float(zeta[camada].max()),
                           "qnice_max_r5_porkg": float(qn[:, n5].max()),
                           "ncristais_r5": float(np.sum((qn * rho * dz)[:, n5]) * 1e6)}
    print("C vortice lido:", len(out), "horarios", flush=True)
    return out


def analisa_aux(dirx, an):
    import netCDF4
    from shapely import vectorized
    arq = glob.glob(os.path.join(dirx, "wrfaux_d03*"))[0]
    with netCDF4.Dataset(arq) as f:
        T_ = nomes_tempo(f); lat, lon, x, y, r = geometria(f)
        anf = vectorized.contains(an, lon, lat)
        rn = np.asarray(f.variables["RAINNC"][:]) + np.asarray(f.variables["RAINC"][:])
        olr = np.asarray(f.variables["OLR"][:])
    idx = {t[:16]: i for i, t in enumerate(T_)}
    i0, i1 = idx["2026-08-26_01:30"], idx["2026-08-26_03:00"]
    d = rn[i1] - rn[i0]
    taxa = np.diff(rn[i0:i1 + 1], axis=0) * 4.0                        # mm/h a partir de 15 min
    js = np.unravel_index(np.argmin(r), r.shape)
    return {"chuva_anfiteatro_mm": round(float(d[anf].mean()), 2), "chuva_max_r30_mm": round(float(d[r <= 30].max()), 2),
            "volume_r30_m3": round(float(d[r <= 30].sum() * 1e-3 * 1e6), 0),
            "taxa_max_r30_mm_h": round(float(taxa[:, r <= 30].max()), 1),
            "olr_sitio_0245_W_m2": round(float(olr[idx["2026-08-26_02:45"]][js]), 1)}


def recorte(d, nome):
    for c in (os.path.join(d, "graupel", nome), os.path.join(d, nome)):
        if os.path.exists(c):
            return c
    raise FileNotFoundError(os.path.join(d, nome))


def main(dc, db, da, geo, saida, rotulos="C,B,A"):
    R = rotulos.split(",")
    from shapely.geometry import shape
    an = shape(json.load(open(geo, encoding="utf-8"))["features"][0]["geometry"])
    res = {R[0] + "_vortice": analisa_vortice(recorte(dc, "recorte_vortice_d03.nc"))}
    for rot, d in ((R[0], dc), (R[1], db), (R[2], da)):
        res[rot + "_gelo"] = analisa_gelo(recorte(d, "recorte_gelo_d03.nc"), rot)
        res[rot + "_liberacao"] = analisa_aux(d, an)
    for rot in R:
        g = res[rot + "_gelo"]
        a, b = g.get("2026-08-26_01:30"), g.get("2026-08-26_03:00")
        if a and b:
            dm = b["gelo_r5_kg"] - a["gelo_r5_kg"]
            res[rot + "_nucleacao"] = {"dgelo_r5_0130_0300_kg": dm, "calor_latente_J": dm * LF if dm > 0 else 0.0,
                                       "dslw_r5_0130_0300_kg": b["slw_r5_kg"] - a["slw_r5_kg"]}
    json.dump(res, open(saida, "w", encoding="utf-8"), indent=1)
    # resumo legivel
    vt = res[R[0] + "_vortice"]
    print("\n1. vortice (%s): " % R[0] + "; ".join("%s vt %.1f m/s, zeta %.1e /s" % (t[11:], vt[t]["vt_max_2_6km_r10"], vt[t]["zeta_max_2_6km_r10"])
                                         for t in ("2026-08-26_00:00", "2026-08-26_01:30", "2026-08-26_02:30") if t in vt))
    for rot in R:
        g = res[rot + "_gelo"]
        pre = [g[t] for t in g if "2026-08-25_23:00" <= t <= "2026-08-26_01:30"]
        print("2. %s: SLW max (23:00-01:30) r5 %.2e kg, r30 %.2e kg; w max r5 %.1f m/s" % (
            rot, max(p["slw_r5_kg"] for p in pre), max(p["slw_r30_kg"] for p in pre), max(p["w_max_r5"] for p in pre)))
        if rot + "_nucleacao" in res:
            nu = res[rot + "_nucleacao"]
            print("3. %s: dgelo r5 01:30->03:00 %.2e kg (L_f x = %.1e J); dSLW %.2e kg" % (
                rot, nu["dgelo_r5_0130_0300_kg"], nu["calor_latente_J"], nu["dslw_r5_0130_0300_kg"]))
        li = res[rot + "_liberacao"]
        pos = [g[t] for t in g if t >= "2026-08-26_01:30"]
        print("4. %s: chuva 01:30-03 anfiteatro %.2f mm, max r30 %.2f mm, volume r30 %.2e m3, taxa max %.1f mm/h; w min r30 %.1f m/s" % (
            rot, li["chuva_anfiteatro_mm"], li["chuva_max_r30_mm"], li["volume_r30_m3"], li["taxa_max_r30_mm_h"],
            min(p["w_min_r30"] for p in pos)))
        print("5. %s: OLR no sitio 02:45 = %.1f W/m2" % (rot, li["olr_sitio_0245_W_m2"]))
    print("QNICE max r5 (%s): " % R[0] + "; ".join("%s %.2e /kg" % (t[11:], vt[t]["qnice_max_r5_porkg"]) for t in sorted(vt)[::2]))


if __name__ == "__main__":
    main(*sys.argv[1:7])
