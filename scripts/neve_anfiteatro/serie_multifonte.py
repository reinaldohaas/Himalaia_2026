# -*- coding: utf-8 -*-
"""
Serie multifonte de neve/gelo sobre o anfiteatro do Lhende Khola, 01/07 a 18/10/2026, para estimar o erro da
area de neve/gelo (e da sua variacao em torno do colapso de 26/08 02:52 UTC) pela dispersao entre fontes,
limiares e mascaras de nuvem, contra dois controles que nao participaram do evento.

Fontes (todas por STAC, sem credencial; so a janela do anfiteatro + controles e lida):
  s2es   Sentinel-2 L2A, Earth Search (Element 84)  green/swir16/scl; offset BOA ja aplicado pelo ES (conferido)
  s2l1c  Sentinel-2 L1C, Earth Search: topo da atmosfera (sem correcao atmosferica), nuvem pela SCL do L2A
  s2pc   Sentinel-2 L2A, Planetary Computer          B03/B11/SCL;   offset -1000 DN a partir da baseline 04.00
  ls     Landsat 8/9 C2 L2, Planetary Computer        green/swir16/qa_pixel; SR = DN*2,75e-5 - 0,2
  hlss   HLS S30 v2 (Sentinel-2, correcao LaSRC)      B03/B11/Fmask
  hlsl   HLS L30 v2 (Landsat)                         B03/B06/Fmask
  modis  MOD10A1/MYD10A1 v6.1 NDSI_Snow_Cover, 500 m (diario; 0-100 = NDSI*100, >100 = sinalizadores)
  s1     Sentinel-1 RTC (gamma0 VV/VH, 10 m): independente de nuvem; mudanca de retroespalhamento

Para cada cena e regiao (anfiteatro, alto_fora, cume_fora) grava: fracao observavel, area de neve observada e
fracao de neve nos pixels observados para NDSI > 0,30 / 0,42 / 0,50 (e verde > 0,11), duas mascaras de nuvem
(estrita e branda), uma terceira (espectral = estrita + teste verde > 0,35 e SWIR > 0,25 sem NDSI de neve,
para a nuvem sobre neve que a SCL nao marca) e a mediana do NDSI. Grava tambem o NDSI da janela inteira (nan onde nuvem estrita ou verde <= 0,11) por cena em .npz,
com as mascaras das regioes, para as diferencas por pixel em comum.

Uso: python serie_multifonte.py <fonte> <dir_dados>   (dir_dados com anfiteatro.geojson e controles.geojson)
"""
import json
import os
import sys
import traceback

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

DATAS = "2026-07-01T00:00:00Z/2026-10-18T23:59:59Z"
LIMIARES = (0.30, 0.42, 0.50)
VERDE_MIN = 0.11


def regioes(d, corredor=False):
    from shapely.geometry import shape
    an = shape(json.load(open(os.path.join(d, "anfiteatro.geojson")))["features"][0]["geometry"])
    c = {f["properties"]["nome"]: shape(f["geometry"]) for f in json.load(open(os.path.join(d, "controles.geojson")))["features"]}
    r = {"anfiteatro": an, "alto_fora": c["alto_fora_anfiteatro"].difference(an),
         "cume_fora": c["cume_langtang_lirung"].difference(an.buffer(0.0005))}
    if corredor:      # percurso a jusante do exutorio (anfiteatro_glo30.py), em trechos de 5 km
        for f in json.load(open(os.path.join(d, "corredor.geojson")))["features"]:
            if f["properties"]["nome"].startswith("corredor_"):
                r[f["properties"]["nome"]] = shape(f["geometry"]).difference(an)
    return r


