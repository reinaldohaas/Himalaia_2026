# -*- coding: utf-8 -*-
"""
Caracterizacao do anfiteatro de erosao do Lhende Khola (a bacia de origem, acima do exutorio a 4.010 m):

* morfometria no Copernicus GLO-30: area, perimetro, comprimento maximo (do exutorio ao ponto mais distante),
  largura media, relevo, razao de relevo, indice de Melton (relevo/raiz da area; Melton 1965), razao de
  alongamento e circularidade, integral hipsometrica (Strahler 1952), distribuicao de declividades e de
  orientacoes, declividade e desnivel do talvegue do ponto USGS ao exutorio, parede (declividade > 45 graus)
  e fundo (< 15 graus);
* criterio morfometrico de Wilford et al. (2004) para bacias de fluxo de detritos: Melton > 0,53 e comprimento
  < 2,7 km;
* cobertura da superficie no Sentinel-2 L2A de 12/08/2026 (cena limpa; mascara espectral) e de 18/10/2026:
  neve/gelo (NDSI > 0,42), sem neve (rocha ou detrito) e nao observado, por faixa de cota e de declividade;
* geleira mapeada no OpenStreetMap dentro do anfiteatro.

Grava caracterizacao_anfiteatro.json e caracterizacao_anfiteatro.png.
Uso: python caracteriza_anfiteatro.py <dir_dados> <saida.png>
"""
import json
import os
import sys
import urllib.parse
import urllib.request

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

COTA_EXU = 4010.0


def dem():
    from shapely.geometry import box
    it = comum.stac_busca(comum.PC, ["cop-dem-glo-30"], [85.40, 28.18, 85.65, 28.38], "2000-01-01/2030-01-01")[0]
    href = comum.pc_assina(it["assets"]["data"]["href"])
    return comum.ler_janela(href, box(85.44, 28.22, 85.58, 28.34), folga_m=0)


