# -*- coding: utf-8 -*-
"""
Fase do topo da nuvem sobre o anfiteatro de Lhende, a cada 10 min, de 25/08 22:00 a 26/08 03:30 UTC
(Himawari-9 AHI, B07 3,9 um e B13 10,4 um, disco inteiro, segmento 3, 2 km).

De 00:00 UTC em diante e dia no sitio (nascer do sol ~23:55 UTC; 02:50 UTC = 08:35 NPT). De dia o B07 soma a
emissao termica e a radiacao solar refletida. A refletancia em 3,9 um (Rosenfeld & Lensky 1998; Setvak & Doswell
1991) separa gotas pequenas de agua (r39 alta, ~0,1-0,3) de gelo e neve (r39 baixa, < ~0,05):
    r39 = (L39 - B39(T13)) / (E39 cos(sza) / pi - B39(T13))
com B39(T13) a emissao em 3,9 um a temperatura do B13 e E39 a irradiancia solar na banda (Planck de 5772 K a 1 UA,
aproximacao de banda estreita). Topo frio (T13 < 273 K) com r39 alta = agua liquida super-resfriada no topo.
Ressalvas: rocha nua e solo seco tambem tem r39 moderada; com o sol baixo (sza > 75 graus) a r39 fica ruidosa.

A paralaxe e tratada como em tb_paralaxe: para cada altura de topo h, o pixel aparente que o Himawari ve para
uma nuvem a h km sobre o sitio (inversao de ahi_hsd.paralaxe).

Uso: python fase_topo_10min.py [dir_bruto] [dir_saida]
"""
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import ahi_hsd as hsd

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
BRUTO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "data", "raw", "himawari_10min")
SAIDA = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "data", "processed", "himawari_fase_topo")
BUCKET = "https://noaa-himawari9.s3.amazonaws.com"
SITIO = (28.271, 85.515)
ALTURAS = (4, 6, 8, 10, 12, 14)          # km acima do nivel do mar
H_PLANCK, C_LUZ, K_B = 6.62607015e-34, 2.99792458e8, 1.380649e-23


def horarios():
    t, fim = datetime(2026, 8, 25, 22, 0), datetime(2026, 8, 26, 3, 30)
    while t <= fim:
        yield t
        t += timedelta(minutes=10)


def baixar(t, banda):
    os.makedirs(BRUTO, exist_ok=True)
    nome = "HS_H09_%s_%s_FLDK_R20_S0310.DAT.bz2" % (t.strftime("%Y%m%d_%H%M"), banda)
    dst = os.path.join(BRUTO, nome)
    if os.path.exists(dst):
        return dst
    key = "AHI-L1b-FLDK/%s/%s" % (t.strftime("%Y/%m/%d/%H%M"), nome)
    urllib.request.urlretrieve(BUCKET + "/" + key, dst + ".part")
    os.replace(dst + ".part", dst)
    return dst


def planck(lam_um, T):
    lam = lam_um * 1e-6
    return 2 * H_PLANCK * C_LUZ ** 2 / lam ** 5 / (np.exp(H_PLANCK * C_LUZ / (lam * K_B * T)) - 1) * 1e-6   # W m-2 sr-1 um-1


def zenite_solar(t, lat, lon):
    n = t.timetuple().tm_yday
    g = 2 * np.pi / 365 * (n - 1 + (t.hour - 12) / 24)
    dec = 0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g) + 0.000907 * np.sin(2 * g)
    eqt = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g) - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    hs = np.radians(((t.hour * 60 + t.minute + eqt + 4 * lon) / 4) - 180)
    la = np.radians(lat)
    return np.degrees(np.arccos(np.sin(la) * np.sin(dec) + np.cos(la) * np.cos(dec) * np.cos(hs)))


def aparente(h, sub):
    la, lo = SITIO
    for _ in range(10):
        tl, to = hsd.paralaxe(la, lo, h, sub)
        la, lo = la - (tl - SITIO[0]), lo - (to - SITIO[1])
    return la, lo


def pixel(s, la, lo):
    c, l = hsd.ll2cl(np.array([la]), np.array([lo]), s["sub_lon"], s["cfac"], s["lfac"], s["coff"], s["loff"])
    return int(np.rint(l[0])) - 1 - (s["lin0"] - 1), int(np.rint(c[0])) - 1


def main():
    os.makedirs(SAIDA, exist_ok=True)
    # irradiancia solar na banda do B07 (Planck do Sol a 1 UA; distancia Terra-Sol em 26/08 ~1,0105 UA)
    linhas = ["# Himawari-9, pixel sobre o sitio corrigido da paralaxe para topos a h km; 3x3 pixels (~6 km)",
              "# colunas: UTC NPT sza | para cada h: T13 (K) e r39 do pixel 3x3 de T13 minima",
              "UTC   NPT    sza  | " + " | ".join("h=%2d km: T13  r39" % h for h in ALTURAS)]
    reg = []
    for t in horarios():
        try:
            a7, a13 = baixar(t, "B07"), baixar(t, "B13")
        except Exception as e:
            print(t, "sem dados:", e, flush=True)
            continue
        s7, s13 = hsd.ler_segmento(a7), hsd.ler_segmento(a13)
        sza = float(zenite_solar(t, *SITIO))
        e39 = np.pi * planck(s7["lambda_um"], 5772.0) * (6.957e8 / 1.496e11) ** 2 / 1.0105 ** 2
        mu = np.cos(np.radians(min(sza, 89.0)))
        L7 = s7["rad"].astype(np.float64)   # W m-2 sr-1 um-1 (calibracao do proprio arquivo)
        ent = {"utc": t.strftime("%Y-%m-%dT%H:%MZ"), "sza": round(sza, 1), "h": {}}
        cel = []
        for h in ALTURAS:
            la, lo = aparente(h, s13["sub_lon"])
            i, j = pixel(s13, la, lo)
            T = s13["tb"][i - 1:i + 2, j - 1:j + 2].astype(np.float64)
            L = L7[i - 1:i + 2, j - 1:j + 2]
            k = np.unravel_index(np.nanargmin(T), T.shape)
            Be = planck(s7["lambda_um"], T[k])
            r39 = (L[k] - Be) / (e39 * mu / np.pi - Be) if sza < 89 else np.nan
            ent["h"][h] = (round(float(T[k]), 1), round(float(r39), 3))
            cel.append("%5.1f %5.3f" % (T[k], r39))
        npt = (t + timedelta(hours=5, minutes=45)).strftime("%H:%M")
        linhas.append("%s %s %5.1f | %s" % (t.strftime("%H:%M"), npt, sza, " | ".join("      " + c for c in cel)))
        reg.append(ent)
        print(linhas[-1], flush=True)
    open(os.path.join(SAIDA, "fase_topo_sitio_10min.txt"), "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    import json
    json.dump(reg, open(os.path.join(SAIDA, "fase_topo_sitio_10min.json"), "w", encoding="utf-8"), indent=1)
    print("gravado em", SAIDA)


if __name__ == "__main__":
    main()
