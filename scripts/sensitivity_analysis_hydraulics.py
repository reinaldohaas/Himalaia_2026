# -*- coding: utf-8 -*-
"""
scripts/sensitivity_analysis_hydraulics.py
Parametric Sensitivity Analysis for Catchment Inverse Hydrology
Demonstrates under which physical conditions a water deficit exists or vanishes
when varying total_bulk_m3 (+-30%), basin_area_km2 (15 to 100 km2), and measured precipitation.
"""

import os
import yaml
import pandas as pd
import numpy as np

def run_sensitivity_analysis():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cfg_path = os.path.join(repo_dir, "config", "hydraulic_assumptions.yaml")
    out_csv = os.path.join(repo_dir, "data", "processed", "sensitivity_analysis_hydraulics.csv")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    events_to_test = ["himalaia_2026", "kedarnath_2013"]
    results = []

    print("=" * 90)
    print("  CATCHMENT INVERSE HYDROLOGY: PARAMETRIC SENSITIVITY ANALYSIS")
    print("=" * 90)

    for eid in events_to_test:
        ev = cfg["events"][eid]
        name = ev["name"]
        hydro = ev["hydrology"]
        v_bulk_base = float(hydro["total_bulk_m3"]["value"])
        Cv = float(hydro["Cv"]["value"])
        v_lake = float(hydro["lake_vol_m3"]["value"])
        c_runoff = float(hydro["C_runoff"]["value"])
        baseflow_q = hydro.get("baseflow_m3_s", {}).get("value", 0.0)
        dur_h = hydro.get("flood_duration_hours", {}).get("value", 4.0)
        v_baseflow = float(baseflow_q) * float(dur_h) * 3600.0 if baseflow_q else 0.0

        print(f"\n[EVENTO: {name}]")
        print(f"  Base: V_bulk={v_bulk_base/1e6:.2f}M m3, Cv={Cv}, V_lake={v_lake/1e6:.2f}M m3, V_baseflow={v_baseflow/1e6:.2f}M m3")

        v_bulk_factors = [0.70, 0.85, 1.00, 1.15, 1.30]  # +-30%
        basin_areas = [15.0, 28.0, 42.0, 55.0, 65.7, 85.0, 100.0]  # km2
        p_hypothetical = [20.0, 40.0, 60.0, 87.0, 110.0, 150.0, 200.0, 325.0]  # mm

        for factor in v_bulk_factors:
            v_bulk = v_bulk_base * factor
            v_water_gross = v_bulk * (1.0 - Cv)
            v_runoff_req = max(0.0, v_water_gross - v_lake - v_baseflow)

            for area in basin_areas:
                area_m2 = area * 1e6
                p_req = (v_runoff_req / (area_m2 * c_runoff)) * 1000.0

                for p_meas in p_hypothetical:
                    ratio = p_req / p_meas if p_meas > 0 else float("inf")
                    deficit_exists = (ratio > 1.0)
                    results.append({
                        "event_id": eid,
                        "event_name": name,
                        "v_bulk_factor": factor,
                        "v_bulk_m3": round(v_bulk, 1),
                        "v_water_gross_m3": round(v_water_gross, 1),
                        "v_runoff_req_m3": round(v_runoff_req, 1),
                        "basin_area_km2": area,
                        "c_runoff": c_runoff,
                        "p_req_mm": round(p_req, 1),
                        "p_meas_tested_mm": p_meas,
                        "deficit_multiplier": round(ratio, 2) if ratio != float("inf") else "INFINITY",
                        "deficit_status": "DEFICIT" if deficit_exists else "SEM_DEFICIT"
                    })

    df = pd.DataFrame(results)
    df.to_csv(out_csv, index=False)
    print(f"\nAnálise gravada em: {out_csv} ({len(df)} simulações)")

    # Resumo Himalaia 2026
    df_2026 = df[(df["event_id"] == "himalaia_2026") & (df["v_bulk_factor"] == 1.0)]
    print("\n[RESUMO: HIMALAIA 2026 - V_bulk base = 20.7M m3, Cv = 0.314, V_lake = 7.54M, V_baseflow = 2.59M]")
    print(f"{'Área (km2)':<12} | {'P_req (mm)':<12} | {'Ratio em P=22mm':<18} | {'Ratio em P=60mm':<18} | {'P_crit p/ zerar deficit':<22}")
    print("-" * 88)
    for area in [15.0, 28.0, 55.0, 65.7, 100.0]:
        sub = df_2026[df_2026["basin_area_km2"] == area]
        p_req = sub["p_req_mm"].iloc[0]
        m22 = round(p_req / 22.0, 2)
        m60 = round(p_req / 60.0, 2)
        print(f"{area:<12.1f} | {p_req:<12.1f} | {m22:<18.2f}x | {m60:<18.2f}x | {p_req:<22.1f} mm")

    # Resumo Kedarnath 2013
    df_ked = df[(df["event_id"] == "kedarnath_2013") & (df["v_bulk_factor"] == 1.0)]
    print("\n[RESUMO: KEDARNATH 2013 - V_bulk base = 7.2M m3, P_real = 325 mm]")
    print(f"{'Área (km2)':<12} | {'P_req (mm)':<12} | {'Ratio em P=35mm':<18} | {'Ratio em P=325mm (Real)':<28} | {'Status Real':<15}")
    print("-" * 90)
    for area in [28.0, 42.0, 55.0]:
        sub = df_ked[df_ked["basin_area_km2"] == area]
        p_req = sub["p_req_mm"].iloc[0]
        m35 = round(p_req / 35.0, 2)
        m325 = round(p_req / 325.0, 2)
        status_real = "SEM DÉFICIT" if m325 <= 1.0 else "DÉFICIT"
        print(f"{area:<12.1f} | {p_req:<12.1f} | {m35:<18.2f}x | {m325:<28.2f}x | {status_real:<15}")

    return df

if __name__ == "__main__":
    run_sensitivity_analysis()