def main(d, png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from shapely.geometry import shape
    from rasterio.features import shapes
    z, T, crs, nd = dem(); z = z.astype(float); ny, nx = z.shape
    lat = T.f + T.e * (np.arange(ny) + 0.5); lon = T.c + T.a * (np.arange(nx) + 0.5)
    dy = abs(T.e) * 111320.0; dxs = T.a * 111320.0 * np.cos(np.radians(lat))
    A = (dy * dxs)[:, None] * np.ones((1, nx))
    gy, gx = np.gradient(z)
    sy = gy / (-dy); sx = gx / dxs[:, None]                     # dz/dnorte, dz/dleste
    dec = np.degrees(np.arctan(np.hypot(sx, sy)))
    asp = (np.degrees(np.arctan2(-sx, -sy)) + 360) % 360        # direcao para onde a encosta desce (0 = norte)
    an = shape(json.load(open(os.path.join(d, "anfiteatro.geojson")))["features"][0]["geometry"])
    m = comum.mascara(an, z.shape, T, crs)
    res = {"anfiteatro": calc(m, z, A, dec, asp, lat, lon, T, d)}
    # talvegue do ponto USGS ao exutorio
    tal = [f for f in json.load(open(os.path.join(d, "corredor.geojson")))["features"] if f["properties"]["nome"] == "talvegue_completo"][0]
    dist = np.array(tal["properties"]["dist_m"]); cota = np.array(tal["properties"]["cota_m"])
    k = int(np.argmin(abs(dist - tal["properties"]["km_exutorio"] * 1000)))
    res["anfiteatro"]["talvegue_usgs_exutorio"] = {"comprimento_m": round(float(dist[k])), "desnivel_m": round(float(cota[0] - cota[k])),
                                                    "declividade_media_graus": round(float(np.degrees(np.arctan((cota[0] - cota[k]) / dist[k]))), 1),
                                                    "cota_inicio_m": round(float(cota[0])), "cota_exutorio_m": round(float(cota[k]))}
    # cobertura pelo Sentinel-2 (mascara espectral) em 12/08 e 18/10
    res["anfiteatro"]["cobertura"] = cobertura(d)
    # geleira do OSM
    res["anfiteatro"]["geleira_osm"] = geleira_osm(an)
    # criterio de Wilford et al. (2004)
    a = res["anfiteatro"]
    a["wilford2004"] = {"melton": a["melton"], "comprimento_km": a["comprimento_km"],
                        "classe": "fluxo de detritos" if (a["melton"] > 0.53 and a["comprimento_km"] < 2.7) else
                                  ("cheia com detritos" if a["melton"] > 0.30 else "cheia")}
    json.dump(res, open(os.path.join(d, "caracterizacao_anfiteatro.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1)[:4000])
    figura(png, z, m, dec, asp, A, lat, lon, T, res, tal)


def calc(m, z, A, dec, asp, lat, lon, T, d):
    from shapely.geometry import shape
    from rasterio.features import shapes
    import shapely
    area = float(A[m].sum()); zz = z[m]
    zmin, zmax, zmean = float(zz.min()), float(zz.max()), float(np.average(zz, weights=A[m]))
    g = shapely.unary_union([shape(s) for s, v in shapes(m.astype(np.uint8), mask=m, transform=T) if v == 1])
    # perimetro e comprimentos em metros (projecao local equiretangular)
    lat0 = float(np.mean(lat[m.any(1)]))
    from shapely.ops import transform as shtr
    gm = shtr(lambda x, y, zc=None: ((np.asarray(x) - 85.5) * 111320 * np.cos(np.radians(lat0)), (np.asarray(y) - 28.27) * 111320), g)
    per = float(gm.length)
    jj, ii = np.where(m)
    X = (lon[ii] - 85.5) * 111320 * np.cos(np.radians(lat0)); Y = (lat[jj] - 28.27) * 111320
    kex = np.argmin(z[jj, ii]); L = float(np.max(np.hypot(X - X[kex], Y - Y[kex])))
    relevo = zmax - zmin
    d_ = dec[m]; w = A[m]
    hist_dec = {"%d-%d" % (a, b): round(float(w[(d_ >= a) & (d_ < b)].sum() / area), 3) for a, b in ((0, 15), (15, 30), (30, 45), (45, 60), (60, 90))}
    o = asp[m]
    setores = {}
    for nome, c in (("N", 0), ("NE", 45), ("E", 90), ("SE", 135), ("S", 180), ("SW", 225), ("W", 270), ("NW", 315)):
        dd = (o - c + 180) % 360 - 180
        setores[nome] = round(float(w[np.abs(dd) < 22.5].sum() / area), 3)
    faixas = {}
    for z0 in range(4000, 7300, 500):
        s = (zz >= z0) & (zz < z0 + 500)
        if s.any():
            faixas["%d-%d" % (z0, z0 + 500)] = {"area_ha": round(float(w[s].sum() / 1e4), 1), "declividade_media": round(float(np.average(d_[s], weights=w[s])), 1)}
    return {"area_km2": round(area / 1e6, 3), "perimetro_km": round(per / 1000, 2), "comprimento_km": round(L / 1000, 2),
            "largura_media_km": round(area / L / 1000, 2), "cota_min_m": round(zmin), "cota_max_m": round(zmax), "cota_media_m": round(zmean),
            "relevo_m": round(relevo), "razao_de_relevo": round(relevo / L, 2), "melton": round((relevo / 1000) / np.sqrt(area / 1e6), 2),
            "razao_alongamento": round(2 * np.sqrt(area / np.pi) / L, 2), "circularidade": round(4 * np.pi * area / per ** 2, 2),
            "integral_hipsometrica": round((zmean - zmin) / relevo, 3), "declividade_media_graus": round(float(np.average(d_, weights=w)), 1),
            "declividade_p90_graus": round(float(np.percentile(d_, 90)), 1), "frac_declividade": hist_dec,
            "parede_gt45_ha": round(float(w[d_ > 45].sum() / 1e4), 1), "fundo_lt15_ha": round(float(w[d_ < 15].sum() / 1e4), 1),
            "frac_orientacao": setores, "faixas_500m": faixas}


def cobertura(d):
    import linha_de_neve as L
    z = np.load(os.path.join(d, "mascaras_s2es.npz"))
    ser = {r["id"]: r for r in json.load(open(os.path.join(d, "serie_s2es.json"))) if "erro" not in r}
    anf = z["regiao__anfiteatro"]
    out = {}
    zz = None
    for alvo in ("2026-08-12", "2026-10-18"):
        ks = [k[:-6] for k in z.files if k.endswith("__ndsi") and ser.get(k[:-6], {}).get("datetime", "")[:10] == alvo]
        if not ks:
            continue
        k = ks[0]; nd = z[k + "__ndsi"].astype(float); T = z[k + "__T"]
        if zz is None:
            zz = L.dem_na_grade(T, anf.shape)
            gy, gx = np.gradient(zz); dec = np.degrees(np.arctan(np.hypot(gx / 20.0, gy / 20.0)))
        ok = np.isfinite(nd) & anf
        r = {"cena": k, "frac_observada": round(float(ok.sum() / anf.sum()), 3),
             "neve_gelo_ha": round(float((ok & (nd > 0.42)).sum() * 0.04), 1), "sem_neve_ha": round(float((ok & (nd <= 0.42)).sum() * 0.04), 1),
             "nao_observado_ha": round(float((anf & ~ok).sum() * 0.04), 1), "por_cota": {}, "por_declividade": {}}
        for z0 in range(4000, 7300, 500):
            s = anf & (zz >= z0) & (zz < z0 + 500)
            if s.sum():
                o = s & ok
                r["por_cota"]["%d-%d" % (z0, z0 + 500)] = {"obs": round(float(o.sum() / s.sum()), 2),
                                                          "neve_frac_obs": round(float((o & (nd > 0.42)).sum() / max(o.sum(), 1)), 2)}
        for a, b in ((0, 15), (15, 30), (30, 45), (45, 60), (60, 90)):
            s = anf & (dec >= a) & (dec < b)
            if s.sum():
                o = s & ok
                r["por_declividade"]["%d-%d" % (a, b)] = {"area_ha": round(float(s.sum() * 0.04), 1), "obs": round(float(o.sum() / s.sum()), 2),
                                                          "neve_frac_obs": round(float((o & (nd > 0.42)).sum() / max(o.sum(), 1)), 2)}
        out[alvo] = r
    return out


def geleira_osm(an):
    from shapely.geometry import Polygon
    q = '[out:json][timeout:60];way["natural"="glacier"](28.24,85.48,28.30,85.56);out geom;'
    try:
        r = urllib.request.Request("https://overpass-api.de/api/interpreter", data=urllib.parse.urlencode({"data": q}).encode(),
                                   headers={"User-Agent": "himalaia-auditoria/1.0"})
        el = json.load(urllib.request.urlopen(r, timeout=90))["elements"]
    except Exception as e:
        return {"erro": repr(e)[:200]}
    out = []
    for e in el:
        pts = [(p["lon"], p["lat"]) for p in e.get("geometry", [])]
        if len(pts) < 4:
            continue
        g = Polygon(pts).buffer(0)
        inter = g.intersection(an)
        if inter.is_empty:
            continue
        c = np.cos(np.radians(28.27)) * 111320 * 111320
        out.append({"osm": "way/%d" % e["id"], "nome": e.get("tags", {}).get("name"), "area_total_ha": round(g.area * c / 1e4, 1),
                    "area_no_anfiteatro_ha": round(inter.area * c / 1e4, 1)})
    return out


def figura(png, z, m, dec, asp, A, lat, lon, T, res, tal):
    import matplotlib.pyplot as plt
    a = res["anfiteatro"]
    jj, ii = np.where(m)
    j0, j1 = max(jj.min() - 15, 0), jj.max() + 15; i0, i1 = max(ii.min() - 15, 0), ii.max() + 15
    fig = plt.figure(figsize=(11, 7.6))
    ax = fig.add_axes([0.04, 0.08, 0.42, 0.86])
    ls = np.clip(np.cos(np.radians(dec)) * 0.5 + 0.5 * np.cos(np.radians(asp - 315)) * np.sin(np.radians(dec)), 0, 1)
    ext = (lon[i0], lon[i1], lat[j1], lat[j0])
    ax.imshow(ls[j0:j1, i0:i1], cmap="gray", extent=ext, vmin=0, vmax=1)
    h = ax.imshow(np.where(m, dec, np.nan)[j0:j1, i0:i1], cmap="magma_r", extent=ext, vmin=0, vmax=70, alpha=0.75)
    cs = ax.contour(lon[i0:i1], lat[j0:j1], z[j0:j1, i0:i1], levels=range(4000, 7300, 250), colors="k", linewidths=0.3)
    ax.clabel(cs, levels=range(4000, 7300, 1000), fmt="%d", fontsize=7)
    ax.contour(lon[i0:i1], lat[j0:j1], m[j0:j1, i0:i1].astype(float), levels=[0.5], colors="cyan", linewidths=1.4)
    xy = np.array(tal["geometry"]["coordinates"]); k = int(np.argmin(abs(np.array(tal["properties"]["dist_m"]) - tal["properties"]["km_exutorio"] * 1000)))
    ax.plot(xy[:k + 1, 0], xy[:k + 1, 1], "-", c="deepskyblue", lw=1.5)
    ax.plot(*comum.COLAPSO, "x", c="lime", ms=10, mew=2.5); ax.plot(xy[k, 0], xy[k, 1], "o", c="yellow", mec="k", ms=7)
    ax.set_aspect(1 / np.cos(np.radians(28.27))); ax.tick_params(labelsize=7.5)
    cb = fig.colorbar(h, ax=ax, shrink=0.6, pad=0.02); cb.set_label("declividade (graus)", fontsize=8); cb.ax.tick_params(labelsize=7.5)
    ax.text(0.02, 0.98, "a", transform=ax.transAxes, fontweight="bold", va="top", fontsize=12, color="w")
    # hipsometria
    ax2 = fig.add_axes([0.56, 0.58, 0.18, 0.36])
    zz = np.sort(z[m])[::-1]; w = np.ones_like(zz)
    ax2.plot(np.cumsum(w) / w.sum(), (zz - zz.min()) / (zz.max() - zz.min()), c="k")
    ax2.plot([0, 1], [1, 0], ":", c="0.5")
    ax2.set_xlabel("área relativa a/A", fontsize=8); ax2.set_ylabel("altura relativa h/H", fontsize=8); ax2.tick_params(labelsize=7.5)
    ax2.text(0.55, 0.85, "HI = %.2f" % a["integral_hipsometrica"], transform=ax2.transAxes, fontsize=8)
    ax2.text(0.02, 0.98, "b", transform=ax2.transAxes, fontweight="bold", va="top", fontsize=12)
    # declividades
    ax3 = fig.add_axes([0.80, 0.58, 0.18, 0.36])
    d_ = dec[m]; ax3.hist(d_, bins=np.arange(0, 80, 5), weights=A[m] / 1e4, color="0.4")
    ax3.axvline(45, c="r", lw=0.8, ls="--")
    ax3.set_xlabel("declividade (graus)", fontsize=8); ax3.set_ylabel("área (ha)", fontsize=8); ax3.tick_params(labelsize=7.5)
    ax3.text(0.02, 0.98, "c", transform=ax3.transAxes, fontweight="bold", va="top", fontsize=12)
    # orientacao (rosa)
    ax4 = fig.add_axes([0.55, 0.08, 0.2, 0.36], projection="polar")
    o = asp[m]; hh, be = np.histogram(o, bins=np.arange(0, 361, 22.5), weights=A[m] / 1e4)
    ax4.bar(np.radians(be[:-1] + 11.25), hh, width=np.radians(22.5), color="0.45", edgecolor="w")
    ax4.set_theta_zero_location("N"); ax4.set_theta_direction(-1); ax4.tick_params(labelsize=7)
    ax4.set_thetagrids(range(0, 360, 45), ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], fontsize=7.5)
    ax4.set_title("orientação das encostas (ha)", fontsize=8, pad=12)
    ax4.text(-0.15, 1.08, "d", transform=ax4.transAxes, fontweight="bold", fontsize=12)
    # cobertura por cota em 12/08
    ax5 = fig.add_axes([0.84, 0.08, 0.14, 0.32])
    cob = a["cobertura"].get("2026-08-12", {}).get("por_cota", {})
    ks = list(cob); y = np.arange(len(ks))
    obs = np.array([cob[k]["obs"] for k in ks]); nf = np.array([cob[k]["neve_frac_obs"] for k in ks])
    ax5.barh(y, obs * nf, color="tab:cyan", label="neve/gelo"); ax5.barh(y, obs * (1 - nf), left=obs * nf, color="tab:brown", label="sem neve")
    ax5.barh(y, 1 - obs, left=obs, color="0.85", label="não observado")
    ax5.set_yticks(y); ax5.set_yticklabels([k.replace("-", "–") for k in ks], fontsize=7); ax5.set_xlim(0, 1); ax5.tick_params(labelsize=7.5)
    ax5.set_xlabel("fração da faixa, 12/08", fontsize=8); ax5.legend(fontsize=6.5, loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=1, frameon=False)
    ax5.text(-0.55, 1.02, "e", transform=ax5.transAxes, fontweight="bold", fontsize=12)
    __import__("figlang").prepara(fig); fig.savefig(__import__("figlang").caminho(png), dpi=200)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
