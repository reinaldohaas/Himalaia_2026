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

## Experimento C: vórtice dinâmico que inicia a nucleação secundária (20/10/2026)

**Pedido do pesquisador:** pôr um vórtice dinâmico no WRF, e que esse vórtice inicie a nucleação secundária.

**Código (executável C):** o mesmo patch, estendido.
* `toro_vortice`: força tangencial ciclônica somada a `RUBLTEN`/`RVBLTEN` no driver da camada limite. A força é F = γ(t)·α·(r/rₘ)·e^(1−r/rₘ)·sech²(h/z_r), com h a altura acima do terreno e γ uma rampa linear.
* No **núcleo do vórtice** (r ≤ `raio_vn_km`, a partir de `t_vn_ini`), o Estado A é levantado, o Hallett–Mossop é multiplicado por `fhm_v` e a nucleação primária por `fnuc_v`. É o aerossol que o vórtice traz. Fora do núcleo, o Estado A continua até o fim.
* `main/depend.common` ganha a dependência do driver da camada limite no arquivo do NSSL. Sem `toro_wrf.txt`, C também fica inerte.

**Configuração** (`toro_wrf_vortice.txt`):
* Estado A de 17 UTC até 03 UTC a até 150 km, sem liberação por tempo.
* Vórtice de 00 UTC a 03 UTC (rampa de 1 h), centrado no anfiteatro, só no d03, com rₘ = 5 km, z_r = 3 km e α = 1 × 10⁻² m/s².
* Nucleação no núcleo (r ≤ 5 km) a partir de 01:30, com Hallett–Mossop ×10 e nucleação primária ×100.

**Validação:**
1. C sem `toro_wrf.txt` = A, byte a byte (30 min, d01 + d02).
2. C com `toro_wrf_teste_v.txt` (vórtice e núcleo no d02, 30 min): as linhas `toro_wrf` aparecem e U e V diferem de C inerte em torno do anfiteatro.

**Critérios** (fixados antes de rodar; comparação com B e com A):
1. **Vórtice:** vento tangencial máximo e vorticidade relativa máxima entre 2 e 6 km acima do terreno, a até 10 km do anfiteatro, às 01:30 e às 02:30 UTC.
2. **Reservatório no núcleo antes de 01:30:** água super-resfriada a até 5 km e a até 30 km, e ascendente máxima no núcleo.
3. **Nucleação secundária depois de 01:30:** número e massa de gelo (QNICE, QICE) e graupel e granizo no núcleo; fração da água super-resfriada congelada por hora; calor latente de congelamento liberado (L_f × massa congelada).
4. **Liberação:** taxa máxima de chuva, volume precipitado a até 30 km e sobre o anfiteatro de 01:30 a 03 UTC, e descendente máxima.
5. **Satélite:** OLR sobre o sítio às 02:45, contra o Himawari.

O resultado só conta como candidato ao toró se (2) mostrar um reservatório da ordem de 10¹⁰ kg sobre a bacia e (4) uma liberação da ordem de 10⁶–10⁷ m³. Abaixo disso, é o limite do modelo, e isso será dito.

## Experimento D: nucleação no núcleo disparada pela ascendente (20/10/2026)

**Pedido do pesquisador:** a água super-resfriada tem de continuar retida sobre o anfiteatro. A nucleação secundária e a liberação do calor latente só começam onde as ascendentes do vórtice chegam. Em C, o núcleo inteiro (r ≤ 5 km) passava à física normal às 01:30, com ou sem ascendente. Em D isso deixa de acontecer.

**Código (executável D):** o mesmo patch de C, com uma condição de disparo ponto a ponto na microfísica.
* No núcleo do vórtice (r ≤ `raio_vn_km`, de `t_vn_ini` a `t_v_fim`), o disparo vale onde:
  * w > `w_crit` (2 m/s);
  * a água líquida qc + qr > `q_crit` (10⁻⁵ kg/kg, 0,01 g/kg);
  * T < 0 °C.
