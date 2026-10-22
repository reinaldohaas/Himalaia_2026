# ERF sobre o maciço do Langtang Lirung / Tsangbu Ri — caso idealizado com terreno imerso (22/10/2026)

## Por que o ERF

O WRF a 1 km rebaixa o maciço: o ponto mais alto do modelo tem 6.438 m, contra 7.216 m no GLO-30. A área acima de 6.000 m cai de 11,8 km² para 5 km². As encostas altas, onde a hipótese revisada põe a acumulação de granizo, graupel e gelo, praticamente não existem no WRF (`scripts/toro_wrf/LEIA-ME_toro_wrf.md`, "Precipitação sólida acumulada no solo").

O ERF (Energy Research and Forecasting, DOE, sobre o AMReX) tem **terreno imerso** (`erf.terrain_type = ImmersedForcing`): a malha é plana, e o relevo é imposto como contorno imerso, sem coordenadas que sigam o terreno e sem precisar suavizar o relevo.

## Compilação (WSL)

* **ERF 26.09** (commit `6d09aeb`, 4/9/2026), com os submódulos AMReX, Noah-MP, RRTMGP, EKAT/Kokkos, WW3 e googletest (versões em `bin_erf/versao_sub.txt`).
* **Ambiente:** CPU, MPI (Open MPI 4.1.6, g++ 13.3), **sem NetCDF**. Com NetCDF, o AMReX exige HDF5 paralelo, e o WSL só tem o serial. Para inicializar com `wrfinput`/`wrfbdy` é preciso instalar `libhdf5-mpi-dev` e `libnetcdf-mpi-dev` e recompilar.
* **Executável:** `erf_exec` (sha256 em `bin_erf/SHA256SUMS_ERF.txt`).
* **No vlab** roda pelo mesmo `kit_wrf` do WRF. A única biblioteca que faltava no kit, `libmpi_cxx.so.40`, vai em `bin_erf/lib/`.
* **Superpartículas:** exigem recompilar com `ERF_ENABLE_PARTICLES=ON`, sem instalar nada. Ainda não foi feito.

## O caso (`gerar_caso_erf.py`, `caso/`)

* **Domínio:** 20 × 20 km centrado em 28,278 N / 85,520 E, entre o anfiteatro e a cicatriz. Topo a 16 km acima da base.
* **Base:** z = 0 do modelo = 3.000 m ASL.
* **Relevo:** GLO-30 por média de área, sem suavização no interior, levado suavemente a 0 numa faixa de 2 km nas bordas para as laterais periódicas.
  * 200 m: máximo **7.160 m ASL**, 15 km² acima de 6.000 m ASL.
  * 500 m: máximo 7.032 m ASL.
* **Sondagem:** ERA5 do sítio, 25/08 18 UTC, pico do sistema (`data/processed/toro_cm1/snd_ok_pico_3000`). O ERF exige que θ e qv da linha de superfície sejam iguais aos da primeira linha de dados; o gerador garante isso.
* **Física:** microfísica Morrison (2 momentos, com graupel), LES Smagorinsky, camada de superfície MOST no contorno imerso, sem radiação, sem Coriolis, amortecimento de Rayleigh nos 4 km de cima. `eb2.cover_multiple_cuts = 1`, porque o relevo íngreme corta células mais de duas vezes; sem isso o ERF aborta na montagem do contorno.

| Entrada | dx | Células | dt | Duração | Onde |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `inputs_teste` | 500 m | 40 × 40 × 64 | 2 s | 10 passos | WSL e vlab (teste) |
| `inputs_vlab` | 200 m | 100 × 100 × 160 | 1 s | 3 h | vlab, NP = 80 |

## Teste no WSL (22/10/2026)

O `inputs_teste` rodou os 10 passos sem erro e sem NaN (4,1 s em 4 núcleos), com terreno imerso e Morrison. O ERF corrigiu sozinho as células com múltiplos cortes ("fixed 3 multicuts").

## Critérios para a rodada de 200 m (fixados antes de rodar)

1. **Estabilidade:** 3 h sem NaN nem aborto com relevo de até 7.160 m e encostas de 45° ou mais.
2. **Precipitação sólida no chão das encostas altas:** `snow_accum` e `graup_accum` acima de 6.000 m ASL, com massa total e máximo, comparados com o WRF, que dá ~0.
3. **Nuvem e dinâmica sobre o maciço:** água super-resfriada (qc + qr com T < 0 °C), graupel, ascendente e descendente máximas sobre o anfiteatro.

Este é um teste de **capacidade do modelo**, não uma reprodução do evento:
* a sondagem é fixa;
* as laterais são periódicas;
* não há radiação nem forçante de escala sinótica.

Se o ERF depositar precipitação sólida apreciável nas encostas altas onde o WRF não deposita nada, o próximo passo é a inicialização com dados reais (`wrfinput`/`wrfbdy`, com NetCDF paralelo).

## Uso no vlab

```
bash rodar_erf.sh verificar
bash rodar_erf.sh teste
bash rodar_erf.sh rodada
bash rodar_erf.sh estado
```
