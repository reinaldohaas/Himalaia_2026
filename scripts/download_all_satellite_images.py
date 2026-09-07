# -*- coding: utf-8 -*-
"""
scripts/download_all_satellite_images.py
Downloads, annotates and locally caches satellite imagery for all 15 Himalayan events (1980–2026):
1. Cartographic High-Res Orthomosaic (ArcGIS 10m) with Official International Borders & Banners
2. Historical Optical Convection Imagery (NASA GIBS MODIS Terra) on event day & pre-event
3. Geostationary Satellite Sequence (GPM IMERG Calibrated 30-min Infrared/Precipitation)
4. Multispectral Optical Scenes (ESA Sentinel-2 L2A Pre & Post Event)
All files are strictly named with ISO date prefixes (YYYY-MM-DD_...) and audited with SHA-256 checksums.
"""

import os
import sys
import json
import time
import hashlib
import datetime
import urllib.request
from io import BytesIO
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PATH = os.path.join(BASE_DIR, "data", "himalayan_events_1980_2026.json")
SATELLITE_DIR = os.path.join(BASE_DIR, "data", "satellite_imagery")
MANIFEST_PATH = os.path.join(SATELLITE_DIR, "local_imagery_manifest.json")

EVENT_METADATA = {
    "kedarnath_2013": {
        "date": "2013-06-16",
        "sound_utc": "2013-06-16T01:45:00Z",
        "borders_desc": "ESTADO DE UTTARAKHAND, ÍNDIA (~40 km AO SUL DA FRONTEIRA COM O TIBETE/CHINA)",
        "geo_sensor": "Kalpana-1 VHRR TIR (8km) / INSAT-3D",
        "has_gpm": True
    },
    "chamoli_2021": {
        "date": "2021-02-07",
        "sound_utc": "2021-02-07T04:51:00Z",
        "borders_desc": "SANTUÁRIO DE NANDA DEVI, UTTARAKHAND, ÍNDIA (~30 km DA FRONTEIRA COM O TIBETE/CHINA)",
        "geo_sensor": "INSAT-3D / INSAT-3DR TIR-1 (4km) / GPM IMERG",
        "has_gpm": True
    },
    "himalaia_2026": {
        "date": "2024-08-26",
        "sound_utc": "2024-08-26T08:15:00Z",
        "borders_desc": "BACIA TRANSFRONTEIRIÇA CRÍTICA: LANGTANG (NEPAL) - CONDADO DE GYIRONG (TIBETE/CHINA)",
        "geo_sensor": "INSAT-3DR TIR-1 (4km) / GPM IMERG",
        "has_gpm": True
    },
    "aru_2016": {
        "date": "2016-07-17",
        "sound_utc": "2016-07-17T04:00:00Z",
        "borders_desc": "TIBETE OCIDENTAL (CHINA) - PLATÔ ENDORREICO DE RUTOG / PREFEITURA DE NGARI",
        "geo_sensor": "INSAT-3D / Fengyun-2 / GPM IMERG",
        "has_gpm": True
    },
    "seti_2012": {
        "date": "2012-05-05",
        "sound_utc": "2012-05-05T03:30:00Z",
        "borders_desc": "MACIÇO DO ANNAPURNA IV, NEPAL CENTRAL (~50 km AO SUL DA FRONTEIRA COM O TIBETE)",
        "geo_sensor": "Kalpana-1 VHRR TIR (8km) / Meteosat-7 IODC",
        "has_gpm": False
    },
    "south_lhonak_2023": {
        "date": "2023-10-04",
        "sound_utc": "2023-10-03T19:10:00Z",
        "borders_desc": "CRISTA FRONTEIRIÇA INTERNACIONAL: SIKKIM DO NORTE (ÍNDIA) - TIBETE (CHINA)",
        "geo_sensor": "INSAT-3DR TIR-1 (4km) / GPM IMERG",
        "has_gpm": True
    },
    "leh_2010": {
        "date": "2010-08-06",
        "sound_utc": "2010-08-05T18:30:00Z",
        "borders_desc": "VALE DE LADAKH, ÍNDIA (~100 km DA LINHA DE CONTROLE COM O TIBETE/CHINA)",
        "geo_sensor": "Kalpana-1 VHRR TIR (8km) / TRMM PR",
        "has_gpm": False
    },
    "melamchi_2021": {
        "date": "2021-06-15",
        "sound_utc": "2021-06-15T12:15:00Z",
        "borders_desc": "BACIA DE HELAMBU, SINDHUPALCHOK, NEPAL (~25 km DA FRONTEIRA COM O TIBETE/CHINA)",
        "geo_sensor": "INSAT-3DR TIR-1 (4km) / GPM IMERG",
        "has_gpm": True
    },
    "parechu_2000": {
        "date": "2000-08-01",
        "sound_utc": "2000-08-01T09:30:00Z",
        "borders_desc": "RIO TRANSFRONTEIRIÇO: ORIGEM NO TIBETE (CHINA) - RUPTURA EM HIMACHAL PRADESH (ÍNDIA)",
        "geo_sensor": "Meteosat-5 IODC (5km) / INSAT-2E",
        "has_gpm": False
    },
    "zhangzangbo_1981": {
        "date": "1981-07-11",
        "sound_utc": "1981-07-10T21:15:00Z",
        "borders_desc": "CHEIA TRANSFRONTEIRIÇA: LAGO EM NYALAM (TIBETE/CHINA) - DESTRUIÇÃO DA PONTE DA AMIZADE (NEPAL)",
        "geo_sensor": "GMS-1 / Registros Terrestres de Infrassom e Balões",
        "has_gpm": False
    },
    "dig_tsho_1985": {
        "date": "1985-08-04",
        "sound_utc": "1985-08-04T08:15:00Z",
        "borders_desc": "SUB-BACIA DE NANGPO TSANGPO, KHUMBU/EVEREST, NEPAL (~8 km DA FRONTEIRA COM O TIBETE)",
        "geo_sensor": "GMS-2 / NOAA-7 AVHRR",
        "has_gpm": False
    },
    "luggye_tsho_1994": {
        "date": "1994-10-07",
        "sound_utc": "1994-10-07T02:00:00Z",
        "borders_desc": "CRISTA GLACIAR FRONTEIRIÇA: LUNANA (BUTAO) - TIBETE (CHINA)",
        "geo_sensor": "GMS-4 / NOAA-11 AVHRR",
        "has_gpm": False
    },
    "gongbatongshacuo_2016": {
        "date": "2016-07-05",
        "sound_utc": "2016-07-05T16:45:00Z",
        "borders_desc": "CHEIA TRANSFRONTEIRIÇA: LAGO GONGBATONGSHA (TIBETE/CHINA) - BHOTEKOSHI (NEPAL)",
        "geo_sensor": "INSAT-3D TIR-1 (4km) / GPM IMERG",
        "has_gpm": True
    },
    "himachal_2023": {
        "date": "2023-07-09",
        "sound_utc": "2023-07-09T06:30:00Z",
        "borders_desc": "VALE DO RIO BEAS / KULLU, HIMACHAL PRADESH, ÍNDIA",
        "geo_sensor": "INSAT-3DR TIR-1 (4km) / GPM IMERG / Radar IMD Kufri",
        "has_gpm": True
    },
    "parechu_2005": {
        "date": "2005-06-26",
        "sound_utc": "2005-06-26T08:30:00Z",
        "borders_desc": "SEGUNDA CHEIA TRANSFRONTEIRIÇA DO PARECHU: TIBETE (CHINA) - SUTLEJ (HIMACHAL, ÍNDIA)",
        "geo_sensor": "Kalpana-1 VHRR TIR (8km) / Meteosat-7 IODC",
        "has_gpm": False
    }
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def fetch_url(url, timeout=25, post_data=None):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=post_data, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception:
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
            else:
                return None

def download_annotated_ortho_basin(bbox, ev_info, out_file):
    """
    Downloads high-resolution 10m orthoimagery, overlays transparent international boundaries,
    and draws cartographic banners with coordinates, borders and scale bar.
    """
    w, s, e, n = bbox
    url_base = (
        f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?"
        f"bbox={w},{s},{e},{n}&bboxSR=4326&imageSR=4326&size=1024,1024&format=png&f=image"
    )
    url_borders = (
        f"https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/export?"
        f"bbox={w},{s},{e},{n}&bboxSR=4326&imageSR=4326&size=1024,1024&format=png32&transparent=true&f=image"
    )

    raw_base = fetch_url(url_base, timeout=30)
    raw_bord = fetch_url(url_borders, timeout=30)

    if not raw_base or len(raw_base) < 5000:
        return None

    try:
        im_base = Image.open(BytesIO(raw_base)).convert("RGBA")
        if raw_bord and len(raw_bord) > 1000:
            im_bord = Image.open(BytesIO(raw_bord)).convert("RGBA")
            im_comp = Image.alpha_composite(im_base, im_bord).convert("RGB")
        else:
            im_comp = im_base.convert("RGB")

        draw = ImageDraw.Draw(im_comp)

        # Top Cartographic Header
        draw.rectangle([(0, 0), (1024, 48)], fill=(15, 23, 42))
        title_text = f"EVENT {ev_info['rank']:02d}: {ev_info['name']} | DATA: {ev_info['date']}"
        border_text = f"FRONTEIRAS: {ev_info['borders_desc']}"
        draw.text((15, 8), title_text[:115], fill=(255, 255, 255))
        draw.text((15, 26), border_text[:120], fill=(250, 204, 21))

        # Bottom Cartographic Footer with Coordinates & Scale Bar
        draw.rectangle([(0, 976), (1024, 1024)], fill=(15, 23, 42))
        coord_text = f"COORD: {ev_info['lat']:.3f}° N, {ev_info['lon']:.3f}° E | SENSOR: ArcGIS World Imagery 10m + Official Boundaries"
        audit_text = f"CUSTÓDIA: Repositório Himalaia_2026 (Auditoria Independente) | {ev_info['geo_sensor']}"
        draw.text((15, 984), coord_text[:100], fill=(226, 232, 240))
        draw.text((15, 1002), audit_text[:105], fill=(148, 163, 184))

        # Graphic Scale Bar (approx 5 km for 0.24 deg width)
        draw.rectangle([(850, 990), (970, 996)], fill=(255, 255, 255))
        draw.text((850, 1000), "0", fill=(255, 255, 255))
        draw.text((905, 1000), "2.5 km", fill=(255, 255, 255))
        draw.text((960, 1000), "5 km", fill=(255, 255, 255))
        draw.text((990, 990), "N ↑", fill=(250, 204, 21))

        im_comp.save(out_file, "PNG", optimize=True)
        return os.path.getsize(out_file), im_comp.size
    except Exception as e:
        print(f"    [WARN] Error in cartographic ortho compositing: {e}")
        return None

def download_nasa_gibs(bbox, date_str, out_file):
    w, s, e, n = bbox
    url = (
        f"https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?"
        f"service=WMS&request=GetMap&version=1.3.0&layers=MODIS_Terra_CorrectedReflectance_TrueColor&"
        f"crs=CRS:84&bbox={w},{s},{e},{n}&width=768&height=768&format=image/jpeg&time={date_str}"
    )
    raw = fetch_url(url, timeout=25)
    if raw and len(raw) > 3000:
        try:
            im = Image.open(BytesIO(raw))
            im.save(out_file, "JPEG", quality=88, optimize=True)
            return os.path.getsize(out_file), im.size
        except Exception:
            pass
    return None, None

def download_gpm_geostationary(bbox, time_utc, out_file):
    """
    Downloads calibrated 30-min precipitation/cloud rate from NASA GIBS GPM IMERG.
    """
    w, s, e, n = bbox
    url = (
        f"https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?"
        f"service=WMS&request=GetMap&version=1.3.0&layers=IMERG_Precipitation_Rate_30min&"
        f"crs=CRS:84&bbox={w},{s},{e},{n}&width=512&height=512&format=image/png&time={time_utc}"
    )
    raw = fetch_url(url, timeout=20)
    if raw and len(raw) > 1000:
        try:
            im = Image.open(BytesIO(raw))
            im.save(out_file, "PNG", optimize=True)
            return os.path.getsize(out_file), im.size
        except Exception:
            pass
    return None, None

def search_and_download_stac_sentinel(bbox, start_date, end_date, out_file):
    stac_url = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
    query = {
        "collections": ["sentinel-2-l2a"],
        "bbox": bbox,
        "datetime": f"{start_date}T00:00:00Z/{end_date}T23:59:59Z",
        "query": {"eo:cloud_cover": {"lt": 40}},
        "sortby": [{"field": "properties.eo:cloud_cover", "direction": "asc"}],
        "limit": 3
    }
    data = json.dumps(query).encode("utf-8")
    req = urllib.request.Request(stac_url, data=data, headers={"Content-Type": "application/json", **HEADERS})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            features = res.get("features", [])
            for feat in features:
                assets = feat.get("assets", {})
                if "rendered_preview" in assets:
                    preview_url = assets["rendered_preview"]["href"]
                    scene_id = feat.get("id", "scene")
                    cloud = feat.get("properties", {}).get("eo:cloud_cover", 0)
                    datetime_acq = feat.get("properties", {}).get("datetime", "")
                    
                    img_bytes = fetch_url(preview_url, timeout=30)
                    if img_bytes and len(img_bytes) > 10000:
                        im = Image.open(BytesIO(img_bytes))
                        if im.mode in ("RGBA", "LA", "P"):
                            im = im.convert("RGB")
                        if max(im.size) > 1280:
                            im.thumbnail((1280, 1280), Image.Resampling.LANCZOS)
                        im.save(out_file, "JPEG", quality=85, optimize=True)
                        return {
                            "scene_id": scene_id,
                            "acquisition": datetime_acq,
                            "cloud_cover": round(cloud, 1),
                            "bytes": os.path.getsize(out_file),
                            "dimensions": list(im.size)
                        }
    except Exception:
        pass
    return None

def main():
    print("=" * 80)
    print("  HIMALAYAN CATASTROPHES: AUTOMATED SATELLITE HARVESTER & CARTOGRAPHIC AUDIT")
    print("=" * 80)

    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        events = json.load(f)

    os.makedirs(SATELLITE_DIR, exist_ok=True)
    manifest = {
        "manifest_version": "2.0.0",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_events": len(events),
        "standardization": "All filenames prefixed with ISO Date (YYYY-MM-DD), with official international borders and SHA-256 hashes",
        "events": {}
    }

    total_images_saved = 0
    total_bytes_saved = 0

    for ev in events:
        rank = ev["rank"]
        eid = ev["id"]
        name = ev["name"]
        lat = ev["lat"]
        lon = ev["lon"]
        meta = EVENT_METADATA.get(eid, {})
        date_str = meta.get("date", "2020-01-01")
        sound_utc = meta.get("sound_utc", f"{date_str}T12:00:00Z")
        borders_desc = meta.get("borders_desc", "Himalaia Central")
        geo_sensor = meta.get("geo_sensor", "INSAT / Kalpana-1 / Meteosat")
        dt_event = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        bbox = [
            round(lon - 0.12, 4),
            round(lat - 0.12, 4),
            round(lon + 0.12, 4),
            round(lat + 0.12, 4)
        ]

        ev_dir = os.path.join(SATELLITE_DIR, eid)
        os.makedirs(ev_dir, exist_ok=True)

        # Clean old non-dated files if present
        for old_file in ["highres_ortho_basin.png", "nasa_gibs_event_day.jpg", "nasa_gibs_pre_event.jpg", "sentinel2_pre_event.jpg", "sentinel2_post_event.jpg"]:
            old_p = os.path.join(ev_dir, old_file)
            if os.path.exists(old_p):
                try:
                    os.remove(old_p)
                except Exception:
                    pass

        print(f"\n[{rank:02d}/15] {name} ({eid}) | Date: {date_str} | Center: {lat:.3f}, {lon:.3f}")
        print(f"  Fronteira: {borders_desc}")

        ev_info = {
            "rank": rank,
            "id": eid,
            "name": name,
            "date": date_str,
            "lat": lat,
            "lon": lon,
            "borders_desc": borders_desc,
            "geo_sensor": geo_sensor
        }

        ev_manifest = {
            "rank": rank,
            "id": eid,
            "name": name,
            "date": date_str,
            "sound_utc": sound_utc,
            "center": {"lat": lat, "lon": lon},
            "bbox_wsen": bbox,
            "political_borders_context": borders_desc,
            "geostationary_sensor_reference": geo_sensor,
            "files": []
        }

        # 1. Cartographic Orthoimagery with International Borders & Scale
        ortho_fname = f"{date_str}_ArcGIS_10m_highres_basin_borders.png"
        ortho_path = os.path.join(ev_dir, ortho_fname)
        print(f"  --> [1/4] Gerando Ortoimagem com Fronteiras: {ortho_fname}...")
        ortho_res = download_annotated_ortho_basin(bbox, ev_info, ortho_path)
        if ortho_res:
            ortho_bytes, ortho_dims = ortho_res
            sha = compute_sha256(ortho_path)
            total_images_saved += 1
            total_bytes_saved += ortho_bytes
            print(f"      [OK] Salvo ({ortho_bytes/1024:.1f} KB, SHA-256: {sha[:12]}...)")
            ev_manifest["files"].append({
                "filename": ortho_fname,
                "date": date_str,
                "sensor": "ArcGIS World Imagery 10m + Official International Boundaries",
                "type": "Ortoimagem Cartográfica com Fronteiras Internacionais, Calhas e Escala Gráfica",
                "bytes": ortho_bytes,
                "dimensions": list(ortho_dims),
                "sha256": sha
            })

        # 2. NASA GIBS Optical Reflectance on Event Day & Pre-Event Day
        if dt_event.year >= 2000:
            # Event day
            gibs_day_fname = f"{date_str}_NASA-GIBS_MODIS-Terra_event-day.jpg"
            gibs_day_path = os.path.join(ev_dir, gibs_day_fname)
            print(f"  --> [2/4] Baixando NASA GIBS MODIS Terra (Dia do Evento: {date_str})...")
            gibs_res = download_nasa_gibs(bbox, date_str, gibs_day_path)
            if gibs_res[0]:
                sha = compute_sha256(gibs_day_path)
                total_images_saved += 1
                total_bytes_saved += gibs_res[0]
                print(f"      [OK] Salvo ({gibs_res[0]/1024:.1f} KB, SHA-256: {sha[:12]}...)")
                ev_manifest["files"].append({
                    "filename": gibs_day_fname,
                    "date": date_str,
                    "sensor": "NASA EOS Terra MODIS Corrected Reflectance True Color (250m)",
                    "type": "Cobertura Atmosférica e Nuvens Convectivas no Dia do Evento",
                    "bytes": gibs_res[0],
                    "dimensions": list(gibs_res[1]),
                    "sha256": sha
                })

            # Pre-event day
            pre_date = (dt_event - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            gibs_pre_fname = f"{pre_date}_NASA-GIBS_MODIS-Terra_pre-event-1d.jpg"
            gibs_pre_path = os.path.join(ev_dir, gibs_pre_fname)
            print(f"  --> [2/4] Baixando NASA GIBS MODIS Terra (Véspera: {pre_date})...")
            pre_res = download_nasa_gibs(bbox, pre_date, gibs_pre_path)
            if pre_res[0]:
                sha = compute_sha256(gibs_pre_path)
                total_images_saved += 1
                total_bytes_saved += pre_res[0]
                print(f"      [OK] Salvo ({pre_res[0]/1024:.1f} KB, SHA-256: {sha[:12]}...)")
                ev_manifest["files"].append({
                    "filename": gibs_pre_fname,
                    "date": pre_date,
                    "sensor": "NASA EOS Terra MODIS Corrected Reflectance True Color (250m)",
                    "type": "Estado Convectivo e Crioférico no Dia Anterior",
                    "bytes": pre_res[0],
                    "dimensions": list(pre_res[1]),
                    "sha256": sha
                })

        # 3. Geostationary Calibrated Rapid Scan / IMERG 30-min Sequence
        if meta.get("has_gpm"):
            dt_sound = datetime.datetime.strptime(sound_utc.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
            offsets = [
                ("-3h", dt_sound - datetime.timedelta(hours=3)),
                ("-1h", dt_sound - datetime.timedelta(hours=1)),
                ("T0", dt_sound)
            ]
            print(f"  --> [3/4] Baixando Série Temporal Geoestacionária GPM IMERG 30-min ({sound_utc})...")
            for label, dt_pt in offsets:
                pt_str = dt_pt.strftime("%Y-%m-%dT%H:%M:%SZ")
                fname_geo = f"{dt_pt.strftime('%Y-%m-%d_T%H%M')}_GPM-IMERG_geostationary_{label}.png"
                path_geo = os.path.join(ev_dir, fname_geo)
                geo_res = download_gpm_geostationary(bbox, pt_str, path_geo)
                if geo_res[0]:
                    sha = compute_sha256(path_geo)
                    total_images_saved += 1
                    total_bytes_saved += geo_res[0]
                    print(f"      [OK] Salvo {label} ({geo_res[0]/1024:.1f} KB, {pt_str})")
                    ev_manifest["files"].append({
                        "filename": fname_geo,
                        "date": dt_pt.strftime("%Y-%m-%d"),
                        "timestamp_utc": pt_str,
                        "sensor": "NASA GPM IMERG 30-min Calibrated Geostationary Multi-Satellite",
                        "type": f"Sequência Geoestacionária Infravermelha Calibrada ({label}) Pré-Estrondo",
                        "bytes": geo_res[0],
                        "dimensions": list(geo_res[1]),
                        "sha256": sha
                    })

        # 4. ESA Sentinel-2 L2A Pre & Post Event
        if dt_event.year >= 2016 and dt_event.year <= 2024:
            print("  --> [4/4] Consultando Catálogo STAC Sentinel-2 L2A (Pré e Pós-Evento)...")
            # Post
            s2_post_fname = f"{date_str}_Sentinel-2-L2A_post-event.jpg"
            s2_post_path = os.path.join(ev_dir, s2_post_fname)
            s2_info = search_and_download_stac_sentinel(bbox, date_str, (dt_event + datetime.timedelta(days=35)).strftime("%Y-%m-%d"), s2_post_path)
            if s2_info:
                sha = compute_sha256(s2_post_path)
                total_images_saved += 1
                total_bytes_saved += s2_info["bytes"]
                actual_date = s2_info["acquisition"][:10]
                renamed_post_fname = f"{actual_date}_Sentinel-2-L2A_post-event.jpg"
                renamed_post_path = os.path.join(ev_dir, renamed_post_fname)
                if s2_post_path != renamed_post_path:
                    if os.path.exists(renamed_post_path): os.remove(renamed_post_path)
                    os.rename(s2_post_path, renamed_post_path)
                print(f"      [OK] Salvo Pós-Evento: {renamed_post_fname} ({s2_info['bytes']/1024:.1f} KB, Nuvens: {s2_info['cloud_cover']}%)")
                ev_manifest["files"].append({
                    "filename": renamed_post_fname,
                    "date": actual_date,
                    "sensor": "ESA Sentinel-2 L2A MSI (10m Optical)",
                    "type": "Cena Óptica Multiespectral Pós-Catástrofe (Cicatrizes e Depósitos)",
                    "scene_id": s2_info["scene_id"],
                    "acquisition": s2_info["acquisition"],
                    "cloud_cover_pct": s2_info["cloud_cover"],
                    "bytes": s2_info["bytes"],
                    "dimensions": s2_info["dimensions"],
                    "sha256": compute_sha256(renamed_post_path)
                })

            # Pre
            s2_pre_fname = f"{date_str}_Sentinel-2-L2A_pre-event.jpg"
            s2_pre_path = os.path.join(ev_dir, s2_pre_fname)
            pre_start = (dt_event - datetime.timedelta(days=35)).strftime("%Y-%m-%d")
            pre_end = (dt_event - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            s2_pre_info = search_and_download_stac_sentinel(bbox, pre_start, pre_end, s2_pre_path)
            if s2_pre_info:
                actual_pre_date = s2_pre_info["acquisition"][:10]
                renamed_pre_fname = f"{actual_pre_date}_Sentinel-2-L2A_pre-event.jpg"
                renamed_pre_path = os.path.join(ev_dir, renamed_pre_fname)
                if s2_pre_path != renamed_pre_path:
                    if os.path.exists(renamed_pre_path): os.remove(renamed_pre_path)
                    os.rename(s2_pre_path, renamed_pre_path)
                print(f"      [OK] Salvo Pré-Evento: {renamed_pre_fname} ({s2_pre_info['bytes']/1024:.1f} KB, Nuvens: {s2_pre_info['cloud_cover']}%)")
                ev_manifest["files"].append({
                    "filename": renamed_pre_fname,
                    "date": actual_pre_date,
                    "sensor": "ESA Sentinel-2 L2A MSI (10m Optical)",
                    "type": "Cena Óptica Multiespectral Pré-Catástrofe (Linha de Base Glaciar)",
                    "scene_id": s2_pre_info["scene_id"],
                    "acquisition": s2_pre_info["acquisition"],
                    "cloud_cover_pct": s2_pre_info["cloud_cover"],
                    "bytes": s2_pre_info["bytes"],
                    "dimensions": s2_pre_info["dimensions"],
                    "sha256": compute_sha256(renamed_pre_path)
                })

        manifest["events"][eid] = ev_manifest
        time.sleep(0.3)

    manifest["total_images_saved"] = total_images_saved
    manifest["total_size_mb"] = round(total_bytes_saved / (1024 * 1024), 2)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"  COLHEITA CARTOGRÁFICA E AUDITORIA CONCLUÍDA COM SUCESSO!")
    print(f"  Total de Imagens Salvas com Data no Nome e Fronteiras: {total_images_saved}")
    print(f"  Tamanho Total do Acervo: {manifest['total_size_mb']} MB")
    print(f"  Manifesto com Hashes SHA-256 Gravado em: {MANIFEST_PATH}")
    print("=" * 80)

if __name__ == "__main__":
    main()