* Onde há disparo, o Estado A é levantado, o Hallett–Mossop é multiplicado por `fhm_v` e a nucleação primária por `fnuc_v`.
* No resto do núcleo e fora dele, o Estado A continua (a máscara do Estado A agora inclui o núcleo).
* O w usado é `wvel(mgs)`, a média de w nas duas faces do ponto, calculada pelo próprio NSSL. O NSSL já usa w > 2 m/s como limiar de ascendente (`wvel(mgs) > 2.0`), e por isso 2 m/s.
* No primeiro disparo, o processo grava no seu `rsl.error` a linha `toro_wrf: nucleacao no nucleo disparada`, com w, ql e T.

**Configuração** (`toro_wrf_vortice_D.txt`): igual à de C (`toro_wrf_vortice.txt`), mais `w_crit = 2.0` e `q_crit = 1.0e-5`.

**Ordem:** D só roda depois que a rodada C terminar, no mesmo host. Os passos de D no `rodar_toro_wrf.sh` recusam rodar enquanto `wrf_C.exe` estiver ativo.

**Validação:**
1. D sem `toro_wrf.txt` = A, byte a byte (30 min, d01 + d02).
2. D com `toro_wrf_teste_vD.txt` (vórtice e núcleo no d02, 30 min, limiar baixado para 0,2 m/s só no teste): a linha do disparo aparece.

**Critérios** (fixados antes de rodar). São os mesmos cinco de C, comparados com C, B e A, mais dois:
6. **Disparo:** fração dos pontos do núcleo com w > 2 m/s e água líquida abaixo de 0 °C, por hora de 01:30 a 03 UTC, e altura desses pontos.
7. **Reservatório retido em D contra C depois de 01:30:** água super-resfriada a até 5 km e a até 30 km. D tem de manter mais água do que C, salvo onde houve disparo.

A regra de C vale para D: o resultado só conta como candidato ao toró com um reservatório da ordem de 10¹⁰ kg sobre a bacia e uma liberação da ordem de 10⁶–10⁷ m³. Abaixo disso, é o limite do modelo, e isso será dito.

## Resultado do experimento C (21/10/2026)

**A rodada:**
* A primeira tentativa morreu com a queda do contêiner do vlab.
* C foi relançada do zero no host novo e terminou sem erro (`SUCCESS COMPLETE WRF` às 09:41:02 UTC de 21/10, em 5 h 35 min).
* CFL igual ao de A e B: 66 linhas no d01 e nenhuma no d02 e no d03, nem com o vórtice ligado.
* **C = B bit a bit até 23:45 UTC.** Só se separa depois que o vórtice liga, às 00 UTC.
* Relatório do vlab: `saida/wrf_lhende/relatorios/toro_wrf/LEIA_toro_wrf_C.txt`.

**Análise:** `scripts/wrf/criterios_toro_C.py` e `scripts/wrf/agua_superresfriada_wrf.py`, sobre os recortes do d03 (1 km). Saídas em `data/processed/wrf_lhende/toro_wrf/criterios_C.json` e `agua_sr_C.log`.

| Critério | C | B | A |
| :--- | ---: | ---: | ---: |
| 1. Vento tangencial máximo, 2–6 km acima do terreno, até 10 km (00:00 / 01:30 / 02:30) | 7,6 / 13,1 / 14,4 m/s | — | — |
| 1. Vorticidade relativa máxima (01:30 / 02:30) | 7,7 / 6,7 × 10⁻³ s⁻¹ | — | — |
| 2. Água super-resfriada máxima até 5 km, 23:00–01:30 | 2,9 × 10⁶ kg | 80 kg | 420 kg |
| 2. Idem até 30 km | 1,6 × 10⁷ kg | 9,6 × 10⁶ kg | 5,2 × 10⁶ kg |
| 2. Água super-resfriada até 30 km às 02:00–02:30 | ~5 × 10⁷ kg (máx. 1,7 g/kg, ~−2 °C) | 1–2 × 10⁶ kg | — |
| 2. Ascendente máxima até 5 km, antes de 01:30 | 3,8 m/s | 1,5 m/s | 1,5 m/s |
| 3. QNICE máximo até 5 km, 01:30–03:00 | 0,6–1,6 × 10⁵ /kg | — | — |
| 3. Variação da massa de gelo até 5 km, 01:30 → 03:00 | −8,1 × 10⁵ kg (sem congelamento líquido) | −6,5 × 10⁵ kg | −3,7 × 10⁵ kg |
| 3. Graupel e granizo sobre o anfiteatro e até 30 km | ≤ 40 kg | ~0 | ~0 |
| 4. Chuva 01:30–03:00 sobre o anfiteatro | 0,01 mm | 0,00 mm | 0,00 mm |
| 4. Volume de chuva até 30 km, 01:30–03:00 | 2,0 × 10³ m³ | 5,1 × 10⁴ m³ | 7,1 × 10⁴ m³ |
| 4. Descendente mínima até 30 km, 01:30–03:00 | −14,1 m/s | −2,8 m/s | −3,2 m/s |
| 5. OLR sobre o sítio às 02:45 | 241 W/m² | 238 W/m² | 238 W/m² |

