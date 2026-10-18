# -*- coding: utf-8 -*-
"""
Downloads da ERA5 (Copernicus CDS) para o WRF do Lhende Khola e para a verificacao do sistema convectivo.
Credencial: so a do ~/.cdsapirc (nunca impressa).

  python baixar_era5.py verificacao <dir>   -> era5_verif_sl.nc: campos de nivel unico, horarios,
        25/08 06 UTC -> 26/08 03 UTC, 22-34 N, 78-95 E: onda longa no topo (OLR), nuvem alta, chuva total
        e convectiva, CAPE, gelo de nuvem na coluna
  python baixar_era5.py wrf <dir>           -> era5_wrf_pl.grib e era5_wrf_sl.grib: o que o ungrib (Vtable.ECMWF)
        precisa, horario, 24/08 18 UTC -> 26/08 06 UTC, 15-40 N, 70-100 E
"""
import os
import sys

import cdsapi

NIVEIS = ["1", "2", "3", "5", "7", "10", "20", "30", "50", "70", "100", "125", "150", "175", "200", "225", "250",
          "300", "350", "400", "450", "500", "550", "600", "650", "700", "750", "775", "800", "825", "850", "875",
          "900", "925", "950", "975", "1000"]
HORAS = ["%02d:00" % h for h in range(24)]


def periodo_wrf():
    return [("2026", "08", ["24"], ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]),
            ("2026", "08", ["25"], HORAS),
            ("2026", "08", ["26"], ["%02d:00" % h for h in range(7)])]


def main(modo, d):
    os.makedirs(d, exist_ok=True)
    c = cdsapi.Client(quiet=True)
    if modo == "verificacao":
        for nome, dia, horas in (("era5_verif_sl_25.nc", "25", ["%02d:00" % h for h in range(6, 24)]),
                                 ("era5_verif_sl_26.nc", "26", ["%02d:00" % h for h in range(4)])):
            alvo = os.path.join(d, nome)
            if os.path.exists(alvo):
                continue
            c.retrieve("reanalysis-era5-single-levels", {
                "product_type": ["reanalysis"],
                "variable": ["mean_top_net_long_wave_radiation_flux", "high_cloud_cover", "total_precipitation",
                             "convective_precipitation", "convective_available_potential_energy",
                             "total_column_cloud_ice_water"],
                "year": ["2026"], "month": ["08"], "day": [dia], "time": horas,
                "area": [34, 78, 22, 95], "data_format": "netcdf", "download_format": "unarchived"}, alvo)
            print("gravado", alvo, os.path.getsize(alvo))
    elif modo == "wrf":
        for k, (a, m, dias, horas) in enumerate(periodo_wrf()):
            pl = os.path.join(d, "era5_wrf_pl_%d.grib" % k); sl = os.path.join(d, "era5_wrf_sl_%d.grib" % k)
            comum = {"product_type": ["reanalysis"], "year": [a], "month": [m], "day": dias, "time": horas,
                     "area": [40, 70, 15, 100], "data_format": "grib", "download_format": "unarchived"}
            if not os.path.exists(pl):
                c.retrieve("reanalysis-era5-pressure-levels", dict(comum, variable=[
                    "geopotential", "temperature", "u_component_of_wind", "v_component_of_wind", "relative_humidity",
                    "specific_humidity"], pressure_level=NIVEIS), pl)
                print("gravado", pl, os.path.getsize(pl))
            if not os.path.exists(sl):
                c.retrieve("reanalysis-era5-single-levels", dict(comum, variable=[
                    "surface_pressure", "mean_sea_level_pressure", "2m_temperature", "2m_dewpoint_temperature",
                    "10m_u_component_of_wind", "10m_v_component_of_wind", "skin_temperature", "sea_surface_temperature",
                    "sea_ice_cover", "land_sea_mask", "geopotential", "snow_depth", "snow_density",
                    "soil_temperature_level_1", "soil_temperature_level_2", "soil_temperature_level_3",
                    "soil_temperature_level_4", "volumetric_soil_water_layer_1", "volumetric_soil_water_layer_2",
                    "volumetric_soil_water_layer_3", "volumetric_soil_water_layer_4"]), sl)
                print("gravado", sl, os.path.getsize(sl))
    else:
        sys.exit("modo: verificacao | wrf")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
