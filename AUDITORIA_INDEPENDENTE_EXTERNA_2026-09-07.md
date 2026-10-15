# Auditoria Independente Externa — Repositório `reinaldohaas/Himalaia_2026`

**Data da auditoria:** 07 de setembro de 2026
**Commit auditado:** `87ed6aa` (branch `main`)
**Escopo:** proveniência de dados, consistência interna, reprodutibilidade computacional, correção das citações e confronto com registros externos independentes (USGS FDSN, NOAA/SWPC, literatura revisada por pares, relatos públicos do evento de 26/08/2026).
**Natureza:** auditoria adversarial. O objetivo não é confirmar as conclusões do projeto, mas tentar quebrá-las. O que sobreviver é o que está sustentado.

---

## 0. Veredito resumido

| Pilar da investigação | Situação após auditoria |
| :--- | :--- |
| Cronologia física do evento (colapso rocha-gelo → barramento → galgamento) | **Sustenta-se.** Confirmado por fonte externa independente. |
| Reconstrução hidráulica de Manning (aritmética) | **Correta.** Os números conferem. |
| "Déficit hídrico de ~10×" | **Não sustentado.** É artefato de premissas escolhidas à mão, não resultado medido. |
| "Forçamento solar $J_z$" / rede de 14 magnetômetros | **Refutado.** Não existe inversão de magnetômetro alguma no repositório. Os valores são gerados por fórmula analítica, com o salto do flare inserido à mão no código. |
| Dados de raios/descargas dos 15 eventos | **Refutado para os eventos anteriores a 2004.** Nenhuma rede capaz de produzir esses números existia. |
| Reprodutibilidade "100%" anunciada no README | **Falsa.** O comando-mestre da auditoria falha e sai com erro já na primeira etapa. |
| Rigor de citação | **Deficiente.** A referência central sobre Chamoli tem DOI, título e paginação errados, e a conclusão que lhe é atribuída é o inverso da conclusão publicada. |

**Conclusão geral:** o repositório contém trabalho de sistematização e visualização considerável, e a descrição da cadeia física do desastre de 26/08/2026 está essencialmente correta. Porém, **as duas conclusões que o projeto apresenta como descobertas originais — o déficit hídrico de 10× e o forçamento eletrodinâmico solar — não são suportadas pelos dados contidos no próprio repositório.** Ambas são consequências aritméticas de parâmetros digitados à mão em dicionários Python, apresentados ao leitor como observações instrumentais.

---

## 1. Achados críticos de proveniência (dados sintéticos apresentados como observação)

### 1.1 A "inversão de $J_z$ com rede de 14 magnetômetros" não lê nenhum magnetômetro

`TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md` (§3) e `README.md` afirmam que $V_I = 356{,}4$ kV e $J_z \approx 4{,}57$ pA/m² foram "invertidos através de uma rede de 14 estações Trans-Himalaia (LZA, XAN, CDT, KKN, TIR)". O `DATA_PROVENANCE_AND_INDEPENDENT_AUDIT_PROTOCOL.md` (linha 61) declara cadência de **1 segundo**, proveniência **INTERMAGNET / China Earthquake Administration**, e variações de $H$, $D$, $Z$.

O que o código faz de fato, em `scripts/recalculate_jz_with_china_network.py:88`:

```python
dH_LZA = 15.0 + 50.0 * sq_china   # Lhasa (3.650m)
dH_XAN = 16.0 + 46.0 * sq_china   # Xi'an
...
```

Cada uma das 14 "estações" é uma constante somada a um seno diurno. **Nenhum arquivo de magnetômetro é lido; nenhum existe no repositório.** Não há componentes $D$ nem $Z$, nem dado de 1 s — apenas uma série horária construída.

O "salto do flare" é inserido literalmente à mão (`scripts/recalculate_jz_with_china_network.py:105-110`):

```python
if dt.strftime("%Y-%m-%d %H") == "2026-08-25 10":
    xray_flux = 7.0e-5
    delta_V_solar = 118.4
    dH_LZA += 25.0
```

E o $J_z$ resultante é simplesmente (`:118`):

```python
Rc_himalaya = 0.78e17
Jz = (VI * 1e3) / Rc_himalaya * 1e12
```

