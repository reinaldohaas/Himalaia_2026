# -*- coding: utf-8 -*-
"""
Origem do topo frio sobre o sitio em 25-26/08/2026: conveccao local ou bigorna do sistema convectivo a leste?

Himawari-9 AHI, B13 (10,4 um) e B07 (3,9 um), a cada 10 min (segmento 3), numa grade lat/lon de 0,02 grau em
coordenadas APARENTES (sem paralaxe; o sitio entra na posicao aparente de um topo a H_SITIO km).
Em cada horario:
  * no sitio (ate 10 km): Tb13 minima e media, taxa de resfriamento em 10 min e B07 - B13 (de noite ~0 em nuvem
    opaca espessa, positiva em cirro fino semitransparente);
  * objetos frios (Tb13 < 235 K, conectividade 8): o objeto que cobre o sitio, sua area, Tb minima e se contem
    nucleos profundos (< 213 K); o sistema = maior objeto < 213 K a menos de 400 km;
  * sela: a menor temperatura-limiar em que o pixel mais frio perto do sitio ainda se liga ao nucleo do sistema
    (Tb < limiar, conectividade 8). Sela muito mais quente que o minimo local = nucleo proprio (conveccao local);
    sela proxima do minimo local = o sitio e so a borda de uma nuvem que vem do nucleo (bigorna);
  * linhagem: o objeto do sitio e seguido para tras pela maior sobreposicao com os objetos do horario anterior,
    ate onde aparece pela primeira vez (nasceu perto do sitio ou chegou do leste?).
Saida: origem_topo_frio.txt, .json e .png.

Uso: python3 origem_topo_frio.py <dir_himawari_10min> <dir_saida>
"""
import glob
import json
import os
import sys
from datetime import datetime, timedelta

import numpy as np
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ahi_hsd as hsd  # noqa: E402

BRUTO, SAIDA = sys.argv[1], sys.argv[2]
SITIO = (28.271, 85.515)
H_SITIO = 10.0                                # km: altura do topo para a posicao aparente do sitio
LAT, LON = np.arange(26.8, 30.4001, 0.02), np.arange(83.6, 90.0001, 0.02)
T_OBJ, T_NUC = 235.0, 213.0
R_SITIO, R_PERTO = 10.0, 30.0                 # km
LIMIARES = np.arange(213.0, 260.01, 1.0)


def km(la, lo, p):
    return np.hypot((lo - p[1]) * 111.195 * np.cos(np.radians(p[0])), (la - p[0]) * 111.195)


def aparente(h, sub):
    la, lo = SITIO
    for _ in range(10):
        tl, to = hsd.paralaxe(la, lo, h, sub)
        la, lo = la - (tl - SITIO[0]), lo - (to - SITIO[1])
    return la, lo


def grade(s, glat, glon):
    c, l = hsd.ll2cl(glat, glon, s["sub_lon"], s["cfac"], s["lfac"], s["coff"], s["loff"])
    i = np.rint(l).astype(int) - 1 - (s["lin0"] - 1); j = np.rint(c).astype(int) - 1
    ok = (i >= 0) & (i < s["tb"].shape[0]) & (j >= 0) & (j < s["tb"].shape[1])
    out = np.full(glat.shape, np.nan, np.float32)
    out[ok] = s["tb"][i[ok], j[ok]]
    return out


