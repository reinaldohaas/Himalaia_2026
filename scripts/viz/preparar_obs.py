# -*- coding: utf-8 -*-
"""
Dados observados e do antigravity para o visualizador, na grade local do CM1 (km a partir de
85,515 E; 28,271 N, mesma projecao de scripts/toro_cm1/terreno_glo30_cm1.py).

Do antigravity usa SO os dados brutos (integros pelo MANIFESTO), reprocessados com as correcoes da
verificacao (VERIFICACAO_ANTIGRAVITY_NEVE_EROSAO.md):
  * Sentinel-2 L2A (recortes de 20 km, bandas verde/vermelho/NIR/SWIR gravadas so com escala 0,0001):
    aplica o offset -0,1 que faltou; nodata = valor gravado 0.
    falsa cor SWIR-NIR-vermelho (neve/gelo = ciano; rocha = marrom) e mascara de neve
    NDSI > 0,40 e NIR > 0,11.
  * ERA5-Land (GRIB horario de ago/2026): celula mais proxima do ponto do colapso; acumulados
    diarios pelo ULTIMO passo do dia (o antigravity usou a media dos passos, ~2x a menos).
  * polígono da bacia a montante do ponto do evento do JSON (aoi_bacia).
  NAO usa as tabelas do relatorio do antigravity nem a "cicatriz" (defeitos documentados).
Observacoes: Himawari-9 B13 e IMERG V07 Late de data/processed/viz_series.json.
Series de modelo: JSONs do analisar_rad.py (referencia local, rad_12utc local, realizacao do vlab).
"""
import base64
import io
import json
import os
import sys
import numpy as np
import rasterio
from pyproj import Transformer
from PIL import Image

RAIZ = r"C:\Users\haas\github\Himalaia_2026"
WT = os.path.join(RAIZ, r".claude\worktrees\himalaia-enchentes-auditoria-fcfdb5")
SP = sys.argv[1]                       # scratchpad (JSONs de series locais)
SAIDA = os.path.join(WT, r"viz\dados\obs.json")
LON0, LAT0 = 85.515, 28.271
R = 6371000.0
MLAT = np.pi / 180 * R
MLON = MLAT * np.cos(np.radians(LAT0))


def km(lon, lat):
    return (np.asarray(lon) - LON0) * MLON / 1000.0, (np.asarray(lat) - LAT0) * MLAT / 1000.0


def png_b64(arr):
    b = io.BytesIO(); Image.fromarray(arr).save(b, format="PNG", optimize=True)
    return base64.b64encode(b.getvalue()).decode()


def sentinel(arq, rotulo, res_km=0.025):
    with rasterio.open(arq) as s:
        g, r, n, w = [s.read(i) for i in (1, 2, 3, 4)]
        T = s.transform; crs = s.crs.to_epsg()
        H, W = g.shape
    utm2ll = Transformer.from_crs(crs, 4326, always_xy=True)
    ll2utm = Transformer.from_crs(4326, crs, always_xy=True)
    cx = np.array([0, W, 0, W]) * T.a + T.c; cy = np.array([0, 0, H, H]) * T.e + T.f
    lo, la = utm2ll.transform(cx, cy); kx, ky = km(lo, la)
    x0, x1, y0, y1 = kx.min(), kx.max(), ky.min(), ky.max()
    xs = np.arange(x0, x1, res_km) + res_km / 2; ys = np.arange(y1, y0, -res_km) - res_km / 2
    X, Y = np.meshgrid(xs, ys)
    lon = LON0 + X * 1000.0 / MLON; lat = LAT0 + Y * 1000.0 / MLAT
    ux, uy = ll2utm.transform(lon, lat)
    col = np.floor((ux - T.c) / T.a).astype(int); lin = np.floor((uy - T.f) / T.e).astype(int)
    ok = (col >= 0) & (col < W) & (lin >= 0) & (lin < H)
    col = np.clip(col, 0, W - 1); lin = np.clip(lin, 0, H - 1)
    G, Rr, N, S = (b[lin, col] for b in (g, r, n, w))
    valido = ok & (G > 0)
    G, Rr, N, S = (b - 0.1 for b in (G, Rr, N, S))            # offset -0,1 do L2A (processamento >= 04.00)
    with np.errstate(divide="ignore", invalid="ignore"):
        ndsi = (G - S) / (G + S)
    neve = valido & (ndsi > 0.40) & (N > 0.11)
    rgb = np.dstack([S, N, Rr])
    rgb = np.clip(rgb / 0.8, 0, 1) ** (1 / 1.6)
    rgb = (rgb * 255).astype(np.uint8); rgb[~valido] = 0
    rgba = np.dstack([rgb, np.where(valido, 255, 0).astype(np.uint8)])
    masc = np.zeros(neve.shape + (4,), np.uint8)
    masc[neve] = (60, 200, 255, 200)
    frac = float(neve.sum() / max(valido.sum(), 1))
    print("%s: grade %dx%d a %.0f m, validos %.0f%%, neve %.1f%%" % (rotulo, len(xs), len(ys), res_km * 1000,
          100 * valido.mean(), 100 * frac))
    return {"rotulo": rotulo, "ext_km": [float(x0), float(x1), float(y0), float(y1)],
            "falsa_cor": png_b64(rgba), "neve": png_b64(masc), "frac_neve_validos": frac,
            "fonte": os.path.basename(arq) + " (antigravity, bruto; reprocessado com offset -0,1)"}