def ler_bandas(hrefs, ref, geom_ll, folga_m=300.0, metodos=None):
    """le as bandas na grade da banda `ref` (janela que envolve geom_ll); as outras sao reamostradas para ela
    (media para refletancia, vizinho para QA). Bordas da janela alinhadas a grade ref."""
    import rasterio
    from rasterio.windows import from_bounds
    from rasterio.enums import Resampling
    from pyproj import Transformer
    metodos = metodos or {}
    env = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY="5", GDAL_HTTP_RETRY_DELAY="3",
               CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif,.TIF,.tiff,.jp2", VSI_CACHE="TRUE", GDAL_HTTP_MULTIRANGE="YES", GDAL_NUM_THREADS="4")
    out = {}
    with rasterio.Env(**env):
        with rasterio.open(hrefs[ref]) as s:
            tr = Transformer.from_crs(4326, s.crs, always_xy=True)
            x0, y0, x1, y1 = geom_ll.bounds
            xs, ys = tr.transform([x0, x1, x0, x1], [y0, y0, y1, y1])
            f = folga_m / 111000.0 if s.crs.is_geographic else folga_m
            w = from_bounds(min(xs) - f, min(ys) - f, max(xs) + f, max(ys) + f, s.transform).round_offsets().round_lengths()
            T = s.window_transform(w); crs = s.crs; shp = (int(w.height), int(w.width))
            out[ref] = s.read(1, window=w, boundless=True, fill_value=s.nodata if s.nodata is not None else 0)
            nd = {ref: s.nodata}
            bnd = rasterio.windows.bounds(w, s.transform)
        for k, h in hrefs.items():
            if k == ref:
                continue
            with rasterio.open(h) as s:
                if s.crs != crs:
                    raise RuntimeError("CRS diferente entre bandas: %s" % k)
                w2 = from_bounds(*bnd, s.transform)
                out[k] = s.read(1, window=w2, out_shape=shp, boundless=True, fill_value=s.nodata if s.nodata is not None else 0,
                                resampling=getattr(Resampling, metodos.get(k, "average")))
                nd[k] = s.nodata
    return out, T, crs, nd


def area_px(T, crs, shp):
    if crs.is_geographic:
        lat = T.f + T.e * (np.arange(shp[0]) + 0.5)
        return (abs(T.e) * 111320.0 * T.a * 111320.0 * np.cos(np.radians(lat)))[:, None] * np.ones((1, shp[1]))
    return np.full(shp, abs(T.a * T.e))


def metricas(verde, swir, inval_estrita, inval_branda, masks, A, extra=None, inval_esp=None):
    """verde/swir em refletancia; devolve dict por regiao"""
    with np.errstate(invalid="ignore", divide="ignore"):
        ndsi = (verde - swir) / (verde + swir)
    fis = np.isfinite(ndsi)
    r = {}
    for nome, m in masks.items():
        tot = A[m].sum()
        d = {"area_total_ha": round(float(tot / 1e4), 2)}
        for rot, inv in (("estrita", inval_estrita), ("branda", inval_branda)) + ((("espectral", inval_esp),) if inval_esp is not None else ()):
            ok = m & ~inv & fis
            ao = A[ok].sum()
            e = {"frac_obs": round(float(ao / tot), 4) if tot else None,
                 "ndsi_mediana": round(float(np.median(ndsi[ok])), 3) if ok.any() else None,
                 "frac_ndsi_gt1": round(float((ndsi[ok] > 1.0).mean()), 4) if ok.any() else None,
                 "frac_swir_neg": round(float((swir[ok] < 0).mean()), 4) if ok.any() else None}
            for t in LIMIARES:
                nv = ok & (ndsi > t) & (verde > VERDE_MIN)
                e["neve_ha_%02d" % int(round(t * 100))] = round(float(A[nv].sum() / 1e4), 2)
                e["frac_neve_%02d" % int(round(t * 100))] = round(float(A[nv].sum() / ao), 4) if ao else None
            d[rot] = e
        if extra:
            d.update(extra(m))
        r[nome] = d
    return r, ndsi


# ---------------------------------------------------------------- leitores por fonte
def it_s2es(geom):
    its = comum.stac_busca(comum.ES, ["sentinel-2-l2a"], list(geom.bounds), DATAS)
    return sorted(its, key=lambda i: i["properties"]["datetime"])