def horarios():
    t = datetime(2026, 8, 25, 17, 0)
    while t <= datetime(2026, 8, 26, 3, 30):
        yield t
        t += timedelta(minutes=10)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    glat, glon = np.meshgrid(LAT, LON, indexing="ij")
    oito = np.ones((3, 3), bool)
    reg, mapas, ant = [], {}, None
    sit = None
    for t in horarios():
        a13 = glob.glob(os.path.join(BRUTO, "HS_H09_%s_B13_FLDK_R20_S0310.DAT.bz2" % t.strftime("%Y%m%d_%H%M")))
        a07 = glob.glob(os.path.join(BRUTO, "HS_H09_%s_B07_FLDK_R20_S0310.DAT.bz2" % t.strftime("%Y%m%d_%H%M")))
        if not a13:
            continue
        s13 = hsd.ler_segmento(a13[0])
        if sit is None:
            sit = aparente(H_SITIO, s13["sub_lon"])
            dsit = km(glat, glon, sit); msit = dsit <= R_SITIO; mperto = dsit <= R_PERTO
            isit = np.unravel_index(np.argmin(dsit), dsit.shape)
            dsis = km(glat, glon, sit)
        tb = grade(s13, glat, glon)
        tb7 = grade(hsd.ler_segmento(a07[0]), glat, glon) if a07 else np.full_like(tb, np.nan)
        e = {"utc": t.strftime("%Y-%m-%dT%H:%MZ"), "tb_min_sitio": float(np.nanmin(tb[msit])),
             "tb_med_sitio": float(np.nanmean(tb[msit]))}
        fr = msit & (tb < 240)
        e["btd_07_13_sitio"] = float(np.nanmean(tb7[fr] - tb[fr])) if fr.any() else None
        # objetos frios e o sistema
        lab, n = ndimage.label(np.nan_to_num(tb, nan=999) < T_OBJ, structure=oito)
        nuc, nn = ndimage.label(np.nan_to_num(tb, nan=999) < T_NUC, structure=oito)
        sistema = None
        if nn:
            areas = ndimage.sum(np.ones_like(tb), nuc, index=np.arange(1, nn + 1)) * 4.0
            cand = [(areas[k - 1], k) for k in range(1, nn + 1) if dsis[nuc == k].min() <= 400]
            if cand:
                ak, k = max(cand)
                mk = nuc == k
                e["sistema"] = {"area_km2": float(ak), "tb_min": float(tb[mk].min()),
                                "lat": float(glat[mk].mean()), "lon": float(glon[mk].mean()),
                                "dist_sitio_km": float(km(glat[mk].mean(), glon[mk].mean(), sit))}
                sistema = mk
        # objeto do sitio: o objeto < 235 K que cobre o pixel mais frio perto do sitio
        pp = np.where(mperto, np.nan_to_num(tb, nan=999), 999)
        ipp = np.unravel_index(np.argmin(pp), pp.shape)
        e["tb_min_30km"] = float(pp[ipp]); e["min_30km_lat_lon"] = [float(glat[ipp]), float(glon[ipp])]
        ks = lab[ipp]
        obj = None
        if ks:
            obj = lab == ks
            e["objeto_sitio"] = {"area_km2": float(obj.sum() * 4.0), "tb_min": float(tb[obj].min()),
                                 "tem_nucleo_213": bool((tb[obj] < T_NUC).any()),
                                 "contem_sistema": bool(sistema is not None and (obj & sistema).any()),
                                 "lon_oeste_faixa_28_28p6": float(glon[obj & (glat >= 28.0) & (glat <= 28.6)].min()) if (obj & (glat >= 28.0) & (glat <= 28.6)).any() else None}
            # sela ate o nucleo do sistema
            sela = None
            if sistema is not None:
                for L in LIMIARES:
                    if L < pp[ipp]:
                        continue
                    lb, _ = ndimage.label(np.nan_to_num(tb, nan=999) < L, structure=oito)
                    if lb[ipp] and (lb[sistema] == lb[ipp]).any():
                        sela = float(L); break
            e["sela_ate_sistema_K"] = sela
            e["sela_menos_min_local_K"] = None if sela is None else sela - float(pp[ipp])
        # linhagem: sobreposicao com o horario anterior
        if obj is not None and ant is not None:
            lab0, info0 = ant
            sob = np.bincount(lab0[obj], minlength=lab0.max() + 1); sob[0] = 0
            k0 = int(np.argmax(sob))
            e["antecessor"] = None if sob[k0] == 0 else {"rotulo": k0, "sobreposicao_km2": float(sob[k0] * 4.0), **info0.get(k0, {})}
        info = {}
        for k in range(1, n + 1):
            mk = lab == k
            if mk.sum() < 3:
                continue
            info[k] = {"area_km2": float(mk.sum() * 4.0), "tb_min": float(tb[mk].min()), "lat": float(glat[mk].mean()),
                       "lon": float(glon[mk].mean()), "tem_nucleo_213": bool((tb[mk] < T_NUC).any())}
        e["rotulo_sitio"] = int(ks)
        ant = (lab, info)
        reg.append(e)
        if t.strftime("%H%M") in ("2100", "2200", "2230", "2300", "2330", "0000", "0030", "0100"):
            mapas[t.strftime("%H:%M")] = tb
    # resfriamento em 10 min
    for a, b in zip(reg[:-1], reg[1:]):
        b["dtb_10min_sitio"] = b["tb_min_sitio"] - a["tb_min_sitio"]
    # linhagem do objeto do sitio as 23:30 (topo mais frio), para tras
    L = ["Origem do topo frio sobre o sitio (Himawari-9 B13/B07, 10 min, coordenadas aparentes; sitio aparente para topo a %.0f km: %.3f N, %.3f E)" % (H_SITIO, sit[0], sit[1]),
         "objeto = Tb13 < %.0f K (conectividade 8); sistema = maior objeto < %.0f K a ate 400 km; sela = menor limiar que liga o minimo ate 30 km do sitio ao nucleo do sistema" % (T_OBJ, T_NUC),
         "",
         "UTC    Tbmin10 Tbmed10 dTb10 B07-B13 | Tbmin30  | obj: area_km2 Tbmin  <213 contem_sist lon_oeste | sela  sela-min | sistema: area  dist_km",
         ]
    for e in reg:
        o = e.get("objeto_sitio"); s = e.get("sistema")
        L.append("%s %6.1f %7.1f %5s %7s | %6.1f   | %s | %5s %6s | %s" % (
            e["utc"][11:16], e["tb_min_sitio"], e["tb_med_sitio"],
            "%+.1f" % e["dtb_10min_sitio"] if "dtb_10min_sitio" in e else "", "%.1f" % e["btd_07_13_sitio"] if e["btd_07_13_sitio"] is not None else "-",
            e["tb_min_30km"],
            ("%9.0f %6.1f %5s %5s %8s" % (o["area_km2"], o["tb_min"], "sim" if o["tem_nucleo_213"] else "nao", "sim" if o["contem_sistema"] else "nao",
                                          "%.2f" % o["lon_oeste_faixa_28_28p6"] if o["lon_oeste_faixa_28_28p6"] is not None else "-")) if o else "%37s" % "(sitio fora de nuvem < 235 K)",
            "%.0f" % e["sela_ate_sistema_K"] if e.get("sela_ate_sistema_K") is not None else "-",
            "%.0f" % e["sela_menos_min_local_K"] if e.get("sela_menos_min_local_K") is not None else "-",
            "%7.0f %6.0f" % (s["area_km2"], s["dist_sitio_km"]) if s else "-"))
    L += ["", "Linhagem do objeto do sitio (para tras pela maior sobreposicao, Tb13 < %.0f K):" % T_OBJ]
    for e in reg:
        a = e.get("antecessor")
        if e.get("objeto_sitio") and a:
            L.append("  %s <- area %7.0f km2, Tbmin %.1f, centro %.2f N %.2f E, nucleo<213 %s (sobreposicao %.0f km2)" % (
                e["utc"][11:16], a.get("area_km2", 0), a.get("tb_min", 0), a.get("lat", 0), a.get("lon", 0), a.get("tem_nucleo_213"), a["sobreposicao_km2"]))
        elif e.get("objeto_sitio"):
            L.append("  %s <- (sem antecessor: o objeto aparece neste horario)" % e["utc"][11:16])
    txt = "\n".join(L) + "\n"
    open(os.path.join(SAIDA, "origem_topo_frio.txt"), "w", encoding="utf-8").write(txt)
    json.dump({"sitio_aparente": sit, "registros": reg}, open(os.path.join(SAIDA, "origem_topo_frio.json"), "w", encoding="utf-8"), indent=1)
    print(txt)
    figura(mapas, glat, glon, sit, reg)