Verificação: $(238{,}0 + 118{,}4)\times10^3 / 0{,}78\times10^{17} = 4{,}569\times10^{-12}$ A/m² $= 4{,}57$ pA/m². **O valor de pico publicado é a consequência aritmética direta do `118.4` digitado no código.** Não é medida nem inversão: é tautologia.

O mesmo vale para os 15 eventos. Conferi a coluna inteira de `data/himalayan_events_1980_2026.json`: em **todos** os casos $J_z = V_I / 0{,}78\times10^{17}$, com a **mesma** resistência colunar de 1981 a 2026 e de Ladakh (34°N, ~3.500 m) a Sikkim (27,9°N, ~5.200 m). Ou seja, $J_z$ não carrega informação alguma além de $V_I$, e $V_I$ é atribuído à mão evento a evento. A "correlação solar" é uma renomeação, não um resultado.

### 1.2 Duas versões incompatíveis do mesmo arquivo de saída

`scripts/process_7day_magnetometers_jz.py` define uma rede de **8** estações com coeficientes diferentes e grava **no mesmo arquivo** `data/processed/space_weather/jz_7day_magnetometer_inversion.csv` que o script de 14 estações. O conteúdo do dataset depende de qual script rodou por último. Além disso, esse script lê o Kp como lista-de-listas (`row[0][:13]`), mas `noaa_planetary_k_index_real.json` é uma lista de dicionários — a leitura quebraria fora do `try`.

### 1.3 Fluxo de raios X rotulado `observed` é gerado por fórmula

`data/raw/space_weather/goes_xray_flux.csv` tem coluna `status` preenchida com `observed`. O arquivo é escrito por `scripts/generate_space_weather_datasets.py:40-49`, que constrói uma gaussiana de subida e uma exponencial de decaimento em torno de um pico *hard-coded* de `7.0e-5` às `2026-08-25 10:02`.

**Ressalva justa ao autor:** o flare em si é real (§3.2), e `goes_xrays_7day_real.json` aparenta ser download genuíno do serviço da NOAA (formato, cadência de 1 min, campos `electron_correction`, janela de 7 dias, nenhum script gerador no repositório). O problema é de rotulagem: um arquivo idealizado e um arquivo baixado convivem com nomes quase idênticos, e o idealizado se declara `observed`.

### 1.4 A precipitação — base de todo o argumento — não existe no repositório

O "déficit de 10×" compara o volume reconstruído contra a chuva do GPM IMERG. Porém:

* `data/raw/meteorology/GPM_3IMERGHH.07` tem **0 bytes**.
* `data/raw/meteorology/gpm_imerg_granules_catalog_real.json` cataloga grânulos de **25 de agosto de 2024** — dois anos antes do evento. Todos os registros são de 2024.
* `scripts/process_gpm_hdf5_miniforge.py` não tem nada para processar.

Portanto o número "15–30 mm do GPM" (README) e o `p_meas_mm: 22.0  # GPM IMERG 10km grid` (`scripts/calculate_inverse_hydraulics.py:39`) **não são rastreáveis a nenhum dado neste repositório**.

### 1.5 Dados de raios impossíveis para os eventos antigos

`data/lightning_data_20km_jz_window_events.json` reporta, por evento, contagem de descargas, razão IC/CG com uma casa decimal, percentual de +CG, contagem de "descargas ascendentes de crista" e corrente de pico em kA. Para os eventos antigos, os "sensores" declarados são:

