# -*- coding: utf-8 -*-
"""
Agua super-resfriada no topo das nuvens perto do anfiteatro e do ponto do drone (28,293985 N, 85,523964 E), noite de
25 para 26/08/2026, 17:00-03:00 UTC a cada 10 min, Himawari-9 (B07 3,9 um, B13 10,4 um, 2 km; de dia tambem B03 e B05).

1) Posicao: cada pixel e levado da posicao aparente para a verdadeira com a altura do topo tirada do B13 pela sondagem
   do ERA5 (input_sounding_pre_colapso_4322 do CM1). A 66 graus de zenite, um topo a 8 km desloca ~20 km.
2) Fase do topo (so pixels com 238 K <= T13 < 273 K, isto e, topo abaixo de 0 C e acima do limite de -35 C):
   noite (sza > 88): agua se BTD = T07 - T13 <= -2 K (gotas emitem menos em 3,9 um que em 10,4 um);
   dia: agua se r39 >= 0,10 (refletancia em 3,9 um; gelo < ~0,05) e B05 (1,6 um) >= 0,25.
   Com o sol baixo (75 <= sza <= 88, 00:00-01:00 UTC) a r39 e o B05/cos(sza) explodem: fase indeterminada (sem pixel de agua).
3) Massa:
   a) nuvem sintetica (dia e noite): coluna adiabatica de agua liquida do nivel de 0 C (z0) ate o topo (zt):
      LWP_ad = 0,5 G (zt - z0)^2, G ~ 1,0 g m-3 por km (gradiente adiabatico do conteudo de agua a -5 C, ~550 hPa);
      a massa sintetica e a soma de LWP_ad x area, com fator subadiabatico f = 0,3 (tipico) a 1 (teto).
   b) de dia, pela refletancia do B03 (duas correntes, g = 0,85): tau = 2R / ((1-g)(1-R)); LWP = (2/3) rho tau re,
      re = 10 um (6-15 um). Vale so com sza < 75.
Aneis: 5, 10 e 30 km do ponto do drone (posicoes verdadeiras).
Uso: python agua_sr_satelite.py <dir_b07_b13> <dir_b03> <dir_b05>
Saidas: data/processed/agua_sr_satelite/agua_sr_satelite.txt, .json, .png
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

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
DIR_IR, DIR_B03, DIR_B05 = sys.argv[1:4]
SAIDA = os.path.join(RAIZ, "data", "processed", "agua_sr_satelite")
SOND = os.path.join(RAIZ, "data", "processed", "toro_cm1", "input_sounding_pre_colapso_4322")
BUCKET = "https://noaa-himawari9.s3.amazonaws.com"
P = (28.293985, 85.523964)
ANEIS = (5, 10, 30)
G_AD = 1.0e-3          # kg m-3 por km
RE = 10e-6


def baixar(t, banda, pasta, res="R20"):
    os.makedirs(pasta, exist_ok=True)
    nome = "HS_H09_%s_%s_FLDK_%s_S0310.DAT.bz2" % (t.strftime("%Y%m%d_%H%M"), banda, res)
    dst = os.path.join(pasta, nome)
    if not os.path.exists(dst):
        urllib.request.urlretrieve("%s/AHI-L1b-FLDK/%s/%s" % (BUCKET, t.strftime("%Y/%m/%d/%H%M"), nome), dst + ".part")
        os.replace(dst + ".part", dst)
    return dst


def perfil():
    L = open(SOND).read().split("\n"); ps = float(L[0].split()[0])
    d = np.array([list(map(float, l.split())) for l in L[1:] if l.strip()])
    z, th, qv = d[:, 0], d[:, 1], d[:, 2] / 1e3
    g, Rd, cp = 9.81, 287.04, 1004.5; pi = [(ps / 1000) ** (Rd / cp)]
    for k in range(1, len(z)):
        thv = 0.5 * (th[k] * (1 + 0.61 * qv[k]) + th[k - 1] * (1 + 0.61 * qv[k - 1])); pi.append(pi[-1] - g * (z[k] - z[k - 1]) / (cp * thv))
    return (z + 4322.0) / 1000.0, th * np.array(pi)       # km ASL, K


def zenite(t, lat, lon):
    n = t.timetuple().tm_yday
    g = 2 * np.pi / 365 * (n - 1 + (t.hour - 12) / 24)
    dec = 0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g) + 0.000907 * np.sin(2 * g)
    eqt = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g) - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    hs = np.radians(((t.hour * 60 + t.minute + eqt + 4 * lon) / 4) - 180)
    la = np.radians(lat)
    return np.degrees(np.arccos(np.sin(la) * np.sin(dec) + np.cos(la) * np.cos(dec) * np.cos(hs)))


def planck(lam_um, T):
    h, c, k = 6.62607015e-34, 2.99792458e8, 1.380649e-23
    lam = lam_um * 1e-6
    return 2 * h * c ** 2 / lam ** 5 / (np.exp(h * c / (lam * k * T)) - 1) * 1e-6


def main():
    os.makedirs(SAIDA, exist_ok=True)
    zp, Tp = perfil()
    z0 = float(np.interp(273.15, Tp[::-1], zp[::-1]))
    alt_de_T = lambda T: np.interp(-T, -Tp, zp)                    # T decresce com z
    s13 = hsd.ler_segmento(baixar(datetime(2026, 8, 26, 2, 50), "B13", DIR_IR))
    # caixa de pixels aparentes: topos ate 14 km sobre o anel de 30 km deslocam ate ~35 km para WNW
    c, l = hsd.ll2cl(np.array([P[0] - 0.45, P[0] + 0.55]), np.array([P[1] - 0.75, P[1] + 0.40]), s13["sub_lon"], s13["cfac"], s13["lfac"], s13["coff"], s13["loff"])
    i0, i1 = int(min(l)) - (s13["lin0"] - 1) - 2, int(max(l)) - (s13["lin0"] - 1) + 2
    j0, j1 = int(min(c)) - 2, int(max(c)) + 2
    I, J = np.mgrid[i0:i1, j0:j1]
    # lat/lon aparentes dos pixels (inversao numerica de ll2cl numa grade fina)
    gl, gn = np.meshgrid(np.arange(P[0] - 0.6, P[0] + 0.7, 0.005), np.arange(P[1] - 0.9, P[1] + 0.55, 0.005), indexing="ij")
    cc, ll = hsd.ll2cl(gl, gn, s13["sub_lon"], s13["cfac"], s13["lfac"], s13["coff"], s13["loff"])
    from scipy.interpolate import griddata
    pts = np.c_[(ll.ravel() - 1 - (s13["lin0"] - 1)), cc.ravel() - 1]
    LA = griddata(pts, gl.ravel(), (I, J), method="linear"); LO = griddata(pts, gn.ravel(), (I, J), method="linear")
    # area de cada pixel no chao (km2), pelo jacobiano das posicoes aparentes
    dLAi, dLAj = np.gradient(LA); dLOi, dLOj = np.gradient(LO)
    area_px = float(np.nanmedian(np.abs(dLAi * dLOj - dLAj * dLOi))) * 111.32 ** 2 * np.cos(np.radians(P[0]))
    print("area por pixel %.1f km2" % area_px)
    dkm = lambda la, lo: np.hypot((la - P[0]) * 111.32, (lo - P[1]) * 111.32 * np.cos(np.radians(P[0])))

    reg, mapas = [], {}
    t = datetime(2026, 8, 25, 17, 0)
    while t <= datetime(2026, 8, 26, 3, 0):
        try:
            s7, s13 = hsd.ler_segmento(baixar(t, "B07", DIR_IR)), hsd.ler_segmento(baixar(t, "B13", DIR_IR))
        except Exception as e:
            print(t, "sem dados:", e, flush=True); t += timedelta(minutes=10); continue
        sza = float(zenite(t, *P))
        T13 = s13["tb"][i0:i1, j0:j1].astype(float); T07 = s7["tb"][i0:i1, j0:j1].astype(float)
        L07 = s7["rad"][i0:i1, j0:j1].astype(float)
        zt = alt_de_T(T13)
        frio = (T13 >= 238) & (T13 < 273.15)
        if sza > 88:
            agua = frio & (T07 - T13 <= -2.0)
            r39 = np.full(T13.shape, np.nan); b05 = r39.copy(); R03 = r39.copy()
        else:
            e39 = np.pi * planck(s7["lambda_um"], 5772.0) * (6.957e8 / 1.496e11) ** 2 / 1.0105 ** 2
            mu = np.cos(np.radians(sza)); Be = planck(s7["lambda_um"], T13)
            r39 = (L07 - Be) / (e39 * mu / np.pi - Be)
            try:
                s5 = hsd.ler_segmento(baixar(t, "B05", DIR_B05))
                b05 = (s5["rad"] * s5["c_albedo"])[i0:i1, j0:j1] / mu
            except Exception:
                b05 = np.full(T13.shape, np.nan)
            try:
                s3 = hsd.ler_segmento(baixar(t, "B03", DIR_B03, "R05"))
                a3 = s3["rad"].astype(float) * s3["c_albedo"] / mu
                off = (s13["lin0"] - 1) * 4 - (s3["lin0"] - 1)          # linhas do B03 (500 m) = 4 x as do B13 (2 km)
                R03 = np.array([[np.nanmean(a3[4 * a + off:4 * a + off + 4, 4 * b:4 * b + 4]) for b in range(j0, j1)] for a in range(i0, i1)])
            except Exception:
                R03 = np.full(T13.shape, np.nan)
            # com sza >= 75 a r39 e o B05/cos(sza) explodem (denominador pequeno): fase indeterminada
            agua = frio & (r39 >= 0.10) & ((b05 >= 0.25) | ~np.isfinite(b05)) & (sza < 75)
        # posicao verdadeira de cada pixel com a altura do topo
        TLA, TLO = LA.copy(), LO.copy()
        for a, b in zip(*np.where(np.isfinite(LA) & (T13 < 285))):
            TLA[a, b], TLO[a, b] = hsd.paralaxe(LA[a, b], LO[a, b], float(zt[a, b]), s13["sub_lon"])
        dist = dkm(TLA, TLO)
        H = np.clip(zt - z0, 0, None)
        lwp_ad = 0.5 * (G_AD * 1e3) * H ** 2                               # kg m-2: 0,5 G H^2 com G em g m-3 km-1 e H em km
        tau = np.where(np.isfinite(R03), 2 * np.clip(R03, 0, 0.95) / ((1 - 0.85) * (1 - np.clip(R03, 0, 0.95))), np.nan)
        lwp_vis = (2.0 / 3.0) * 1000.0 * tau * RE                          # kg m-2
        ent = {"utc": t.strftime("%d %H:%M"), "sza": round(sza, 1), "fase": "indeterminada" if 75 <= sza <= 88 else "ok"}
        for r in ANEIS:
            m = agua & (dist <= r); mf = frio & (dist <= r)
            ent["r%d" % r] = {
                "area_frio_km2": round(float(mf.sum() * area_px), 0), "area_agua_km2": round(float(m.sum() * area_px), 0),
                "zt_med_km": round(float(np.nanmean(zt[m])), 1) if m.any() else None,
                "massa_sint_f1_kg": float(np.nansum(lwp_ad[m]) * area_px * 1e6),
                "massa_vis_kg": float(np.nansum(lwp_vis[m]) * area_px * 1e6) if (m.any() and sza < 75) else None,
                "T13_min": round(float(np.nanmin(T13[dist <= r])), 1)}
        reg.append(ent)
        if t.strftime("%H%M") in ("1900", "2100", "2300", "0000", "0050", "0130", "0230", "0250"):
            mapas[t.strftime("%d %H:%M")] = (TLA, TLO, T13, agua, sza)
        e30, e10 = ent["r30"], ent["r10"]
        print("%s sza %5.1f | r10 agua %4.0f km2 | r30 frio %5.0f agua %5.0f km2 zt %s sint %.1e vis %s" % (
            ent["utc"], sza, e10["area_agua_km2"], e30["area_frio_km2"], e30["area_agua_km2"], e30["zt_med_km"],
            e30["massa_sint_f1_kg"], "%.1e" % e30["massa_vis_kg"] if e30["massa_vis_kg"] else "-"), flush=True)
        t += timedelta(minutes=10)

    lin = ["# Agua super-resfriada no topo (238 K <= T13 < 273 K e assinatura de gotas), Himawari-9, posicoes corrigidas da paralaxe",
           "# pela altura do topo (B13 + sondagem ERA5); aneis em torno do ponto do drone. 0 C a %.2f km." % z0,
           "# massa_sint = nuvem sintetica adiabatica do 0 C ao topo (f = 1, teto; f tipico 0,3); massa_vis = pela refletancia do B03 (dia, sza < 75)",
           "dia hora  sza  | r5: agua km2 vis kg | r10: agua km2 sint_f1 kg vis kg | r30: frio km2 agua km2 zt km sint_f1 kg vis kg | T13 min r30"]
    for e in reg:
        a, b, c = e["r5"], e["r10"], e["r30"]
        fv = lambda x: "%.1e" % x["massa_vis_kg"] if x["massa_vis_kg"] else "-"
        lin.append("%s %5.1f | %5.0f %8s | %5.0f %8.1e %8s | %6.0f %6.0f %4s %8.1e %8s | %5.1f%s" % (
            e["utc"], e["sza"], a["area_agua_km2"], fv(a), b["area_agua_km2"], b["massa_sint_f1_kg"], fv(b), c["area_frio_km2"], c["area_agua_km2"],
            "%.1f" % c["zt_med_km"] if c["zt_med_km"] else "-", c["massa_sint_f1_kg"], fv(c), c["T13_min"], "  (fase indeterminada)" if e["fase"] != "ok" else ""))
    open(os.path.join(SAIDA, "agua_sr_satelite.txt"), "w", encoding="utf-8").write("\n".join(lin) + "\n")
    json.dump({"z0_km": z0, "area_px_km2": area_px, "registros": reg}, open(os.path.join(SAIDA, "agua_sr_satelite.json"), "w", encoding="utf-8"), indent=1)

    # serie temporal e mapas
    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_subplot(2, 1, 1)
    x = np.arange(len(reg)); rot = [e["utc"][3:] for e in reg]
    for r, cor in zip(ANEIS, ("C3", "C1", "C0")):
        ax.plot(x, [e["r%d" % r]["area_agua_km2"] for e in reg], "-o", ms=3, color=cor, label="topo de agua super-resfriada, ate %d km" % r)
    ax.plot(x, [e["r30"]["area_frio_km2"] for e in reg], "k--", lw=1, label="topo entre -35 e 0 C, ate 30 km")
    ax.set_ylabel("area (km2)"); ax.set_xticks(x[::3]); ax.set_xticklabels(rot[::3], fontsize=7)
    ax2 = ax.twinx(); ax2.semilogy(x, [max(e["r30"]["massa_sint_f1_kg"], 1) for e in reg], "g-", lw=1.5, label="massa sintetica ate 30 km (f = 1)")
    ax2.semilogy(x, [e["r30"]["massa_vis_kg"] or np.nan for e in reg], "g^", ms=4, label="massa pelo B03 ate 30 km")
    ax2.set_ylabel("kg"); ax2.set_ylim(1e5, 1e11)
    for xx, tt in ((rot.index("26 00:00") if "26 00:00" in rot else None, "nascer do sol"),):
        if xx is not None: ax.axvline(xx, color="0.6", lw=0.8)
    ax.legend(loc="upper left", fontsize=7); ax2.legend(loc="upper right", fontsize=7)
    ax.set_title("Himawari-9: area com topo de agua super-resfriada perto do ponto do drone e massa da nuvem sintetica, 25/08 17:00 a 26/08 03:00 UTC", fontsize=9)
    for n, (h, (TLA, TLO, T13, agua, sza)) in enumerate(mapas.items()):
        a = fig.add_subplot(2, 8, 9 + n)
        sc = a.scatter(TLO, TLA, c=T13, s=6, cmap="inferno", vmin=200, vmax=290)
        a.scatter(TLO[agua], TLA[agua], s=8, facecolors="none", edgecolors="c", linewidths=0.6)
        th = np.linspace(0, 2 * np.pi, 100)
        for r in (10, 30):
            a.plot(P[1] + r / (111.32 * np.cos(np.radians(P[0]))) * np.cos(th), P[0] + r / 111.32 * np.sin(th), "w-", lw=0.6)
        a.plot(P[1], P[0], "y*", ms=8, mec="k")
        a.set_xlim(P[1] - 0.4, P[1] + 0.4); a.set_ylim(P[0] - 0.35, P[0] + 0.35); a.set_aspect(1 / np.cos(np.radians(P[0])))
        a.set_title(h + " UTC", fontsize=7); a.tick_params(labelsize=5)
    fig.text(0.5, 0.02, "Mapas: T13 nas posicoes verdadeiras (cor; 200-290 K); circulos ciano = topo de agua super-resfriada; aneis de 10 e 30 km do ponto (estrela)",
             ha="center", fontsize=8)
    fig.savefig(os.path.join(SAIDA, "agua_sr_satelite.png"), dpi=120, bbox_inches="tight")
    print("gravado em", SAIDA)


if __name__ == "__main__":
    main()
