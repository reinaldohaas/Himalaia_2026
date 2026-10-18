# -*- coding: utf-8 -*-
"""
O sistema convectivo de 25-26/08/2026 visto pelo Himawari-9 esta na ERA5?

Le os campos de nivel unico da ERA5 (baixar_era5.py verificacao; zips com netCDF instant/accum/avg) e, a
cada hora, marca o "sistema" como na trajetoria do Himawari: objeto com OLR < limiar (OLR = -mtnlwrf,
W/m2; 120 W/m2 ~ sigma*213^4, e 150 W/m2 como margem), o maior a menos de 600 km do sitio, e seguido
por continuidade (< 150 km por hora). Compara area, centro e distancia com
data/processed/himawari_trajetoria/trajetoria.json. Tambem: chuva convectiva e total no sistema e no sitio,
nuvem alta, CAPE.

Uso: python verificar_mcs_era5.py <dir_era5> <trajetoria.json> <saida_prefixo>
"""
import glob
import io
import json
import os
import sys
import zipfile
from datetime import datetime

import numpy as np
import xarray as xr
from scipy import ndimage

SITIO = (28.271, 85.515)


def abrir(d):
    ds = []
    for f in sorted(glob.glob(os.path.join(d, "era5_verif_sl_*.nc"))):
        z = zipfile.ZipFile(f)
        dx = f + "_extraido"; os.makedirs(dx, exist_ok=True); z.extractall(dx)
        partes = [xr.open_dataset(os.path.join(dx, n), engine="netcdf4").load() for n in z.namelist()]
        partes = [p.drop_vars([v for v in ("expver", "number") if v in p.variables]) for p in partes]
        ds.append(xr.merge(partes, compat="override"))
    return xr.concat(ds, dim="valid_time").sortby("valid_time")


def dist(la1, lo1, la2, lo2):
    dy = (la2 - la1) * 111.32; dx = (lo2 - lo1) * 111.32 * np.cos(np.radians(0.5 * (la1 + la2)))
    return float(np.hypot(dx, dy)), float((np.degrees(np.arctan2(dx, dy)) + 360) % 360)


def objetos(campo, lat, lon, A, limiar):
    lab, n = ndimage.label(campo < limiar)
    out = []
    LON, LAT = np.meshgrid(lon, lat)
    for k in range(1, n + 1):
        m = lab == k; ar = float(A[m].sum())
        if ar < 500:
            continue
        w = (limiar - campo[m]).clip(1e-6)
        la, lo = float(np.average(LAT[m], weights=w)), float(np.average(LON[m], weights=w))
        d, r = dist(SITIO[0], SITIO[1], la, lo)
        out.append({"area_km2": round(ar), "olr_min": round(float(campo[m].min()), 1), "lat": round(la, 2), "lon": round(lo, 2),
                    "dist": round(d), "rumo": round(r), "m": m})
    return sorted(out, key=lambda o: -o["area_km2"])


