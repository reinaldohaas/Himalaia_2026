# -*- coding: utf-8 -*-
"""
scripts/download_all_satellite_images.py
Downloads and locally caches satellite imagery for all 15 catastrophic Himalayan events (1980–2026):
1. ArcGIS World Imagery High-Resolution Orthoimagery (10m / sub-meter basin & scar views)
2. NASA GIBS Historical Optical/Convection Imagery (MODIS Terra True Color on event date and pre-event day)
3. Planetary Computer STAC Multispectral Previews (Sentinel-2 L2A / Landsat)
Generates data/satellite_imagery/local_imagery_manifest.json with full metadata for independent auditing.
"""

import os
import sys
import json
import time
import datetime
import urllib.request
import urllib.error
from io import BytesIO
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_PATH = os.path.join(BASE_DIR, "data", "himalayan_events_1980_2026.json")
SATELLITE_DIR = os.path.join(BASE_DIR, "data", "satellite_imagery")
MANIFEST_PATH = os.path.join(SATELLITE_DIR, "local_imagery_manifest.json")

# Accurate event anchor dates
EVENT_DATES = {
    "kedarnath_2013": "2013-06-16",
    "chamoli_2021": "2021-02-07",
    "himalaia_2026": "2024-08-26",  # Benchmark monsoon baseline for August
    "aru_2016": "2016-07-17",
    "seti_2012": "2012-05-05",
    "south_lhonak_2023": "2023-10-04",
    "leh_2010": "2010-08-06",
    "melamchi_2021": "2021-06-15",
    "parechu_2000": "2000-08-01",
    "zhangzangbo_1981": "1981-07-11",
    "dig_tsho_1985": "1985-08-04",
    "luggye_tsho_1994": "1994-10-07",
    "gongbatongshacuo_2016": "2016-07-05",
    "himachal_2023": "2023-07-09",
    "parechu_2005": "2005-06-26"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}

def fetch_url(url, timeout=25, post_data=None):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=post_data, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as e:
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
            else:
                print(f"    [WARN] Failed to fetch {url[:80]}... error: {e}")
                return None

def download_arcgis_ortho(bbox, out_file):
    """
    Downloads high-resolution orthoimagery from ArcGIS World Imagery export endpoint.
    Bbox format: [lon_min, lat_min, lon_max, lat_max]
    """
    w, s, e, n = bbox
    url = (
        f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?"
        f"bbox={w},{s},{e},{n}&bboxSR=4326&imageSR=4326&size=1024,1024&format=png&f=image"
    )
    raw = fetch_url(url, timeout=30)
    if raw and len(raw) > 5000:
        try:
            im = Image.open(BytesIO(raw))
            im.save(out_file, optimize=True)
            return len(raw), im.size
        except Exception as err:
            print(f"    [WARN] Image parsing error for ArcGIS ortho: {err}")
    return None, None

def download_nasa_gibs(bbox, date_str, out_file):
    """
    Downloads historical MODIS Terra Corrected Reflectance TrueColor from NASA GIBS WMS.
    """
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
            return len(raw), im.size
        except Exception as err:
            print(f"    [WARN] Image parsing error for NASA GIBS: {err}")
    return None, None

def search_and_download_stac_sentinel(bbox, start_date, end_date, out_file):
    """
    Searches Planetary Computer STAC for Sentinel-2 L2A scene and downloads rendered preview.
    """
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
                        if im.mode in ('RGBA', 'LA', 'P'):
                            im = im.convert('RGB')
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
    except Exception as e:
        print(f"    [WARN] STAC Sentinel-2 query error: {e}")
    return None

