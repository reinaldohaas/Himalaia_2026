# -*- coding: utf-8 -*-
"""
input_sounding do CM1 hidrostaticamente consistente a partir dos niveis de pressao da ERA5.

Diferenca para era5_to_cm1/era5_to_sounding.py (que NAO foi alterado):
  la, p_sup/T2m/Td2m da celula ERA5 (cota da celula) sao colocados na altitude pedida
  sem correcao, e o CM1 deriva T de theta com essa pressao -> coluna fria se altitude < cota da celula.
  aqui, p, theta, qv, u, v na base sao interpolados do proprio perfil de niveis de pressao
  (ln p linear em z geopotencial), sem usar os campos de superficie.
Uso: python sondagem_consistente.py <pl.nc> <altitude_base_m> <saida>
"""
import sys
import numpy as np
import xarray as xr
sys.path.insert(0, r"C:\Users\haas\github\era5_to_cm1")
from era5_to_sounding import TARGET_HEIGHTS, get_variable, get_coord, KAPPA, G

LAT, LON = 28.2849, 85.5132
pl, alt, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
d = xr.open_dataset(pl).sel(latitude=LAT, longitude=LON, method="nearest").squeeze()
p = get_coord(d, ['level', 'pressure_level', 'isobaricInhPa', 'plev']).values.astype(float)
z = get_variable(d, ['z', 'geopotential']).values / G
T = get_variable(d, ['t', 'temperature']).values
q = get_variable(d, ['q', 'specific_humidity']).values
u = get_variable(d, ['u', 'u_component_of_wind']).values
v = get_variable(d, ['v', 'v_component_of_wind']).values
o = np.argsort(z); p, z, T, q, u, v = p[o], z[o], T[o], q[o], u[o], v[o]
th = T * (1000.0 / p) ** KAPPA
qv = q / (1 - q) * 1000.0
zz = np.array(TARGET_HEIGHTS, float) + alt
pb = float(np.exp(np.interp(alt, z, np.log(p))))
thi, qvi, ui, vi = (np.interp(zz, z, a) for a in (th, qv, u, v))
with open(out, "w") as f:
    f.write(f"{pb:9.2f}{thi[0]:11.2f}{qvi[0]:11.2f}\n")
    for h, a, b, c, e in zip(TARGET_HEIGHTS, thi, qvi, ui, vi):
        f.write(f"{h:12.4f}{a:15.4f}{max(b, 0):15.5f}{c:19.7E}{e:15.7E}\n")
print("%s: base %.0f m  p=%.1f hPa  T=%.1f C  qv=%.2f g/kg  (nivel ERA5 mais baixo acima da base: %.0f hPa)"
      % (out.split("\\")[-1].split("/")[-1], alt, pb, thi[0] * (pb / 1000) ** KAPPA - 273.15, qvi[0], p[z > alt].max()))