def cena_s2es(it, geom):
    a = it["assets"]
    if not it["properties"].get("earthsearch:boa_offset_applied", False) and float(it["properties"].get("s2:processing_baseline", "0")) >= 4:
        off = -0.1
    else:
        off = 0.0
    b, T, crs, nd = ler_bandas({"swir": a["swir16"]["href"], "verde": a["green"]["href"], "scl": a["scl"]["href"]}, "swir", geom,
                               metodos={"scl": "nearest"})
    return b["verde"] * 1e-4 + off, b["swir"] * 1e-4 + off, b["scl"], T, crs, {"offset": off, "baseline": it["properties"].get("s2:processing_baseline"),
                                                                          "boa_offset_applied": it["properties"].get("earthsearch:boa_offset_applied")}


def it_s2pc(geom):
    its = comum.stac_busca(comum.PC, ["sentinel-2-l2a"], list(geom.bounds), DATAS)
    return sorted(its, key=lambda i: i["properties"]["datetime"])


def cena_s2pc(it, geom):
    a = it["assets"]
    bl = float(it["properties"].get("s2:processing_baseline", "0"))
    off = -0.1 if bl >= 4 else 0.0
    b, T, crs, nd = ler_bandas({"swir": comum.pc_assina(a["B11"]["href"]), "verde": comum.pc_assina(a["B03"]["href"]),
                                "scl": comum.pc_assina(a["SCL"]["href"])}, "swir", geom, metodos={"scl": "nearest"})
    return b["verde"] * 1e-4 + off, b["swir"] * 1e-4 + off, b["scl"], T, crs, {"offset": off, "baseline": it["properties"].get("s2:processing_baseline")}


def it_s2l1c(geom):
    its = comum.stac_busca(comum.ES, ["sentinel-2-l1c"], list(geom.bounds), DATAS)
    return sorted(its, key=lambda i: i["properties"]["datetime"])


_SCL = {}


def cena_s2l1c(it, geom):
    """topo da atmosfera (sem correcao atmosferica); a mascara de nuvem e a SCL do L2A do mesmo granulo (ES)"""
    a = it["assets"]
    off = a["green"].get("raster:bands", [{}])[0].get("offset", 0.0)
    if not _SCL:
        for i in it_s2es(geom):
            _SCL[i["id"].replace("_L2A", "")] = i["assets"]["scl"]["href"]
    scl = _SCL.get(it["id"].replace("_L1C", ""))
    if scl is None:
        raise RuntimeError("sem L2A correspondente para a SCL")
    # os JP2 do ES ficam num bucket S3 que cobra do leitor (exige credencial AWS): le-se o mesmo produto no espelho publico do Google
    import urllib.request
    pu = it["properties"]["s2:product_uri"]
    u = "https://storage.googleapis.com/storage/v1/b/gcp-public-data-sentinel-2/o?prefix=tiles/45/R/UM/%s/GRANULE/&fields=items(name)" % pu
    nomes = [x["name"] for x in json.load(urllib.request.urlopen(u, timeout=60)).get("items", []) if "/IMG_DATA/" in x["name"]]
    g = lambda bd: "/vsicurl/https://storage.googleapis.com/gcp-public-data-sentinel-2/" + [n for n in nomes if n.endswith("_%s.jp2" % bd)][0]
    b, T, crs, nd = ler_bandas({"swir": g("B11"), "verde": g("B03"), "scl": scl}, "swir", geom, metodos={"scl": "nearest"})
    return b["verde"] * 1e-4 + off, b["swir"] * 1e-4 + off, b["scl"], T, crs, {"offset": off, "baseline": it["properties"].get("s2:processing_baseline"), "produto": pu}


def inval_scl(scl, verde):
    nd = (scl == 0) | (verde <= -0.09)
    estrita = nd | np.isin(scl, [1, 3, 7, 8, 9, 10])          # saturado, sombra de nuvem, nao classificado, nuvem media/alta, cirro
    branda = nd | np.isin(scl, [1, 8, 9])                     # so nuvem media/alta e saturado
    return estrita, branda


def it_ls(geom):
    its = comum.stac_busca(comum.PC, ["landsat-c2-l2"], list(geom.bounds), DATAS, consulta={"platform": {"in": ["landsat-8", "landsat-9"]}})
    return sorted(its, key=lambda i: i["properties"]["datetime"])


