# -*- coding: utf-8 -*-
"""
scripts/generate_space_weather_datasets.py
Gera modelos paramétricos sintéticos e timeline mestre do projeto.
AVISO DE AUDITORIA:
As saídas numéricas de raios X, vento solar e índices geomagnéticos gerados
por este script são MODELOS SINTÉTICOS PARAMETRIZADOS e são salvas exclusivamente
no diretório data/synthetic/ com status = 'modeled'.
"""

import os
import math
import json
import csv
from datetime import datetime, timedelta

def main():
    print("Iniciando geração de conjuntos de dados solares sintéticos e timeline-mestra...")
    
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    synth_dir = os.path.join(repo_dir, "data", "synthetic")
    proc_dir = os.path.join(repo_dir, "data", "processed", "space_weather")
    meta_dir = os.path.join(repo_dir, "data", "metadata")
    proc_root = os.path.join(repo_dir, "data", "processed")
    
    os.makedirs(synth_dir, exist_ok=True)
    os.makedirs(proc_dir, exist_ok=True)
    os.makedirs(meta_dir, exist_ok=True)
    os.makedirs(proc_root, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. GERAR MODELO IDEALIZADO GOES X-RAY FLUX (Salvo em synthetic/)
    # -------------------------------------------------------------
    xray_file = os.path.join(synth_dir, "goes_xray_IDEALIZED_MODEL.csv")
    with open(xray_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime_utc", "datetime_npt", "xray_short_005_04nm_Wm2", "xray_long_01_08nm_Wm2", "flare_class", "status"])
        
        start = datetime(2026, 8, 25, 0, 0)
        end = datetime(2026, 8, 26, 12, 0)
        curr = start
        
        while curr <= end:
            npt = curr + timedelta(hours=5, minutes=45)
            base_long = 1.5e-6
            base_short = 2.0e-7
            
            flare_time = datetime(2026, 8, 25, 10, 2)
            dt_min = (curr - flare_time).total_seconds() / 60.0
            
            if -20 <= dt_min <= 45:
                if dt_min <= 0:
                    factor = math.exp(-((dt_min / 6.0) ** 2))
                else:
                    factor = math.exp(-(dt_min / 14.0))
                long_val = base_long + (6.98e-5 - base_long) * factor
                short_val = base_short + (2.5e-5 - base_short) * factor
            else:
                long_val = base_long + 2.0e-7 * math.sin(curr.hour)
                short_val = base_short + 3.0e-8 * math.cos(curr.hour)
            
            f_class = "C1.5"
            if long_val >= 1.0e-4:
                f_class = f"X{long_val/1e-4:.1f}"
            elif long_val >= 1.0e-5:
                f_class = f"M{long_val/1e-5:.1f}"
            elif long_val >= 1.0e-6:
                f_class = f"C{long_val/1e-6:.1f}"
            else:
                f_class = "B"
                
            writer.writerow([
                curr.strftime("%Y-%m-%d %H:%M:%S"),
                npt.strftime("%Y-%m-%d %H:%M:%S"),
                f"{short_val:.4e}",
                f"{long_val:.4e}",
                f_class,
                "modeled"
            ])
            curr += timedelta(minutes=5)
            
    print(f"Salvo modelo sintético: {xray_file}")

    # -------------------------------------------------------------
    # 2. GERAR MODELO IDEALIZADO DE VENTO SOLAR (Salvo em synthetic/)
    # -------------------------------------------------------------
    solar_wind_file = os.path.join(synth_dir, "dscovr_solar_wind_IDEALIZED_MODEL.csv")
    with open(solar_wind_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime_utc", "datetime_npt", "v_sw_kms", "n_p_cm3", "p_dyn_nPa", "bt_nT", "bx_gsm_nT", "by_gsm_nT", "bz_gsm_nT", "ey_convective_mVm", "status"])
        
        curr = datetime(2026, 8, 23, 0, 0)
        end = datetime(2026, 8, 27, 23, 59)
        
        while curr <= end:
            npt = curr + timedelta(hours=5, minutes=45)
            t_hours = (curr - datetime(2026, 8, 23, 0, 0)).total_seconds() / 3600.0
            dt_from_flare = (curr - datetime(2026, 8, 25, 10, 2)).total_seconds() / 3600.0
            
            if dt_from_flare < 12:
                v_sw = 390.0 + 15.0 * math.sin(t_hours / 6.0)
                n_p = 5.2 + 1.2 * math.cos(t_hours / 8.0)
                bt = 5.0 + 0.8 * math.sin(t_hours / 4.0)
                bz = 1.2 * math.sin(t_hours / 3.0)
            else:
                ramp = min(1.0, (dt_from_flare - 12.0) / 10.0)
                v_sw = 390.0 + ramp * 85.0 + 12.0 * math.sin(t_hours / 5.0)
                n_p = 5.2 + ramp * 4.5 + 1.5 * math.cos(t_hours / 6.0)
                bt = 5.0 + ramp * 3.5 + 1.0 * math.sin(t_hours / 4.0)
                bz = -3.5 * ramp + 2.0 * math.sin(t_hours / 2.5)
                
            bx = -bt * 0.5 * math.cos(t_hours / 7.0)
            by = bt * 0.6 * math.sin(t_hours / 5.0)
            p_dyn = 1.6726e-6 * n_p * (v_sw ** 2)
            e_y = (v_sw * (-bz)) * 1.0e-3
            
            writer.writerow([
                curr.strftime("%Y-%m-%d %H:%M:%S"),
                npt.strftime("%Y-%m-%d %H:%M:%S"),
                f"{v_sw:.1f}",
                f"{n_p:.2f}",
                f"{p_dyn:.3f}",
                f"{bt:.2f}",
                f"{bx:.2f}",
                f"{by:.2f}",
                f"{bz:.2f}",
                f"{e_y:.3f}",
                "modeled"
            ])
            curr += timedelta(minutes=15)
            
    print(f"Salvo modelo sintético: {solar_wind_file}")

    # -------------------------------------------------------------
    # 3. GERAR MODELO IDEALIZADO DE ÍNDICES GEOMAGNÉTICOS (synthetic/)
    # -------------------------------------------------------------
    geomag_file = os.path.join(synth_dir, "geomagnetic_indices_IDEALIZED_MODEL.csv")
    with open(geomag_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime_utc", "datetime_npt", "kp_index", "dst_nT", "sym_h_nT", "ae_index_nT", "neutron_count_oulu_normalized", "status"])
        
        curr = datetime(2026, 8, 23, 0, 0)
        end = datetime(2026, 8, 27, 23, 0)
        
        while curr <= end:
            npt = curr + timedelta(hours=5, minutes=45)
            dt_from_flare = (curr - datetime(2026, 8, 25, 10, 2)).total_seconds() / 3600.0
            
            if dt_from_flare < 12:
                kp = 1.7 + 0.3 * math.sin(curr.hour / 3.0)
                dst = -8.0 + 4.0 * math.cos(curr.hour / 4.0)
                sym_h = dst + 2.0 * math.sin(curr.hour / 2.0)
                ae = 110.0 + 35.0 * math.sin(curr.hour / 1.5)
                gcr = 1.000 + 0.003 * math.cos(curr.hour / 6.0)
            else:
                ramp = min(1.0, (dt_from_flare - 12.0) / 14.0)
                kp = 1.7 + ramp * 1.6 + 0.3 * math.sin(curr.hour / 2.0)
                dst = -8.0 - ramp * 24.0 + 3.0 * math.cos(curr.hour / 3.0)
                sym_h = dst - 4.0 * ramp + 2.0 * math.sin(curr.hour / 1.5)
                ae = 110.0 + ramp * 240.0 + 40.0 * math.sin(curr.hour)
                gcr = 1.000 - ramp * 0.012 + 0.002 * math.cos(curr.hour / 4.0)
                
            writer.writerow([
                curr.strftime("%Y-%m-%d %H:%M:%S"),
                npt.strftime("%Y-%m-%d %H:%M:%S"),
                f"{kp:.1f}",
                f"{dst:.1f}",
                f"{sym_h:.1f}",
                f"{ae:.1f}",
                f"{gcr:.4f}",
                "modeled"
            ])
            curr += timedelta(hours=1)
            
    print(f"Salvo modelo sintético: {geomag_file}")

    # -------------------------------------------------------------
    # 4. MODELO DO CIRCUITO ELÉTRICO GLOBAL (GEC) E Jz
    # -------------------------------------------------------------
    gec_file = os.path.join(synth_dir, "gec_jz_model_himalaya.csv")
    with open(gec_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "datetime_utc", "datetime_npt", 
            "vi_ionospheric_potential_kV", 
            "rc_column_resistance_1e17_Ohm_m2", 
            "jz_modeled_pA_m2", 
            "ez_fair_weather_Vm", 
            "solar_xray_flux_Wm2", 
            "lag_hours_from_flare", 
            "status", "notes"
        ])
        
        curr = datetime(2026, 8, 24, 0, 0)
        end = datetime(2026, 8, 27, 12, 0)
        
        while curr <= end:
            npt = curr + timedelta(hours=5, minutes=45)
            dt_from_flare = (curr - datetime(2026, 8, 25, 10, 2)).total_seconds() / 3600.0
            
            carnegie_factor = 1.0 + 0.18 * math.sin((curr.hour - 11.0) * math.pi / 12.0)
            base_vi = 250.0 * carnegie_factor
            base_rc = 0.78
            
            flare_sid_perturbation = 0.0
            if 0.0 <= dt_from_flare <= 3.0:
                flare_sid_perturbation = 28.0 * math.exp(-(dt_from_flare / 0.8) ** 2)
                
            delayed_gec_perturbation = 0.0
            if 12.0 <= dt_from_flare <= 24.0:
                ramp = math.sin((dt_from_flare - 12.0) * math.pi / 12.0)
                delayed_gec_perturbation = 18.0 * ramp
                
            vi_total = base_vi + flare_sid_perturbation + delayed_gec_perturbation
            jz = (vi_total / base_rc) * 0.01
            ez = (jz * 1.0e-12) / 2.5e-14
            
            writer.writerow([
                curr.strftime("%Y-%m-%d %H:%M:%S"),
                npt.strftime("%Y-%m-%d %H:%M:%S"),
                f"{vi_total:.2f}",
                f"{base_rc:.3f}",
                f"{jz:.3f}",
                f"{ez:.1f}",
                f"{1.5e-6 if dt_from_flare < 0 else 6.98e-5 * math.exp(-max(0, dt_from_flare)/0.5):.2e}",
                f"{dt_from_flare:.2f}",
                "modeled",
                "Modelo parametrizado GEC acoplado a curva Carnegie e altitude do Himalaia"
            ])
            curr += timedelta(minutes=30)
            
    print(f"Salvo modelo sintético: {gec_file}")

    # -------------------------------------------------------------
    # 5. GERAR TIMELINE-MESTRA CORRIGIDA (timeline_master.csv)
    # -------------------------------------------------------------
    master_file = os.path.join(proc_root, "timeline_master.csv")
    with open(master_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "datetime_utc", "datetime_npt", "category", "variable", "value", "unit",
            "latitude", "longitude", "source", "source_url", "instrument",
            "temporal_resolution", "quality_flag", "status", "uncertainty", "notes"
        ])
        
        events = [
            ("2026-08-25 09:48:00", "2026-08-25 15:33:00", "Solar", "X-Ray Flux (0.1-0.8nm)", "1.02e-5", "W/m2",
             "0.0", "0.0", "NOAA SWPC / GOES-18", "https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/", "XRS (X-Ray Sensor)", "1 min", "good", "observed", "+/- 5%", "Início oficial da erupção classe M na AR 4513 (classificação oficial NOAA: M6.9)"),
             
            ("2026-08-25 10:02:00", "2026-08-25 15:47:00", "Solar", "X-Ray Peak Flux", "6.98e-5", "W/m2",
             "0.0", "0.0", "NOAA SWPC / GOES-18", "https://www.spaceweather.gov/", "XRS", "1 min", "good", "observed", "+/- 3%", "Pico da erupção solar classe M6.9 (fluxo 6.98e-5 W/m2; AR 4513) / R2 Moderate Radio Blackout"),
             
            ("2026-08-25 10:24:00", "2026-08-25 16:09:00", "Solar", "X-Ray Flux", "9.50e-6", "W/m2",
             "0.0", "0.0", "NOAA SWPC / GOES-18", "https://www.spaceweather.gov/", "XRS", "1 min", "good", "observed", "+/- 5%", "Retorno gradual ao nível basal C1.5"),

            ("2026-08-25 10:10:00", "2026-08-25 15:55:00", "Ionosphere", "Sudden Ionospheric Disturbance (SID)", "28.5", "dB attenuation",
             "28.27", "85.52", "Ionosonde / D-RAP Model", "https://www.swpc.noaa.gov/products/d-region-absorption-predictions-d-rap", "D-RAP / Global HF Absorption", "15 min", "estimated", "modeled", "+/- 15%", "Modelo de absorção em ondas curtas (HF) no hemisfério iluminado (Ásia / Himalaia)"),

            ("2026-08-25 12:00:00", "2026-08-25 17:45:00", "Space_Weather", "Proton Flux (>10 MeV)", "0.85", "pfu",
             "0.0", "0.0", "GOES-18 / SEISS", "https://www.swpc.noaa.gov/", "SEISS", "5 min", "good", "observed", "+/- 10%", "Abaixo do limiar de tempestade de radiação S1 (10 pfu)"),

            ("2026-08-25 19:00:00", "2026-08-26 00:45:00", "Atmospheric_Electricity", "Vertical Current Density (Jz)", "3.85", "pA/m2",
             "28.27", "85.52", "GEC Himalayan Model", "https://github.com/reinaldohaas/Himalaia_2026", "Carnegie-Altitude Column Model", "30 min", "fair", "modeled", "+/- 30%", "Modelo paramétrico teórico do GEC com potencial residual assumido"),

            ("2026-08-25 21:30:00", "2026-08-26 03:15:00", "Meteorology", "Cloud-Top Brightness Temp", "-62.0", "degC",
             "28.35", "85.45", "INSAT-3D / Himawari-8", "https://weather.isro.gov.in/", "TIR-1 (10.8 um)", "30 min", "good", "observed", "+/- 2 degC", "Formação de nuvens convectivas profundas (Cumulonimbus) no vale do Langtang / Gyirong"),

            ("2026-08-25 23:45:00", "2026-08-26 05:30:00", "Meteorology", "Lightning Stroke Count", "14", "strokes/100km2/h",
             "28.30", "85.48", "WWLLN Proxy", "https://wwlln.net/", "VLF Sensor Network", "1 h", "fair", "modeled", "+/- 20%", "Estimativa paramétrica baseada em proxy VLF (dados brutos WWLLN exigem acordo institucional)"),

            ("2026-08-26 01:30:00", "2026-08-26 07:15:00", "Meteorology", "Precipitation Rate", "[DADO INDISPONÍVEL]", "mm/h",
             "28.28", "85.50", "NASA GPM / IMERG V07", "https://gpm.nasa.gov/data/imerg", "GPM Microwave-IR Merged", "30 min", "unverified", "unverified", "N/A", "[DADO INDISPONÍVEL — Requer credenciais Earthdata do usuário para extração de grânulos IMERG V07 de 2026]"),

            ("2026-08-26 02:20:00", "2026-08-26 08:05:00", "Infrasound", "Atmospheric Pressure Wave (0.1-0.8 Hz)", "0.95", "Pa",
             "28.27", "85.52", "Infrasonic Convective Model", "https://github.com/reinaldohaas/Himalaia_2026", "Microbarometer Simulation", "continuous", "unverified", "modeled", "N/A", "Modelo teórico de onda acústica (requer requisição formal vDEC/CTBTO)"),

            ("2026-08-26 02:52:10", "2026-08-26 08:37:10", "Geophysics", "Seismic Magnitude (Ms)", "5.2", "Ms",
             "28.271", "85.515", "USGS NEIC (Evento us7000tbwb)", "https://earthquake.usgs.gov/earthquakes/eventpage/us7000tbwb", "Broadband Seismometer Network", "point event", "excellent", "observed", "+/- 0.1 Ms", "Deslizamento maciço classificado oficialmente pelo USGS como 'landslide' (magType: ms_vx, h: 0 km)"),

            ("2026-08-26 03:05:00", "2026-08-26 08:50:00", "Hydrology", "Barrier Dam Volume", "7.54e6", "m3",
             "28.2740", "85.4800", "Estimativa Morfológica", "https://emergency.copernicus.eu/", "Optical Satellite & DEM", "1 h", "fair", "modeled", "+/- 35%", "Estimativa paramétrica de represamento temporário no gargalo morâinico a 3.950m"),

            ("2026-08-26 03:35:00", "2026-08-26 09:20:00", "Hydrology", "Peak Outburst Discharge (Q_max)", "3450", "m3/s",
             "28.2740", "85.4800", "Hydraulic Breach Model", "https://github.com/reinaldohaas/Himalaia_2026", "1D/2D Hydrodynamic Modeling", "point event", "fair", "modeled", "+/- 30%", "Simulação hidráulica paramétrica de ruptura de barramento"),

            ("2026-08-26 03:55:00", "2026-08-26 09:40:00", "Impact", "Bridge Destruction", "1", "bridge washed out",
             "28.2789", "85.3781", "ICIMOD / DOR Nepal", "https://data.humdata.org/dataset/hot_flood_npl", "Field Survey & Satellite", "point event", "excellent", "observed", "0", "Destruição da Ponte da Amizade Miteri e soterramento da alfândega"),

            ("2026-08-26 04:05:00", "2026-08-26 09:50:00", "Infrastructure", "Power Plant Outage", "111", "MW shut down",
             "28.2650", "85.3780", "Nepal Electricity Authority (NEA)", "https://www.nea.org.np/", "Operational Telemetry", "point event", "excellent", "observed", "0", "Invasão de sedimentos e corte emergencial da central geradora"),

            ("2026-08-26 06:00:35", "2026-08-26 11:45:35", "Geophysics", "Second Seismic Event (Ms)", "4.2", "Ms",
             "28.268", "85.510", "USGS NEIC (Evento us7000tc90)", "https://earthquake.usgs.gov/earthquakes/eventpage/us7000tc90", "Broadband Seismometer Network", "point event", "excellent", "observed", "+/- 0.1 Ms", "Segundo evento sísmico classificado oficialmente pelo USGS como 'landslide' (magType: ms_vx, h: 0 km)"),

            ("2026-08-26 12:00:00", "2026-08-26 17:45:00", "Human_Toll", "Casualties and Missing", "1000-1400 mortos; 4000-5500 desaparecidos", "persons",
             "28.1610", "85.3370", "Levantamentos Humanitários e Noticiosos / UN OCHA / Nepal DRR Portal", "https://data.humdata.org/dataset/hot_flood_npl", "Relatórios Oficiais de Emergência", "cumulative", "good", "observed", "estimado", "Balanço humano estimado: 1.000 a 1.400 mortos, 4.000 a 5.500 desaparecidos e impacto em 13 usinas hidrelétricas ao longo do corredor do Trishuli"),

            ("2026-08-26 18:00:00", "2026-08-26 23:45:00", "Infrastructure", "Bridges Destroyed/Affected (Cumulative)", "33 rodoviárias, 68 suspensas", "bridges",
             "28.1610", "85.3370", "ICIMOD Bridge Damage Assessment / UN OCHA", "https://www.icimod.org/", "Remote Sensing & Ground Truth", "event summary", "excellent", "observed", "0", "33 pontes rodoviárias e 68 pontes suspensas afetadas/destruídas ao longo do vale")
        ]
        
        for ev in events:
            writer.writerow(ev)
            
    print(f"Salvo: {master_file} com {len(events)} eventos estruturados!")

    # -------------------------------------------------------------
    # 6. GERAR METADADOS EM JSON (data/metadata/sources_metadata.json)
    # -------------------------------------------------------------
    meta_file = os.path.join(meta_dir, "sources_metadata.json")
    metadata = {
        "project": "Himalaia 2026 Solar-Jz-Storm Investigation",
        "last_updated_utc": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "coordinate_reference_system": "WGS84 (EPSG:4326)",
        "time_standards": {
            "primary": "UTC",
            "secondary": "NPT (Nepal Time = UTC+5:45)"
        },
        "critical_timestamps": {
            "solar_flare_m69_peak_utc": "2026-08-25T10:02:00Z",
            "disaster_onset_seismic_utc": "2026-08-26T02:52:10Z",
            "second_landslide_seismic_utc": "2026-08-26T06:00:35Z",
            "delta_time_hours": 16.8361,
            "delta_time_formatted": "16h 50min 10s"
        },
        "data_sources": [
            {
                "name": "NOAA Space Weather Prediction Center (SWPC)",
                "products": ["GOES X-Ray Flux (XRS)", "Solar Protons (SEISS)", "DSCOVR Solar Wind"],
                "url": "https://www.spaceweather.gov/",
                "status": "observed",
                "notes": "Arquivos reais mantidos em data/raw/space_weather/; modelos analíticos segregados em data/synthetic/."
            },
            {
                "name": "USGS Earthquake Hazards Program",
                "products": ["Seismic Event us7000tbwb (Ms 5.2 landslide) e us7000tc90 (Ms 4.2 landslide)"],
                "url": "https://earthquake.usgs.gov/fdsnws/event/1/",
                "status": "observed",
                "notes": "Classificação oficial USGS: landslide (h = 0 km)."
            },
            {
                "name": "UN OCHA / Humanitarian Data Exchange (HDX)",
                "products": ["Nepal Flood 2026 Corridor AOI", "ICIMOD Bridge Damage Assessment (33 rodoviárias, 68 suspensas)"],
                "url": "https://data.humdata.org/dataset/hot_flood_npl",
                "status": "observed"
            },
            {
                "name": "OpenStreetMap Foundation (OSM)",
                "products": ["Relations 21284197 (Bhotekoshi) and 4839538 (Trishuli River)"],
                "url": "https://www.openstreetmap.org/",
                "status": "observed"
            }
        ]
    }
    
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {meta_file}")

if __name__ == "__main__":
    main()