| Evento | Sensores declarados | Descargas | Ascendentes |
| :--- | :--- | ---: | ---: |
| Zhangzangbo, 11/07/**1981** | "CMA Historical Records, DHM Nepal" | 540 | 22 |
| Dig Tsho, 04/08/**1985** | "Expedições Glaciológicas Khumbu / DHM" | 65 | 6 |
| Luggye Tsho, 07/10/**1994** | "Dept. Geology & Mines (Butão)" | 28 | 1 |

Nenhuma dessas instituições opera rede de localização de descargas. A WWLLN começou a operar em 2004; a TRMM/LIS foi lançada em 1997 e desativada em 2015. Para Leh 2010 declara-se "IMD Radar Proxy" — radar meteorológico não detecta descargas. Ainda: a WWLLN não classifica IC vs. CG nem mede corrente de pico com confiabilidade, e nenhum sensor orbital identifica "raio ascendente de crista". **Esses números não podem ter origem observacional.**

---

## 2. O "déficit hídrico" é construído, não medido

### 2.1 Toda a cadeia de cálculo parte de parâmetros digitados à mão

Em `scripts/calculate_inverse_hydraulics.py`, os 15 eventos são descritos por um dicionário onde **todos** os insumos são escolhas do analista: `B`, `z`, `dh`, `S0`, `n`, `basin_area_km2`, `C_runoff`, `total_bulk_m3`, `Cv`, `lake_vol_m3`, `mass_kg`, `delta_H_m`, `ice_fraction`, `eta_frict`, `p_meas_mm`. Nenhum é lido de hidrograma, seção topobatimétrica, DEM ou pluviômetro.

O resultado é aritmética correta sobre premissas não verificáveis:

* $V_{\text{water}} = \texttt{total\_bulk} \times (1 - C_v)$ — o "volume de água líquida" é escolhido ao escolher `total_bulk_m3` e `Cv`.
* $P_{\text{req}} = V_{\text{water}} / (A \cdot C)$ — o déficit é comparado com `p_meas_mm`, também digitado.

**O "déficit" é, literalmente, a razão entre dois números que o autor escolheu.**

### 2.2 O caso Kedarnath se autorrefuta dentro do próprio repositório

O `LITERATURE_REGISTER_HIMALAYAN_DISASTERS.md` cita corretamente Dobhal et al. (2013) e Allen et al. (2016) registrando **>325 mm em 48 h** sobre a bacia de Chorabari. O script, no mesmo repositório, adota `p_meas_mm = 35.0` e calcula $P_{\text{req}} = 131{,}1$ mm, anunciando "déficit de 3,7×".

Mas $131{,}1\ \text{mm} < 325\ \text{mm}$. **Com o valor que o próprio repositório cita da literatura, não há déficit algum — há folga de mais de 2×.** O déficit em Kedarnath existe apenas porque 325 mm foi substituído por 35 mm sem justificativa registrada.

O padrão se repete: Himachal Pradesh, julho de 2023, recebe `p_meas_mm = 45.0` (o evento real teve acumulados de centenas de mm em 2–3 dias); Melamchi 2021 recebe `28.0` mm.

### 2.3 Erro de unidade provável: 65,7 hectares virou 65,7 km²

O relatório técnico (linha 31) informa: "Sentinel-2 mapeou o lago do Lhende Khola em **65,7 hectares**". O script de hidráulica usa, para o mesmo evento, `basin_area_km2: 65.7` (`scripts/calculate_inverse_hydraulics.py:36`).

A coincidência exata dos dígitos com uma troca de unidade (ha → km², fator 100) é forte indício de que a área da bacia foi preenchida com a área do lago. Não é detalhe: é o denominador da lâmina de chuva requerida.

### 2.4 Três documentos, quatro áreas de bacia, respostas incompatíveis

| Documento | Área adotada | Lâmina de chuva requerida |
| :--- | ---: | ---: |
| `TECHNICAL_REPORT_..._2026.md` (§5.3) | 15 / 28 / 50 / 100 km² | **507 a 947 mm** (até 1.114 mm com $C=0{,}85$) |
| `README.md` (pilar 3) | — | **">500 a 950 mm"** |
| `scripts/calculate_inverse_hydraulics.py` | 65,7 km² | **254,3 mm** |
| `conta_hidrologica_inversa_toro.md` (§4) | 55 km² | **164,6 mm** |

Os quatro descrevem o mesmo evento. O intervalo publicado vai de **164,6 mm a 1.113,9 mm** — fator de 6,8×. O número de manchete do README (">500–950 mm", apresentado como fisicamente extraordinário) é 2 a 6 vezes maior do que o que o código-mestre do próprio projeto calcula. Uma lâmina de 164,6 mm em bacia himalaia durante a monção não é anômala: é chuva forte comum.

### 2.5 Balanço de massa incompleto: a vazão do próprio rio nunca é subtraída

A seção de Manning é aplicada "na garganta entre Gyirong Port e Rasuwagadhi". Segundo o próprio `perfil_rio_trishuli.md`, essa seção drena ~2.000 km² em território tibetano, com vazão média anual de 170–220 m³/s e picos de monção acima de 1.200 m³/s.

O hidrograma de 5 horas é integrado em 20,70 M m³ **sem subtrair a vazão de base**. Com 150–250 m³/s durante 18.000 s, o rio sozinho entrega **2,7 a 4,5 M m³** — de 19% a 32% do "déficit" de 14,2 M m³. Esse termo não aparece no balanço.

Somando: lago pré-evento (5,2 M m³, ou 7,54 M m³ no pico segundo a própria linha do tempo do relatório) + vazão de base (2,7–4,5 M m³) + fusão por atrito consome a maior parte dos 14,2 M m³ antes de qualquer "toró".

### 2.6 Inconsistências aritméticas entre documentos

* **Energia potencial:** o relatório técnico diz $E_p \approx 388$ TJ; `conta_hidrologica_inversa_toro.md` calcula $3{,}178\times10^{14}$ J $= 317{,}8$ TJ para a mesma massa e a mesma queda. Diferença de 22%.
* **Fração de gelo fundida:** o relatório afirma "no máximo ≤3,5% da massa de gelo funde (<0,45 M m³)". Mas 0,45 M m³ = $4{,}5\times10^8$ kg, que é **1,67%** de $2{,}7\times10^{10}$ kg, não 3,5%. Os dois números não descrevem o mesmo cálculo.
* **Massa do colapso:** `conta_hidrologica_inversa_toro.md` usa $2{,}7\times10^{10}$ kg com queda de 1.200 m; `calculate_inverse_hydraulics.py:38` usa `mass_kg: 4.0e10` com `delta_H_m: 3200`. Mesmo evento, insumos termodinâmicos divergentes por fatores de 1,5× e 2,7×.

### 2.7 A "análise de sensibilidade" testa os parâmetros que não importam

O `DATA_PROVENANCE_...md` (§5) varia $n$, $C_{\text{runoff}}$ e $\eta_{\text{fusão}}$ e conclui que "as anomalias de 10×–20× permanecem fisicamente comprovadas fora de qualquer margem de erro".

Mas os parâmetros que **determinam** o resultado — `total_bulk_m3`, `p_meas_mm` e `basin_area_km2` — são mantidos fixos e nunca testados. Variar $C_{\text{runoff}}$ é irrelevante (o próprio quadro admite: "Invariante"); variar `p_meas_mm` de 22 para 200 mm eliminaria o déficit inteiro.

Além disso, **os números da tabela de sensibilidade não são reproduzíveis com o código do repositório.** A tabela alega $Q_{\text{peak}}$ entre 4.100 e 6.800 m³/s ao variar $n$ de 0,040 a 0,075. Recalculando com a geometria do próprio script:

* Kedarnath ($A=202{,}5$; $R_h=5{,}04$; $S_0=0{,}055$): **1.857 a 3.481 m³/s**
* Chamoli ($A=506{,}4$; $R_h=8{,}04$; $S_0=0{,}065$): **6.897 a 12.932 m³/s**

O intervalo publicado não corresponde a nenhum dos dois eventos citados.

### 2.8 Erro de categoria: avalanche de gelo tratada como hidrograma de cheia

Para Aru (Tibete, 2016) — colapso de geleira sobre um platô, não uma cheia — o script atribui `total_bulk_m3 = 68e6` e `Cv = 0.20`, contabilizando **54,4 M m³ como "água líquida"** e exigindo **818 mm de chuva** ("déficit de 163,6×"). Mas a massa de uma avalanche de gelo *é gelo*: não é água líquida nem precipitação. O mesmo problema afeta Chamoli (`Cv = 0.42` → 10,73 M m³ de "água" em pleno inverno seco).

Nesses dois casos o "déficit" não mede fenômeno algum: mede a decisão de chamar de água o que é gelo e rocha.

---

## 3. Confronto com registros externos independentes

### 3.1 O sismo: magnitude e tipo estão errados no relatório

O relatório afirma, com o selo `[DIRECT - USGS SEISMIC]`, um **"Magnitude 4.4 mb"** às 02:52 UTC.

Consulta direta ao catálogo FDSN do USGS (`earthquake.usgs.gov/fdsnws/event/1/query`, janela 24–29/08/2026, 27–29,5°N / 84–87°E) retorna dois eventos:

| ID | Tempo (UTC) | Lat / Lon | Prof. | Mag | Tipo de mag. | Tipo de evento |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `us7000tbwb` | **2026-08-26T02:52:10Z** | 28,271 / 85,515 | 0 km | **5,2** | `ms_vx` | **landslide** |
| `us7000tc90` | 2026-08-26T06:00:35Z | 28,270 / 85,515 | 0 km | 4,2 | `ms_vx` | landslide |

O horário de origem confere ao segundo — o repositório de fato usou o evento correto. Mas:

1. A magnitude catalogada é **Ms 5,2**, não "4,4 **mb**". O valor 4,4 foi estimativa preliminar, posteriormente recatalogada. O repositório congelou o número preliminar e ainda lhe atribuiu o tipo errado (`mb` em vez de `ms_vx`).
2. O USGS classifica o evento como **`landslide`**, não como terremoto — o que *apoia* a leitura do autor de que se trata de colapso de massa, e deveria ser citado.
3. O segundo deslizamento (Ms 4,2 às 06:00:35 UTC) **não aparece na linha do tempo do relatório**.
4. O "Estágio 1 precursor às 01:45 UTC" não tem registro sísmico. O tremor precursor efetivamente reportado ocorreu às 08:20 NPT = **02:35 UTC**, 50 minutos depois do horário postulado.

### 3.2 O flare solar: real, mas com classe e região ativa erradas

O evento solar existe e é verificável: **M6.9, região ativa AR 4513, pico às 10:02 UTC de 25/08/2026**, com blackout de rádio R2 e CME associado (alerta G2 da NOAA para 28/08).

O repositório registra **"M7.0 (AR 3792)"**. A classe é diferença de arredondamento defensável (o fluxo do arquivo de 7 dias, $6{,}977\times10^{-5}$, arredonda para M7,0), mas **o número da região ativa está errado** — AR 3792 é numeração de 2023. Um detalhe assim, publicado sem fonte, indica que o campo não foi verificado.

### 3.3 A "correlação solar" é indistinguível do acaso — e o próprio arquivo do repositório mostra isso

O argumento é que houve flare/Kp elevado nas 12–72 h anteriores a cada um dos 15 desastres. Analisei o `goes_xrays_7day_real.json` do próprio repositório (21–28/08/2026, 169 horas):

| Métrica | Resultado |
| :--- | :--- |
| Horas em nível ≥ C1 | **102 de 169 (60%)** |
| Horas em nível ≥ M1 | 11 de 169 (7%) |
| Dias com ao menos um flare classe M | **4 de 8** (21/08 M1,7; 24/08 M1,8; 25/08 M7,0; 26/08 M2,2) |

Em máximo solar, "houve um flare classe M nas 72 h anteriores" tem taxa-base próxima de 100%, e "houve classe C" é praticamente contínuo. Encontrar um flare antes de cada um dos 15 eventos é, portanto, **esperado sob a hipótese nula**. O repositório não apresenta:

* nenhum grupo-controle (datas sem desastre na mesma região);
* nenhum teste estatístico, valor-p ou razão de verossimilhança;
* nenhuma análise de superposição de épocas.

Sem isso, a associação declarada não tem força evidencial. Agravante: o conjunto acomoda tanto **0 descargas** (Chamoli, "céu 100% limpo") quanto **3.850 descargas** (Himachal 2023) como confirmações do mesmo mecanismo — o que torna a hipótese, na forma em que está posta, não falsificável.

**Objeção física adicional, independente da estatística.** O mecanismo invocado (Tinsley; modulação de $J_z$ e microfísica de nuvens por partículas energéticas) depende de variação da ionização da coluna atmosférica. A região de Gyirong/Langtang está entre as de **maior rigidez de corte geomagnético do planeta (~13–14 GV)** — é justamente ali que prótons solares e decréscimos de Forbush produzem a *menor* variação de ionização. O efeito proposto é máximo em altas latitudes geomagnéticas e mínimo exatamente onde o trabalho o invoca. Isso precisa ser enfrentado explicitamente.

### 3.4 A magnitude do colapso pode estar subestimada em mais de uma ordem

O repositório assume $15\times10^6$ m³ de rocha-gelo, sem fonte declarada. As descrições públicas do evento indicam destacamento de ~0,2 km² a ~5,2 km de altitude com queda de ~1,2 km, e estimativas de material mobilizado da ordem de $2\times10^8$ m³.

Se a massa real for uma ordem de grandeza maior, **todo o balanço energético e de fusão por atrito muda de escala** — e o termo que o relatório descarta como "<3%" passa a ser candidato dominante. Este ponto sozinho basta para exigir a reabertura do balanço de massa antes de qualquer alegação de déficit.

### 3.5 A velocidade reconstruída diverge dos relatos por fator ~4

Manning devolve $v = 11{,}6$ m/s (41,7 km/h). Relatos públicos descrevem a frente percorrendo ~20 km em ~7 minutos (~180 km/h, ~50 m/s). Ainda que velocidade de frente e velocidade média em seção não sejam a mesma grandeza, uma divergência de 4× indica que a parametrização ($n = 0{,}060$, $S_0 = 0{,}045$) não está calibrada contra observação alguma. Acrescente-se que Manning — formulação para escoamento turbulento uniforme em regime permanente — é de aplicabilidade duvidosa a fluxo hiperconcentrado supercrítico (o próprio resultado dá $Fr \approx 1{,}35$).

### 3.6 Omissão editorial grave: as vítimas

O evento causou, segundo balanços públicos, da ordem de **1.000 a 1.400 mortos e 4.000 a 5.500 desaparecidos**, além de danos de centenas de bilhões de rupias e 13 usinas hidrelétricas atingidas.

Nem o `TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md` nem o `README.md` mencionam uma única vítima. Há seções dedicadas a cheiros, gases, sons e ao dragão *Druk*, e nenhuma linha sobre os mortos. Além do problema ético, isso enfraquece o documento perante qualquer instituição do Nepal ou da China a quem ele é endereçado como convite de colaboração.

Menor, na mesma linha: o relatório diz "25 pontes destruídas"; o README fala em "33 pontes"; os levantamentos públicos indicam 33 pontes rodoviárias e 68 pontes suspensas afetadas.

---

## 4. Erros de citação

### 4.1 A referência sobre Chamoli está errada em DOI, título, paginação — e na conclusão

O relatório (ref. 6) cita:

> Shugar, D. H. et al. (2021). *A huge rock and ice avalanche caused the 2021 Chamoli disaster, Uttarakhand, India*. **Science**, 373(6552), 300–306. DOI: 10.1126/science.abg6027

O artigo real é *"A massive rock and ice avalanche caused the 2021 disaster at Chamoli, Indian Himalaya"*, **Science** 373, eabh4455, **DOI: 10.1126/science.abh4455**. Título, paginação e DOI estão todos incorretos.

Mais sério: o script atribui a Shugar o limite de 1% de eficiência de fusão (`"eta_frict": 0.010,  # Shugar et al. Science 2021: 1%`, `scripts/calculate_inverse_hydraulics.py:33`) e conclui déficit hídrico infinito em Chamoli. **A conclusão publicada é o oposto:** os autores documentam ~27×10⁶ m³ de rocha e gelo e concluem que o aquecimento por atrito derreteu praticamente todo o gelo contido na avalanche, e que foi isso que a transformou em fluxo de detritos de alta mobilidade. O trabalho revisado por pares que o repositório cita como âncora do "problema do 1%" na verdade **resolve** o balanço hídrico de Chamoli sem qualquer déficit.

Enquanto essa citação não for corrigida, o "Evento 2" do registro de literatura não pode ser usado como evidência de anomalia.

---

## 5. Reprodutibilidade

O README anuncia "Reprodutibilidade 100%" e um protocolo de auditoria independente em um comando. Executei-o.

### 5.1 O comando-mestre falha

```
$ python scripts/run_full_independent_audit.py
  [HASH MISMATCH] data/hot_flood_npl_aoi.geojson
  [HASH MISMATCH] data/hot_flood_npl_bridges_damage_icimod.geojson
  [HASH MISMATCH] data/hot_flood_npl_tm_projects.geojson
  [HASH MISMATCH] data/osm_waterways_raw.json
  [HASH MISMATCH] data/talvegue_completo_kml.txt
  [HASH MISMATCH] data/metadata/sources_metadata.json
  FAILURES: 6, MISSING: 0
  RESULTADO FINAL: AUDITORIA APONTOU INCONSISTENCIAS.    (exit 1)
```

**Causa diagnosticada:** os hashes foram calculados sobre arquivos com terminação LF, mas o repositório não tem `.gitattributes` e o Git no Windows entrega CRLF. Confirmei recalculando: com CRLF o hash é `2d2cef8d…`; normalizando para LF obtém-se exatamente o `12fcfce0…` esperado.

Ou seja, o conteúdo está íntegro — mas **o certificado criptográfico que o projeto oferece como principal garantia de auditabilidade falha em qualquer clone feito no Windows**, que é justamente a plataforma do autor. Correção: adicionar `.gitattributes` com `* -text` (ou `binary` para os arquivos de dados), ou recalcular os hashes após normalização.

### 5.2 Todos os scripts de processamento têm o caminho absoluto do autor embutido

```
scripts/generate_space_weather_datasets.py:10:    base_dir = "C:/Users/haas/github/Himalaia_2026"
scripts/inverse_hydrology_balance.py:107
scripts/process_7day_magnetometers_jz.py:10
scripts/process_gpm_hdf5_miniforge.py:8
scripts/recalculate_jz_with_china_network.py:9
```

Nenhum deles roda em outra máquina. Isso contradiz diretamente o "Passo 1 — clonar o repositório" do guia do auditor. (Os dois scripts de auditoria propriamente ditos usam `os.path.dirname(__file__)` e estão corretos.)

### 5.3 Mensagem de aprovação pré-escrita

Em `scripts/run_full_independent_audit.py:39`, a etapa de checksums retorna a string fixa `"111 / 111 arquivos verificados com integridade bit a bit (SHA-256)"` sempre que o subprocesso sai com código 0, sem ler a contagem real. O texto de sucesso é constante, não medido.

### 5.4 `requirements.txt` incompleto

`h5py` é importado por `process_gpm_hdf5_miniforge.py` mas não está declarado.

---

## 6. O que se sustenta

Para ser justo com o trabalho, estes pontos passaram na auditoria:

1. **A cadeia física do evento de 26/08/2026 está correta** e é confirmada por fonte independente: destacamento de rocha-gelo em altitude → queda de ~1,2 km → barramento do Lhende Khola → galgamento e fluxo de detritos hiperconcentrado descendo pelo Bhote Koshi/Trishuli. O horário-chave (02:52:10 UTC) confere ao segundo com o catálogo do USGS.
2. **A aritmética de Manning está correta.** Reproduzi $A = 291{,}1$ m², $R_h = 5{,}94$ m, $Q = 3.376$ m³/s a partir dos parâmetros declarados. O erro não está na conta; está nos insumos.
3. **A elevação de nível de ~8,5 m** é compatível com os ~9 m em 30 minutos reportados no Trishuli.
4. **A classificação do USGS como `landslide`** apoia a leitura do autor de que o sinal sísmico é de colapso de massa, e não de terremoto tectônico — vale citar isso explicitamente.
5. **O trabalho de sistematização** (15 eventos georreferenciados, acervo de imagens antes/depois com datas ISO, KML/KMZ, visualizadores 3D/4D) tem valor real e independente das hipóteses.
6. **A postura declarada é honesta:** o §1 do relatório assume explicitamente que as hipóteses são heterodoxas. O problema não é propor hipótese heterodoxa — é apresentar parâmetros escolhidos como se fossem telemetria.

---

## 7. Recomendações, em ordem de prioridade

**Bloqueadores — enquanto não forem resolvidos, as conclusões não devem ser divulgadas como resultado:**

1. **Rotular como sintético tudo o que é sintético.** Renomear `goes_xray_flux.csv` → `goes_xray_flux_IDEALIZED_MODEL.csv`, trocar `status: observed` por `status: modeled`, e renomear `jz_7day_magnetometer_inversion.csv` → `jz_7day_GEC_PARAMETRIC_MODEL.csv`. Remover as expressões "inversão", "rede de 14 magnetômetros" e "cadência de 1 s" de todos os documentos — ou baixar de fato os dados do INTERMAGNET.
2. **Retirar ou refazer o pilar $J_z$.** Na forma atual, $J_z = V_I/R_c$ com $R_c$ constante não contém informação independente. Se a hipótese for mantida, precisa de dados magnéticos reais, grupo-controle e teste estatístico.
3. **Corrigir a citação de Shugar et al. (2021)** — DOI `10.1126/science.abh4455` — e reconhecer que o artigo conclui que a fusão por atrito derreteu quase todo o gelo. Reavaliar o caso Chamoli à luz disso.
4. **Corrigir o sismo para Ms 5,2 (`us7000tbwb`, tipo `landslide`)** e incluir o segundo deslizamento (Ms 4,2, `us7000tc90`, 06:00:35 UTC).
5. **Obter precipitação real.** Baixar os grânulos IMERG de **2026**-08-25/26 (o catálogo atual é de 2024) e substituir todos os `p_meas_mm` digitados por valores extraídos com procedimento documentado.
6. **Refazer o balanço de massa** incluindo (a) a vazão de base do Trishuli/Kyirong Tsangpo na seção de controle, (b) o volume de lago no pico (7,54 M m³, não 5,2), e (c) massa de colapso compatível com as estimativas publicadas.
7. **Remover ou reconstruir os dados de raios anteriores a 2004**, que não podem ter origem instrumental.

**Correções de rigor:**

8. Reconciliar as quatro áreas de bacia (15 / 28 / 55 / 65,7 km²) e investigar a provável troca ha → km².
9. Reconciliar $E_p$ (388 vs. 317,8 TJ), a fração de fusão (3,5% vs. 1,67%) e a massa/queda (2,7e10 kg / 1.200 m vs. 4,0e10 kg / 3.200 m).
10. Refazer a análise de sensibilidade variando `total_bulk_m3`, `p_meas_mm` e `basin_area_km2`, e corrigir a tabela do §5 (os intervalos publicados não correspondem a nenhum dos dois eventos citados).
11. Tratar avalanches de gelo (Aru, Chamoli) fora do arcabouço "chuva requerida" — atribuir massa de gelo a precipitação é erro de categoria.

**Reprodutibilidade:**

12. Adicionar `.gitattributes` (`* -text`) ou recalcular os checksums; hoje a auditoria falha em qualquer clone Windows.
13. Substituir os caminhos `C:/Users/haas/...` por caminhos relativos a `__file__`.
14. Unificar os dois geradores de `jz_7day_magnetometer_inversion.csv`, que se sobrescrevem.
15. Declarar `h5py` no `requirements.txt`.
16. Remover a mensagem fixa "111/111 verificados" e imprimir a contagem real.

**Editorial:**

17. Incluir o balanço humano do desastre (mortos, desaparecidos, deslocados) na abertura dos relatórios.
18. Separar fisicamente o material de geomitologia do corpo técnico. Ele é legítimo como estudo cultural, mas colocado ao lado da física em documento endereçado a CAS, CMA, ICIMOD e DHM, deprecia a recepção do que há de sólido no trabalho.

---

## 8. Nota metodológica sobre esta auditoria

**Verificações locais:** leitura integral do código em `scripts/`; recálculo independente das equações de Manning, do balanço de massa e das conversões $V_I \to J_z$ para os 15 eventos; execução de `verify_audit_integrity.py` e `run_full_independent_audit.py`; diagnóstico da causa dos 6 mismatches por recomputação de hash com e sem normalização de fim de linha; contagem de taxa-base de flares a partir do próprio `goes_xrays_7day_real.json`; inspeção de todos os arquivos em `data/raw/`.

**Verificações externas:** consulta direta ao serviço FDSN do USGS para a janela e a região do evento; verificação da classe e da região ativa do flare de 25/08/2026 junto a fontes de clima espacial; verificação do título, DOI e conclusão de Shugar et al. (2021); confronto da cronologia, do mecanismo e dos números de danos com relatos públicos do evento.

**Limitações declaradas:** não foi possível acessar o texto integral de Shugar et al. atrás do *paywall* da *Science* (HTTP 403) — a conclusão citada vem do resumo público e da cobertura primária do artigo. Estimativas de volume do colapso e de velocidade da frente provêm de compilações públicas e devem ser tratadas como preliminares, não como valores de referência.
