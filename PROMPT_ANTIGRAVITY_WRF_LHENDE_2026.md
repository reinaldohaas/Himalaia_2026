# Prompt para o antigravity — simulação WRF do Lhende Khola, 24–26/08/2026

**Data:** 14 de outubro de 2026
**Uso:** copiar a PARTE B inteira para o antigravity. A PARTE A é para o pesquisador.

---

# PARTE A — Para o pesquisador (não enviar)

## A.1 Por que WRF agora

O toro-CM1 levou o teste até onde um domínio idealizado consegue (ver `TORO_CM1_SONDAGEM_REAL_ERA5.md`). Restaram quatro limitações que só um modelo de mesoescala aninhado e forçado pela reanálise resolve:

| Limitação do CM1 | Como o WRF resolve |
| :--- | :--- |
| Sondagem única, horizontalmente homogênea; sem o sistema que o Himawari mostrou às 18 UTC | condição inicial e de fronteira 3D da ERA5, horária, em domínios aninhados |
| Radiação sem inclinação nem sombra: a face norte do circo recebe o sol de uma face sul | `slope_rad=1`, `topo_shading=1` |
| Solo sem neve: a geleira passa de 0 °C | Noah-MP, com neve em camadas e tratamento de geleira |
| Ascendências espúrias de 50–67 m/s sobre encostas íngremes aquecidas | coordenada híbrida, `epssm`, suavização de terreno controlada, e um diagnóstico obrigatório do artefato |

## A.2 O que o prompt exige

* **Pré-registro.** A configuração e os critérios de falseamento são gravados e commitados **antes** da primeira rodada. Depois disso, qualquer mudança é registrada e justificada, e nenhuma pode ser feita para aproximar o resultado de uma hipótese.
* **Validação antes de interpretação.** Precipitação contra o IMERG e convecção contra o Himawari. Se o modelo errar o tempo ou a quantidade, isso é dito antes de qualquer número sobre o anfiteatro.
* **Nada inventado.** Se o WRF não compilar, não rodar ou explodir, o relatório diz isso e mostra o erro. "Resultado esperado" não é resultado.
* **Custo explícito.** O domínio de 333 m é caro. O prompt permite parar em 1 km, desde que isso seja declarado.

## A.3 O que vou verificar quando voltar

* Os `namelist.wps`/`namelist.input` commitados são os mesmos que geraram os `wrfout`. Confiro pelo cabeçalho global do NetCDF e pelo hash do commit.
* Os `rsl.out.0000`/`rsl.error.0000` mostram `SUCCESS COMPLETE WRF`.
* Recalculo três números do relatório a partir dos `wrfout`.
* A comparação com o IMERG usa os mesmos grânulos já baixados neste repositório.

---

# PARTE B — Prompt (copiar daqui para baixo)

---

Você vai configurar, rodar e analisar uma simulação **WRF-ARW** aninhada do evento do Lhende Khola (Rasuwa, Nepal / Gyirong, Tibete). O colapso ocorreu em **26/08/2026 às 02:52:10 UTC**, no ponto **28,271 N, 85,515 E**, em ~5.200–5.600 m. A pergunta é **discriminar hipóteses**, não confirmar uma.

## B.0 Regras invioláveis

1. **Nenhum número sem arquivo.** Todo valor do relatório vem de um `wrfout`, de um arquivo de validação baixado ou de um script do repositório que o calcula. Cada figura e tabela indica o script que a gerou.
2. **Se algo falhar, diga.** Não compilou, `real.exe` falhou, a rodada explodiu por CFL, a máquina não aguenta 333 m: registre o erro com as linhas relevantes do `rsl.error.0000` e pare naquela etapa, ou use o recuo previsto na §B.7. **Nunca** descreva resultados de uma rodada que não terminou com `SUCCESS COMPLETE WRF`.
3. **Pré-registro (§B.6) antes da primeira rodada.** Commite `namelist.wps`, `namelist.input` e o arquivo de critérios **antes** de rodar. O hash desse commit entra no relatório.
4. **Proibido ajustar a configuração para aproximar o resultado de uma hipótese.** Toda mudança depois do pré-registro, mesmo por estabilidade numérica, vai para `wrf/MUDANCAS.md` com data, motivo e efeito. Mudanças por estabilidade são aceitáveis; mudanças por resultado, não.
5. **Credenciais** só dos arquivos já configurados (`~/.cdsapirc`, `~/.netrc`, `~/.earthdata_token.txt`). Nunca imprima, registre em log nem commite token ou senha. Não crie contas. Uma requisição de teste por serviço; se vier 401 ou 403, pare aquele serviço.
6. **Não altere** arquivos existentes do repositório. Tudo novo vai em `wrf/`, `scripts/wrf/`, `data/raw/wrf_input/` e `data/processed/wrf/`. **Não commite `wrfout` completos.** Commite os subconjuntos da §B.5 e o manifesto.