def cena_ls(it, geom):
    a = it["assets"]
    b, T, crs, nd = ler_bandas({"swir": comum.pc_assina(a["swir16"]["href"]), "verde": comum.pc_assina(a["green"]["href"]),
                                "qa": comum.pc_assina(a["qa_pixel"]["href"])}, "swir", geom, metodos={"qa": "nearest"})
    q = b["qa"].astype(np.int64)
    v = np.where(b["verde"] == 0, np.nan, b["verde"] * 2.75e-5 - 0.2); s = np.where(b["swir"] == 0, np.nan, b["swir"] * 2.75e-5 - 0.2)
    return v, s, q, T, crs, {"plataforma": it["properties"].get("platform"), "wrs": "%s/%s" % (it["properties"].get("landsat:wrs_path"), it["properties"].get("landsat:wrs_row"))}


def inval_qa_ls(q, verde):
    bit = lambda n: (q >> n) & 1 == 1
    nd = bit(0) | ~np.isfinite(verde)
    estrita = nd | bit(1) | bit(2) | bit(3) | bit(4)          # nuvem dilatada, cirro, nuvem, sombra
    branda = nd | bit(3)                                      # so nuvem
    return estrita, branda


def it_hls(col):
    def f(geom):
        its = comum.stac_busca(comum.PC, [col], list(geom.bounds), DATAS)
        return sorted(its, key=lambda i: i["properties"]["datetime"])
    return f


def cena_hls(sw):
    def f(it, geom):
        a = it["assets"]
        b, T, crs, nd = ler_bandas({"swir": comum.pc_assina(a[sw]["href"]), "verde": comum.pc_assina(a["B03"]["href"]),
                                    "fm": comum.pc_assina(a["Fmask"]["href"])}, "swir", geom, metodos={"fm": "nearest"})
        v = np.where(b["verde"] == -9999, np.nan, b["verde"] * 1e-4); s = np.where(b["swir"] == -9999, np.nan, b["swir"] * 1e-4)
        return v, s, b["fm"].astype(np.int64), T, crs, {}
    return f


def inval_fmask(q, verde):
    bit = lambda n: (q >> n) & 1 == 1
    nd = (q == 255) | ~np.isfinite(verde)
    estrita = nd | bit(1) | bit(2) | bit(3)                   # nuvem, adjacente, sombra
    branda = nd | bit(1)
    return estrita, branda


# ---------------------------------------------------------------- execucao
def roda_optico(fonte, busca, cena, inval, dados, saida):
    regs = regioes(dados); from shapely.ops import unary_union
    geom = unary_union(list(regs.values())).envelope
    its = busca(geom); print(fonte, len(its), "cenas", flush=True)
    res, masks_salvas = [], {}
    for it in its:
        try:
            verde, swir, qa, T, crs, meta = cena(it, geom)
            ie, ib = inval(qa, verde)
            with np.errstate(invalid="ignore", divide="ignore"):
                nd0 = (verde - swir) / (verde + swir)
            # teste espectral de nuvem: claro no verde E no SWIR e sem assinatura de neve (a SCL deixa passar nuvem sobre neve)
            ies = ie | ((verde > 0.35) & (swir > 0.25) & ~(nd0 > 0.42))
            shp = verde.shape; A = area_px(T, crs, shp)
            masks = {k: comum.mascara(g, shp, T, crs) for k, g in regs.items()}
            r, ndsi = metricas(verde, swir, ie, ib, masks, A, inval_esp=ies)
            rec = {"fonte": fonte, "id": it["id"], "datetime": it["properties"]["datetime"],
                   "nuvem_cena_pct": it["properties"].get("eo:cloud_cover"), **meta, "regioes": r}
            res.append(rec)
            an = r["anfiteatro"]["estrita"]
            print("%s %s obs %.2f neve42 %.1f ha ndsi_med %s (alto_fora obs %.2f fneve %.3f)" % (
                fonte, it["properties"]["datetime"][:16], an["frac_obs"], an["neve_ha_42"], an["ndsi_mediana"],
                r["alto_fora"]["estrita"]["frac_obs"], r["alto_fora"]["estrita"]["frac_neve_42"] or -1), flush=True)
            if an["frac_obs"] and an["frac_obs"] > 0.05:
                # janela inteira, para as diferencas por pixel em comum (anfiteatro e controles)
                k = it["id"]
                masks_salvas[k + "__ndsi"] = np.where(ies | (verde <= VERDE_MIN), np.nan, ndsi).astype(np.float16)      # mascara espectral
                masks_salvas[k + "__ndsiE"] = np.where(ie | (verde <= VERDE_MIN), np.nan, ndsi).astype(np.float16)     # so SCL estrita
                masks_salvas[k + "__T"] = np.array([T.a, T.b, T.c, T.d, T.e, T.f])
                for nome, mm in masks.items():
                    masks_salvas.setdefault("regiao__" + nome, mm)
        except Exception as e:
            print("FALHA", fonte, it["id"], repr(e)[:200], flush=True)
            res.append({"fonte": fonte, "id": it["id"], "datetime": it["properties"]["datetime"], "erro": repr(e)[:300]})
        json.dump(res, open(os.path.join(saida, "serie_%s.json" % fonte), "w"), indent=0)
    np.savez_compressed(os.path.join(saida, "mascaras_%s.npz" % fonte), **masks_salvas)


