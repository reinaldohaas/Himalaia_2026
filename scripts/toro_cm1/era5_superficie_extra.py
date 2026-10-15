# -*- coding: utf-8 -*-
"""ERA5: perfil das 06 UTC (download_era5 do autor) + skt e stl3 para 06 e 12 UTC de 25/08/2026."""
import os, sys
import cdsapi
sys.path.insert(0, r"C:\Users\haas\github\era5_to_cm1")
import era5_to_sounding as E
SP = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(SP, "sondagens")
LAT, LON = 28.2849, 85.5132
pl, sl = os.path.join(D, "era5_pl_06.nc"), os.path.join(D, "era5_sl_06.nc")
if not (os.path.exists(pl) and os.path.exists(sl)):
    E.download_era5(LAT, LON, "2026-08-25", "06:00", pl, sl)
out = os.path.join(D, "era5_skt_stl_25ago.nc")
if not os.path.exists(out):
    cdsapi.Client().retrieve("reanalysis-era5-single-levels", {
        "product_type": ["reanalysis"], "data_format": "netcdf", "download_format": "unarchived",
        "variable": ["skin_temperature", "soil_temperature_level_3", "2m_temperature"],
        "year": "2026", "month": "08", "day": "25", "time": ["06:00", "12:00"],
        "area": [LAT + 0.25, LON - 0.25, LAT - 0.25, LON + 0.25]}, out)
print("ok", pl, sl, out)
