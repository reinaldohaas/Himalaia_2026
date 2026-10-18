# -*- coding: utf-8 -*-
"""
Trajetoria do sistema convectivo de 25-26/08/2026 no Himawari-9 AHI, banda 13 (10,4 um).

1. baixa (bucket publico da NOAA no AWS, sem credencial) so os segmentos do disco completo que cobrem
   24-33 N, 78-93 E, de 25/08 09:00 a 26/08 03:00 UTC, a cada 30 min;
2. reamostra a Tb para uma grade lat/lon de 0,04 grau (vizinho mais proximo);
3. em cada horario, objetos frios (Tb < 213 K, -60 C): area, Tb minima, centroide aparente e centroide
   corrigido da paralaxe (altura do topo pela Tb: h = 16 - 0,143 (Tb - 195) km, entre 9 e 17 km);
   o "sistema" e o maior objeto a menos de 400 km do sitio; trajetoria = sequencia de centroides;
4. grava trajetoria.json, trajetoria.txt e um painel de mapas (.png).
Validacao: Tb no pixel do sitio as 02:50 UTC deve ser ~272,7 K (valor ja registrado no repositorio).

Uso: python3 trajetoria_sistema.py <dir_dados_brutos> <dir_saida>
"""
import glob
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ahi_hsd as hsd  # noqa: E402

SITIO = (28.271, 85.515)
BOX = (24.0, 33.0, 78.0, 93.0)
DG = 0.04
LIM = 213.0
BUCKET = "https://noaa-himawari9.s3.amazonaws.com"


def horarios():
    t = datetime(2026, 8, 25, 9, 0)
    out = []
    while t <= datetime(2026, 8, 26, 3, 0):
        out.append(t); t += timedelta(minutes=30)
    out.insert(out.index(datetime(2026, 8, 26, 3, 0)), datetime(2026, 8, 26, 2, 50))
    return out


def lista(prefixo):
    url = BUCKET + "/?list-type=2&prefix=" + prefixo
    xml = urllib.request.urlopen(url, timeout=60).read().decode()
    return re.findall(r"<Key>([^<]+)</Key>", xml)


def baixar(t, bruto, segs):
    pre = "AHI-L1b-FLDK/%s/" % t.strftime("%Y/%m/%d/%H%M")
    chaves = [k for k in lista(pre) if "_B13_FLDK_R20_S" in k and int(k.split("_S")[-1][:2]) in segs]
    arqs = []
    for k in chaves:
        dst = os.path.join(bruto, os.path.basename(k))
        if not os.path.exists(dst):
            urllib.request.urlretrieve(BUCKET + "/" + k, dst + ".part"); os.replace(dst + ".part", dst)
        arqs.append(dst)
    return sorted(arqs)


def grade():
    lat = np.arange(BOX[1], BOX[0] - 1e-9, -DG); lon = np.arange(BOX[2], BOX[3] + 1e-9, DG)
    return lat, lon


def reamostra(arqs, lat, lon):
    segs = [hsd.ler_segmento(a) for a in arqs]
    s0 = segs[0]
    LON, LAT = np.meshgrid(lon, lat)
    c, l = hsd.ll2cl(LAT, LON, s0["sub_lon"], s0["cfac"], s0["lfac"], s0["coff"], s0["loff"])
    ci = np.rint(c).astype(int) - 1; li = np.rint(l).astype(int) - 1      # 0-based global
    tb = np.full(LAT.shape, np.nan, np.float32)
    for s in segs:
        a = s["lin0"] - 1; b = a + s["tb"].shape[0]
        m = (li >= a) & (li < b) & (ci >= 0) & (ci < s["tb"].shape[1])
        tb[m] = s["tb"][li[m] - a, ci[m]]
    return tb, s0


def area_px(lat):
    return (DG * 111.32) * (DG * 111.32 * np.cos(np.radians(lat)))


def dist_rumo(lat1, lon1, lat2, lon2):
    dy = (lat2 - lat1) * 111.32; dx = (lon2 - lon1) * 111.32 * np.cos(np.radians(0.5 * (lat1 + lat2)))
    return float(np.hypot(dx, dy)), float((np.degrees(np.arctan2(dx, dy)) + 360) % 360)


