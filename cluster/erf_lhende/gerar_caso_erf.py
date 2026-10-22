# -*- coding: utf-8 -*-
"""
Caso idealizado do ERF (26.09) sobre o macico do Langtang Lirung / Tsangbu Ri com terreno IMERSO
(erf.terrain_type = ImmersedForcing), relevo do Copernicus GLO-30 sem suavizacao no interior.

Objetivo (pedido do pesquisador, 22/10/2026): testar o que o WRF a 1 km nao consegue -- o relevo do WRF chega a
6.438 m contra 7.216 m no GLO-30 -- e saber se a precipitacao solida chega ao chao das encostas altas (6-7 km).

Gera, em cluster/erf_lhende/caso/:
  terreno_dx<dx>.txt      formato texto do ERF: nx, ny, x(nx), y(ny), z(nx*ny) contiguo em y (ERF_ProbCommon.H)
  input_sounding          sondagem ERA5 do sitio, 25/08 18 UTC (pico do sistema), base 3.000 m (snd_ok_pico_3000)
  inputs_teste            500 m, poucos passos (so para ver se o caso inicia)
  inputs_vlab             200 m, 3 h (a rodada)
Malha plana com o relevo imposto: z = 0 do modelo = 3.000 m ASL; o relevo abaixo de 3.000 m vira o chao do dominio.
Laterais periodicas: o relevo e levado suavemente a 0 numa faixa de 2 km nas bordas.
Uso: python gerar_caso_erf.py
"""
import os
import shutil
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "scripts", "neve_anfiteatro"))
from comum import stac_busca, pc_assina, ler_janela, PC

CENTRO = (85.520, 28.278)           # lon, lat: entre o anfiteatro e a cicatriz
LADO = 20000.0                      # m
Z0 = 3000.0                         # m ASL no chao do modelo (base da sondagem)
TOPO = 16000.0                      # m acima de Z0 (19 km ASL)
FAIXA = 2000.0                      # m de transicao nas bordas
SONDAGEM = os.path.join(RAIZ, "data", "processed", "toro_cm1", "snd_ok_pico_3000")
CASO = os.path.join(AQUI, "caso")


def relevo(dx):
    from shapely.geometry import box
    from pyproj import Transformer
    from rasterio.warp import reproject, Resampling
    from affine import Affine
    t = Transformer.from_crs(4326, 32645, always_xy=True)
    xc, yc = t.transform(*CENTRO)
    ti = Transformer.from_crs(32645, 4326, always_xy=True)
    lo0, la0 = ti.transform(xc - LADO / 2 - 3000, yc - LADO / 2 - 3000)
    lo1, la1 = ti.transform(xc + LADO / 2 + 3000, yc + LADO / 2 + 3000)
    g = box(lo0, la0, lo1, la1)
    n = int(round(LADO / dx)) + 1                          # nos (inclui as duas bordas)
    tr = Affine(dx, 0, xc - LADO / 2 - dx / 2, 0, -dx, yc + LADO / 2 + dx / 2)
    z = np.full((n, n), np.nan, np.float32)
    for f in stac_busca(PC, ["cop-dem-glo-30"], list(g.bounds), "2000-01-01/2030-01-01"):
        a, ta, ca, nd = ler_janela(pc_assina(f["assets"]["data"]["href"], "cop-dem-glo-30"), g, folga_m=0)
        out = np.full((n, n), np.nan, np.float32)
        reproject(a.astype(np.float32), out, src_transform=ta, src_crs=ca, dst_transform=tr, dst_crs="EPSG:32645",
                  resampling=Resampling.average, src_nodata=nd, dst_nodata=np.nan)
        z = np.where(np.isfinite(out), out, z)
    assert np.isfinite(z).all(), "GLO-30 nao cobriu o dominio"
    zmax_glo = float(z.max())
    h = np.clip(z - Z0, 0.0, None)
    # linhas de z: de norte (topo) para sul; o ERF quer y crescente -> inverte
    h = h[::-1, :]
    s = np.arange(n) * dx
    d = np.minimum.outer(np.minimum(s, LADO - s), np.minimum(s, LADO - s))   # distancia a borda mais proxima
    w = np.clip(d / FAIXA, 0, 1)
    w = 0.5 - 0.5 * np.cos(np.pi * w)
    h = h * w
    return s, h, zmax_glo