**Leitura:**
1. **O vórtice funciona como dinâmica.**
   * Gira a ~13–14 m/s entre 2 e 6 km, com vorticidade de ~7 × 10⁻³ s⁻¹.
   * Produz ascendentes de até 8 m/s e descendentes de até 14 m/s a até 30 km, contra 2–3 m/s em A e B.
2. **O vórtice concentra água super-resfriada, mas pouca.**
   * Até 5 km do centro: 2,9 × 10⁶ kg, contra 80–400 kg em B e A.
   * Até 30 km: ~5 × 10⁷ kg às 02:00–02:30, ~25 vezes B.
   * Ainda assim, 2,5–3,5 ordens de grandeza abaixo dos ~1,4 × 10¹⁰ kg pedidos.
   * A água fica a ~−2 °C, pouco super-resfriada.
3. **Não há surto de congelamento.**
   * A massa de gelo no núcleo cai de 01:30 a 03:00 em C, como em B e A.
   * Graupel e granizo não passam de dezenas de kg.
   * O Hallett–Mossop ×10 e a nucleação ×100 no núcleo não geram congelamento líquido mensurável. Com a água a −2 °C, abaixo da faixa ativa do Hallett–Mossop (−3 a −8 °C), o efeito do primeiro fica pequeno.
   * O calor latente de congelamento estimado é nulo.
4. **Não há liberação.**
   * A chuva sobre o anfiteatro continua nula.
   * O volume de chuva até 30 km é menor que em B e A (2 × 10³ contra 5–7 × 10⁴ m³), apesar das descendentes fortes.
   * Muito abaixo de 10⁶–10⁷ m³.
5. **O OLR às 02:45 é igual ao de A e B** (~241 W/m², ~255 K). Não reproduz o céu sem nuvem alta que o Himawari mostra (topo ≥ 263 K, § 6 do GEOESTACIONARIO).

**Veredito pela regra pré-registrada:**
* C **não** é candidato ao toró: o reservatório fica em ~10⁷ kg sobre a bacia, contra 10¹⁰, e a liberação é ~10³ m³, contra 10⁶–10⁷.
* É o limite do modelo nesta configuração. O vórtice gera a dinâmica, mas a microfísica não acumula nem congela água em escala comparável.
* **O experimento D** (nucleação só onde w > 2 m/s) testa se reter a água fora das ascendentes aumenta o reservatório e concentra o congelamento.

## Executável único: A, B, C e D pelo `namelist.input` (21/10/2026)

**Pedido do pesquisador:** administrar os experimentos pelo `namelist.input`, e não por executáveis diferentes.

**Código:** o mesmo módulo, versão 3 (`module_toro_wrf.F`), compilado uma vez em `wrf_toro.exe` (sha256 `422faac0…`).
* **Configuração** no grupo `&toro_wrf` do próprio `namelist.input`. O WRF ignora grupos de namelist que não conhece. A forma antiga, o arquivo `toro_wrf.txt`, continua aceita.
* **A** = sem o grupo, ou com `ligado = .false.`: o módulo fica inerte.
* **Duas chaves novas** fazem C e D saírem do mesmo código:

  | Chave | D (padrão) | C |
  | :--- | :--- | :--- |
  | `disparo_w` | `.true.`: nucleação no núcleo só onde w > `w_crit`, com água líquida e T < 0 °C | `.false.`: no núcleo inteiro |
  | `nucleo_no_estado_A` | `.true.`: o núcleo segue no Estado A fora do disparo | `.false.`: o núcleo fica fora do Estado A |

