# -*- coding: utf-8 -*-
"""
Gera input_sounding do CM1 para o Lhende Khola a partir da ERA5, reutilizando
as funcoes do proprio era5_to_cm1/era5_to_sounding.py do usuario.

Instantes (escolhidos pela serie do Himawari-9):
  2026-08-25 12:00 UTC  pre-convectivo  (6 h antes do 1o pico)
  2026-08-25 18:00 UTC  pico do 1o sistema (8.413 km2 < -60 C)
  2026-08-26 00:00 UTC  3 h antes do colapso (02:52 UTC)

Solo do dominio plano: 4.010 m ASL -- cota medida no GLO-30 do ponto onde a
massa alcanca o fundo do vale, saida do anfiteatro de 3,39 km2.
"""
import os
import sys

sys.path.insert(0, r"C:\Users\haas\github\era5_to_cm1")
import era5_to_sounding as E          # codigo do usuario, sem modificacao

LAT, LON = 28.2849, 85.5132
ALT = 4010.0
SP = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SP, "sondagens")
os.makedirs(OUT, exist_ok=True)

INSTANTES = [("2026-08-25", "12:00", "pre"),
             ("2026-08-25", "18:00", "pico"),
             ("2026-08-26", "00:00", "pre_colapso")]

for data, hora, tag in INSTANTES:
    pl = os.path.join(OUT, "era5_pl_%s.nc" % tag)
    sl = os.path.join(OUT, "era5_sl_%s.nc" % tag)
    snd = os.path.join(OUT, "input_sounding_%s" % tag)
    print("=" * 70)
    print("%s %s UTC  (%s)" % (data, hora, tag))
    print("=" * 70)
    if not (os.path.exists(pl) and os.path.exists(sl)):
        E.download_era5(LAT, LON, data, hora, pl, sl)
    E.process_sounding(pl, sl, LAT, LON, ALT, "Lhende Khola (anfiteatro)", snd)
    print()
