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
* **Segunda tentativa (18/10 23:28):** caiu na partida com `malloc(): unaligned tcache chunk` no `orterun` do kit (intermitente; já tinha aparecido às 21:27). Correção: `PMIX_MCA_gds=hash` no `mpi_kit.sh` (sem o segmento compartilhado do PMIx, mapeado em endereço fixo).
* **Terceira tentativa (18/10 23:37):** subiu na primeira vez; d01 e d02 de 00 a 03 UTC sem nenhum aviso de CFL. **Travou ao gravar o `wrfrst_d02` das 03 UTC** (arquivo com 48 B, rank 0 sem linha nova, 112 ranks girando). Correção: reinício desligado de novo (`restart_interval = 100000`); a rodada sem reinício já tinha ido de 00 a 12 UTC sem problema.

## Resultado da rodada de 27 h (19/10/2026)

* **A rodada terminou** às 04:32 UTC de 19/10 (`SUCCESS COMPLETE WRF`), relançada às 01:21 (a primeira partida, às 01:19, caiu de novo com o `malloc` do `orterun`; o `PMIX_MCA_gds=hash` não resolve essa falha). **O d03 ficou estável até o fim**, sem nenhuma linha de CFL; o d01 teve w-cfl até 2,20 (W = 20,6 m/s às 07:25 UTC, rank 37).
* **Critério pré-registrado: NÃO PASSA.** Entre 18 e 22 UTC nenhum objeto com OLR < 120 W/m² de ≥ 5.000 km² fica a ≤ 100 km do centro do Himawari; os objetos desse porte ficam a 272–489 km (`data/processed/wrf_lhende/diag_mcs_d02.txt`).
* **O que o WRF pegou:**
  * a **fase madura** do sistema do planalto, perto de Lhasa: a 66–108 km do centro observado às 12–13 UTC, mas com no máximo **1/7 da área fria** observada (20.782 contra 141.681 km² às 12:30). Ele morre às 16:30 UTC indo para o norte, em vez de seguir para oés-sudoeste como no Himawari;
  * a **convecção noturna perto do sítio**: 4.000–5.500 km² com OLR < 120 W/m² a até 150 km do sítio entre 18 e 23 UTC, contra 4.300–6.000 km² < 213 K no Himawari. O maior objeto do WRF fica a 85–98 km a sudoeste (27,6–27,8 N; 84,7–85,1 E); o Himawari tinha células de 1.100–1.800 km² a 50–60 km a oés-sudoeste (≈ 28,0 N; 85,0 E) às 19:00–20:30. Mesma quantidade e horário, deslocada 30–50 km para o sul.
* **Chuva no d03 (1 km): 0,0 mm sobre o anfiteatro de 12 a 03 UTC**; máximo de 8,1 mm a menos de 30 km, quase todo até 23 UTC. No d02, o ponto do sítio acumula 13,5 mm até 12 UTC e nada depois. Pela regra pré-registrada, como o critério falhou, essa chuva **não é interpretada** como a da tempestade.
* **Limitações das saídas:** `REFD_MAX` saiu zero em tudo (a refletividade não foi ligada: `do_radar_ref`). Graupel e granizo (`QGRAUP`, `QHAIL` e números) só estão nos `wrfout` completos (~18 GB), que ficaram no vlab.
* **Defeito corrigido no diagnóstico:** no instante inicial o WRF grava OLR = 0 em todo o domínio, e o rastreio seguia esse "objeto". O `diag_mcs_wrf.py` agora ignora esse quadro e faz também a leitura literal do critério, objeto a objeto, sem rastreio. As duas leituras dão "não passa".
* Figura: `data/processed/wrf_lhende/wrf_himawari.png` (`scripts/artigo/fig_wrf_himawari.py`).
