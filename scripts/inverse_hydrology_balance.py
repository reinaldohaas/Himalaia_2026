"""
================================================================================
INVERSE HYDROLOGICAL BALANCE & FLOOD INFLOW RECONSTRUCTION
Himalayan Flash Flood & Debris Flow Disaster (August 26, 2026)
Location: Langtang Lirung / Lhende Khola / Trishuli River Canyon
================================================================================
"""

import numpy as np
import pandas as pd
import os

def run_inverse_hydrology():
    print("=" * 80)
    print("  INVERSE HYDROLOGICAL BALANCE: TRISHULI RIVER DEBRIS FLOOD (AUG 2026)")
    print("=" * 80)

    # 1. Hydraulic Channel Properties (Gyirong - Rasuwagadhi Canyon Gorge)
    B = 30.0          # Average channel bed width (meters)
    z = 0.5           # Side slope ratio 1:0.5 (steep rock canyon)
    S0 = 0.045        # Longitudinal bed slope (4.5% or 0.045 m/m)
    n = 0.060         # Manning's roughness coefficient (boulder/bedrock gorge)
    delta_h = 8.5     # Peak surge water depth rise (meters)

    # Manning equation calculation
    A_peak = (B + z * delta_h) * delta_h
    P_peak = B + 2 * delta_h * np.sqrt(1 + z**2)
    Rh_peak = A_peak / P_peak
    v_peak = (1.0 / n) * (Rh_peak ** (2.0 / 3.0)) * (S0 ** 0.5)
    Q_peak = A_peak * v_peak

    print(f"\n[1] HYDRAULIC PARAMETERS AT PEAK STAGE:")
    print(f"  - Peak Flow Depth (h):       {delta_h:.2f} m")
    print(f"  - Cross-Sectional Area (A):  {A_peak:.1f} m²")
    print(f"  - Hydraulic Radius (Rh):     {Rh_peak:.2f} m")
    print(f"  - Mean Flow Velocity (v):    {v_peak:.2f} m/s ({v_peak * 3.6:.1f} km/h)")
    print(f"  - Calculated Peak Flow (Q):  {Q_peak:.1f} m³/s")

    # 2. Reconstructed Temporal Hydrograph (02:00 to 07:00 UTC / 07:45 to 12:45 NPT)
    hydrograph_data = [
        {"time_utc": "02:00", "time_npt": "07:45", "elapsed_min": 0,   "Q_total_m3s": 60,   "Cv": 0.05},
        {"time_utc": "02:30", "time_npt": "08:15", "elapsed_min": 30,  "Q_total_m3s": 150,  "Cv": 0.10},
        {"time_utc": "03:00", "time_npt": "08:45", "elapsed_min": 60,  "Q_total_m3s": 950,  "Cv": 0.25},
        {"time_utc": "03:30", "time_npt": "09:15", "elapsed_min": 90,  "Q_total_m3s": 2800, "Cv": 0.35},
        {"time_utc": "03:40", "time_npt": "09:25", "elapsed_min": 100, "Q_total_m3s": 3500, "Cv": 0.40}, # Peak Stage
        {"time_utc": "04:15", "time_npt": "10:00", "elapsed_min": 135, "Q_total_m3s": 2200, "Cv": 0.35},
        {"time_utc": "05:00", "time_npt": "10:45", "elapsed_min": 180, "Q_total_m3s": 1100, "Cv": 0.25},
        {"time_utc": "06:00", "time_npt": "11:45", "elapsed_min": 240, "Q_total_m3s": 450,  "Cv": 0.15},
        {"time_utc": "07:00", "time_npt": "12:45", "elapsed_min": 300, "Q_total_m3s": 120,  "Cv": 0.08},
    ]

    df_h = pd.DataFrame(hydrograph_data)
    df_h["Q_water_m3s"] = df_h["Q_total_m3s"] * (1.0 - df_h["Cv"])
    df_h["Q_solids_m3s"] = df_h["Q_total_m3s"] * df_h["Cv"]

    # Numerical integration using trapezoidal rule (seconds)
    time_sec = df_h["elapsed_min"].values * 60.0
    try:
        trapz_func = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
    except Exception:
        trapz_func = None
    
    if trapz_func is not None:
        V_total = trapz_func(df_h["Q_total_m3s"].values, time_sec)
        V_water = trapz_func(df_h["Q_water_m3s"].values, time_sec)
        V_solids = trapz_func(df_h["Q_solids_m3s"].values, time_sec)
    else:
        # Fallback manual trapezoidal integration
        V_total = np.sum(0.5 * (df_h["Q_total_m3s"].values[:-1] + df_h["Q_total_m3s"].values[1:]) * np.diff(time_sec))
        V_water = np.sum(0.5 * (df_h["Q_water_m3s"].values[:-1] + df_h["Q_water_m3s"].values[1:]) * np.diff(time_sec))
        V_solids = np.sum(0.5 * (df_h["Q_solids_m3s"].values[:-1] + df_h["Q_solids_m3s"].values[1:]) * np.diff(time_sec))

    print(f"\n[2] HYDROGRAPH INTEGRATION (300 min duration):")
    print(f"  - Total Bulk Mixture Volume: {V_total / 1e6:.2f} Million m³")
    print(f"  - Solid Debris Volume:       {V_solids / 1e6:.2f} Million m³ (Mean Cv ~ {V_solids/V_total*100:.1f}%)")
    print(f"  - Net Liquid Water Volume:   {V_water / 1e6:.2f} Million m³")

    # 3. Inverse Precipitation Estimation Across Different Catchment Scales
    catchments = [
        {"name": "Narrow Cloudburst Core", "area_km2": 15.0},
        {"name": "Lhende Khola Headwater", "area_km2": 28.0},
        {"name": "Upper Trishuli Sub-basin", "area_km2": 50.0},
        {"name": "Full Regional Catchment", "area_km2": 100.0}
    ]

    print(f"\n[3] EQUIVALENT RAINFALL DEPTH REQUIRED TO PRODUCE {V_water/1e6:.2f}M m³ WATER:")
    print("-" * 80)
    print(f"{'Catchment Domain':<28} | {'Area (km²)':<12} | {'Net Rain (mm)':<15} | {'Runoff Coeff (C=0.85)':<20}")
    print("-" * 80)

    results = []
    for c in catchments:
        area_m2 = c["area_km2"] * 1e6
        precip_mm_100pct = (V_water / area_m2) * 1000.0
        precip_mm_85pct = (V_water / (area_m2 * 0.85)) * 1000.0
        print(f"{c['name']:<28} | {c['area_km2']:<12.1f} | {precip_mm_100pct:<15.1f} | {precip_mm_85pct:<20.1f}")
        results.append({
            "catchment": c["name"],
            "area_km2": c["area_km2"],
            "net_water_m3": V_water,
            "precip_mm_100pct": precip_mm_100pct,
            "precip_mm_85pct": precip_mm_85pct
        })
    print("-" * 80)

    # Save summary table
    repo_dir = "C:/Users/haas/github/Himalaia_2026"
    out_csv = os.path.join(repo_dir, "data/processed/hydrology_inverse_balance_summary.csv")
    pd.DataFrame(results).to_csv(out_csv, index=False)
    print(f"\nSummary table saved to: {out_csv}")

if __name__ == "__main__":
    run_inverse_hydrology()