## B.1 Hipóteses a discriminar

* **H1 — sem aporte atmosférico relevante:** o colapso é gravitacional e a água veio do que já estava no sistema.
* **H3 — acumulação orográfica prévia:** nuvem com água super-resfriada a sotavento ou sobre o circo deposita por *riming* nas horas anteriores, carregando a massa.
* **H4 — aguaceiro confinado:** precipitação extrema sobre < 15 km², invisível ao IMERG a 0,1°.

O que já foi medido, com fonte no repositório:

| Grandeza | Valor | Arquivo |
| :--- | :--- | :--- |
| IMERG V07 Late até o colapso | 5,09 mm; 0,000 mm/h no instante; 12,66 mm em 25+26/08 | `IMERG_15_EVENTOS_RESULTADO.md`, `data/processed/imerg_15_eventos.csv` |
| Himawari-9 B13, área < 213 K | 8.413 km² às 18 UTC de 25/08 → 4.892 → 810 → **0 km²** às 02:50 | `GEOESTACIONARIO_NOITE_25_26AGO2026.md` |
| BT sobre o sítio às 02:50 | 272,7 K | idem |
| Bacia a montante da chegada ao vale | 3,39 km², 4.010–7.216 m, 77 % face norte | `ANALISE_DEM_GLO30_E_AUSENCIA_DE_LAGO.md` |
| ERA5 no ponto | coluna livre estável; 0 °C a ~5.890 m; vento de 0,4–2,8 m/s entre 4 e 8 km | `TORO_CM1_SONDAGEM_REAL_ERA5.md` §1 |
| CM1 com terreno, radiação e fluxos | convecção à tarde adiantada 4–6 h e 2,5× mais chuva que o IMERG; nuvem líquida a 0 a −3 °C sobre o circo no colapso, sem gelo | idem, §8 |

Os resultados do CM1 são **contexto**, não alvo. Não ajuste nada para reproduzi-los nem para contradizê-los.

## B.2 Dados de entrada

| Dado | Origem | Detalhe |
| :--- | :--- | :--- |
| **ERA5 níveis de pressão** | CDS, `reanalysis-era5-pressure-levels`, **GRIB** | 37 níveis; z, t, u, v, w, q, r; **horário**; de 24/08 12 UTC a 26/08 06 UTC; caixa 20–36 N, 76–95 E |
| **ERA5 níveis únicos** | CDS, `reanalysis-era5-single-levels`, GRIB | sp, msl, 2t, 2d, 10u, 10v, skt, sst, lsm, z (geopotencial de superfície), stl1–4, swvl1–4, sd, rsn, tsn, ci; mesma janela |
| Vtable | `Vtable.ECMWF` do WPS, ou `Vtable.ERA-interim.pl` | registre qual |
| **Topografia d03/d04** | **Copernicus GLO-30** (tiles `N27–N29`, `E084–E086`, AWS aberto), reamostrada para 1 km e 333 m e convertida ao formato binário do geogrid (`index` + tiles) | o GMTED 30″ padrão é grosso demais para 333 m; documente o script de conversão |
| Topografia d01/d02 | GMTED2010 30″ padrão do WPS | — |
| Uso do solo | MODIS IGBP 15″ padrão (`modis_landuse_20class_15s`) | sensibilidade opcional com ESA WorldCover 2021 |
| Validação, precipitação | GPM IMERG V07 Late meia-horária: os grânulos já catalogados em `data/raw/meteorology/` | não rebaixar o que já existe |
| Validação, nuvem | Himawari-9 AHI B13 (10,4 µm), série de 18 instantes já processada | `GEOESTACIONARIO_NOITE_25_26AGO2026.md` |

Faça os pedidos ao CDS **por dia**, para respeitar o limite de custo. Grave tudo no manifesto (§B.8).

## B.3 Configuração (pré-registrada)

**Período:** início em **24/08/2026 12 UTC** (38 h de *spin-up* antes do colapso), fim em **26/08/2026 06 UTC**.

**Domínios** (aninhamento de mão dupla, projeção Mercator, centro do d04 em 28,271 N, 85,515 E):

| | Δx | Pontos (aprox.) | Extensão | `time_step` inicial | Saída |
| :--- | ---: | :--- | :--- | ---: | :--- |
| d01 | 9 km | 220 × 190 | ~2.000 × 1.700 km | 45 s | 1 h |
| d02 | 3 km | 241 × 241 | ~720 km | razão 3 | 1 h |
| d03 | 1 km | 241 × 241 | ~240 km | razão 3 | 30 min |
| d04 | 333 m | 181 × 181 | ~60 km | razão 3 | **10 min** |

