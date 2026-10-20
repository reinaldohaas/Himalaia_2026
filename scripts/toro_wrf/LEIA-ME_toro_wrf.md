# WRF no "modo super-resfriado" — experimento de limite (19/10/2026)

**Pergunta do pesquisador:** se a anti-varredura de Tinsley segurar a água no estado líquido super-resfriado dentro da tempestade real daquela noite, quanta água o modelo consegue reter, onde ela fica e o que acontece quando um vórtice traz aerossol e a física normal volta?

**Natureza:** experimento de **limite**. Os fatores são escolhidos, não medidos. Nenhum processo de carga elétrica é modelado. O WRF não representa sinterização, afunilamento nem deriva centrífuga de hidrometeoros. O que se mede é até onde a física do modelo chega com essas alavancas.

## Código

* `module_toro_wrf.F`: módulo novo, inserido no próprio arquivo do NSSL. É **inerte sem `toro_wrf.txt`** no diretório da rodada.
* `aplicar_patch_toro_wrf.py`: só acrescenta linhas em `phys/module_mp_nssl_2mom.F` (185) e em `phys/module_microphysics_driver.F`. Confere o sha256 do v4.7.1 (f52c197) antes e para se alguma âncora não for única.
* Compilação no WSL (gfortran 13.3, Open MPI 4.1.6, netCDF-Fortran 4.5.4, dmpar, sem química), em dois executáveis da mesma ferramenta:
  * **A**: v4.7.1 sem alteração;
  * **B**: v4.7.1 com o patch.
* O executável que rodou em 18–19/10 foi compilado em outra máquina (gfortran 11.4, CMake, com química), cuja árvore não existe mais. Por isso o **controle é refeito com A**.

## Validação (antes de qualquer experimento)

1. **B sem `toro_wrf.txt` = A, bit a bit**, num teste de 30 min (d01 + d02): todas as variáveis do `wrfout` no último horário.
2. **B com o módulo ativo muda o resultado**: teste curto com `t_ini = 0`, `t_rel = 0,4 h` e `t_dur = 0,1 h`; a linha `toro_wrf: modo super-resfriado ATIVO` aparece no `rsl.error.0000`.

## Experimento (`toro_wrf.txt`)

* **Estado A**, de 25/08 17 UTC a 26/08 02:15 UTC, a até 150 km do ponto USGS, nos três domínios. Ficam suprimidos:
  * a chuva quente (autoconversão, autocoleta e acreção);
  * o congelamento por contato;
  * a nucleação primária de gelo;
  * o Hallett–Mossop;
  * o congelamento de chuva e da coleta de chuva por gelo e neve;
  * o congelamento de gotículas acima de −38 °C.

  O congelamento homogêneo fica intacto. A deposição de vapor sobre gelo que entra pelas bordas também.
* **Liberação**, de 02:15 a 02:45 UTC: física normal em todo lugar e nucleação primária ×100 numa coluna de 5 km de raio sobre o anfiteatro. É o aerossol trazido pelo vórtice. O vórtice como dinâmica imposta não está implementado nesta versão.
* Mesma rodada de 27 h (ERA5; 9/3/1 km), com `do_radar_ref = 1` nos dois casos para ter refletividade.

## Critérios (fixados antes de rodar)

1. **Retenção:** a massa máxima de água super-resfriada (`QCLOUD + QRAIN` com T < 0 °C) a até 150 km, comparada com o alvo de **1,4 × 10¹⁰ kg** e com o controle.
2. **Localização:** a massa e a coluna (kg/m²) sobre a bacia do Lhende (raio de 30 km do ponto USGS) e sobre o anfiteatro, às 02:00–02:15 UTC.
3. **Ausência de chuva antes da liberação:** chuva acumulada no anfiteatro e a até 30 km, de 17 UTC a 02:15 UTC, < 5 mm.
4. **Liberação**, de 02:15 a 03:00 UTC: taxa de congelamento, calor latente liberado, graupel e granizo formados, chuva máxima (mm/h), volume precipitado na bacia (m³) e descendente máxima (m/s).
5. **Satélite:** topo de nuvem (OLR) sobre o sítio às 02:50, contra os 272,7 K do Himawari (céu sem nuvem alta).

