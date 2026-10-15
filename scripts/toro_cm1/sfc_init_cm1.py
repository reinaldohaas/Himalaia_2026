# -*- coding: utf-8 -*-
"""
sfc_init.dat para o CM1 (initsfc=5): 4 registros nx*ny float32 -> tsk, tmn, lu_index, xland.

  tsk(i,j) = T_ar(z_terreno) + (skt - t2m)_ERA5      [diferenca pele-ar medida na celula ERA5]
  tmn(i,j) = T_ar(z_terreno) + (stl3 - t2m)_ERA5     [solo 28-100 cm]
  T_ar(z)  : da propria sondagem do modelo (input_sounding), na cota de cada celula
  neve/gelo (USGS 24): tsk e tmn limitados a 273,15 K
  xland = 2 (agua) onde USGS 16; senao 1
Uso: python sfc_init_cm1.py <dir_terreno> <input_sounding> <era5_skt_stl.nc> <hora 06|12> <saida>
"""
import sys
import numpy as np
import xarray as xr
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import diag_sondagem as D

dterr, snd, nc, hora, out = sys.argv[1:6]
zs = np.load(dterr + "/zs_modelo_asl.npy").astype(float)     # m ASL
lu = np.load(dterr + "/lu_usgs.npy").astype(float)
z, p, T, qv, u, v = D.ler(snd)
ZBASE = 3000.0
Tz = np.interp(zs - ZBASE, z, T)
d = xr.open_dataset(nc).sel(latitude=28.2849, longitude=85.5132, method="nearest")
tdim = "valid_time" if "valid_time" in d.dims else "time"
d = d.isel({tdim: 0 if hora == "06" else 1})
dskt = float(d["skt"] - d["t2m"]); dstl = float(d["stl3"] - d["t2m"])
tsk = Tz + dskt; tmn = Tz + dstl
neve = lu == 24
tsk[neve] = np.minimum(tsk[neve], 273.15); tmn[neve] = np.minimum(tmn[neve], 273.15)
xland = np.where(lu == 16, 2.0, 1.0)
with open(out, "wb") as f:
    for a in (tsk, tmn, lu, xland):
        a.astype("<f4").tofile(f)
print("hora %s UTC: skt-t2m = %+.2f K, stl3-t2m = %+.2f K | tsk %.1f a %.1f K | tmn %.1f a %.1f K | celulas neve/gelo %d"
      % (hora, dskt, dstl, tsk.min(), tsk.max(), tmn.min(), tmn.max(), neve.sum()))
