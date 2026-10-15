# -*- coding: utf-8 -*-
"""ESA WorldCover 2021 v200 (10 m) -> classe USGS do CM1, por maioria em celulas de 500 m."""
import json, os, sys
import numpy as np
import rasterio
URL = ("/vsicurl/https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/"
       "ESA_WorldCover_10m_2021_v200_N27E084_Map.tif")
M = json.load(open(sys.argv[1]))                     # terreno_meta.json
OUT = os.path.dirname(sys.argv[1])
NX, NY, DX = M["nx"], M["ny"], M["dx"]
(lon_a, lon_b), (lat_a, lat_b) = M["lon"], M["lat"]
# WorldCover -> USGS 24 classes (LANDUSE.TBL do CM1)
WC2USGS = {10: 15, 20: 8, 30: 7, 40: 2, 50: 1, 60: 19, 70: 24, 80: 16, 90: 17, 95: 17, 100: 20}
with rasterio.open(URL) as ds:
    T = ds.transform
    c0 = int(np.floor((lon_a - T.c) / T.a)); c1 = int(np.ceil((lon_b - T.c) / T.a))
    r0 = int(np.floor((lat_b - T.f) / T.e)); r1 = int(np.ceil((lat_a - T.f) / T.e))
    wc = ds.read(1, window=((r0, r1), (c0, c1)))
    lon = T.c + T.a * (np.arange(c0, c1) + 0.5); lat = T.f + T.e * (np.arange(r0, r1) + 0.5)
R = 6371000.0; mlat = np.pi / 180 * R; mlon = mlat * np.cos(np.radians(M["lat0"]))
ix = np.clip(((lon - M["lon0"]) * mlon + NX * DX / 2) // DX, 0, NX - 1).astype(int)
iy = np.clip(((lat - M["lat0"]) * mlat + NY * DX / 2) // DX, 0, NY - 1).astype(int)
classes = sorted(WC2USGS)
cont = np.zeros((len(classes), NY, NX))
IX, IY = np.meshgrid(ix, iy)
for n, c in enumerate(classes):
    m = wc == c
    np.add.at(cont[n], (IY[m], IX[m]), 1)
maj = np.array(classes)[cont.argmax(axis=0)]
usgs = np.vectorize(WC2USGS.get)(maj).astype(np.float32)
frac = cont / cont.sum(axis=0, keepdims=True)
np.save(os.path.join(OUT, "lu_usgs.npy"), usgs)
np.save(os.path.join(OUT, "frac_neve_gelo_wc.npy"), frac[classes.index(70)].astype(np.float32))
tot = {c: float((wc == c).mean()) for c in classes}
print("pixels WorldCover:", wc.shape, " fracao por classe:", {k: round(v, 3) for k, v in tot.items() if v > 0.001})
u, n = np.unique(usgs, return_counts=True)
print("celulas USGS:", dict(zip(u.astype(int).tolist(), n.tolist())))
