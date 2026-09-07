# -*- coding: utf-8 -*-
"""
scripts/extract_solar_forcing.py
Compiles Space Weather, GOES Solar Flare X-ray, OMNI Solar Wind, and Jz Coupling Data
for all 15 Himalayan Catastrophes (1980-2026).
"""

import json
import os

def generate_solar_forcing_dataset(events_path, output_path):
    with open(events_path, 'r', encoding='utf-8') as f:
        events = json.load(f)

    solar_data = []

    for ev in events:
        entry = {
            "rank": ev["rank"],
            "id": ev["id"],
            "name": ev["name"],
            "date": ev["date"],
            "country": ev["country"],
            "solar_flare": {
                "flare_class": ev.get("solar_flare_class", "N/A"),
                "time_utc": ev.get("solar_flare_time", "N/A"),
                "xray_flux_w_m2": ev.get("solar_xray_flux", "N/A"),
                "delay_hours": ev.get("solar_delay", "N/A"),
                "kp_index": ev.get("solar_kp", "N/A")
            },
            "electrodynamics_coupling": {
                "ionospheric_potential_vi": ev.get("solar_vi", "N/A"),
                "jz_peak_density": ev.get("solar_jz_peak", "N/A"),
                "atmospheric_physics": ev.get("solar_physics", "N/A")
            },
            "lightning_activity_20km": {
                "total_count": ev.get("lightning_20km_count", 0),
                "density_per_km2": ev.get("lightning_20km_density", 0.0),
                "ic_pct": ev.get("lightning_20km_ic_pct", 0.0),
                "cg_pct": ev.get("lightning_20km_cg_pct", 0.0),
                "positive_cg_pct": ev.get("lightning_20km_pos_pct", 0.0),
                "upward_discharges": ev.get("lightning_20km_upward", 0),
                "peak_current": ev.get("lightning_20km_peak_kA", "N/A"),
                "time_window": ev.get("lightning_20km_window_desc", "N/A")
            }
        }
        solar_data.append(entry)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(solar_data, f, ensure_ascii=False, indent=2)

    print(f"Solar forcing dataset generated successfully at {output_path}")
    return solar_data

if __name__ == "__main__":
    base_dir = r"C:\Users\haas\github\Himalaia_2026"
    ev_path = os.path.join(base_dir, "data", "himalayan_events_1980_2026.json")
    out_path = os.path.join(base_dir, "data", "solar_space_weather", "solar_forcing_all_events.json")
    generate_solar_forcing_dataset(ev_path, out_path)
