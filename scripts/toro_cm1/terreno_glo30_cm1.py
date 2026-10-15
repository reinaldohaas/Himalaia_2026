# -*- coding: utf-8 -*-
"""
Terreno do Copernicus GLO-30 para o CM1 (itern=4, arquivo perts.dat).

  dominio  : NX x NY celulas de DX m, centrado no ponto de colapso (85.515 E, 28.271 N)
  projecao : equiretangular local em torno do centro (erro < 0,1 % em 40 km)
  reamostr.: media em blocos de DX
  suaviz.  : filtro 1-2-1 aplicado NPASS vezes (o solver terrain-following nao aguenta 48 graus a 500 m)
  base     : ZBASE m ASL; terreno abaixo disso e preenchido (vales profundos do Bhote Koshi)
  borda    : as NBORDA celulas externas sao misturadas com um campo muito suavizado
             para reduzir reflexao nos contornos abertos
Saida: perts.dat (float32, x mais rapido, j de sul para norte) + zs.npy + metadados.
"""
import hashlib
import json
import os
import sys
import numpy as np
import rasterio

URL = ("/vsicurl/https://copernicus-dem-30m.s3.amazonaws.com/"
       "Copernicus_DSM_COG_10_N28_00_E085_00_DEM/Copernicus_DSM_COG_10_N28_00_E085_00_DEM.tif")
LON0, LAT0 = 85.515, 28.271
NX = NY = int(os.environ.get("NX", 80))
DX = float(os.environ.get("DX", 500.0))
ZBASE = float(os.environ.get("ZBASE", 3000.0))
NPASS = int(os.environ.get("NPASS", 4))
NBORDA = 8
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

R = 6371000.0
mlat = np.pi / 180 * R
mlon = mlat * np.cos(np.radians(LAT0))
Lx, Ly = NX * DX, NY * DX
lon_a, lon_b = LON0 - Lx / 2 / mlon, LON0 + Lx / 2 / mlon
lat_a, lat_b = LAT0 - Ly / 2 / mlat, LAT0 + Ly / 2 / mlat

with rasterio.open(URL) as ds:
    T = ds.transform
    c0 = int(np.floor((lon_a - T.c) / T.a)); c1 = int(np.ceil((lon_b - T.c) / T.a))
    r0 = int(np.floor((lat_b - T.f) / T.e)); r1 = int(np.ceil((lat_a - T.f) / T.e))
    z = ds.read(1, window=((r0, r1), (c0, c1))).astype(np.float64)
    lon = T.c + T.a * (np.arange(c0, c1) + 0.5)
    lat = T.f + T.e * (np.arange(r0, r1) + 0.5)
np.save(os.path.join(OUT, "glo30_janela.npy"), z.astype(np.float32))
print("janela GLO-30: %d x %d px, %.1f a %.1f m" % (z.shape[1], z.shape[0], z.min(), z.max()))

# coordenadas locais de cada pixel e media em blocos
X = (lon - LON0) * mlon + Lx / 2
Y = (lat - LAT0) * mlat + Ly / 2
ix = np.clip((X // DX).astype(int), 0, NX - 1)
iy = np.clip((Y // DX).astype(int), 0, NY - 1)
soma = np.zeros((NY, NX)); n = np.zeros((NY, NX))
IX, IY = np.meshgrid(ix, iy)
np.add.at(soma, (IY, IX), z); np.add.at(n, (IY, IX), 1)
zb = soma / n                       # linha 0 = sul (Y cresce para norte)
zmax_bloco = np.zeros((NY, NX)); np.maximum.at(zmax_bloco, (IY, IX), z)


def f121(a, npass):
    a = a.copy()
    for _ in range(npass):
        p = np.pad(a, 1, mode="edge")
        a = (p[1:-1, :-2] + 2 * p[1:-1, 1:-1] + p[1:-1, 2:]) / 4
        p = np.pad(a, 1, mode="edge")
        a = (p[:-2, 1:-1] + 2 * p[1:-1, 1:-1] + p[2:, 1:-1]) / 4
    return a


zs = f121(zb, NPASS)
longe = f121(zb, 60)
w = np.ones((NY, NX))
for k in range(NBORDA):
    fac = (k + 0.5) / NBORDA
    w[k, :] = np.minimum(w[k, :], fac); w[-1 - k, :] = np.minimum(w[-1 - k, :], fac)
    w[:, k] = np.minimum(w[:, k], fac); w[:, -1 - k] = np.minimum(w[:, -1 - k], fac)
zs = w * zs + (1 - w) * longe
preench = float(np.mean(zs < ZBASE))
zs_rel = np.maximum(zs - ZBASE, 0.0)

gy, gx = np.gradient(zs_rel, DX)
inc = np.degrees(np.arctan(np.hypot(gx, gy)))
gy0, gx0 = np.gradient(zb, DX)
inc0 = np.degrees(np.arctan(np.hypot(gx0, gy0)))
# celula do ponto de colapso e do anfiteatro (saida a 4.010 m)
ic, jc = NX // 2, NY // 2
meta = dict(lon0=LON0, lat0=LAT0, nx=NX, ny=NY, dx=DX, zbase=ZBASE, npass=NPASS, nborda=NBORDA,
            lon=[lon_a, lon_b], lat=[lat_a, lat_b],
            glo30_min=float(z.min()), glo30_max=float(z.max()),
            bloco_max=float(zb.max()), suav_max=float(zs.max()), suav_min=float(zs.min()),
            frac_preenchida=preench, incl_max_bloco=float(inc0.max()), incl_max_modelo=float(inc.max()),
            incl_p95_modelo=float(np.percentile(inc, 95)),
            z_centro_bloco=float(zb[jc, ic]), z_centro_modelo=float(zs[jc, ic]))
zs_rel.astype("<f4").tofile(os.path.join(OUT, "perts.dat"))
np.save(os.path.join(OUT, "zs_modelo_asl.npy"), (zs_rel + ZBASE).astype(np.float32))
np.save(os.path.join(OUT, "zs_bloco_asl.npy"), zb.astype(np.float32))
meta["sha256_perts"] = hashlib.sha256(open(os.path.join(OUT, "perts.dat"), "rb").read()).hexdigest()
json.dump(meta, open(os.path.join(OUT, "terreno_meta.json"), "w"), indent=1)
for k, v in meta.items():
    print("  %-18s %s" % (k, v))