def main(bruto, saida):
    from scipy import ndimage
    os.makedirs(bruto, exist_ok=True); os.makedirs(saida, exist_ok=True)
    lat, lon = grade()
    # segmentos que cobrem a caixa (calculados com a geometria nominal do AHI 2 km)
    cs, ls = hsd.ll2cl(np.array([BOX[0], BOX[0], BOX[1], BOX[1]]), np.array([BOX[2], BOX[3], BOX[2], BOX[3]]),
                       140.7, 20466275, 20466275, 2750.5, 2750.5)
    segs = sorted(set(int((x - 1) // 550) + 1 for x in np.linspace(ls.min(), ls.max(), 20)))
    print("segmentos necessarios:", segs, flush=True)
    A = area_px(lat)[:, None] * np.ones((1, lon.size))
    LON, LAT = np.meshgrid(lon, lat)
    js = int(np.argmin(abs(lat - SITIO[0]))); is_ = int(np.argmin(abs(lon - SITIO[1])))
    reg, mapas = [], {}
    for t in horarios():
        try:
            arqs = baixar(t, bruto, segs)
        except Exception as e:
            print(t, "falhou o download:", e, flush=True); continue
        if not arqs:
            print(t, "sem arquivos", flush=True); continue
        tb, s0 = reamostra(arqs, lat, lon)
        frio = tb < LIM
        lab, n = ndimage.label(frio)
        obj = []
        for k in range(1, n + 1):
            m = lab == k; ar = float(A[m].sum())
            if ar < 200:
                continue
            w = (LIM - tb[m]).clip(0)
            la, lo = float(np.average(LAT[m], weights=w)), float(np.average(LON[m], weights=w))
            tmin = float(np.nanmin(tb[m])); h = float(np.clip(16 - 0.143 * (np.nanmean(tb[m]) - 195), 9, 17))
            lat_c, lon_c = hsd.paralaxe(la, lo, h, s0["sub_lon"])
            d, r = dist_rumo(SITIO[0], SITIO[1], lat_c, lon_c)
            obj.append({"area_km2": round(ar), "tb_min": round(tmin, 1), "h_topo_km": round(h, 1),
                        "lat_ap": round(la, 3), "lon_ap": round(lo, 3), "lat": round(lat_c, 3), "lon": round(lon_c, 3),
                        "dist_sitio_km": round(d), "rumo_do_sitio": round(r)})
        obj.sort(key=lambda o: -o["area_km2"])
        perto = [o for o in obj if o["dist_sitio_km"] < 400]
        sis = perto[0] if perto else None
        tb_s = float(tb[js, is_])
        a213 = float(A[(tb < 213) & (np.hypot((LAT - SITIO[0]) * 111.32, (LON - SITIO[1]) * 111.32 * np.cos(np.radians(SITIO[0]))) < 150)].sum())
        reg.append({"utc": t.strftime("%Y-%m-%dT%H:%MZ"), "tb_sitio": round(tb_s, 1), "area213_150km": round(a213),
                    "sistema": sis, "objetos": obj[:8]})
        print("%s  Tb sitio %.1f K | area<213 K em 150 km %6.0f km2 | sistema: %s" % (
            t.strftime("%d %H:%M"), tb_s, a213,
            ("%6d km2, Tbmin %.0f K, centro %.2fN %.2fE (paralaxe corrigida), a %d km do sitio, rumo %d" % (
                sis["area_km2"], sis["tb_min"], sis["lat"], sis["lon"], sis["dist_sitio_km"], sis["rumo_do_sitio"])) if sis else "-"), flush=True)
        if t.minute == 0 and t.hour % 3 == 0 or t == datetime(2026, 8, 26, 2, 50):
            mapas[t.strftime("%d %H:%M")] = tb
    # rastreio por continuidade: parte do maior sistema a menos de 400 km do sitio (o MCS) e segue, para
    # frente e para tras, o objeto cujo centroide esta a menos de 150 km do anterior; fora disso, sem sistema
    cand = [(k, r["sistema"]) for k, r in enumerate(reg) if r["sistema"]]
    k0 = max(cand, key=lambda kv: kv[1]["area_km2"])[0] if cand else None
    if k0 is not None:
        fixo = {k0: reg[k0]["sistema"]}
        for passo in (1, -1):
            ant = reg[k0]["sistema"]; k = k0 + passo
            while 0 <= k < len(reg):
                viz = [(dist_rumo(ant["lat"], ant["lon"], o["lat"], o["lon"])[0], o) for o in reg[k]["objetos"]]
                viz = [v for v in viz if v[0] < 150.0]
                if not viz:
                    break
                ant = min(viz, key=lambda v: v[0])[1]; fixo[k] = ant; k += passo
        for k, r in enumerate(reg):
            r["sistema"] = dict(fixo[k]) if k in fixo else None
    # velocidades entre horarios consecutivos
    for a, b in zip(reg[:-1], reg[1:]):
        if a["sistema"] and b["sistema"]:
            dt = (datetime.strptime(b["utc"], "%Y-%m-%dT%H:%MZ") - datetime.strptime(a["utc"], "%Y-%m-%dT%H:%MZ")).total_seconds()
            d, r = dist_rumo(a["sistema"]["lat"], a["sistema"]["lon"], b["sistema"]["lat"], b["sistema"]["lon"])
            b["sistema"]["vel_kmh"] = round(d / (dt / 3600.0), 1); b["sistema"]["rumo_desloc"] = round(r)
    json.dump({"sitio": SITIO, "limiar_K": LIM, "caixa": BOX, "grade_graus": DG, "registros": reg},
              open(os.path.join(saida, "trajetoria.json"), "w"), indent=1)
    with open(os.path.join(saida, "trajetoria.txt"), "w", encoding="utf-8") as f:
        f.write("Himawari-9 B13 -- sistema convectivo (maior objeto < 213 K a menos de 400 km do sitio), paralaxe corrigida\n")
        f.write(" UTC          Tb_sitio  area213_150km | area_km2  Tbmin  lat     lon     dist  rumo | vel(km/h) rumo_desloc\n")
        for r in reg:
            s = r["sistema"]
            f.write("%s  %7.1f  %10.0f   | %s\n" % (r["utc"], r["tb_sitio"], r["area213_150km"],
                    ("%7d  %5.0f  %6.2f  %6.2f  %4d  %4d | %8s  %s" % (s["area_km2"], s["tb_min"], s["lat"], s["lon"],
                     s["dist_sitio_km"], s["rumo_do_sitio"], s.get("vel_kmh", "-"), s.get("rumo_desloc", "-"))) if s else "-"))
    figura(os.path.join(saida, "trajetoria.png"), mapas, lat, lon, reg)
    print("gravado em", saida)


def figura(arq, mapas, lat, lon, reg):
    os.environ["MPLBACKEND"] = "Agg"
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ks = list(mapas)[:9]
    nc = 3; nl = int(np.ceil(len(ks) / nc))
    fig, axs = plt.subplots(nl, nc, figsize=(15, 4.4 * nl), constrained_layout=True)
    tr = [(r["sistema"]["lon"], r["sistema"]["lat"]) for r in reg if r["sistema"]]
    for ax, k in zip(np.ravel(axs), ks):
        pc = ax.pcolormesh(lon, lat, mapas[k], cmap="gray_r", vmin=190, vmax=300, shading="auto")
        ax.contour(lon, lat, mapas[k], levels=[213], colors="red", linewidths=0.8)
        if tr:
            ax.plot(*zip(*tr), "-", color="orange", lw=1.2)
        ax.plot(SITIO[1], SITIO[0], "c*", ms=12)
        ax.set_title(k + " UTC (contorno: 213 K; laranja: trajetoria com paralaxe corrigida)", fontsize=9)
        ax.set_aspect(1 / np.cos(np.radians(28.5)))
    for ax in np.ravel(axs)[len(ks):]:
        ax.axis("off")
    fig.colorbar(pc, ax=axs, shrink=0.6, label="Tb B13 (K)")
    fig.savefig(arq, dpi=100)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
