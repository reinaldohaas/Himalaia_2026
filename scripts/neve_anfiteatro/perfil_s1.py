# -*- coding: utf-8 -*-
"""
Perfil longitudinal da mudanca de retroespalhamento do Sentinel-1 (gamma0 VV, media 5 x 5) ao longo do talvegue,
do ponto de colapso (km 0) ao exutorio do anfiteatro (4.010 m) e 25 km vale abaixo (anfiteatro_glo30.py:
talvegue_completo). Para cada trecho de 250 m: fracao dos pixels a <= 250 m do talvegue com dVV > +3 dB no par de
12 dias que contem o colapso, em cada orbita, contra a media e o desvio dos pares sem evento da mesma orbita.
Onde o sinal comeca = onde o fluxo comeca a deixar marca na superficie (resolucao ~50 m apos o filtro).
Uso: python perfil_s1.py <dir_dados> <saida.png>
"""
import json
import os
import sys
from datetime import datetime

import numpy as np

COLAPSO_T = datetime(2026, 8, 26, 2, 52)
PASSO = 250.0
LIM = 3.0


def main(d, png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.ndimage import uniform_filter
    from pyproj import Transformer
    tal = [f for f in json.load(open(os.path.join(d, "corredor.geojson")))["features"] if f["properties"]["nome"] == "talvegue_completo"][0]
    xy = np.array(tal["geometry"]["coordinates"]); dist = np.array(tal["properties"]["dist_m"]); cota = np.array(tal["properties"]["cota_m"])
    km_exu = tal["properties"]["km_exutorio"]
    X, Y = Transformer.from_crs(4326, 32645, always_xy=True).transform(xy[:, 0], xy[:, 1])
    X = np.asarray(X); Y = np.asarray(Y)
    # pontos do talvegue a cada 25 m
    dd = np.arange(0, dist[-1], 25.0)
    px = np.interp(dd, dist, X); py = np.interp(dd, dist, Y); pz = np.interp(dd, dist, cota)
    z = np.load(os.path.join(d, "cubos_s1.npz"))
    orbs = {}
    for k in z.files:
        if k.endswith("__vv"):
            orb, dt = k.split("__")[:2]
            orbs.setdefault(orb, []).append((datetime.strptime(dt, "%Y-%m-%dT%H%M%S"), z[k].astype(np.float32), z[k[:-4] + "__T"]))
    bins = np.arange(0, dist[-1] + PASSO, PASSO)
    res = {"km": list((bins[:-1] + PASSO / 2) / 1000), "cota_m": [float(np.interp(b + PASSO / 2, dist, cota)) for b in bins[:-1]], "km_exutorio": km_exu, "orbitas": {}}
    for orb, l in sorted(orbs.items()):
        l.sort(key=lambda x: x[0])
        T = l[0][2]; shp = l[0][1].shape
        jj, ii = np.mgrid[0:shp[0], 0:shp[1]]
        gx = T[2] + T[0] * (ii + 0.5); gy = T[5] + T[4] * (jj + 0.5)
        # pixel -> trecho do talvegue mais proximo (se a <= 250 m)
        from scipy.spatial import cKDTree
        tr = cKDTree(np.c_[px, py])
        dmin, idx = tr.query(np.c_[gx.ravel(), gy.ravel()], distance_upper_bound=250.0)
        ok = np.isfinite(dmin)
        trecho = np.full(gx.size, -1); trecho[ok] = np.digitize(dd[idx[ok]], bins) - 1
        filt = []
        for t, db, _ in l:
            lin = np.where(np.isfinite(db), 10 ** (db / 10.0), 0.0); w = np.isfinite(db).astype(float)
            m = uniform_filter(lin, 5) / np.maximum(uniform_filter(w, 5), 1e-6)
            filt.append((t, np.where(w > 0, 10 * np.log10(np.maximum(m, 1e-6)), np.nan).ravel()))
        nb = len(bins) - 1
        ev, ref = None, []
        for (ta, a), (tb, b) in zip(filt[:-1], filt[1:]):
            dv = b - a; v = np.isfinite(dv) & (trecho >= 0)
            cnt = np.bincount(trecho[v], minlength=nb).astype(float)
            sob = np.bincount(trecho[v], weights=(dv[v] > LIM).astype(float), minlength=nb)
            med = np.bincount(trecho[v], weights=dv[v], minlength=nb)
            fr = np.where(cnt > 0, sob / np.maximum(cnt, 1), np.nan); mm = np.where(cnt > 0, med / np.maximum(cnt, 1), np.nan)
            if ta < COLAPSO_T < tb:
                ev = (str(ta)[:10], str(tb)[:10], fr, mm)
            else:
                ref.append(fr)
        ref = np.array(ref)
        rm = np.nanmean(ref, 0); rs = np.nanstd(ref, 0)
        res["orbitas"][orb] = {"par": ev[:2], "frac_sobe": [None if not np.isfinite(x) else round(float(x), 4) for x in ev[2]],
                               "dvv_medio_db": [None if not np.isfinite(x) else round(float(x), 2) for x in ev[3]],
                               "ref_media": [None if not np.isfinite(x) else round(float(x), 4) for x in rm],
                               "ref_dp": [None if not np.isfinite(x) else round(float(x), 4) for x in rs], "n_ref": int(len(ref))}
    # inicio do sinal: primeiro trecho (a partir do colapso) em que >= 2 orbitas passam de media + 3 dp e de 10 %
    km = np.array(res["km"]); acima = np.zeros(len(km))
    for o in res["orbitas"].values():
        f = np.array([np.nan if x is None else x for x in o["frac_sobe"]]); m = np.array([np.nan if x is None else x for x in o["ref_media"]]); s = np.array([np.nan if x is None else x for x in o["ref_dp"]])
        acima += np.nan_to_num((f > m + 3 * s) & (f > 0.10)).astype(float)
    sinal = acima >= 2
    res["trechos_com_sinal_km"] = [round(float(k), 3) for k in km[sinal]]
    res["inicio_sinal_km"] = round(float(km[sinal][0]), 3) if sinal.any() else None
    if sinal.any():
        res["inicio_sinal_cota_m"] = round(float(np.array(res["cota_m"])[sinal][0]))
    json.dump(res, open(os.path.join(d, "perfil_s1.json"), "w"), indent=1)
    print("exutorio no km %.2f; sinal (>= 2 orbitas > media + 3 dp e > 10 %%) comeca no km %s (cota %s m); trechos com sinal: %d de %d" % (
        km_exu, res["inicio_sinal_km"], res.get("inicio_sinal_cota_m"), sinal.sum(), len(km)))
    print("km com sinal:", res["trechos_com_sinal_km"][:60])
    fig, ax = plt.subplots(2, 1, figsize=(11, 6.5), sharex=True, gridspec_kw={"height_ratios": [3, 1.3]})
    cores = {"asc_85": "tab:blue", "des_121": "tab:orange", "des_19": "tab:green"}
    for orb, o in res["orbitas"].items():
        f = np.array([np.nan if x is None else x for x in o["frac_sobe"]]); m = np.array([np.nan if x is None else x for x in o["ref_media"]]); s = np.array([np.nan if x is None else x for x in o["ref_dp"]])
        ax[0].plot(km, 100 * f, "-", c=cores.get(orb), lw=1.4, label="%s  %s > %s (evento)" % (orb, o["par"][0][5:], o["par"][1][5:]))
        ax[0].fill_between(km, 100 * np.clip(m - s, 0, None), 100 * (m + 3 * s), color=cores.get(orb), alpha=0.12, lw=0)
    ax[0].axvline(km_exu, c="k", ls="--", lw=0.8); ax[0].text(km_exu, ax[0].get_ylim()[1] * 0.95, " exutório 4.010 m", fontsize=8, va="top")
    ax[0].axvline(0, c="r", lw=0.8); ax[0].text(0, ax[0].get_ylim()[1] * 0.85, " ponto de colapso", fontsize=8, va="top", color="r")
    for k in km[sinal]:
        ax[0].axvspan(k - PASSO / 2000, k + PASSO / 2000, color="red", alpha=0.08, lw=0)
    ax[0].set_ylabel("% da faixa (±250 m) com\nΔVV > +3 dB"); ax[0].legend(fontsize=8, loc="upper right")
    ax[0].set_title("Sentinel-1D RTC ao longo do talvegue: par de 12 dias com o colapso (linha) × pares sem evento (faixa: média−dp a média+3dp)", fontsize=9.5)
    ax[1].plot(km, res["cota_m"], c="k"); ax[1].set_ylabel("cota (m)"); ax[1].set_xlabel("distância ao longo do talvegue a partir do ponto de colapso (km)")
    ax[1].axvline(km_exu, c="k", ls="--", lw=0.8)
    fig.tight_layout(); fig.savefig(png, dpi=130)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