def roda_modis(dados, saida):
    regs = regioes(dados); from shapely.ops import unary_union
    geom = unary_union(list(regs.values())).envelope
    its = sorted(comum.stac_busca(comum.PC, ["modis-10A1-061"], list(geom.bounds), DATAS), key=lambda i: i["properties"]["datetime"])
    print("modis", len(its), "granulos", flush=True)
    res = []
    for it in its:
        try:
            b, T, crs, nd = ler_bandas({"n": comum.pc_assina(it["assets"]["NDSI_Snow_Cover"]["href"])}, "n", geom, folga_m=1000)
            n = b["n"].astype(float); shp = n.shape; A = area_px(T, crs, shp)
            r = {}
            for k, g in regs.items():
                # 500 m: fracao de cobertura de cada pixel pelo poligono (supersamplagem 10x10) em vez de centro do pixel
                from rasterio.transform import Affine
                T10 = T * Affine.scale(0.1)
                m10 = comum.mascara(g, (shp[0] * 10, shp[1] * 10), T10, crs)
                fr = m10.reshape(shp[0], 10, shp[1], 10).mean(axis=(1, 3))
                tot = (fr * A).sum()
                val = (n <= 100); ok = fr * val
                ao = (ok * A).sum()
                d = {"area_total_ha": round(float(tot / 1e4), 1), "n_pixels_tocados": int((fr > 0).sum()),
                     "frac_obs": round(float(ao / tot), 3) if tot else None,
                     "frac_nuvem": round(float((fr * (n == 250) * A).sum() / tot), 3) if tot else None,
                     "frac_noite_ou_sem_decisao": round(float((fr * np.isin(n, [201, 211]) * A).sum() / tot), 3) if tot else None}
                for t in LIMIARES:
                    sn = ok * (n > t * 100)
                    d["frac_neve_%02d" % int(round(t * 100))] = round(float((sn * A).sum() / ao), 3) if ao else None
                    d["neve_ha_%02d" % int(round(t * 100))] = round(float((sn * A).sum() / 1e4), 1)
                d["ndsi_medio_obs"] = round(float((ok * A * n).sum() / ao / 100), 3) if ao else None
                r[k] = d
            rec = {"fonte": "modis", "id": it["id"], "datetime": it["properties"]["datetime"], "plataforma": it["properties"].get("platform"), "regioes": r}
            res.append(rec)
            print("modis %s %s obs %.2f fneve42 %s" % (it["id"][:7], it["properties"]["datetime"][:10], r["anfiteatro"]["frac_obs"] or 0, r["anfiteatro"]["frac_neve_42"]), flush=True)
        except Exception as e:
            print("FALHA modis", it["id"], repr(e)[:200], flush=True)
            res.append({"fonte": "modis", "id": it["id"], "datetime": it["properties"]["datetime"], "erro": repr(e)[:300]})
        json.dump(res, open(os.path.join(saida, "serie_modis.json"), "w"), indent=0)


