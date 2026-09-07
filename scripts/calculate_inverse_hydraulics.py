# -*- coding: utf-8 -*-
"""
scripts/calculate_inverse_hydraulics.py
Unified Inverse Hydrology & First-Principles Thermodynamics Calculator (Audit-Compliant)
Reads transparent assumptions from config/hydraulic_assumptions.yaml.
Distinguishes solid mass movements (avalanches) from rainfall floods and handles missing data honestly.
"""

import json
import math
import os
import yaml

def calculate_hydraulics_and_thermodynamics(events_path, config_path, output_path):
    with open(events_path, 'r', encoding='utf-8') as f:
        events = json.load(f)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    event_configs = config.get("events", {})
    results = []

    for ev in events:
        eid = ev["id"]
        cp = event_configs.get(eid)
        if not cp:
            continue

        # 1. Hydraulic Channel Properties (Manning)
        geom = cp.get("channel_geometry", {})
        B = float(geom["B"]["value"])
        z = float(geom["z"]["value"])
        dh = float(geom["dh"]["value"])
        S0 = float(geom["S0"]["value"])
        n = float(geom["n"]["value"])

        # Cross-section geometry
        A = (B + z * dh) * dh
        P = B + 2 * dh * math.sqrt(1 + z * z)
        Rh = A / P
        v_manning = (1.0 / n) * (Rh ** (2.0 / 3.0)) * math.sqrt(S0)
        q_peak_manning = A * v_manning

        # Froude number
        g = 9.80665
        T = B + 2 * z * dh # Top width
        D = A / T          # Hydraulic depth
        froude = v_manning / math.sqrt(g * D)

        # 2. Bulk & Net Liquid Water Separation
        hydro = cp.get("hydrology", {})
        total_bulk = float(hydro["total_bulk_m3"]["value"])
        Cv = float(hydro["Cv"]["value"])
        v_solids = total_bulk * Cv
        v_water_gross = total_bulk * (1.0 - Cv)

        # Lake volume
        lake_vol = float(hydro["lake_vol_m3"]["value"])
        if lake_vol > 0:
            lake_deficit_ratio = round(v_water_gross / lake_vol, 2)
        else:
            lake_deficit_ratio = "NO_LAKE (Inapplicable)"

        # Baseflow volume subtraction
        baseflow_q = hydro.get("baseflow_m3_s", {}).get("value")
        flood_hours = hydro.get("flood_duration_hours", {}).get("value")
        if baseflow_q is not None and flood_hours is not None:
            v_baseflow = float(baseflow_q) * float(flood_hours) * 3600.0
        elif baseflow_q is not None:
            # Assume 4h duration if unspecified
            v_baseflow = float(baseflow_q) * 4.0 * 3600.0
        else:
            v_baseflow = 0.0

        v_runoff_req = max(0.0, v_water_gross - lake_vol - v_baseflow)

        # 3. Thermodynamics of Frictional Melting
        thermo = cp.get("thermodynamics", {})
        mass = float(thermo["mass_kg"]["value"])
        delta_H = float(thermo["delta_H_m"]["value"])
        Ep_joules = mass * g * delta_H
        Lf = 334000.0 # J/kg
        eta = float(thermo["eta_frict"]["value"])
        m_melt_max_kg = (Ep_joules * eta) / Lf
        v_melt_max_m3 = m_melt_max_kg / 1000.0
        melt_pct_of_water = (v_melt_max_m3 / v_water_gross) * 100.0 if v_water_gross > 0 else 0.0

        # 4. Precipitation Balance
        basin_area_km2 = float(hydro["basin_area_km2"]["value"])
        basin_area_m2 = basin_area_km2 * 1e6
        C_runoff = float(hydro["C_runoff"]["value"])
        p_req_mm = (v_runoff_req / (basin_area_m2 * C_runoff)) * 1000.0

        precip_info = cp.get("precipitation", {}).get("p_meas_mm", {})
        p_meas = precip_info.get("value")
        p_source = precip_info.get("source", "N/A")
        p_notes = precip_info.get("notes", "")

        event_type = cp.get("event_type", "Debris Flood / GLOF")

        if p_meas is None:
            deficit_multiplier = None
            deficit_status = "[DADO INDISPONÍVEL — Requer dados pluviométricos reais / NASA Earthdata]"
        elif "avalanche" in event_type.lower() or "collapse" in event_type.lower() or "frictional" in event_type.lower():
            deficit_multiplier = "NOT_APPLICABLE"
            deficit_status = "Inaplicável: movimento de massa sólida de rocha/gelo sem dependência de chuva"
        elif p_meas > 0:
            ratio = p_req_mm / p_meas
            deficit_multiplier = round(ratio, 2)
            if ratio <= 0.0:
                deficit_status = "SEM DÉFICIT (Volume do lago ou vazão de base suprem integralmente a fase líquida)"
            elif ratio <= 1.0:
                folga = round(1.0 / ratio, 2)
                deficit_status = f"SEM DÉFICIT (Precipitação observada cobre com folga de {folga}x)"
            else:
                deficit_status = f"DÉFICIT APARENTE ({deficit_multiplier}x da referência pontual)"
        else:
            deficit_multiplier = "INFINITY (Zero gauge)"
            deficit_status = "Inexistência de chuva registrada no pluviômetro local"

        res = {
            "rank": ev["rank"],
            "id": eid,
            "name": ev["name"],
            "country": ev["country"],
            "date": ev["date"],
            "event_type": event_type,
            "provenance_notice": "Parâmetros hidráulicos e geomorfológicos carregados de config/hydraulic_assumptions.yaml.",
            "catchment_hydraulics": {
                "cross_section_B_m": B,
                "stage_rise_dh_m": dh,
                "bed_slope_S0": S0,
                "manning_n": n,
                "flow_area_m2": round(A, 1),
                "hydraulic_radius_m": round(Rh, 2),
                "velocity_m_s": round(v_manning, 2),
                "froude_number": round(froude, 2),
                "flow_regime": "Supercrítico (Fr > 1)" if froude > 1.0 else "Subcrítico (Fr < 1)",
                "q_peak_m3_s": round(q_peak_manning, 1)
            },
            "mass_balance": {
                "total_bulk_m3": total_bulk,
                "Cv_solids": Cv,
                "solid_volume_m3": round(v_solids, 1),
                "gross_liquid_water_m3": round(v_water_gross, 1),
                "lake_volume_m3": lake_vol,
                "baseflow_volume_m3": round(v_baseflow, 1),
                "net_runoff_required_m3": round(v_runoff_req, 1),
                "lake_deficit_ratio": lake_deficit_ratio
            },
            "thermodynamics_frictional_melt": {
                "potential_energy_TJ": round(Ep_joules / 1e12, 2),
                "frictional_efficiency_eta": eta,
                "max_frictional_water_m3": round(v_melt_max_m3, 1),
                "frictional_water_pct_of_flood": round(melt_pct_of_water, 2),
                "physical_limit_note": f"Fusão por atrito explica no máximo {round(melt_pct_of_water, 1)}% da fase líquida."
            },
            "precipitation_balance": {
                "effective_basin_area_km2": basin_area_km2,
                "required_precip_mm": round(p_req_mm, 1),
                "measured_precip_mm": p_meas,
                "precip_source": p_source,
                "precip_notes": p_notes,
                "deficit_multiplier": deficit_multiplier,
                "deficit_status": deficit_status
            }
        }
        results.append(res)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Inverse hydraulics audit complete. Results saved to {output_path}")
    return results

if __name__ == "__main__":
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ev_path = os.path.join(repo_dir, "data", "himalayan_events_1980_2026.json")
    cfg_path = os.path.join(repo_dir, "config", "hydraulic_assumptions.yaml")
    out_path = os.path.join(repo_dir, "data", "catchment_hydraulics", "inverse_hydraulics_all_events.json")
    calculate_hydraulics_and_thermodynamics(ev_path, cfg_path, out_path)
