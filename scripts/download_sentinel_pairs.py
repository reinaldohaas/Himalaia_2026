# -*- coding: utf-8 -*-
"""
scripts/download_sentinel_pairs.py
Automated Search & Metadata Harvester for Pre- and Post-Event Satellite Imagery
(Sentinel-2 L2A, Landsat-8/9, and PlanetScope / STAC APIs) for the 15 Himalayan Events.
"""

import json
import os
import datetime
import urllib.request

def build_satellite_search_catalog(events_path, output_path):
    with open(events_path, 'r', encoding='utf-8') as f:
        events = json.load(f)

    # Specific event date anchors for STAC search
    event_dates = {
        "kedarnath_2013": "2013-06-16",
        "chamoli_2021": "2021-02-07",
        "himalaia_2026": "2026-08-26",
        "aru_2016": "2016-07-17",
        "seti_2012": "2012-05-05",
        "south_lhonak_2023": "2023-10-04",
        "leh_2010": "2010-08-06",
        "melamchi_2021": "2021-06-15",
        "parechu_2000": "2000-08-01",
        "zhangzangbo_1981": "1981-07-26",
        "dig_tsho_1985": "1985-08-04",
        "luggye_tsho_1994": "1994-10-07",
        "bhotekoshi_2016": "2016-07-05",
        "himachal_2023": "2023-07-09",
        "parechu_2005": "2005-06-26"
    }

    catalog = []

    for ev in events:
        eid = ev["id"]
        lat = ev["lat"]
        lon = ev["lon"]
        date_str = event_dates.get(eid, "2020-01-01")
        dt_event = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        # Bounding box (+/- 0.15 degrees ~ 16 km radius)
        bbox = [
            round(lon - 0.15, 4),
            round(lat - 0.15, 4),
            round(lon + 0.15, 4),
            round(lat + 0.15, 4)
        ]

        # Sensor selection based on era
        if dt_event.year >= 2016:
            primary_sensor = "Sentinel-2 L2A (10m Multispectral) & PlanetScope (3m)"
            stac_collection = "sentinel-2-l2a"
        elif dt_event.year >= 2013:
            primary_sensor = "Landsat-8 OLI (15m/30m) & EO-1 ALI"
            stac_collection = "landsat-c2-l2"
        elif dt_event.year >= 1999:
            primary_sensor = "Landsat-7 ETM+ & ASTER (15m VNIR)"
            stac_collection = "landsat-c2-l2"
        else:
            primary_sensor = "Landsat-4/5 TM & Corona Declassified Reconnaissance"
            stac_collection = "landsat-c2-l1"

        pre_window = [
            (dt_event - datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            (dt_event - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        ]
        post_window = [
            (dt_event + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            (dt_event + datetime.timedelta(days=35)).strftime("%Y-%m-%d")
        ]

        # Geostationary rapid scan target sensors
        if dt_event.year >= 2014:
            geo_sensor = "INSAT-3D / INSAT-3DR TIR (10.8µm) & Sounder (4km, 15-30 min cadence)"
        elif dt_event.year >= 2002:
            geo_sensor = "Kalpana-1 (MetSat-1) VHRR Thermal IR (8km, 30 min cadence)"
        else:
            geo_sensor = "Meteosat-5/7 IODC (Indian Ocean Data Coverage, 5km)"

        # Linear scars diagnostic target
        item = {
            "rank": ev["rank"],
            "id": eid,
            "name": ev["name"],
            "date": date_str,
            "country": ev["country"],
            "coordinates": {"lat": lat, "lon": lon},
            "bounding_box_wsen": bbox,
            "target_linear_scar": {
                "origin_ridge": f"Crista e arestas de cume a montante de {ev.get('elevation', '').split('->')[0].strip()}",
                "runout_chute": f"Calha de drenagem convergindo para o vale em {lat}, {lon}",
                "diagnostic_feature": "Faixa linear contínua de decapagem de leito rochoso (bedrock stripping), remoção total de solo e supressão de NDVI",
                "dem_differencing_target": "Perda de volume vertical por comparação geodésica de DEM (SRTM / ALOS vs. Copernicus 30m / ArcticDEM)"
            },
            "satellite_pairs_pipeline": {
                "optical_mission": primary_sensor,
                "stac_collection": stac_collection,
                "pre_event_window": pre_window,
                "post_event_window": post_window,
                "cloud_filter": "< 25% cloud cover",
                "bands_required": ["Red (B04)", "Green (B03)", "Blue (B02)", "NIR (B08)", "SWIR-1 (B11)", "SWIR-2 (B12)"],
                "derived_indices": ["NDVI (Vegetation Stripping)", "NDWI (Flood Slurry)", "SWIR Composite (Bedrock Exposure)"]
            },
            "pre_blast_geostationary_and_radar": {
                "geostationary_satellite": geo_sensor,
                "pre_sound_window_utc": f"{date_str} T-03:00 to T-00:15 UTC",
                "key_observable": "Taxa de decréscimo de Brightness Temperature (T_bb < -60°C) indicando núcleo convectivo penetrante de crista",
                "doppler_radar_station": "IMD Mukteshwar / Srinagar / Kufri (com mapeamento de beam blockage orográfico)"
            }
        }
        catalog.append(item)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"Satellite search catalog generated for all 15 events at {output_path}")
    return catalog

if __name__ == "__main__":
    base_dir = r"C:\Users\haas\github\Himalaia_2026"
    ev_path = os.path.join(base_dir, "data", "himalayan_events_1980_2026.json")
    out_path = os.path.join(base_dir, "data", "satellite_imagery", "sentinel_pairs_index.json")
    build_satellite_search_catalog(ev_path, out_path)
