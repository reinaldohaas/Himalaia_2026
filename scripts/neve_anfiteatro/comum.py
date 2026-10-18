# -*- coding: utf-8 -*-
"""
Comum a analise multifonte de neve/gelo sobre o anfiteatro do Lhende Khola (2026).

* busca STAC no Planetary Computer (PC) e no Earth Search (ES), sem credencial;
* assinatura publica de URL do PC (token SAS anonimo por colecao);
* leitura em janela de COGs (/vsicurl) so do retangulo que envolve um poligono, no CRS do raster.
"""
import json
import time
import urllib.request

import numpy as np

PC = "https://planetarycomputer.microsoft.com/api/stac/v1"
ES = "https://earth-search.aws.element84.com/v1"
COLAPSO = (85.515, 28.271)        # lon, lat do ponto de colapso (GLO-30, z = 5.590 m)
_TOK = {}


def stac_busca(api, colecoes, bbox, datas, consulta=None, limite=200):
    corpo = {"collections": colecoes, "bbox": bbox, "datetime": datas, "limit": limite}
    if consulta:
        corpo["query"] = consulta
    itens, url = [], api + "/search"
    while url:
        req = urllib.request.Request(url, data=json.dumps(corpo).encode(), headers={"Content-Type": "application/json"})
        for k in range(4):
            try:
                d = json.load(urllib.request.urlopen(req, timeout=120)); break
            except Exception:
                if k == 3:
                    raise
                time.sleep(5 * (k + 1))
        for f in d.get("features", []):
            p = f["properties"]
            if not p.get("datetime"):
                p["datetime"] = p.get("start_datetime")          # MODIS: so intervalo
            itens.append(f)
        prox = [l for l in d.get("links", []) if l.get("rel") == "next"]
        if prox and prox[0].get("body"):
            corpo = prox[0]["body"]; url = prox[0]["href"]
        else:
            url = None
    return itens


def pc_assina(href, colecao=None):
    """assina pelo endpoint sign (o token por colecao nem sempre vale para a conta de armazenamento do asset);
    guarda o token por conta/conteiner e o reaproveita"""
    import urllib.parse
    p = urllib.parse.urlparse(href); chave = p.netloc + "/" + p.path.split("/")[1]
    t = _TOK.get(chave)
    if not t or t[1] < time.time() + 300:
        d = json.load(urllib.request.urlopen("https://planetarycomputer.microsoft.com/api/sas/v1/sign?href=" + urllib.parse.quote(href, safe=""), timeout=60))
        _TOK[chave] = (d["href"].split("?", 1)[1], time.time() + 2400)
    return href.split("?")[0] + "?" + _TOK[chave][0]


def ler_janela(href, geom_ll, folga_m=200.0, reamostrar_para=None):
    """le a janela do COG que envolve geom_ll (shapely, EPSG:4326) + folga; devolve (array, transform, crs)"""
    import rasterio
    from rasterio.windows import from_bounds
    from pyproj import Transformer
    env = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY="4", GDAL_HTTP_RETRY_DELAY="2",
               CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif,.TIF,.tiff,.jp2", VSI_CACHE="TRUE")
    with rasterio.Env(**env):
        with rasterio.open(href) as s:
            tr = Transformer.from_crs(4326, s.crs, always_xy=True)
            x0, y0, x1, y1 = geom_ll.bounds
            xs, ys = tr.transform([x0, x1, x0, x1], [y0, y0, y1, y1])
            if s.crs.is_geographic:
                f = folga_m / 111000.0
            else:
                f = folga_m
            w = from_bounds(min(xs) - f, min(ys) - f, max(xs) + f, max(ys) + f, s.transform).round_offsets().round_lengths()
            a = s.read(1, window=w, boundless=True, fill_value=s.nodata if s.nodata is not None else 0)
            return a, s.window_transform(w), s.crs, s.nodata


def mascara(geom_ll, shape, transform, crs):
    """rasteriza o poligono (EPSG:4326) na grade dada"""
    from rasterio.features import rasterize
    from shapely.ops import transform as sh_tr
    from pyproj import Transformer
    tr = Transformer.from_crs(4326, crs, always_xy=True)
    g = sh_tr(lambda x, y, z=None: tr.transform(x, y), geom_ll)
    return rasterize([(g, 1)], out_shape=shape, transform=transform, fill=0, dtype="uint8").astype(bool)


def reamostra_para(a, tr_a, crs_a, shape_b, tr_b, crs_b, metodo="nearest"):
    from rasterio.warp import reproject, Resampling
    out = np.zeros(shape_b, dtype=np.float32)
    reproject(a.astype(np.float32), out, src_transform=tr_a, src_crs=crs_a, dst_transform=tr_b, dst_crs=crs_b,
              resampling=getattr(Resampling, metodo))
    return out