def main():
    print("=" * 75)
    print("  HIMALAYAN CATASTROPHES: AUTOMATED LOCAL SATELLITE IMAGERY HARVESTER")
    print("=" * 75)

    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        events = json.load(f)

    os.makedirs(SATELLITE_DIR, exist_ok=True)
    manifest = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_events": len(events),
        "imagery_directory": "data/satellite_imagery/",
        "events": {}
    }

    total_images_downloaded = 0
    total_bytes_downloaded = 0

    for ev in events:
        rank = ev["rank"]
        eid = ev["id"]
        name = ev["name"]
        lat = ev["lat"]
        lon = ev["lon"]
        date_str = EVENT_DATES.get(eid, "2020-01-01")
        dt_event = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        bbox = [
            round(lon - 0.12, 4),
            round(lat - 0.12, 4),
            round(lon + 0.12, 4),
            round(lat + 0.12, 4)
        ]

        ev_dir = os.path.join(SATELLITE_DIR, eid)
        os.makedirs(ev_dir, exist_ok=True)

        print(f"\n[{rank:02d}/15] {name} ({eid}) | Center: {lat:.3f}, {lon:.3f} | Date: {date_str}")
        ev_manifest = {
            "rank": rank,
            "id": eid,
            "name": name,
            "date": date_str,
            "center": {"lat": lat, "lon": lon},
            "bbox_wsen": bbox,
            "files": []
        }

        # 1. Download High-Res Orthoimagery (ArcGIS World Imagery)
        ortho_path = os.path.join(ev_dir, "highres_ortho_basin.png")
        print("  --> Fetching ArcGIS High-Res Ortho Basin (1024x1024)...")
        ortho_size, dims = download_arcgis_ortho(bbox, ortho_path)
        if ortho_size:
            total_images_downloaded += 1
            total_bytes_downloaded += os.path.getsize(ortho_path)
            print(f"      [OK] Saved {os.path.basename(ortho_path)} ({os.path.getsize(ortho_path)/1024:.1f} KB, {dims[0]}x{dims[1]})")
            ev_manifest["files"].append({
                "filename": "highres_ortho_basin.png",
                "sensor": "ArcGIS World Imagery High-Resolution Orthomosaic (Maxar/CNES/Copernicus)",
                "type": "Geomorphology, Drainage Chute & Moraine Scar Base",
                "bytes": os.path.getsize(ortho_path),
                "dimensions": list(dims),
                "date": "Composite Recent Cloud-Free"
            })
        else:
            print("      [FAIL] Could not fetch ArcGIS Ortho")

        # 2. Download NASA GIBS (MODIS Terra True Color) for events in 2000+
        if dt_event.year >= 2000:
            # Event day
            gibs_day_path = os.path.join(ev_dir, "nasa_gibs_event_day.jpg")
            print(f"  --> Fetching NASA GIBS MODIS Terra (Event Day: {date_str})...")
            gibs_size, g_dims = download_nasa_gibs(bbox, date_str, gibs_day_path)
            if gibs_size:
                total_images_downloaded += 1
                total_bytes_downloaded += os.path.getsize(gibs_day_path)
                print(f"      [OK] Saved {os.path.basename(gibs_day_path)} ({os.path.getsize(gibs_day_path)/1024:.1f} KB)")
                ev_manifest["files"].append({
                    "filename": "nasa_gibs_event_day.jpg",
                    "sensor": "NASA EOS Terra MODIS Corrected Reflectance TrueColor (250m)",
                    "type": "Atmospheric Convective Cells & Cloud Cover (Event Day)",
                    "bytes": os.path.getsize(gibs_day_path),
                    "dimensions": list(g_dims),
                    "date": date_str
                })

            # Pre-event day (1 to 2 days before)
            pre_date = (dt_event - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            gibs_pre_path = os.path.join(ev_dir, "nasa_gibs_pre_event.jpg")
            print(f"  --> Fetching NASA GIBS MODIS Terra (Pre-Event Day: {pre_date})...")
            pre_size, p_dims = download_nasa_gibs(bbox, pre_date, gibs_pre_path)
            if pre_size:
                total_images_downloaded += 1
                total_bytes_downloaded += os.path.getsize(gibs_pre_path)
                print(f"      [OK] Saved {os.path.basename(gibs_pre_path)} ({os.path.getsize(gibs_pre_path)/1024:.1f} KB)")
                ev_manifest["files"].append({
                    "filename": "nasa_gibs_pre_event.jpg",
                    "sensor": "NASA EOS Terra MODIS Corrected Reflectance TrueColor (250m)",
                    "type": "Pre-Event Convective State & Cryosphere Baseline",
                    "bytes": os.path.getsize(gibs_pre_path),
                    "dimensions": list(p_dims),
                    "date": pre_date
                })

        # 3. Download Sentinel-2 L2A multispectral scene for events 2016-2024
        if dt_event.year >= 2016 and dt_event.year <= 2024:
            s2_post_path = os.path.join(ev_dir, "sentinel2_post_event.jpg")
            start_search = date_str
            end_search = (dt_event + datetime.timedelta(days=35)).strftime("%Y-%m-%d")
            print(f"  --> Querying STAC Sentinel-2 L2A Post-Event ({start_search} to {end_search})...")
            s2_info = search_and_download_stac_sentinel(bbox, start_search, end_search, s2_post_path)
            if s2_info:
                total_images_downloaded += 1
                total_bytes_downloaded += s2_info["bytes"]
                print(f"      [OK] Saved {os.path.basename(s2_post_path)} ({s2_info['bytes']/1024:.1f} KB, Cloud: {s2_info['cloud_cover']}%, Acq: {s2_info['acquisition'][:10]})")
                ev_manifest["files"].append({
                    "filename": "sentinel2_post_event.jpg",
                    "sensor": "ESA Sentinel-2 L2A MSI (10m Optical)",
                    "type": "Post-Catastrophe Scars & Flood Deposition",
                    "scene_id": s2_info["scene_id"],
                    "acquisition": s2_info["acquisition"],
                    "cloud_cover_pct": s2_info["cloud_cover"],
                    "bytes": s2_info["bytes"],
                    "dimensions": s2_info["dimensions"]
                })

            # Also check pre-event Sentinel-2
            s2_pre_path = os.path.join(ev_dir, "sentinel2_pre_event.jpg")
            pre_start = (dt_event - datetime.timedelta(days=35)).strftime("%Y-%m-%d")
            pre_end = (dt_event - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            print(f"  --> Querying STAC Sentinel-2 L2A Pre-Event ({pre_start} to {pre_end})...")
            s2_pre_info = search_and_download_stac_sentinel(bbox, pre_start, pre_end, s2_pre_path)
            if s2_pre_info:
                total_images_downloaded += 1
                total_bytes_downloaded += s2_pre_info["bytes"]
                print(f"      [OK] Saved {os.path.basename(s2_pre_path)} ({s2_pre_info['bytes']/1024:.1f} KB, Cloud: {s2_pre_info['cloud_cover']}%, Acq: {s2_pre_info['acquisition'][:10]})")
                ev_manifest["files"].append({
                    "filename": "sentinel2_pre_event.jpg",
                    "sensor": "ESA Sentinel-2 L2A MSI (10m Optical)",
                    "type": "Pre-Catastrophe Lake & Slope Baseline",
                    "scene_id": s2_pre_info["scene_id"],
                    "acquisition": s2_pre_info["acquisition"],
                    "cloud_cover_pct": s2_pre_info["cloud_cover"],
                    "bytes": s2_pre_info["bytes"],
                    "dimensions": s2_pre_info["dimensions"]
                })

        manifest["events"][eid] = ev_manifest
        time.sleep(0.5)

    manifest["total_images_saved"] = total_images_downloaded
    manifest["total_size_mb"] = round(total_bytes_downloaded / (1024 * 1024), 2)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 75)
    print(f"  HARVEST COMPLETE!")
    print(f"  Total Images Saved: {total_images_downloaded}")
    print(f"  Total Size: {manifest['total_size_mb']} MB")
    print(f"  Manifest written to: {MANIFEST_PATH}")
    print("=" * 75)

if __name__ == "__main__":
    main()