* **Configurações por experimento:**

  | Experimento | Arquivo do grupo |
  | :--- | :--- |
  | B | `toro_wrf.txt` |
  | C | `toro_wrf_vortice_C.txt` (= `toro_wrf_vortice.txt` + as duas chaves em `.false.`) |
  | D | `toro_wrf_vortice_D.txt` |

  Testes: `toro_wrf_teste.txt`, `toro_wrf_teste_vC.txt` e `toro_wrf_teste_vD.txt`.
* **Script:** `rodar_toro_wrf.sh rodada_u A|B|C|D` acrescenta o grupo ao `namelist.input` da rodada e roda o `wrf_toro.exe`.

**Validação (antes de usar):** `rodar_toro_wrf.sh teste_unico` roda os quatro testes de 30 min com o executável único. O `wrfout_d01` e o `wrfout_d02` têm de ser iguais, byte a byte, aos dos testes já feitos com os executáveis separados:

| Teste com o executável único | Referência |
| :--- | :--- |
| A | `toro_tA` |
| B | `toro_tBa` |
| C | `toro_tCa` |
| D | `toro_tDa` |

Se os quatro baterem, os executáveis separados podem ser aposentados, e as rodadas A–D já feitas continuam valendo.

**Resultado (22/10/2026): validado.** Os quatro testes (A, B, C e D) conferem byte a byte com as referências, no `wrfout_d01` e no `wrfout_d02`; o de D rodou das 13:38 às 13:47 UTC. Relatório do vlab: `relatorios/toro_wrf/LEIA_toro_wrf_U.txt`.
* O `wrf_toro.exe` lê o grupo pelo `namelist.input` ("modo super-resfriado ATIVO (namelist.input lido)").
* Daqui em diante os experimentos se escolhem só pelo namelist (`rodar_toro_wrf.sh rodada_u A|B|C|D`).

## Resultado do experimento D (22/10/2026)

**A rodada:**
* Foi lançada três vezes por causa das quedas do contêiner.
* A última terminou com `SUCCESS COMPLETE WRF` às 15:53:44 UTC de 21/10, 17 s antes de mais uma queda.
* **D = C bit a bit até 01:30 UTC**, inclusive no d03. As duas só podiam se separar a partir do início da nucleação no núcleo (`t_vn_ini` = 01:30).
* **O disparo aconteceu uma única vez:**
  * só em um dos 112 processos (`rsl.error.0060`), logo depois de 01:30;
  * no ponto, w = 2,03 m/s, logo acima do limiar, ql = 7,8 × 10⁻⁴ kg/kg e T = 271,72 K (−1,4 °C);
  * nenhum outro processo registrou disparo até 03 UTC.
* Relatório do vlab: `relatorios/toro_wrf/LEIA_toro_wrf_D.txt`.

**Análise:** `scripts/wrf/criterios_toro_C.py` com os rótulos D, C, B. Saídas em `data/processed/wrf_lhende/toro_wrf/criterios_D.json` e `.log`.

| Critério | D | C | B |
| :--- | ---: | ---: | ---: |
| 1. Vento tangencial máximo (00:00 / 01:30 / 02:30) | 7,6 / 13,1 / 14,4 m/s | igual | — |
| 2. Água super-resfriada máxima até 5 km, 23:00–01:30 | 2,9 × 10⁶ kg | igual | 80 kg |
| 3. QNICE máximo até 5 km às 02:00 / 02:30 / 03:00 | 1,1 × 10² / 0,4 / 0,04 por kg | 0,6–1,6 × 10⁵ por kg | — |
| 3. Variação da massa de gelo até 5 km, 01:30 → 03:00 | −8,1 × 10⁵ kg | −8,1 × 10⁵ kg | −6,5 × 10⁵ kg |
| 7. Variação da água super-resfriada até 5 km, 01:30 → 03:00 | −4,0 × 10⁵ kg | −4,5 × 10⁵ kg | +1,7 × 10⁴ kg |
| 4. Chuva sobre o anfiteatro, 01:30–03:00 | 0,00 mm | 0,01 mm | 0,00 mm |
| 4. Volume de chuva até 30 km, 01:30–03:00 | 1,9 × 10² m³ | 2,0 × 10³ m³ | 5,1 × 10⁴ m³ |
| 4. Descendente mínima até 30 km | −14,1 m/s | −14,1 m/s | −2,8 m/s |
| 5. OLR sobre o sítio às 02:45 | 242 W/m² | 241 W/m² | 238 W/m² |

