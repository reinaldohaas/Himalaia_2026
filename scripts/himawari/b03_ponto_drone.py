# -*- coding: utf-8 -*-
"""
Visivel B03 (0,64 um, 500 m) do Himawari-9 sobre o ponto do drone (28,293985 N, 85,523964 E) e o anfiteatro,
a cada 10 min de 26/08 00:00 a 03:00 UTC (segmento 3 do disco inteiro). E o unico canal que separa o ponto do
anfiteatro (2,7 km): o B13 tem pixel de 2 km.

Refletancia: albedo do arquivo (c' x radiancia, bloco 5 do HSD) dividido por cos(zenite solar). Com o sol baixo
(sza > ~75 graus, ate ~01:20 UTC) o relevo domina: encostas voltadas para leste brilham e as de oeste ficam na sombra.
O Himawari ve a regiao com zenite de ~66 graus: cada km de altitude desloca a imagem ~2,3 km para WNW, inclusive o
proprio relevo (o Langtang Lirung, a 7,2 km, aparece ~17 km a WNW). Os mapas sao ortorretificados com o GLO-30 a 3"
(tile do d04): cada celula e amostrada na posicao aparente do chao na sua cota. Nuvem baixa colada ao relevo fica no
lugar; um topo a h km sobre o ponto do drone aparece sobre o chao de cota z a (h - z) x 2,3 km a WNW (setas, 6 e 9 km).
O deslocamento e tratado como linear em h (calculado no ponto para h = 5 km).

Uso: python b03_ponto_drone.py [dir_bruto] [dir_saida] [AAAAMMDD]   (dia padrao 20260826; 20260825 = referencia)
Saidas: b03_ponto_drone.png (prancha), b03_ponto_drone_serie.txt/.json (refletancia em 3x3 pixels por altura de topo)
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import ahi_hsd as hsd
from fase_topo_10min import zenite_solar

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
BRUTO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "data", "raw", "himawari_b03")
SAIDA = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "data", "processed", "himawari_b03")
BUCKET = "https://noaa-himawari9.s3.amazonaws.com"
DIA = datetime.strptime(sys.argv[3] if len(sys.argv) > 3 else "20260826", "%Y%m%d")
SUF = "" if DIA.day == 26 else "_" + DIA.strftime("%Y%m%d")
P = (28.293985, 85.523964)
REF = {"anfiteatro (exutorio)": (28.285, 85.513), "Langtang Lirung": (28.2563, 85.5193), "USGS tbwb": (28.271, 85.515)}
CICATRIZ = [(28.2830, 85.5225), (28.2870, 85.5300), (28.2950, 85.5300)]
ALTURAS = (0, 5.5, 7, 9, 12)        # km acima do nivel do mar (0 = o chao do ponto, na cota do GLO-30)
DG = 0.002
TILE = os.path.join(RAIZ, "cluster", "wrf_lhende", "d04", "glo30_3s", "00001-00540.00001-00480")
lat = np.arange(28.36, 28.20, -DG); lon = np.arange(85.42, 85.62, DG)
LON, LAT = np.meshgrid(lon, lat)


def horarios():
    t = DIA
    while t <= DIA + timedelta(hours=3):
        yield t
        t += timedelta(minutes=10)


def baixar(t):
    os.makedirs(BRUTO, exist_ok=True)
    nome = "HS_H09_%s_B03_FLDK_R05_S0310.DAT.bz2" % t.strftime("%Y%m%d_%H%M")
    dst = os.path.join(BRUTO, nome)
    if not os.path.exists(dst):
        urllib.request.urlretrieve("%s/AHI-L1b-FLDK/%s/%s" % (BUCKET, t.strftime("%Y/%m/%d/%H%M"), nome), dst + ".part")
        os.replace(dst + ".part", dst)
    return dst


def aparente(la0, lo0, h, sub):
    la, lo = la0, lo0
    for _ in range(10):
        tl, to = hsd.paralaxe(la, lo, h, sub)
        la, lo = la - (tl - la0), lo - (to - lo0)
    return la, lo


def amostra(s, campo, la, lo):
    c, l = hsd.ll2cl(la, lo, s["sub_lon"], s["cfac"], s["lfac"], s["coff"], s["loff"])
    i = np.rint(l).astype(int) - 1 - (s["lin0"] - 1); j = np.rint(c).astype(int) - 1
    ok = (i >= 0) & (i < campo.shape[0]) & (j >= 0) & (j < campo.shape[1])
    out = np.full(np.shape(la), np.nan)
    out[ok] = campo[i[ok], j[ok]]
    return out, i, j


def relevo_km(la, lo):
    z = np.fromfile(TILE, ">i2").reshape(480, 540).astype(float)     # linha 0 = sul; 28,08 N, 85,30 E, 3"
    r = 3.0 / 3600.0
    return z[((la - 28.08) / r).astype(int), ((lo - 85.30) / r).astype(int)] / 1000.0


def seta_orto(h, d, zchao):
    """celula do chao (ortorretificado) onde aparece um topo a h km sobre o ponto: X = P + (h - z(X)) d"""
    x = np.array(P, float)
    for _ in range(20):
        x = np.array(P) + (h - float(zchao(np.array([x[0]]), np.array([x[1]]))[0])) * d
    return tuple(x)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    Z = relevo_km(LAT, LON)
    zP = float(relevo_km(np.array([P[0]]), np.array([P[1]]))[0])
    quadros, serie, cubo = [], [], {}
    for t in horarios():
        try:
            s = hsd.ler_segmento(baixar(t))
        except Exception as e:
            print(t, "sem dados:", e, flush=True)
            continue
        sza = float(zenite_solar(t, *P))
        refl = s["rad"].astype(np.float64) * s["c_albedo"] / np.cos(np.radians(min(sza, 88.0)))
        d = (np.array(aparente(P[0], P[1], 5.0, s["sub_lon"])) - np.array(P)) / 5.0   # graus por km de altura
        m, _, _ = amostra(s, refl, LAT + Z * d[0], LON + Z * d[1])
        ent = {"utc": t.strftime("%H:%M"), "sza": round(sza, 1), "r": {}, "desloc_km_por_km": round(float(np.hypot(d[0] * 111.32, d[1] * 111.32 * np.cos(np.radians(P[0])))), 2)}
        for h in ALTURAS:
            la, lo = aparente(P[0], P[1], h if h else zP, s["sub_lon"])
            _, i, j = amostra(s, refl, np.array([la]), np.array([lo]))
            v = refl[i[0] - 1:i[0] + 2, j[0] - 1:j[0] + 2]
            ent["r"][h] = (round(float(np.nanmean(v)), 3), round(float(np.nanmax(v)), 3))
        ent["seta"] = {h: seta_orto(h, d, relevo_km) for h in (6, 9)}
        quadros.append((t, sza, m, ent["seta"])); serie.append(ent); cubo[t.strftime("%H%M")] = m.astype(np.float32)
        print(t.strftime("%H:%M"), "sza %.1f" % sza, " ".join("h%d=%.3f" % (h, ent["r"][h][0]) for h in ALTURAS), flush=True)

    lin = ["# Himawari-9 B03 (0,64 um, 500 m): refletancia/cos(sza) em 3x3 pixels (~1,5 km) na posicao aparente de um",
           "# topo a h km sobre o ponto do drone (h = 0: o proprio chao, a %.2f km). media e maximo." % zP,
           "UTC   sza  | " + " | ".join("h=%4.1f km: med  max" % h for h in ALTURAS)]
    for e in serie:
        lin.append("%s %5.1f | %s" % (e["utc"], e["sza"], " | ".join("        %5.3f %5.3f" % tuple(e["r"][h]) for h in ALTURAS)))
    open(os.path.join(SAIDA, "b03_ponto_drone_serie%s.txt" % SUF), "w", encoding="utf-8").write("\n".join(lin) + "\n")
    json.dump(serie, open(os.path.join(SAIDA, "b03_ponto_drone_serie%s.json" % SUF), "w", encoding="utf-8"), indent=1)

    n = len(quadros); nc = 5; nl = int(np.ceil(n / nc))
    fig, axs = plt.subplots(nl, nc, figsize=(3.2 * nc, 3.3 * nl))
    for ax in axs.ravel()[n:]:
        ax.axis("off")
    ext = [lon[0], lon[-1], lat[-1], lat[0]]
    for ax, (t, sza, m, seta) in zip(axs.ravel(), quadros):
        ax.imshow(m, extent=ext, cmap="gray", vmin=0, vmax=1.0 if sza < 75 else 1.5, interpolation="nearest")
        ax.plot([c[1] for c in CICATRIZ], [c[0] for c in CICATRIZ], "r-", lw=1.5)
        ax.plot(P[1], P[0], "y*", ms=10, mec="k")
        for k, v in REF.items():
            ax.plot(v[1], v[0], "c^" if k.startswith("Lang") else "co", ms=4)
        ax.contour(lon, lat, Z, levels=[4, 5, 6, 7], colors=["#4a90d9", "#2ca02c", "#ff7f0e", "#d62728"], linewidths=0.5)
        for h, cor in ((6, "orange"), (9, "m")):
            la, lo = seta[h]
            ax.annotate("", xy=(lo, la), xytext=(P[1], P[0]), arrowprops=dict(arrowstyle="->", color=cor, lw=1))
        ax.set_title("%s UTC (%s NPT) sza %.0f" % (t.strftime("%H:%M"), (t + timedelta(hours=5, minutes=45)).strftime("%H:%M"), sza), fontsize=8)
        ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_aspect(1 / np.cos(np.radians(28.29)))
        ax.tick_params(labelsize=6)
    fig.suptitle("Himawari-9 B03 (0,64 um, 500 m), refletancia/cos(sza), " + DIA.strftime("%d/%m/%Y") + ". Estrela = ponto do drone; vermelho = cicatriz;\n"
                 "triangulo = Langtang Lirung; circulos = exutorio do anfiteatro e USGS tbwb. Ortorretificado com o GLO-30 (curvas de 4, 5, 6 e 7 km);\n"
                 "setas = onde aparece um topo a 6 km (laranja) e 9 km (magenta) sobre o ponto",
                 fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(SAIDA, "b03_ponto_drone%s.png" % SUF), dpi=130)
    np.savez_compressed(os.path.join(SAIDA, "b03_orto%s.npz" % SUF), lat=lat, lon=lon, Z=Z, **{"t" + k: v for k, v in cubo.items()})
    print("gravado em", SAIDA)


if __name__ == "__main__":
    main()
