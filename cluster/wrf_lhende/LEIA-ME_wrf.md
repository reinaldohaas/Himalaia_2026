# WRF do Lhende Khola — a tempestade vinda da atmosfera real (18/10/2026)

**Por quê:** no CM1 (sondagem única, nada pelas fronteiras) o toró foi testado sem a causa. O Himawari mostra um sistema convectivo de mesoescala nascido no planalto tibetano perto de Lhasa (100–146 mil km² < 213 K às 09–13 UTC de 25/08), andando para WSW a ~20–60 km/h e se dissipando a ~200 km a leste do sítio entre 23 e 01 UTC; o sítio esteve na borda ocidental (a jusante) da bigorna (`data/processed/himawari_trajetoria/`).

**A ERA5 tem o sistema só na fase madura** (10–13 UTC, a 10–80 km do centro observado) e o dissipa às 14–16 UTC sem propagá-lo (`data/processed/era5_verificacao_mcs/`). O WRF parte desse estado e tem de fazer a propagação para oeste sozinho, com convecção explícita a 3 km.

## Configuração

* **WRF 4.7.1 / WPS 4.6.0** já compilados no vlab (`privado/WRF-Chem`, gfortran 11.4, dmpar), rodando pelo `kit_wrf` (carregador + glibc 2.39 + OpenMPI 4.1.6 + netCDF-Fortran 4.5.4 / netCDF 4.9.2 / HDF5 1.10.10). Nada instalado; nada em `privado/WRF-Chem` alterado.
* **ERA5** horária, níveis de pressão (37) e superfície, baixada para 24/08 18 UTC → 26/08 06 UTC, 15–40 N, 70–100 E (`scripts/wrf/baixar_era5.py wrf`); a rodada usa **25/08 00 UTC → 26/08 03 UTC (27 h)**, com o d03 a partir de 25/08 12 UTC (o colapso é às 02:52; a aproximação do sistema começa por volta das 17 UTC).
* **Domínios** (Lambert, centro 28,5 N 87,5 E): d01 9 km, 240 × 190 (2.160 × 1.710 km); d02 3 km, 334 × 226 (~1.000 × 675 km, 26–32 N, 83–93 E: toda a trajetória do sistema); d03 1 km, 151 × 151, centrado no sítio, de 25/08 12 UTC em diante. 61 níveis, topo 50 hPa, coordenada terreno-seguidora (`hybrid_opt = 0`: com a híbrida o `real.exe` falha sobre 6.673–7.984 m).
* **Física:** NSSL 2 momentos (`mp_physics = 18`, CCN 0,6 × 10⁹ m⁻³ como no CM1), RRTMG com inclinação e sombreamento do relevo (d02, d03), YSU, Noah, Grell-Freitas só no d01.

## Critério pré-registrado (antes de rodar)

**O WRF só conta como tendo a tempestade se, em algum horário entre 18 e 22 UTC de 25/08, o d02 tiver um sistema com OLR < 120 W/m² de ≥ 5.000 km² a ≤ 100 km do centro do Himawari** (`diag_mcs_wrf.py`). Se não passar, os experimentos do toró no WRF também ficam sem a causa, e isso é dito antes de qualquer interpretação.

Depois (só se passar): portar o `toro_mod` (Estado A/B da anti-varredura) para o NSSL do WRF e repetir as perguntas das séries do CM1 sobre o anfiteatro, agora a jusante da tempestade real.

## Histórico das rodadas

* **27 h, lançada em 18/10 22:14 UTC:** d01 e d02 de 00 a 12 UTC sem erro (só avisos de CFL vertical no d01, w-cfl 2,0–2,2). O **d03 explodiu 72 s depois de entrar** (25/08 12:01:08): W de −142 a −964 m/s nos níveis 2–3 perto de (i, j) = (23–25, 112–113), w-cfl 27, e segfault nos ranks 51 e 59 (`saida/wrf_lhende/relatorios/wrf27h_falha/`). Instabilidade vertical de terreno íngreme a 1 km.
* **Correção (rodada seguinte):** d03 com 3 s (`parent_time_step_ratio = 1, 3, 4`), `epssm = 0.9` nos três domínios, advecção vertical implícita (`zadvect_implicit = 1`, IEVA) e reinício a cada 3 h (`restart_interval = 180`). WPS e `real.exe` não mudam.