**Leitura:**
1. **O disparo pela ascendente quase não acontece.** No núcleo, pontos com w > 2 m/s, água líquida e T < 0 °C aparecem uma vez, num só processo, e logo depois de 01:30. A água do núcleo está a ~−1 a −2 °C. As ascendentes fortes do vórtice (até 8 m/s) ficam em sua maioria fora dessa água ou abaixo de 0 °C.
2. **Sem disparo, o núcleo volta ao Estado A e o gelo some.** O QNICE no núcleo cai de ~10⁵ para ~0 por kg entre 01:30 e 03:00 (em C fica em ~10⁵). A massa de gelo cai como em C.
3. **A água retida é praticamente a mesma de C:** D retém ~5 × 10⁴ kg a mais até 5 km. O critério 7 passa por pouco, sem efeito físico relevante.
4. **Não há liberação:** a chuva até 30 km é ainda menor que em C.

**Veredito pela regra pré-registrada:**
* D **não** é candidato ao toró: o reservatório é de ~10⁷ kg e a liberação de ~10² m³.
* A condição de disparo, que era a correção pedida, mostrou outra coisa. **No modelo, a água super-resfriada do núcleo e as ascendentes que poderiam disparar a nucleação quase não coincidem.**
* Na hipótese revisada (22/10/2026; `LINHA_DO_TEMPO_EVENTO_26AGO2026.md` § 9), a pergunta passa a ser o acúmulo de granizo, graupel e neve no chão das encostas altas. A próxima diagnose é `SNOWNC`, `GRAUPELNC` e `HAILNC` nas rodadas A–D.

## Precipitação sólida acumulada no solo, rodadas A–D (22/10/2026)

**Pergunta da hipótese revisada:** quanto granizo, graupel e neve se acumularam no chão das encostas altas durante a noite?

**Dados e saídas:**
* Recortes `recorte_solo_d03.nc` do vlab (d03, 1 km; `RAINNC`, `SNOWNC`, `GRAUPELNC`, `HAILNC`, `SNOW`, `SNOWH`, de 25/08 17:00 a 26/08 03:00).
* Script `scripts/wrf/acumulado_solo.py`; saída `data/processed/wrf_lhende/toro_wrf/acumulado_solo.json`.

**Resultado, 17:00 → 02:45 UTC, nas quatro rodadas:**

| Região | Células de 1 km | Cota média no WRF | Precipitação total | Sólida (neve + graupel + granizo) | Graupel + granizo | ΔSWE |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Anfiteatro | 4 | 5.749 m | ≤ 0,01 mm | 0,00 mm (≤ 60 kg) | 0 | ~0 |
| Encostas altas, ≥ 6.000 m (caixa 85,48–85,58 E, 28,24–28,30 N) | 5 | 6.255 m | ≤ 0,03 mm | 0,00 mm (≤ 120 kg) | 0 | ~0 |
| Até 1 km da cicatriz | 7 | 4.930 m | 0,00 mm | 0,00 mm | 0 | ~0 |

**Leitura:**
1. **Nenhuma das rodadas deposita precipitação sólida apreciável no maciço**, nem nas encostas altas nem sobre a cicatriz. Os máximos do d03 às 02:45 (neve 18 mm, graupel 6,6 mm, granizo 0,1 mm) ficam longe do sítio.
2. **O relevo do WRF a 1 km está muito suavizado:**
   * no maciço, o ponto mais alto do modelo tem **6.438 m, contra 7.216 m no GLO-30**;
   * a área acima de 6.000 m cai de 11,8 km² (GLO-30) para 5 células (5 km²);
   * as encostas altas, onde a hipótese revisada põe a acumulação, praticamente não existem no modelo.
   * É um argumento forte para o ERF, com terreno imerso e refinamento local.
3. **Em resumo:** com o terreno e a microfísica atuais, o WRF não acumula a massa no alto. Isso pode ser um limite do modelo, por causa do relevo rebaixado, e não um teste conclusivo da hipótese.

## Experimento E: vórtice em níveis médios sobre as encostas altas (24/10/2026)