def roda_s1(dados, saida):
    regs = regioes(dados, corredor=True); from shapely.ops import unary_union
    geom = unary_union(list(regs.values())).envelope
    its = sorted(comum.stac_busca(comum.PC, ["sentinel-1-rtc"], list(geom.bounds), DATAS), key=lambda i: i["properties"]["datetime"])
    print("s1", len(its), "cenas", flush=True)
    res, cubos = [], {}
    for it in its:
        try:
            a = it["assets"]
            hr = {"vv": comum.pc_assina(a["vv"]["href"])}
            if "vh" in a:
                hr["vh"] = comum.pc_assina(a["vh"]["href"])
            b, T, crs, nd = ler_bandas(hr, "vv", geom)
            vv = b["vv"].astype(float); vv[(vv <= 0) | ~np.isfinite(vv)] = np.nan
            shp = vv.shape; A = area_px(T, crs, shp)
            p = it["properties"]; orb = "%s_%s" % (p.get("sat:orbit_state", "?")[:3], p.get("sat:relative_orbit"))
            r = {}
            for k, g in regs.items():
                m = comum.mascara(g, shp, T, crs); ok = m & np.isfinite(vv)
                r[k] = {"frac_valida": round(float(A[ok].sum() / A[m].sum()), 3),
                        "vv_db_mediana": round(float(np.median(10 * np.log10(vv[ok]))), 2) if ok.any() else None}
                if "vh" in b:
                    vh = b["vh"].astype(float); vh[(vh <= 0) | ~np.isfinite(vh)] = np.nan; okh = m & np.isfinite(vh)
                    r[k]["vh_db_mediana"] = round(float(np.median(10 * np.log10(vh[okh]))), 2) if okh.any() else None
            res.append({"fonte": "s1", "id": it["id"], "datetime": p["datetime"], "orbita": orb, "plataforma": p.get("platform"), "regioes": r})
            cubos.setdefault(orb, []).append((p["datetime"], (10 * np.log10(vv)).astype(np.float16), np.array([T.a, T.b, T.c, T.d, T.e, T.f])))
            print("s1 %s %s vv_anf %s dB (alto_fora %s)" % (p["datetime"][:16], orb, r["anfiteatro"]["vv_db_mediana"], r["alto_fora"]["vv_db_mediana"]), flush=True)
        except Exception as e:
            print("FALHA s1", it["id"], repr(e)[:200], flush=True)
            res.append({"fonte": "s1", "id": it["id"], "datetime": it["properties"]["datetime"], "erro": repr(e)[:300]})
        json.dump(res, open(os.path.join(saida, "serie_s1.json"), "w"), indent=0)
    sv = {}
    for orb, l in cubos.items():
        for dt, a, t in l:
            k = "%s__%s" % (orb, dt[:19].replace(":", ""))
            sv[k + "__vv"] = a; sv[k + "__T"] = t
    np.savez_compressed(os.path.join(saida, "cubos_s1.npz"), **sv)


FONTES = {
    "s2es": lambda d, s: roda_optico("s2es", it_s2es, cena_s2es, inval_scl, d, s),
    "s2l1c": lambda d, s: roda_optico("s2l1c", it_s2l1c, cena_s2l1c, inval_scl, d, s),
    "s2pc": lambda d, s: roda_optico("s2pc", it_s2pc, cena_s2pc, inval_scl, d, s),
    "ls": lambda d, s: roda_optico("ls", it_ls, cena_ls, inval_qa_ls, d, s),
    "hlss": lambda d, s: roda_optico("hlss", it_hls("hls2-s30"), cena_hls("B11"), inval_fmask, d, s),
    "hlsl": lambda d, s: roda_optico("hlsl", it_hls("hls2-l30"), cena_hls("B06"), inval_fmask, d, s),
    "modis": roda_modis,
    "s1": roda_s1,
}

if __name__ == "__main__":
    fonte, dados = sys.argv[1], sys.argv[2]
    try:
        FONTES[fonte](dados, dados)
    except Exception:
        traceback.print_exc(); sys.exit(1)