def era5land(arq):
    import cfgrib
    out = {}
    for d in cfgrib.open_datasets(arq):
        for v in d.data_vars:
            a = d[v]
            la, lo = d.latitude.values, d.longitude.values
            i = int(np.argmin(abs(la - LAT0))); j = int(np.argmin(abs(lo - LON0)))
            out["celula"] = [float(la[i]), float(lo[j])]
            x = a.isel(latitude=i, longitude=j).values          # (time, step)
            dias = [str(t)[:10] for t in d["time"].values]
            if v in ("sf", "smlt"):
                out[v] = [None if np.isnan(r[-1]) else round(float(r[-1]) * 1000, 3) for r in x]   # ultimo passo = total do dia
            elif v in ("sde", "t2m"):
                k = (lambda z: z - 273.15) if v == "t2m" else (lambda z: z)
                out[v] = [None if np.all(np.isnan(r)) else round(float(k(np.nanmean(r))), 3) for r in x]
            out["dias"] = dias
    print("ERA5-Land: celula", out.get("celula"), "dias", len(out.get("dias", [])), "variaveis", [k for k in out if k not in ("celula", "dias")])
    return out


def poligono(arq):
    g = json.load(open(arq))["features"][0]
    crs = g["properties"].get("utm_epsg", 32645)
    tr = Transformer.from_crs(crs, 4326, always_xy=True)
    c = np.array(g["geometry"]["coordinates"][0])
    lo, la = tr.transform(c[:, 0], c[:, 1]); x, y = km(lo, la)
    return [[round(float(a), 3), round(float(b), 3)] for a, b in zip(x, y)]


def main():
    obs = {"centro": [LON0, LAT0]}
    opt = os.path.join(RAIZ, r"data\raw\neve_erosao\optico")
    obs["s2"] = [sentinel(os.path.join(opt, "himalaia_2026_Sentinel-2_2026-08-12_pre.tif"), "Sentinel-2 12/08/2026 (14 dias antes)"),
                 sentinel(os.path.join(opt, "himalaia_2026_Sentinel-2_2026-09-16_pos.tif"), "Sentinel-2 16/09/2026 (21 dias depois)")]
    obs["era5land"] = era5land(os.path.join(RAIZ, r"data\raw\neve_erosao\era5\era5land_himalaia_2026_2026_08.grib"))
    aoi = os.path.join(RAIZ, r"data\processed\neve_erosao\aoi")
    obs["poligonos"] = {"bacia_antigravity": poligono(os.path.join(aoi, "aoi_bacia_himalaia_2026.geojson"))}
    px, py = km(85.483, 28.274)
    obs["pontos"] = {"colapso_glo30": [0.0, 0.0], "evento_json_antigravity": [round(float(px), 3), round(float(py), 3)]}
    vz = json.load(open(os.path.join(WT, r"data\processed\viz_series.json"), encoding="utf-8"))
    obs["himawari"] = vz["hima"]                    # [h desde 25/08 00 UTC, BT sitio K, area <213 K km2]
    obs["imerg"] = vz["imerg"]                      # [h, taxa, ?, acumulado mm]
    series = {}
    ref = json.load(open(os.path.join(SP, "ref_cm1_rad_resultados.json")))
    loc = json.load(open(os.path.join(SP, "cm1_rad_resultados.json")))
    vl = json.load(open(os.path.join(SP, r"vlab_recebido_20261017_0311\cm1_rad_resultados.json")))
    keep = ["hora_utc", "slw_anf_t", "rain_anf", "rain_media", "wmax", "wmax_anf", "gelo_kt", "slw_kt", "icnc_max", "hfx_anf"]
    pega = lambda d: {k: d[k] for k in keep if k in d}
    series["rad06_ref"] = pega(ref["rad_06utc"]); series["rad06_vlab"] = pega(vl["rad_06utc"])
    series["rad12_ref"] = pega(loc["rad_12utc"]); series["rad12_vlab"] = pega(vl["rad_12utc"])
    obs["series"] = series
    json.dump(obs, open(SAIDA, "w"), separators=(",", ":"))
    print("obs.json: %.1f MB" % (os.path.getsize(SAIDA) / 1e6))


if __name__ == "__main__":
    main()