Só se o critério 1 chegar à ordem de 10¹⁰ kg **e** o 2 mostrar a água sobre a bacia, a liberação (4) é interpretada como candidata ao toró. Caso contrário, o resultado é o limite do modelo, e isso será dito.

## Resultado (20/10/2026)

As rodadas B (experimento) e A (controle) terminaram sem erro em 19/10. A e B são **idênticos bit a bit até 16:45 UTC** e se separam a partir de 17:30, então toda a diferença vem do módulo. Diagnóstico: `scripts/wrf/agua_superresfriada_wrf.py` sobre os recortes do vlab (sha256 conferidos); saídas em `data/processed/wrf_lhende/toro_wrf/`.

| Critério | B (super-resfriado) | A (controle) |
| :--- | ---: | ---: |
| 1. Água super-resfriada máxima a até 100 km (d02) | 1,26 × 10⁹ kg | 1,26 × 10⁹ kg |
| 1. Idem na caixa 26,5–29,5 N; 83,5–87,5 E (d02) | 5,0 × 10⁹ kg | 4,3 × 10⁹ kg |
| 1. Condensado total a até 100 km (d02) | 2,5 × 10¹⁰ kg | 2,7 × 10¹⁰ kg |
| 2. Água super-resfriada máxima a até 30 km (d02) | 8,8 × 10⁶ kg | 4,6 × 10⁶ kg |
| 2. Sobre o anfiteatro (d03) | ≤ 2,4 t | ≤ 2,3 t |
| 3. Chuva 17 UTC → 02:15 no anfiteatro / máximo a até 30 km | 0,00 / 0,0 mm | 0,01 / 3,0 mm |
| 4. Liberação (02:15 → 03): volume precipitado a até 30 km | 5,1 × 10⁴ m³ | 6,2 × 10⁴ m³ |
| 4. Graupel e granizo a até 30 km depois de 02:15 | < 1 kg | < 1 kg |
| 5. OLR sobre o sítio às 02:45 | 238 W/m² (≈ 255 K) | 238 W/m² (≈ 254 K) |

Alvo do critério 1: 1,4 × 10¹⁰ kg de água super-resfriada. Himawari às 02:50: 272,7 K.

**Leitura:**
1. **A água super-resfriada quase não aumenta.** Nem desligando todos os caminhos heterogêneos de gelo num raio de 150 km: +16% na caixa do d02, o mesmo valor a até 100 km, uma ordem abaixo do alvo. O condensado total a até 100 km (2,5 × 10¹⁰ kg) passa do alvo, mas continua quase todo gelo: os topos da convecção passam de −38 °C, onde o congelamento homogêneo (deixado ligado) gera o gelo, que depois cresce por deposição.
2. **Sem gelo, a convecção enfraquece.** No d03 às 21 UTC: ascendente máxima de 4 m/s em B contra 18 em A; graupel e granizo 3,5 × 10⁷ kg contra 1,9 × 10⁹; condensado total 9,2 × 10⁹ contra 1,5 × 10¹⁰ kg. Sem o calor latente do congelamento, a tempestade perde força e o reservatório não cresce.
3. **Sobre a bacia não há o que soltar.** A até 30 km há ~10⁷ kg; sobre o anfiteatro, toneladas. A liberação por aerossol às 02:15 não produz nada além do controle.
4. **Limite do modelo:** a água daquela noite existiu (~10¹⁰ kg de condensado a até 100 km), mas a ~90 km a sudoeste do sítio, e na fase de gelo. O modo super-resfriado, nesta forma, não a traz para a bacia nem a mantém líquida.