**Vertical:** `e_vert = 80`, `p_top_requested = 5000` Pa, níveis concentrados entre a superfície e 8 km, com espessura ≤ 150 m entre 4 e 7 km ASL; `hybrid_opt = 2`, `etac = 0.2`.

**Física:**

| Opção | d01 | d02 | d03 | d04 |
| :--- | :--- | :--- | :--- | :--- |
| `mp_physics` | **18** (NSSL 2-momentos + CCN; inclui Hallett-Mossop) | 18 | 18 | 18 |
| `cu_physics` | 3 (Grell-Freitas) | 0 | 0 | 0 |
| `bl_pbl_physics` | 5 (MYNN 2.5) | 5 | 5 | **0** (LES: `km_opt=2`, `diff_opt=2`) |
| `sf_sfclay_physics` | 5 | 5 | 5 | 5 |
| `sf_surface_physics` | **4** (Noah-MP) | 4 | 4 | 4 |
| `ra_lw/sw_physics` | 4/4 (RRTMG) | 4/4 | 4/4 | 4/4 |
| `radt` (min) | 9 | 3 | 1 | 1 |
| `slope_rad` / `topo_shading` | 1/1 | 1/1 | 1/1 | 1/1 (`shadlen = 25000`) |
| `diff_opt`/`km_opt` | 2/4 | 2/4 | 2/4 | 2/2 |
| `w_damping` | 1 | 1 | 1 | 1 |
| `epssm` | 0,5 | 0,5 | 0,5 | 0,5 |
| `damp_opt` / `zdamp` / `dampcoef` | 3 / 5000 / 0,2 | idem | idem | idem |

* Noah-MP: `opt_snf` (partição chuva/neve) e `opt_gla` (geleira) nos valores padrão; registre quais.
* `smooth_option = 'smth-desmth_special'` no geogrid, com `smooth_passes` mínimo para estabilidade. **Registre a declividade máxima** do terreno do d04 antes e depois da suavização.
* Saídas extras no d04 por `iofields_filename`: `QNICE`, `QNCLOUD`, `QNRAIN`, `QNSNOW`, `QNGRAUPEL`, `QVOLG`, `W`, `REFL_10CM`, `SNOWNC`, `GRAUPELNC`, `RAINNC`, `SNOW`, `SNOWH`, `HFX`, `LH`, `SWDOWN`, `TSK`.

**Rodadas:**

| Rodada | O que muda | Domínios |
| :--- | :--- | :--- |
| **CTL** | configuração acima | d01–d04 |
| **MP-THO** | `mp_physics = 8` (Thompson) | d01–d03 (d04 se houver recurso) |
| **MP-MOR** | `mp_physics = 10` (Morrison 2-momentos) | d01–d03 (idem) |
| **NOSLOPE** | `slope_rad = 0`, `topo_shading = 0` | d01–d04 |

A NOSLOPE mede exatamente o erro de radiação que o CM1 cometeu.

## B.4 Validação obrigatória (antes de qualquer número sobre o anfiteatro)

1. **Precipitação × IMERG.** Agregue a chuva do d02, d03 e d04 na grade de 0,1° do IMERG. Compare, meia-hora a meia-hora, de 25/08 00 UTC a 26/08 06 UTC: na célula do sítio, nas 8 células vizinhas e na caixa de ±0,25° já usada no repositório. Reporte o viés total, a correlação temporal e o horário do pico.
2. **Nuvem × Himawari.** Calcule a temperatura de topo do modelo (temperatura no nível onde a espessura óptica integrada de cima para baixo atinge 1; documente o método) e a área < 213 K e < 240 K na **mesma caixa** usada no relatório geoestacionário. Compare com 8.413 / 4.892 / 810 / 0 km² às 18, 21, 00 e 02:50 UTC.
3. **Temperatura de topo sobre o sítio às 02:50** contra os 272,7 K do Himawari.
4. **Perfil sobre o ponto × ERA5** às 12, 18 e 00 UTC: T, UR e vento entre 500 e 300 hPa.

**Se o pico de precipitação ou de convecção errar o horário em mais de 3 h, ou o acumulado errar em mais de um fator 2**, escreva isso no topo do relatório. Toda conclusão sobre o anfiteatro passa a ser condicionada a esse erro.

## B.5 Diagnósticos sobre o anfiteatro (d04, a cada 10 min)

Duas máscaras:
* **circo:** a bacia de 3,39 km² delineada no GLO-30 (priority-flood + D8, ponto de saída a 4.010 m), rasterizada na grade do d04;
* **caixa:** 3 × 3 km centrada em 28,271 N, 85,515 E.

Para cada máscara:

