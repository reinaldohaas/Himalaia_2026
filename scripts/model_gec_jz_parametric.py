# -*- coding: utf-8 -*-
"""
scripts/model_gec_jz_parametric.py
==============================================================================
MODELO PARAMÉTRICO DO CIRCUITO ELÉTRICO GLOBAL (GEC) E ESTIMATIVA DE Jz
==============================================================================
AVISO METODOLÓGICO DE AUDITORIA INDEPENDENTE:
Este script implementa um MODELO TEÓRICO/PARAMÉTRICO simplificado baseado na
curva diurna de Carnegie e perturbações logarítmicas de fluxo de raios X solares.
NÃO LÊ MAGNETÔMETROS REAIS E NÃO CONSTITUI UMA INVERSÃO INSTRUMENTAL DE DADOS.
As estações listadas representam coordenadas de referência geográfica para
cálculo de hora solar local (Sq teórico), e não séries observadas.
Saída gerada exclusivamente em data/synthetic/jz_gec_PARAMETRIC_MODEL.csv.
"""

import os
import json
import csv
import math
import pandas as pd
import numpy as np

def model_gec_jz_parametric():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    goes_xray_path = os.path.join(repo_dir, "data", "raw", "space_weather", "goes_xrays_7day_real.json")
    synthetic_dir = os.path.join(repo_dir, "data", "synthetic")
    os.makedirs(synthetic_dir, exist_ok=True)
    output_csv = os.path.join(synthetic_dir, "jz_gec_PARAMETRIC_MODEL.csv")
    
    print("=== EXECUTANDO MODELO PARAMÉTRICO TEÓRICO DE Jz (GEC PARAMETRIC MODEL) ===")
    print("    [AVISO] Dados puramente modelados - sem leitura de magnetômetros reais.")
    
    # 1. Carregar registros do GOES-18 (NOAA SWPC) para modulação solar contínua
    hourly_xray = {}
    if os.path.exists(goes_xray_path):
        with open(goes_xray_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data:
                if entry.get("energy") == "0.1-0.8nm":
                    time_str = entry.get("time_tag", "")
                    if time_str:
                        hour_key = time_str[:13] + ":00:00"
                        val = entry.get("flux")
                        if val is not None and val > 0:
                            if hour_key not in hourly_xray:
                                hourly_xray[hour_key] = []
                            hourly_xray[hour_key].append(val)
    
    # 2. Gerar série horária de 7 dias (21 a 28 de agosto de 2026 - 169 horas)
    start_ts = pd.Timestamp("2026-08-21 00:00:00", tz="UTC")
    time_range = [start_ts + pd.Timedelta(hours=i) for i in range(169)]
    
    records = []
    
    # Curva Diária Teórica de Carnegie para Potencial Ionosférico Basal (kV)
    carnegie_hourly = [
        240.0, 230.0, 220.0, 210.0, 205.0, 205.0, 215.0, 212.0, 218.0, 225.0,
        238.0, 250.0, 262.0, 274.0, 283.0, 290.0, 295.0, 298.0, 295.0, 290.0,
        283.0, 274.0, 263.0, 252.0
    ]
    
    for dt in time_range:
        utc_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        npt_dt = dt + pd.Timedelta(hours=5, minutes=45)
        npt_str = npt_dt.strftime("%Y-%m-%d %H:%M:%S")
        cst_dt = dt + pd.Timedelta(hours=8)
        cst_str = cst_dt.strftime("%Y-%m-%d %H:%M:%S")
        
        hour_utc = dt.hour
        hour_key = dt.strftime("%Y-%m-%dT%H:00:00")
        
        # Fluxo de Raios X médio do GOES-18 (quando disponível no arquivo)
        if hour_key in hourly_xray and len(hourly_xray[hour_key]) > 0:
            xray_flux = float(np.mean(hourly_xray[hour_key]))
        else:
            xray_flux = 2.5e-6
            
        kp_index = 2.0  # Premissa paramétrica constante (não observada)
        
        # Variação Diurna Geomagnética Regular Teórica (Sq analítico)
        lt_india = (hour_utc + 5.5) % 24.0
        sq_eej = max(0.0, math.sin(math.pi * (lt_india - 6.0) / 12.0)) if 6.0 <= lt_india <= 18.0 else 0.0
        
        lt_china = (hour_utc + 8.0) % 24.0
        sq_china = max(0.0, math.sin(math.pi * (lt_china - 6.0) / 12.0)) if 6.0 <= lt_china <= 18.0 else 0.0
        
        # Modelo senoidal paramétrico das variações delta H teóricas
        dH_ABG = 15.0 + 55.0 * sq_eej
        dH_TIR = 20.0 + 145.0 * sq_eej
        dH_EEJ = max(0.0, dH_TIR - dH_ABG)
        
        dH_KKN = 14.0 + 48.0 * sq_eej
        dH_SAB = 16.0 + 52.0 * sq_eej
        dH_JAI = 15.5 + 50.0 * sq_eej
        dH_GUL = 13.0 + 42.0 * sq_eej
        dH_HYB = 17.0 + 60.0 * sq_eej
        
        dH_LZA = 15.0 + 50.0 * sq_china
        dH_XAN = 16.0 + 46.0 * sq_china
        dH_CDT = 16.5 + 48.0 * sq_china
        dH_BJI = 14.5 + 40.0 * sq_china
        dH_QGZ = 18.0 + 75.0 * sq_china
        dH_KSH = 13.5 + 42.0 * sq_china
        dH_WUH = 16.0 + 47.0 * sq_china
        
        # Relação teórica de Cowling (Sigma_C = 85.0 S)
        Ey = dH_EEJ / 85.0
        
        # Potencial Ionosférico Global Basal (VI em kV)
        V_carnegie = carnegie_hourly[hour_utc]
        # Modulação paramétrica contínua derivada do fluxo de raios X (sem injeção manual condicional)
        delta_V_solar = (math.log10(max(xray_flux, 1e-8)) - math.log10(1e-6)) * 28.0
        if delta_V_solar < 0: delta_V_solar = 0.0
        
        VI = V_carnegie + delta_V_solar
        
        # Cálculo paramétrico de Jz sobre a coluna do Himalaia (cota teórica 4.000m)
        # Resistência colunar assumida constante: Rc = 0.78 x 10^17 Ohm.m^2
        Rc_himalaya = 0.78e17
        Jz = (VI * 1e3) / Rc_himalaya * 1e12  # pA/m^2
        
        # Campo elétrico de tempo bom teórico (Ez = Jz / sigma_local, com premissa sigma = 2.5e-14 S/m)
        Ez = (Jz * 1e-12) / 2.5e-14  # V/m
        
        records.append({
            "datetime_utc": utc_str,
            "datetime_npt": npt_str,
            "datetime_cst_china": cst_str,
            "modeled_goes_xray_flux_Wm2": f"{xray_flux:.2e}",
            "assumed_kp_index": f"{kp_index:.2f}",
            "synthetic_dH_LZA_Tibet_nT": f"{dH_LZA:.1f}",
            "synthetic_dH_XAN_China_nT": f"{dH_XAN:.1f}",
            "synthetic_dH_CDT_China_nT": f"{dH_CDT:.1f}",
            "synthetic_dH_BJI_China_nT": f"{dH_BJI:.1f}",
            "synthetic_dH_QGZ_China_nT": f"{dH_QGZ:.1f}",
            "synthetic_dH_KSH_China_nT": f"{dH_KSH:.1f}",
            "synthetic_dH_WUH_China_nT": f"{dH_WUH:.1f}",
            "synthetic_dH_KKN_Nepal_nT": f"{dH_KKN:.1f}",
            "synthetic_dH_SAB_India_nT": f"{dH_SAB:.1f}",
            "synthetic_dH_JAI_India_nT": f"{dH_JAI:.1f}",
            "synthetic_dH_GUL_India_nT": f"{dH_GUL:.1f}",
            "synthetic_dH_ABG_India_nT": f"{dH_ABG:.1f}",
            "synthetic_dH_TIR_India_nT": f"{dH_TIR:.1f}",
            "synthetic_dH_HYB_India_nT": f"{dH_HYB:.1f}",
            "synthetic_EEJ_strength_nT": f"{dH_EEJ:.1f}",
            "modeled_Ey_mVm": f"{Ey:.3f}",
            "modeled_VI_kV": f"{VI:.1f}",
            "modeled_jz_pA_m2": f"{Jz:.3f}",
            "modeled_ez_Vm": f"{Ez:.1f}",
            "data_classification": "PARAMETRIC_SYNTHETIC_MODEL"
        })

    df_out = pd.DataFrame(records)
    df_out.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"-> Arquivo modelo salvo: {output_csv}")
    print(f"-> Total de horas modeladas: {len(df_out)}")
    return output_csv

if __name__ == "__main__":
    model_gec_jz_parametric()
