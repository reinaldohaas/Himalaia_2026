# -*- coding: utf-8 -*-
"""
O WRF reproduz o sistema convectivo do Himawari? (criterio pre-registrado em LEIA-ME_wrf.md)

Le OLR (W/m2), XLAT, XLONG e Times de wrfout_d0N (netCDF4, h5py ou scipy, o que houver), marca objetos com
OLR < 120 W/m2 (~ sigma*213^4), segue o maior a menos de 600 km do sitio por continuidade (< 150 km/h) e
compara, hora a hora, com data/processed/himawari_trajetoria/trajetoria.json (passado como argumento).
Tambem: chuva acumulada (RAINNC+RAINC) e OLR no ponto do sitio.

Uso: python3 diag_mcs_wrf.py <wrfout_d02> <trajetoria.json> <saida_prefixo>
"""
import json
import sys

import numpy as np

SITIO = (28.271, 85.515)


def ler(arq, nomes):
    try:
        import netCDF4
        with netCDF4.Dataset(arq) as d:
            return {n: np.array(d.variables[n][:]) for n in nomes}
    except ImportError:
        pass
    try:
        import h5py
        with h5py.File(arq, "r") as d:
            return {n: np.array(d[n][:]) for n in nomes}
    except (ImportError, OSError):
        from scipy.io import netcdf_file
        with netcdf_file(arq, "r", mmap=False) as d:
            return {n: np.array(d.variables[n][:]) for n in nomes}


def dist(la1, lo1, la2, lo2):
    dy = (la2 - la1) * 111.32; dx = (lo2 - lo1) * 111.32 * np.cos(np.radians(0.5 * (la1 + la2)))
    return float(np.hypot(dx, dy)), float((np.degrees(np.arctan2(dx, dy)) + 360) % 360)