**Motivo:** a hipótese revisada (`LINHA_DO_TEMPO_EVENTO_26AGO2026.md` § 9) põe a formação do granizo e do gelo **no alto**. A massa se formaria sobre as encostas de 6–7 km e escorregaria até a cicatriz (~4.000–5.140 m). Em C e D, o vórtice tinha três desencontros com isso:
* estava centrado no anfiteatro (ponto do USGS);
* tinha a força máxima junto ao chão;
* ligava às 00 UTC e só nucleava a partir de 01:30, depois que o topo da nuvem sobre o sítio já tinha descido ao terreno (Himawari, 00:00–01:20).

Em D, a água do núcleo estava a −1/−2 °C e quase nunca coincidia com as ascendentes.

**Código (módulo versão 4, executável único):** duas opções novas. Com os valores padrão, o comportamento de A–D não muda (a validar byte a byte).
* `perfil_v = 1`: força tangencial gaussiana em altitude, F ∝ exp(−((z − `zc_v_m`)/`zw_v_m`)²). O padrão (`perfil_v = 0`) é o sech²(h/`zr_v_m`) a partir do chão.
* `t_nuc_min_c` e `t_nuc_max_c`: o disparo da nucleação no núcleo só acontece com `t_nuc_min_c` < T < `t_nuc_max_c` (°C). Os padrões −999 e 0 equivalem ao T < 0 °C de D.

**Configuração** (`toro_wrf_vortice_E.txt`; o resto igual a D):

| Parâmetro | D | E | Base |
| :--- | :--- | :--- | :--- |
| Centro do vórtice | 28,271 N / 85,515 E | **28,270 N / 85,535 E** | faixa de 6.000–6.500 m do GLO-30 a ~2 km ao sul (morro acima) da cicatriz, centrada em 28,268 N / 85,534 E; deslocamento de ~1 km a leste pela deriva (vento de 1,5–5 m/s de NE–E entre 7 e 9 km nas sondagens ERA5 das 18 e 00 UTC: um granizo caindo de ~8 km deriva só 1–3 km) |
| Perfil vertical | sech²(h/3 km) a partir do chão | **gaussiana centrada em 7.500 m ASL, meia-largura 1.500 m** | mesociclone em níveis médios, onde ficam a água super-resfriada e o crescimento do granizo |
| Vórtice ligado | 00:00–03:00 (rampa de 1 h) | **22:00–01:30** (rampa de 1 h) | colapso da convecção perto do sítio (22–01 UTC) e descida do topo sobre o sítio (00:00–01:20) |
| Nucleação no núcleo | a partir de 01:30, w > 2 m/s, T < 0 °C | **a partir de 00:00, w > 1 m/s, −8 < T < −3 °C** | faixa ativa do Hallett–Mossop, que no perfil de agosto fica a ~5,8–6,6 km ASL, a altura das encostas altas |

**Validação:**
1. `teste_unico`: A–D com o executável novo, byte a byte iguais às referências.
2. `teste_ativo_u E`: 30 min com `toro_wrf_teste_vE.txt` (no d02); as linhas novas do `toro_wrf` aparecem e o d02 difere de `toro_tDa`.

**Critérios (fixados antes de rodar), comparados com D e A:**
1. **Vórtice:** vento tangencial e vorticidade entre 6 e 9 km ASL, a até 10 km do centro, às 23:00, 00:30 e 01:30.
2. **Disparo:** quantos processos registram disparo, quando e a que temperatura.
3. **Água super-resfriada e gelo** a até 5 e 30 km do centro, de 22:00 a 01:30.
4. **O critério principal da hipótese revisada:** **graupel, granizo e neve acumulados no chão** (`recorte_solo_d03.nc`) nas encostas ≥ 6.000 m e a até 1 km da cicatriz, de 22:00 a 02:45.
5. **Chuva e descendente** sobre o anfiteatro e a até 30 km.

Regra: o resultado só conta como **candidato** se o critério 4 der uma massa sólida no chão das encostas altas da ordem de 10⁹–10¹⁰ kg, o que corresponde a ~10⁶–10⁷ m³ de gelo. Abaixo disso, é o limite do modelo, que tem o relevo rebaixado a 1 km (a ser testado no d04).
