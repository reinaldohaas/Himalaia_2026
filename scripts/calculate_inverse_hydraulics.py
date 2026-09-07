# -*- coding: utf-8 -*-
"""
scripts/calculate_inverse_hydraulics.py
Unified Inverse Hydrology & First-Principles Thermodynamics Calculator
Applies the 2026 standardized physical methodology across all 15 Himalayan catastrophes (1980-2026).
"""

import json
import math
import os

def calculate_hydraulics_and_thermodynamics(events_path, output_path):
    with open(events_path, 'r', encoding='utf-8') as f:
        events = json.load(f)

    # Hydraulic parameters and catchment geometric data for each event
    # S0: bed slope, n: Manning roughness, B: base width (m), z: bank slope (1V:zH), dh: stage rise (m)
    # A_basin: effective upper basin area (km2), C_runoff: runoff coefficient
    catchment_params = {
        "kedarnath_2013": {
            "B": 24.0, "z": 0.4, "dh": 7.5, "S0": 0.055, "n": 0.055,
            "basin_area_km2": 42.0, "C_runoff": 0.85,
            "total_bulk_m3": 7.2e6, "Cv": 0.35, "lake_vol_m3": 0.38e6,
            "mass_kg": 1.2e10, "delta_H_m": 2900, "ice_fraction": 0.35, "eta_frict": 0.025,
            "p_meas_mm": 35.0 # Coarse grid / valley gauge
        },
        "chamoli_2021": {
            "B": 35.0, "z": 0.6, "dh": 12.0, "S0": 0.065, "n": 0.060,
            "basin_area_km2": 58.0, "C_runoff": 0.90,
            "total_bulk_m3": 18.5e6, "Cv": 0.42, "lake_vol_m3": 0.0, # Zero lake!
            "mass_kg": 6.7e10, "delta_H_m": 3400, "ice_fraction": 0.20, "eta_frict": 0.010, # Shugar et al. Science 2021: 1%
            "p_meas_mm": 0.0 # Dry winter day
        },
        "himalaia_2026": {
            "B": 30.0, "z": 0.5, "dh": 8.5, "S0": 0.045, "n": 0.060,
            "basin_area_km2": 65.7, "C_runoff": 0.85,
            "total_bulk_m3": 20.7e6, "Cv": 0.314, "lake_vol_m3": 5.2e6,
            "mass_kg": 4.0e10, "delta_H_m": 3200, "ice_fraction": 0.40, "eta_frict": 0.030,
            "p_meas_mm": 22.0 # GPM IMERG 10km grid
        },
        "aru_2016": {
            "B": 180.0, "z": 0.1, "dh": 6.0, "S0": 0.018, "n": 0.045,
            "basin_area_km2": 95.0, "C_runoff": 0.70,
            "total_bulk_m3": 68.0e6, "Cv": 0.20, "lake_vol_m3": 0.0,
            "mass_kg": 6.0e10, "delta_H_m": 1200, "ice_fraction": 0.85, "eta_frict": 0.008,
            "p_meas_mm": 5.0
        },
        "seti_2012": {
            "B": 28.0, "z": 0.5, "dh": 14.0, "S0": 0.070, "n": 0.065,
            "basin_area_km2": 72.0, "C_runoff": 0.85,
            "total_bulk_m3": 32.0e6, "Cv": 0.45, "lake_vol_m3": 0.0,
            "mass_kg": 7.5e10, "delta_H_m": 3800, "ice_fraction": 0.25, "eta_frict": 0.012,
            "p_meas_mm": 0.0
        },
        "south_lhonak_2023": {
            "B": 32.0, "z": 0.5, "dh": 9.5, "S0": 0.048, "n": 0.055,
            "basin_area_km2": 88.0, "C_runoff": 0.80,
            "total_bulk_m3": 28.0e6, "Cv": 0.30, "lake_vol_m3": 14.5e6,
            "mass_kg": 1.5e10, "delta_H_m": 2200, "ice_fraction": 0.30, "eta_frict": 0.015,
            "p_meas_mm": 18.0
        },
        "leh_2010": {
            "B": 18.0, "z": 0.3, "dh": 5.2, "S0": 0.050, "n": 0.050,
            "basin_area_km2": 35.0, "C_runoff": 0.80,
            "total_bulk_m3": 3.8e6, "Cv": 0.38, "lake_vol_m3": 0.0,
            "mass_kg": 5.0e9, "delta_H_m": 2100, "ice_fraction": 0.05, "eta_frict": 0.005,
            "p_meas_mm": 12.0
        },
        "melamchi_2021": {
            "B": 22.0, "z": 0.4, "dh": 7.0, "S0": 0.052, "n": 0.058,
            "basin_area_km2": 62.0, "C_runoff": 0.82,
            "total_bulk_m3": 12.5e6, "Cv": 0.36, "lake_vol_m3": 0.0,
            "mass_kg": 1.8e10, "delta_H_m": 2600, "ice_fraction": 0.20, "eta_frict": 0.015,
            "p_meas_mm": 28.0
        },
        "parechu_2000": {
            "B": 40.0, "z": 0.5, "dh": 11.0, "S0": 0.035, "n": 0.050,
            "basin_area_km2": 210.0, "C_runoff": 0.75,
            "total_bulk_m3": 45.0e6, "Cv": 0.28, "lake_vol_m3": 25.0e6,
            "mass_kg": 2.0e10, "delta_H_m": 1600, "ice_fraction": 0.10, "eta_frict": 0.010,
            "p_meas_mm": 8.0
        },
        "zhangzangbo_1981": {
            "B": 26.0, "z": 0.4, "dh": 8.8, "S0": 0.046, "n": 0.052,
            "basin_area_km2": 55.0, "C_runoff": 0.85,
            "total_bulk_m3": 19.0e6, "Cv": 0.32, "lake_vol_m3": 18.0e6,
            "mass_kg": 8.0e9, "delta_H_m": 2200, "ice_fraction": 0.25, "eta_frict": 0.015,
            "p_meas_mm": 15.0
        },
        "dig_tsho_1985": {
            "B": 20.0, "z": 0.4, "dh": 6.8, "S0": 0.058, "n": 0.055,
            "basin_area_km2": 32.0, "C_runoff": 0.80,
            "total_bulk_m3": 5.1e6, "Cv": 0.33, "lake_vol_m3": 5.0e6,
            "mass_kg": 6.5e9, "delta_H_m": 2400, "ice_fraction": 0.35, "eta_frict": 0.020,
            "p_meas_mm": 10.0
        },
        "luggye_tsho_1994": {
            "B": 35.0, "z": 0.5, "dh": 9.2, "S0": 0.040, "n": 0.054,
            "basin_area_km2": 110.0, "C_runoff": 0.80,
            "total_bulk_m3": 21.0e6, "Cv": 0.26, "lake_vol_m3": 17.0e6,
            "mass_kg": 1.2e10, "delta_H_m": 1900, "ice_fraction": 0.30, "eta_frict": 0.015,
            "p_meas_mm": 16.0
        },
        "bhotekoshi_2016": {
            "B": 25.0, "z": 0.4, "dh": 7.6, "S0": 0.050, "n": 0.056,
            "basin_area_km2": 48.0, "C_runoff": 0.82,
            "total_bulk_m3": 8.2e6, "Cv": 0.34, "lake_vol_m3": 4.5e6,
            "mass_kg": 9.0e9, "delta_H_m": 2100, "ice_fraction": 0.25, "eta_frict": 0.018,
            "p_meas_mm": 20.0
        },
        "himachal_2023": {
            "B": 45.0, "z": 0.6, "dh": 6.8, "S0": 0.038, "n": 0.048,
            "basin_area_km2": 180.0, "C_runoff": 0.85,
            "total_bulk_m3": 35.0e6, "Cv": 0.25, "lake_vol_m3": 0.0,
            "mass_kg": 1.0e10, "delta_H_m": 1800, "ice_fraction": 0.08, "eta_frict": 0.010,
            "p_meas_mm": 45.0
        },
        "parechu_2005": {
            "B": 42.0, "z": 0.5, "dh": 10.5, "S0": 0.036, "n": 0.050,
            "basin_area_km2": 210.0, "C_runoff": 0.75,
            "total_bulk_m3": 38.0e6, "Cv": 0.28, "lake_vol_m3": 20.0e6,
            "mass_kg": 1.8e10, "delta_H_m": 1600, "ice_fraction": 0.10, "eta_frict": 0.010,
            "p_meas_mm": 10.0
        }
    }

    results = []

    for ev in events:
        eid = ev["id"]
        cp = catchment_params.get(eid, {
            "B": 25.0, "z": 0.5, "dh": 7.0, "S0": 0.05, "n": 0.055,
            "basin_area_km2": 50.0, "C_runoff": 0.8,
            "total_bulk_m3": 10.0e6, "Cv": 0.32, "lake_vol_m3": 2.0e6,
            "mass_kg": 2.0e10, "delta_H_m": 2500, "ice_fraction": 0.25, "eta_frict": 0.015,
            "p_meas_mm": 20.0
        })

        # 1. Manning's Equation for Trapezoidal Channel
        B = cp["B"]
        z = cp["z"]
        dh = cp["dh"]
        S0 = cp["S0"]
        n = cp["n"]

        # Area and Wetted Perimeter
        A = (B + z * dh) * dh
        P = B + 2 * dh * math.sqrt(1 + z * z)
        Rh = A / P
        v_manning = (1.0 / n) * (Rh ** (2.0 / 3.0)) * math.sqrt(S0)
        q_peak_manning = A * v_manning

        # 2. Bulk & Net Liquid Water Separation
        total_bulk = cp["total_bulk_m3"]
        Cv = cp["Cv"]
        v_solids = total_bulk * Cv
        v_water = total_bulk * (1.0 - Cv)

        # 3. Lake Volume Inconsistency
        lake_vol = cp["lake_vol_m3"]
        if lake_vol > 0:
            lake_fraction = lake_vol / v_water
            lake_deficit_ratio = v_water / lake_vol
        else:
            lake_fraction = 0.0
            lake_deficit_ratio = float('inf')

        # 4. First-Principles Thermodynamics of Frictional Melting
        # Ep = m * g * delta_H (Joules)
        # Latent heat of fusion of ice Lf = 334,000 J/kg
        g = 9.80665
        mass = cp["mass_kg"]
        delta_H = cp["delta_H_m"]
        Ep_joules = mass * g * delta_H
        Lf = 334000.0 # J/kg
        eta = cp["eta_frict"] # Fraction of potential energy converted to frictional melting
        m_melt_max_kg = (Ep_joules * eta) / Lf
        v_melt_max_m3 = m_melt_max_kg / 1000.0
        melt_pct_of_water = (v_melt_max_m3 / v_water) * 100.0 if v_water > 0 else 0.0

        # 5. Required Localized Cloudburst Precipitation (mm)
        basin_area_m2 = cp["basin_area_km2"] * 1e6
        C_runoff = cp["C_runoff"]
        p_req_mm = (v_water / (basin_area_m2 * C_runoff)) * 1000.0
        p_meas = cp["p_meas_mm"]
        p_discrepancy_ratio = (p_req_mm / p_meas) if p_meas > 0 else float('inf')

        res = {
            "rank": ev["rank"],
            "id": eid,
            "name": ev["name"],
            "country": ev["country"],
            "date": ev["date"],
            "catchment_hydraulics": {
                "cross_section_B_m": B,
                "stage_rise_dh_m": dh,
                "bed_slope_S0": S0,
                "manning_n": n,
                "flow_area_m2": round(A, 1),
                "hydraulic_radius_m": round(Rh, 2),
                "velocity_m_s": round(v_manning, 2),
                "q_peak_m3_s": round(q_peak_manning, 1)
            },
            "mass_balance": {
                "total_bulk_m3": total_bulk,
                "Cv_solids": Cv,
                "solid_volume_m3": round(v_solids, 1),
                "net_liquid_water_m3": round(v_water, 1),
                "lake_volume_m3": lake_vol,
                "lake_deficit_ratio": round(lake_deficit_ratio, 2) if lake_deficit_ratio != float('inf') else "NO_LAKE (Infinity)"
            },
            "thermodynamics_frictional_melt": {
                "potential_energy_TJ": round(Ep_joules / 1e12, 2),
                "frictional_efficiency_eta": eta,
                "max_frictional_water_m3": round(v_melt_max_m3, 1),
                "frictional_water_pct_of_flood": round(melt_pct_of_water, 2),
                "physical_limit_note": f"Frictional melting explains at most {round(melt_pct_of_water, 1)}% of liquid water."
            },
            "precipitation_inconsistency": {
                "effective_basin_area_km2": cp["basin_area_km2"],
                "required_precip_mm": round(p_req_mm, 1),
                "measured_coarse_precip_mm": p_meas,
                "deficit_multiplier": round(p_discrepancy_ratio, 1) if p_discrepancy_ratio != float('inf') else "DRY_SKY (Infinity)"
            }
        }
        results.append(res)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Calculations complete. Results saved to {output_path}")
    return results

if __name__ == "__main__":
    base_dir = r"C:\Users\haas\github\Himalaia_2026"
    ev_path = os.path.join(base_dir, "data", "himalayan_events_1980_2026.json")
    out_path = os.path.join(base_dir, "data", "catchment_hydraulics", "inverse_hydraulics_all_events.json")
    calculate_hydraulics_and_thermodynamics(ev_path, out_path)