def grava_relevo(arq, s, h):
    nx = ny = len(s)
    with open(arq, "w") as f:
        f.write("%d\n%d\n" % (nx, ny))
        f.write("\n".join("%.1f" % v for v in s) + "\n")
        f.write("\n".join("%.1f" % v for v in s) + "\n")
        # h[j, i] com j = y, i = x; o ERF quer indice i*ny + j (contiguo em y)
        f.write("\n".join("%.2f" % v for v in h.T.ravel()) + "\n")


INPUTS = """# ERF 26.09 -- caso idealizado Lhende/Tsangbu Ri, terreno imerso (gerar_caso_erf.py)
# z = 0 do modelo = {z0:.0f} m ASL; relevo do GLO-30 (max {zmax:.0f} m ASL), {dx:.0f} m
max_step = {max_step}
stop_time = {stop}
amrex.fpe_trap_invalid = 1
fabarray.mfiter_tile_size = 1024 1024 1024

geometry.prob_extent = {L:.0f} {L:.0f} {top:.0f}
amr.n_cell           = {nx} {nx} {nz}
geometry.is_periodic = 1 1 0
zlo.type = "NoSlipWall"
zhi.type = "SlipWall"

erf.fixed_dt           = {dt}
erf.fixed_mri_dt_ratio = {mri}
erf.sum_interval = 10
erf.v = 1
amr.v = 1
amr.max_level = 0
amr.max_grid_size = {mgs}
amr.blocking_factor = 1

erf.check_file = chk
erf.check_int  = {chk}
erf.plot_file_1 = plt
erf.plot_int_1  = {plot}
erf.plot_vars_1 = density x_velocity y_velocity z_velocity pressure temp theta qv qc qi qr qs qg terrain_IB_mask rain_accum snow_accum graup_accum

erf.use_gravity = true
erf.molec_diff_type = "None"
erf.les_type = "Smagorinsky"
erf.Cs = 0.17
erf.rayleigh_damp_U = true
erf.rayleigh_damp_V = true
erf.rayleigh_damp_W = true
erf.rayleigh_damp_T = true
prob.dampcoef = 0.2
prob.zdamp = 4000.

erf.init_type = "input_sounding"
erf.sounding_type = Ideal
erf.input_sounding_file = "input_sounding"

erf.terrain_type = ImmersedForcing
erf.terrain_file_name = {terreno}
erf.immersed_forcing_substep = true
eb2.small_volfrac = 0.005
eb2.cover_multiple_cuts = 1
erf.if_use_most = true
erf.if_surf_temp_flux = 0.0

erf.use_coriolis = false
erf.moisture_model = "{micro}"
erf.moistscal_horiz_adv_type = Upwind_3rd_SL
erf.moistscal_vert_adv_type  = Upwind_3rd_SL
"""


def main():
    os.makedirs(CASO, exist_ok=True)
    # o ERF exige theta e qv da linha de superficie IGUAIS aos da 1a linha de dados (ERF_InputSoundingData.H)
    ls = open(SONDAGEM).read().split("\n")
    ps = ls[0].split()[0]
    z0, th0, qv0 = ls[1].split()[:3]
    ls[0] = "%s %s %s" % (ps, th0, qv0)
    open(os.path.join(CASO, "input_sounding"), "w", newline="\n").write("\n".join(ls))
    for nome, dx, nz, dt, mri, max_step, stop, plot, chk, mgs in (
            ("teste", 500.0, 64, 2.0, 6, 10, 20.0, 5, -1, "20 20 32"),
            ("vlab", 200.0, 160, 1.0, 6, 1000000, 10800.0, 600, 3600, "25 25 32")):
        s, h, zmax = relevo(dx)
        ter = "terreno_dx%d.txt" % dx
        grava_relevo(os.path.join(CASO, ter), s, h)
        nx = len(s) - 1
        txt = INPUTS.format(z0=Z0, zmax=zmax, dx=dx, max_step=max_step, stop=stop, L=LADO, top=TOPO, nx=nx, nz=nz,
                            dt=dt, mri=mri, chk=chk, plot=plot, terreno=ter, micro="Morrison", mgs=mgs)
        open(os.path.join(CASO, "inputs_" + nome), "w", newline="\n").write(txt)
        print(nome, "dx", dx, "celulas", nx, nx, nz, "| relevo: max %.0f m ASL no GLO-30, max %.0f m acima de Z0 no modelo"
              % (zmax, h.max() + Z0 if False else h.max()), "| area > 3 km acima de Z0: %.1f km2" % ((h > 3000).sum() * dx * dx / 1e6))


if __name__ == "__main__":
    main()
