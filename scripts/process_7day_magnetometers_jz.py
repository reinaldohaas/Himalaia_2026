# -*- coding: utf-8 -*-
"""
scripts/process_7day_magnetometers_jz.py
==============================================================================
MODELO PARAMÉTRICO DE SQ IONOSFÉRICO E CORRENTE GEC (8 ESTAÇÕES DE REFERÊNCIA)
==============================================================================
AVISO METODOLÓGICO DE AUDITORIA INDEPENDENTE:
Este script calcula variações paramétricas teóricas do efeito Sq (Solar Quiet)
e do potencial ionosférico com base em equações analíticas e fluxo de raios X.
NÃO CONSTITUI UMA INVERSÃO INSTRUMENTAL DE MAGNETÔMETROS.
Nenhum dado magnetométrico bruto (INTERMAGNET/IIG) é lido por este script.
Saída gerada exclusivamente em data/synthetic/jz_8station_PARAMETRIC_MODEL.csv.
"""

import os
import json
import csv
import math
from datetime import datetime, timedelta

def processar_rede_magnetometros_7dias():
    print("=== MODELAGEM PARAMÉTRICA GEC (8 ESTAÇÕES DE COORDENADAS) ===")
    print("    [AVISO] Dados puramente analíticos/sintéticos - sem magnetômetros reais.")
    
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(repo_dir, "data", "raw", "space_weather")
    synth_dir = os.path.join(repo_dir, "data", "synthetic")
    os.makedirs(synth_dir, exist_ok=True)
    out_csv = os.path.join(synth_dir, "jz_8station_PARAMETRIC_MODEL.csv")
    
    # Coordenadas geográficas nominais de referência (para cálculo de hora solar local)
    estacoes = [
        {"code": "KKN", "name": "Kakani", "lat": 27.801, "lon": 85.280, "alt": 2030},
        {"code": "LZA", "name": "Lhasa", "lat": 29.645, "lon": 91.035, "alt": 3650},
        {"code": "SAB", "name": "Sabhawala", "lat": 30.337, "lon": 77.802, "alt": 500},
        {"code": "JAI", "name": "Jaipur", "lat": 26.920, "lon": 75.800, "alt": 430},
        {"code": "GUL", "name": "Gulmarg", "lat": 34.070, "lon": 74.420, "alt": 2650},
        {"code": "ABG", "name": "Alibag", "lat": 18.640, "lon": 72.870, "alt": 10},
        {"code": "TIR", "name": "Tirunelveli", "lat": 8.710, "lon": 77.800, "alt": 40},
        {"code": "HYB", "name": "Hyderabad", "lat": 17.420, "lon": 78.550, "alt": 540}
    ]
    
    # 2. Carregar dados reais do GOES-18 e K-Index da NOAA quando disponíveis
    xray_json_path = os.path.join(raw_dir, "goes_xrays_7day_real.json")
    kp_json_path = os.path.join(raw_dir, "noaa_planetary_k_index_real.json")
    
    goes_real_hourly = {}
    if os.path.exists(xray_json_path):
        with open(xray_json_path, "r", encoding="utf-8") as f:
            goes_raw = json.load(f)
            for r in goes_raw:
                if r.get("energy") == "0.1-0.8nm":
                    tt = r.get("time_tag", "")
                    dt_key = tt[:13]
                    flux = float(r.get("flux", 1e-6))
                    if dt_key not in goes_real_hourly or flux > goes_real_hourly[dt_key]:
                        goes_real_hourly[dt_key] = flux
                        
    # Mapear dados reais de Kp por hora (lista de dicionários)
    kp_real_hourly = {}
    if os.path.exists(kp_json_path):
        with open(kp_json_path, "r", encoding="utf-8") as f:
            kp_raw = json.load(f)
            for item in kp_raw:
                if isinstance(item, dict):
                    tt = item.get("time_tag", "")[:13]
                    try:
                        kp_real_hourly[tt] = float(item.get("Kp", 2.0))
                    except (ValueError, TypeError):
                        pass
                    
    # 3. Gerar a Série Temporal de 7 Dias (21 a 28 de Agosto de 2026)
    start_dt = datetime(2026, 8, 21, 0, 0)
    end_dt = datetime(2026, 8, 28, 0, 0)
    curr_dt = start_dt
    
    rows = []
    while curr_dt <= end_dt:
        dt_str = curr_dt.strftime("%Y-%m-%d %H:%M:%S")
        dt_key = curr_dt.strftime("%Y-%m-%dT%H")
        npt_str = (curr_dt + timedelta(hours=5, minutes=45)).strftime("%Y-%m-%d %H:%M:%S")
        
        xray_flux = goes_real_hourly.get(dt_key, 2.5e-6)
        kp_val = kp_real_hourly.get(dt_key, 2.0)
        
        # Hora local solar nominal para o Himalaia (UT + 5.7h)
        local_hour = (curr_dt.hour + 5.7) % 24.0
        sq_base = max(0.0, math.sin((local_hour - 6.0) * math.pi / 12.0)) if 6.0 <= local_hour <= 18.0 else 0.0
        
        # Equações paramétricas sintéticas de variação de campo magnético
        delta_h_tir = 110.0 * sq_base + 15.0 * math.log10(max(xray_flux, 1e-9) / 1e-7) + 8.0 * kp_val
        delta_h_abg = 45.0 * sq_base + 6.0 * math.log10(max(xray_flux, 1e-9) / 1e-7) + 6.0 * kp_val
        delta_h_lza = 38.0 * sq_base + 5.0 * math.log10(max(xray_flux, 1e-9) / 1e-7) + 5.5 * kp_val
        delta_h_sab = 42.0 * sq_base + 5.5 * math.log10(max(xray_flux, 1e-9) / 1e-7) + 6.0 * kp_val
        delta_h_kkn = 40.0 * sq_base + 5.2 * math.log10(max(xray_flux, 1e-9) / 1e-7) + 5.8 * kp_val
        delta_h_jai = 44.0 * sq_base + 5.8 * math.log10(max(xray_flux, 1e-9) / 1e-7) + 6.2 * kp_val
        delta_h_gul = 36.0 * sq_base + 4.8 * math.log10(max(xray_flux, 1e-9) / 1e-7) + 5.2 * kp_val
        delta_h_hyb = 52.0 * sq_base + 7.0 * math.log10(max(xray_flux, 1e-9) / 1e-7) + 6.5 * kp_val
        
        delta_eej = max(0.0, delta_h_tir - delta_h_abg)
        e_y_iono = delta_eej / 85.0
        
        # Potencial Carnegie teórico
        carnegie = 1.0 + 0.18 * math.sin((curr_dt.hour - 11.0) * math.pi / 12.0)
        vi_base = 250.0 * carnegie
        vi_solar_perturbation = 22.0 * (xray_flux / 1e-5) + 4.5 * (kp_val - 2.0)
        vi_total = vi_base + vi_solar_perturbation
        
        # Corrente vertical Jz teórica (premissa de Rc constante = 0.78e17 Ohm.m2)
        rc_himalaya = 0.78
        jz_himalaya = (vi_total / rc_himalaya) * 0.01  # pA/m2
        ez_surface = (jz_himalaya * 1e-12) / 2.5e-14   # V/m
        
        rows.append([
            dt_str, npt_str,
            f"{xray_flux:.2e}", f"{kp_val:.2f}",
            f"{delta_h_kkn:.1f}", f"{delta_h_lza:.1f}", f"{delta_h_sab:.1f}",
            f"{delta_h_jai:.1f}", f"{delta_h_gul:.1f}", f"{delta_h_abg:.1f}",
            f"{delta_h_tir:.1f}", f"{delta_h_hyb:.1f}",
            f"{delta_eej:.1f}", f"{e_y_iono:.3f}",
            f"{vi_total:.1f}", f"{jz_himalaya:.3f}", f"{ez_surface:.1f}",
            "PARAMETRIC_SYNTHETIC_MODEL"
        ])
        curr_dt += timedelta(hours=1)
        
    header = [
        "datetime_utc", "datetime_npt",
        "goes_xray_flux_Wm2", "planetary_kp_index",
        "synthetic_delta_h_kkn", "synthetic_delta_h_lza", "synthetic_delta_h_sab",
        "synthetic_delta_h_jai", "synthetic_delta_h_gul", "synthetic_delta_h_abg",
        "synthetic_delta_h_tir", "synthetic_delta_h_hyb",
        "synthetic_delta_eej_nT", "modeled_ey_iono_mVm",
        "modeled_vi_total_kV", "modeled_jz_himalaya_pA_m2", "modeled_ez_surface_Vm",
        "data_classification"
    ]
    
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
        
    print(f"-> Arquivo paramétrico salvo: {out_csv} ({len(rows)} horas)")

if __name__ == "__main__":
    processar_rede_magnetometros_7dias()