def figura(mapas, glat, glon, sit, reg):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(3, 4, figsize=(17, 11), gridspec_kw={"height_ratios": [1, 1, 0.8]})
    for a, (h, tb) in zip(ax[:2].ravel(), mapas.items()):
        im = a.pcolormesh(glon, glat, tb, cmap="Greys", vmin=200, vmax=290, shading="auto")
        a.contour(glon, glat, tb, levels=[T_NUC], colors="red", linewidths=0.8)
        a.contour(glon, glat, tb, levels=[T_OBJ], colors="deepskyblue", linewidths=0.8)
        a.plot(sit[1], sit[0], "y*", ms=11, mec="k")
        a.set_title(h + " UTC"); a.set_aspect(1 / np.cos(np.radians(28.3)))
    fig.colorbar(im, ax=ax[:2].ravel().tolist(), shrink=0.6, label="Tb13 (K)")
    # horas desde 25/08 00 UTC (eixo de datas do matplotlib derruba o processo nesta instalacao do Windows)
    t = [(datetime.strptime(e["utc"], "%Y-%m-%dT%H:%MZ") - datetime(2026, 8, 25)).total_seconds() / 3600 for e in reg]
    g = fig.add_subplot(3, 1, 3)
    for a in ax[2]:
        a.remove()
    g.plot(t, [e["tb_min_sitio"] for e in reg], "k-", label="Tb13 min ate 10 km do sitio")
    g.plot(t, [e.get("sela_ate_sistema_K") or np.nan for e in reg], "r.", label="sela ate o nucleo do sistema")
    for v, cor in ((T_OBJ, "deepskyblue"), (T_NUC, "red")):    # axhline tambem derruba o processo nesta instalacao
        g.plot([t[0], t[-1]], [v, v], color=cor, lw=0.7)
    g.set_ylabel("K"); g.legend(loc="lower left"); g.grid(alpha=0.3)
    hs = np.arange(17, 28)
    g.set_xticks(hs); g.set_xticklabels(["%02d" % (h % 24) for h in hs]); g.set_xlabel("UTC (25-26/08)")
    g2 = g.twinx()
    g2.plot(t, [e["btd_07_13_sitio"] if e["btd_07_13_sitio"] is not None else np.nan for e in reg], "g--", label="B07 - B13 (sitio)")
    g2.set_ylabel("B07 - B13 (K)", color="g")
    fig.suptitle("Himawari-9 B13 - contorno azul 235 K, vermelho 213 K; estrela = sitio aparente (topo a %.0f km)" % H_SITIO)
    fig.savefig(os.path.join(SAIDA, "origem_topo_frio.png"), dpi=110, bbox_inches="tight")


if __name__ == "__main__":
    main()