def main(arq, traj, pref):
    from scipy import ndimage
    v = ler(arq, ["Times", "XLAT", "XLONG", "OLR", "RAINNC", "RAINC"])
    tempos = ["".join(t.astype(str)) if t.dtype.kind in "SU" else bytes(t).decode() for t in v["Times"]]
    lat, lon = v["XLAT"][0], v["XLONG"][0]
    dxkm = dist(lat[0, 0], lon[0, 0], lat[0, 1], lon[0, 1])[0]          # espacamento da grade (km)
    A = dxkm ** 2
    jy, ix = np.unravel_index(np.argmin((lat - SITIO[0]) ** 2 + (lon - SITIO[1]) ** 2), lat.shape)
    H = {r["utc"][:13]: r for r in json.load(open(traj))["registros"] if r["utc"][14:16] == "00"}
    linhas, ant = [], None
    por_t = []
    for k, t in enumerate(tempos):
        olr = v["OLR"][k]
        if float(np.nanmax(olr)) <= 0.0:          # instante inicial: o WRF ainda nao calculou a radiacao (OLR = 0 em tudo)
            por_t.append((t, [])); continue
        lab, n = ndimage.label(olr < 120.0)
        ob = []
        for i in range(1, n + 1):
            m = lab == i; ar = float(m.sum() * A)
            if ar < 500:
                continue
            w = (120.0 - olr[m]).clip(1e-6)
            la, lo = float(np.average(lat[m], weights=w)), float(np.average(lon[m], weights=w))
            d, r = dist(SITIO[0], SITIO[1], la, lo)
            ob.append({"area_km2": round(ar), "olr_min": round(float(olr[m].min()), 1), "lat": round(la, 2), "lon": round(lo, 2), "dist": round(d), "rumo": round(r)})
        ob = sorted([o for o in ob if o["dist"] < 600], key=lambda o: -o["area_km2"])
        por_t.append((t, ob))
    if any(p[1] for p in por_t):
        k0 = max(range(len(por_t)), key=lambda k: por_t[k][1][0]["area_km2"] if por_t[k][1] else 0)
        sis = {k0: por_t[k0][1][0]}
        for passo in (1, -1):
            a = sis[k0]; k = k0 + passo
            while 0 <= k < len(por_t):
                viz = [(dist(a["lat"], a["lon"], o["lat"], o["lon"])[0], o) for o in por_t[k][1]]
                viz = [x for x in viz if x[0] < 150]
                if not viz:
                    break
                a = min(viz, key=lambda x: x[0])[1]; sis[k] = a; k += passo
    else:
        sis = {}
    chuva = v["RAINNC"] + v["RAINC"]
    for k, (t, ob) in enumerate(por_t):
        s = sis.get(k); h = H.get(t[:10] + "T" + t[11:13]); hs = h["sistema"] if h else None
        l = {"utc": t, "wrf": s, "himawari": ({"area_km2": hs["area_km2"], "lat": hs["lat"], "lon": hs["lon"], "dist": hs["dist_sitio_km"]} if hs else None),
             "olr_sitio": round(float(v["OLR"][k][jy, ix]), 1), "chuva_sitio_mm": round(float(chuva[k][jy, ix]), 2)}
        if s and hs:
            l["sep_km"] = round(dist(hs["lat"], hs["lon"], s["lat"], s["lon"])[0])
        linhas.append(l)
    # criterio pre-registrado: em algum horario de 18 a 22 UTC de 25/08, sistema WRF >= 5.000 km2 a <= 100 km do centro do Himawari
    ok = [l for l in linhas if l["utc"][:10] == "2026-08-25" and 18 <= int(l["utc"][11:13]) <= 22 and l["wrf"]
          and l["wrf"]["area_km2"] >= 5000 and l.get("sep_km", 1e9) <= 100]
    # leitura literal do criterio, sem depender do rastreio: em cada saida de 18 a 22 UTC, QUALQUER objeto >= 5.000 km2
    # a <= 100 km do centro do Himawari da hora mais proxima
    direto = []
    for t, ob in por_t:
        if t[:10] != "2026-08-25" or not (18 <= int(t[11:13]) <= 22):
            continue
        h = H.get(t[:10] + "T" + t[11:13]); hs = h["sistema"] if h else None
        if not hs:
            continue
        cand = [dict(o, sep_km=round(dist(hs["lat"], hs["lon"], o["lat"], o["lon"])[0])) for o in ob]
        maior = max(cand, key=lambda o: o["area_km2"]) if cand else None
        perto = min(cand, key=lambda o: o["sep_km"]) if cand else None
        direto.append({"utc": t, "himawari": {"lat": hs["lat"], "lon": hs["lon"], "area_km2": hs["area_km2"]}, "maior_objeto_wrf": maior,
                       "objeto_wrf_mais_proximo": perto, "passa": any(o["area_km2"] >= 5000 and o["sep_km"] <= 100 for o in cand)})
    ok = bool(ok) or any(x["passa"] for x in direto)
    json.dump({"arquivo": arq, "criterio_ok": bool(ok), "criterio_direto": direto, "linhas": linhas}, open(pref + ".json", "w"), indent=1)
    with open(pref + ".txt", "w", encoding="utf-8") as f:
        f.write("WRF (%s) x Himawari-9 -- objeto OLR < 120 W/m2 | criterio (18-22 UTC: >= 5.000 km2 a <= 100 km do centro observado): %s\n" % (arq, "PASSA" if ok else "NAO PASSA"))
        f.write("criterio direto (qualquer objeto, sem rastreio):\n")
        for x in direto:
            m, p = x["maior_objeto_wrf"], x["objeto_wrf_mais_proximo"]
            f.write("  %s Himawari %6d km2 em %.2fN %.2fE | WRF maior: %s | WRF mais proximo: %s | %s\n" % (
                x["utc"], x["himawari"]["area_km2"], x["himawari"]["lat"], x["himawari"]["lon"],
                ("%d km2 a %d km" % (m["area_km2"], m["sep_km"])) if m else "-", ("%d km2 a %d km" % (p["area_km2"], p["sep_km"])) if p else "-",
                "passa" if x["passa"] else "nao"))
        f.write(" UTC                 WRF: area_km2  lat    lon    dist | Himawari: area_km2  lat    lon    dist | sep(km) | sitio: OLR  chuva(mm)\n")
        for l in linhas:
            s, hs = l["wrf"], l["himawari"]
            f.write("%s  %s | %s | %6s | %6.1f %8.2f\n" % (l["utc"], ("%9d %6.2f %6.2f %4d" % (s["area_km2"], s["lat"], s["lon"], s["dist"])) if s else "%29s" % "-",
                    ("%9d %6.2f %6.2f %4d" % (hs["area_km2"], hs["lat"], hs["lon"], hs["dist"])) if hs else "%29s" % "-", l.get("sep_km", "-"), l["olr_sitio"], l["chuva_sitio_mm"]))
    print(open(pref + ".txt", encoding="utf-8").read())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