def main(d, traj, pref):
    ds = abrir(d)
    lat = ds["latitude"].values; lon = ds["longitude"].values
    A = (0.25 * 111.32) * (0.25 * 111.32 * np.cos(np.radians(lat)))[:, None] * np.ones((1, lon.size))
    js, is_ = int(np.argmin(abs(lat - SITIO[0]))), int(np.argmin(abs(lon - SITIO[1])))
    H = {r["utc"][:13]: r for r in json.load(open(traj))["registros"] if r["utc"][14:16] == "00"}
    res = {}
    for lim in (120.0, 150.0):
        linhas, ant = [], None
        # continuidade: comeca no horario de maior objeto perto do sitio
        por_t = []
        for it, t in enumerate(ds["valid_time"].values):
            olr = -ds["avg_tnlwrf"].isel(valid_time=it).values if "avg_tnlwrf" in ds else -ds["mtnlwrf"].isel(valid_time=it).values
            ob = [o for o in objetos(olr, lat, lon, A, lim) if o["dist"] < 600]
            por_t.append((str(t)[:13], olr, ob))
        k0 = max(range(len(por_t)), key=lambda k: por_t[k][2][0]["area_km2"] if por_t[k][2] else 0)
        sis = {k0: por_t[k0][2][0] if por_t[k0][2] else None}
        for passo in (1, -1):
            a = sis[k0]; k = k0 + passo
            while a and 0 <= k < len(por_t):
                viz = [(dist(a["lat"], a["lon"], o["lat"], o["lon"])[0], o) for o in por_t[k][2]]
                viz = [v for v in viz if v[0] < 150]
                if not viz:
                    break
                a = min(viz, key=lambda v: v[0])[1]; sis[k] = a; k += passo
        for k, (t, olr, ob) in enumerate(por_t):
            it = k
            cp = ds["cp"].isel(valid_time=it).values * 1000.0; tp = ds["tp"].isel(valid_time=it).values * 1000.0   # mm/h
            hcc = ds["hcc"].isel(valid_time=it).values; cape = ds["cape"].isel(valid_time=it).values
            s = sis.get(k)
            h = H.get(t)
            hs = h["sistema"] if h else None
            lin = {"utc": t, "olr_sitio": round(float(olr[js, is_]), 1), "tp_sitio_mmh": round(float(tp[js, is_]), 2),
                   "hcc_sitio": round(float(hcc[js, is_]), 2), "cape_max_600km": None, "sistema": None, "himawari": None}
            if s:
                m = s["m"]
                lin["sistema"] = {kk: v for kk, v in s.items() if kk != "m"}
                lin["sistema"]["cp_mmh_media"] = round(float(cp[m].mean()), 2); lin["sistema"]["tp_mmh_media"] = round(float(tp[m].mean()), 2)
                lin["sistema"]["vol_tp_m3_h"] = round(float((tp[m] / 1000.0 * A[m] * 1e6).sum()))
            if hs:
                lin["himawari"] = {"area_km2": hs["area_km2"], "lat": hs["lat"], "lon": hs["lon"], "dist": hs["dist_sitio_km"], "rumo": hs["rumo_do_sitio"]}
                if s:
                    lin["sep_km"] = round(dist(hs["lat"], hs["lon"], s["lat"], s["lon"])[0])
            linhas.append(lin)
        res[str(int(lim))] = linhas
    json.dump(res, open(pref + ".json", "w"), indent=1)
    with open(pref + ".txt", "w", encoding="utf-8") as f:
        f.write("ERA5 x Himawari-9 -- o sistema convectivo de 25-26/08/2026\n")
        for lim, linhas in res.items():
            f.write("\nERA5: objeto OLR < %s W/m2 (seguido por continuidade) | Himawari: objeto Tb < 213 K (paralaxe corrigida)\n" % lim)
            f.write(" UTC            ERA5: area_km2  OLRmin  lat    lon    dist rumo  cp(mm/h) | Himawari: area_km2  lat    lon    dist rumo | separacao(km) | sitio: OLR  tp(mm/h) hcc\n")
            for l in linhas:
                s, hs = l["sistema"], l["himawari"]
                f.write("%s  %s | %s | %6s | %6.1f %6.2f %4.2f\n" % (
                    l["utc"], ("%9d %6.0f %6.2f %6.2f %4d %4d %7.2f" % (s["area_km2"], s["olr_min"], s["lat"], s["lon"], s["dist"], s["rumo"], s["cp_mmh_media"])) if s else "%45s" % "-",
                    ("%9d %6.2f %6.2f %4d %4d" % (hs["area_km2"], hs["lat"], hs["lon"], hs["dist"], hs["rumo"])) if hs else "%33s" % "-",
                    l.get("sep_km", "-"), l["olr_sitio"], l["tp_sitio_mmh"], l["hcc_sitio"]))
    print(open(pref + ".txt", encoding="utf-8").read())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