| Diagnóstico | Definição |
| :--- | :--- |
| Precipitação por fase | `RAINNC`, `SNOWNC`, `GRAUPELNC` acumulados (mm e m³) |
| Variação do equivalente em água da neve | ΔSWE do Noah-MP (mm e m³) |
| Água super-resfriada | massa de QCLOUD + QRAIN com T < 0 °C na coluna (t), e LWC máximo (g/m³) |
| Cristais na faixa de Hallett-Mossop | máx e mediana de QNICE × ρ onde −8 ≤ T ≤ −3 °C (L⁻¹), e graupel na mesma faixa |
| Ascendência | w máx e percentil 99 entre 0 e 3 km acima do solo |
| *Riming* — cota superior | Σ ρ·q_l(T<0)·\|V_h\|·tan α·E·A·Δt no 1º nível, com **E = 1** e **E = 0,3**; reporte as duas |
| Balanço de energia | `HFX`, `LH`, `SWDOWN`, `TSK` médios |

Grave as séries em `data/processed/wrf/anfiteatro_<rodada>.csv` e os campos 2D do d04 a cada 30 min em `data/processed/wrf/d04_<rodada>_2d.nc` (só as variáveis acima).

**Diagnóstico obrigatório de artefato numérico** (houve problema no CM1): a cada saída do d04, a fração dos pontos com w > 10 m/s que estão a menos de 1 km do solo, e a declividade média desses pontos. Se mais de 50 % estiverem a menos de 1 km do solo em algum instante, marque esse instante como **suspeito** nas tabelas.

## B.6 Critérios de falseamento — gravar em `wrf/PRE_REGISTRO.md` antes de rodar

Valem para a rodada CTL, e só se ela passar na validação da §B.4. Se não passar, valem como "indicativos".

* **H4 é rejeitada** se a precipitação total (chuva + neve + graupel) sobre o circo, de 25/08 00 UTC a 26/08 02:52 UTC, for **< 100 mm**, e se a maior taxa em 10 min sobre o circo for **< 50 mm/h**.
* **H3 é rejeitada** se não houver água líquida com T < 0 °C sobre o circo em **nenhuma** saída entre 25/08 18 UTC e 26/08 02:52 UTC, **ou** se a cota superior de *riming* com E = 1 no mesmo intervalo for **< 10⁵ m³**.
* **O aporte atmosférico não fecha o balanço** (o que favorece H1) se a soma precipitação + *riming* (E = 1) + ΔSWE sobre o circo, de 25/08 00 UTC ao colapso, for **< 10⁶ m³**. O valor de 14,2 × 10⁶ m³ do repositório é premissa, não alvo.
* **Nenhuma hipótese é declarada confirmada** pela simulação. O resultado possível é rejeição ou compatibilidade.

## B.7 Recursos e recuo

* Antes de rodar, estime o custo: pontos × passos × rodadas, núcleos e horas de parede. Registre a máquina, o número de núcleos MPI, a versão do WRF/WPS, o compilador e as opções de compilação (`configure.wrf`).
* **Se não houver recurso para o d04**, rode só d01–d03 e diga isso **no título** do relatório: "WRF 1 km, sem LES". Os diagnósticos da §B.5 passam a ser no d03 e valem só como indicativos para um circo de 3,39 km² (~3 células).
* **Se a rodada explodir por CFL:** primeiro reduza o `time_step`; depois aumente `smooth_passes`; por último `epssm` → 0,9. Uma alteração por vez, cada uma registrada em `MUDANCAS.md`.

## B.8 Manifesto e entrega

* `data/raw/wrf_input/MANIFESTO.csv`: `arquivo, sha256, bytes, fonte, requisicao_ou_url, data_download_utc`, para todo GRIB, tile de DEM e arquivo de validação.
* `wrf/`: `namelist.wps`, `namelist.input` de cada rodada, `configure.wrf`, `iofields`, `PRE_REGISTRO.md`, `MUDANCAS.md`, e as últimas 50 linhas de `rsl.out.0000` e `rsl.error.0000` de cada rodada.
* `scripts/wrf/`: conversão do GLO-30 para o geogrid, download da ERA5, pós-processamento, validação e figuras. Tudo reexecutável.
* Relatório **`WRF_LHENDE_2026.md`**, nesta ordem:
  1. o que rodou e o que não rodou, com recursos usados e hash do pré-registro;
  2. validação (§B.4), com o veredito sobre horário e quantidade no topo;
  3. diagnósticos do anfiteatro (§B.5), com instantes suspeitos marcados;
  4. aplicação mecânica dos critérios da §B.6: para cada hipótese, "rejeitada", "compatível" ou "indeterminado", com o número que decide;
  5. limitações.

**Sem seção de discussão que vá além dos critérios.** Se o resultado for indeterminado, escreva "indeterminado".
