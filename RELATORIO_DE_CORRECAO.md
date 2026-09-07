# Relatório de Correção e Auditoria Científica Independente

**Repositório:** `reinaldohaas/Himalaia_2026`  
**Investigador Principal:** Prof. Reinaldo Haas (Departamento de Física, Universidade Federal de Santa Catarina)  
**Data de Conclusão da Correção:** Setembro de 2026  
**Finalidade:** Documentar item por item a eliminação da falsa proveniência, a segregação de modelos sintéticos, a correção de dados observacionais e apresentar as conclusões que não sobreviveram ao escrutínio empírico.

---

## 1. Resumo Executivo da Correção

Uma auditoria científica independente identificou vícios graves no repositório: modelos sintéticos analíticos haviam sido gravados com nomes de arquivos de telemetria observacional, valores de precipitação foram arbitrados sem citar a literatura contraditória, e deduções aritméticas decorrentes de parâmetros digitados manualmente foram anunciadas como descobertas científicas de anomalias universais.

Todas as irregularidades foram corrigidas sem reescrever o histórico do Git:
* **Falsa proveniência eliminada:** Todos os arquivos de dados sintéticos foram transferidos para `data/synthetic/` e documentados.
* **Premissas declaradas abertamente:** 100% das variáveis e constantes foram centralizadas em [`config/hydraulic_assumptions.yaml`](./config/hydraulic_assumptions.yaml) com indicação explícita de fonte primária (URL/DOI) ou `ASSUMED_BY_ANALYST`.
* **Dados observacionais reais restaurados:** A precipitação in-situ de 325 mm de Kedarnath (Dobhal et al., 2013) foi reinserida, o sismo principal do USGS foi corrigido para Ms 5.2 `landslide` (`us7000tbwb`), o flare solar para M6.9 na AR 4513, e o balanço humano oficial (1.000–1.400 mortos, 4.000–5.500 desaparecidos, 33 pontes rodoviárias e 68 suspensas destruídas) foi incorporado.
* **Integridade criptográfica restabelecida:** O manifesto [`data/CHECKSUMS_SHA256.txt`](./data/CHECKSUMS_SHA256.txt) foi recomputado para 114 arquivos autênticos e o pipeline mestre [`scripts/run_full_independent_audit.py`](./scripts/run_full_independent_audit.py) foi executado com 100% de aprovação.

---

## 2. Matriz de Correção de Defeitos (Auditoria P0 a P3)

### Grupo P0 — Falsa Proveniência (Dados Sintéticos Rotulados como Medição)

| ID | Descrição do Defeito Original | Status | Arquivos Afetados | Ação Técnica Realizada |
|---|---|---|---|---|
| **P0-1** | Script `recalculate_jz_with_china_network.py` afirmava inverter 14 magnetômetros com 1s de cadência, mas aplicava fórmula analítica senoidal com condicional forçada (`if date == 2026-08-25 10: delta_V = 118.4`). Arquivos de saída tinham nomes de telemetria. | **CORRIGIDO** | `scripts/model_gec_jz_parametric.py`, `scripts/process_7day_magnetometers_jz.py`, `data/synthetic/` | 1. Script renomeado via `git mv` para `scripts/model_gec_jz_parametric.py`.<br>2. Condicional forçada eliminada.<br>3. Caminhos absolutos substituídos por relativos.<br>4. Saídas redirecionadas para `data/synthetic/jz_gec_PARAMETRIC_MODEL.csv` e `data/synthetic/jz_8station_PARAMETRIC_MODEL.csv`.<br>5. Docstring declara explicitamente tratar-se de modelo analítico Carnegie GEC sem dados magnéticos. |
| **P0-2** | Tabela em `data/himalayan_events_1980_2026.json` apresentava campo `solar_jz_peak` com valores de 2,85 a 4,87 pA/m² como observação instrumental, quando eram resultado de divisão de $V_I$ arbitrado por $R_c$ fixo. | **CORRIGIDO** | `data/himalayan_events_1980_2026.json`, `data/solar_space_weather/solar_forcing_all_events.json` | 1. Campo renomeado para `jz_derived_from_vi_constant_Rc`.<br>2. Adicionado campo `jz_derivation_note` declarando que o valor é derivado de fórmula analítica com $R_c = 0,78\times 10^{17}\,\Omega\cdot\text{m}^2$ sem medição in-situ.<br>3. Relatórios atualizados para classificar o forçamento de $J_z$ como hipótese paramétrica. |
| **P0-3** | Arquivos `goes_xray_flux.csv`, `dscovr_solar_wind_l1.csv` e `geomagnetic_indices_and_gcr.csv` na pasta `data/raw/space_weather/` com flag `observed` eram gerados por fórmula em `generate_space_weather_datasets.py`. | **CORRIGIDO** | `scripts/generate_space_weather_datasets.py`, `data/raw/space_weather/`, `data/synthetic/` | 1. Script reescrito para salvar em `data/synthetic/` (`goes_xray_IDEALIZED_MODEL.csv`, `dscovr_solar_wind_IDEALIZED_MODEL.csv`, `geomagnetic_indices_IDEALIZED_MODEL.csv`).<br>2. Status alterado de `observed` para `modeled`.<br>3. Arquivos sintéticos removidos de `data/raw/space_weather/` via `git rm`. |
| **P0-4** | Arquivos de descargas elétricas (`lightning_data_10km_...json`, `lightning_points_20km_...json`) continham contagens, frações IC/CG e correntes em kA para eventos de 1981, 1985 e 1994, quando essas redes não existiam. | **CORRIGIDO** | `data/himalayan_events_1980_2026.json`, `data/lightning_data_10km_himalayan_events.json`, `data/lightning_data_20km_jz_window_events.json`, `data/synthetic/` | 1. Métricas pré-2004 limpas e marcadas como `[DADO INDISPONÍVEL — Redes de raios não existiam]`.<br>2. Frações não mensuráveis (IC/CG, upward) marcadas como `[NÃO VERIFICADO — Exige acordo institucional WWLLN/GLD360]`.<br>3. `lightning_points_20km_all_events.json` movido para `data/synthetic/lightning_points_PARAMETRIC_SYNTHETIC.json`. |
| **P0-5** | Arquivo `data/raw/meteorology/GPM_3IMERGHH.07` tinha 0 bytes e simulava grânulo HDF5. Catálogo de grânulos de 2024 era apresentado como dados reais de 2026. | **CORRIGIDO** | `data/raw/meteorology/GPM_3IMERGHH.07`, `data/raw/meteorology/gpm_imerg_granules_catalog_real.json` | 1. Arquivo de 0 bytes removido do repositório via `git rm`.<br>2. Catálogo renomeado via `git mv` para `gpm_imerg_granules_catalog_2024_proxy.json`.<br>3. Declarado em `LIMITACOES_E_DADOS_INDISPONIVEIS.md` que dados de 2026 exigem credenciais Earthdata do usuário. |

---

### Grupo P1 — Cálculos Hidráulicos e Premissas Físicas

| ID | Descrição do Defeito Original | Status | Arquivos Afetados | Ação Técnica Realizada |
|---|---|---|---|---|
| **P1-1** | Parâmetros de canal ($B, z, S_0, n, \Delta h$) e de bacia estavam hardcoded no script Python sem indicação de incerteza ou fonte primária. | **CORRIGIDO** | `config/hydraulic_assumptions.yaml`, `scripts/calculate_inverse_hydraulics.py` | 1. Criado `config/hydraulic_assumptions.yaml` com todos os parâmetros dos 15 eventos.<br>2. Cada parâmetro possui campo `source: URL/DOI` ou `source: ASSUMED_BY_ANALYST`.<br>3. `scripts/calculate_inverse_hydraulics.py` atualizado para ler o YAML dinamicamente. |
| **P1-2** | Em Kedarnath 2013, o código utilizava `p_meas_mm: 35.0` gerando um déficit de 3.7x, ignorando que a literatura (Dobhal et al. 2013, Allen et al. 2016) registrou 325 mm no acampamento de Chorabari. | **CORRIGIDO** | `config/hydraulic_assumptions.yaml`, `scripts/calculate_inverse_hydraulics.py`, `data/catchment_hydraulics/inverse_hydraulics_all_events.json` | 1. Atualizado $P_{\text{meas}}$ para 325.0 mm com citação formal.<br>2. Recálculo mostra $P_{\text{req}} = 110.4\text{ mm}$, demonstrando que **o déficit hídrico desaparece** (folga de 2.94x a favor da chuva observada).<br>3. Status registrado como `SEM DÉFICIT`. |
| **P1-3** | Em Chamoli 2021, o código calculava déficit pluviométrico infinito contra zero chuva, ignorando que se tratava de uma avalanche de rocha e gelo em pleno inverno (Shugar et al. 2021). | **CORRIGIDO** | `config/hydraulic_assumptions.yaml`, `scripts/calculate_inverse_hydraulics.py` | 1. Evento categorizado formalmente como `Rock and ice avalanche with frictional melt transformation`.<br>2. Deficit multiplier registrado como `NOT_APPLICABLE` (erro de categoria física aplicar déficit de chuva a avalanche de rocha/gelo). |
| **P1-4** | Em Aru 2016, avaliava-se déficit de chuva sobre um colapso de geleira fria (~95% gelo sólido). | **CORRIGIDO** | `config/hydraulic_assumptions.yaml`, `scripts/calculate_inverse_hydraulics.py` | 1. Evento categorizado como colapso de geleira fria.<br>2. Deficit multiplier registrado como `NOT_APPLICABLE`. |
| **P1-5** | Em 2026, usava-se `p_meas_mm: 22.0` sem base documental, gerando déficit de 11.6x. | **CORRIGIDO** | `config/hydraulic_assumptions.yaml`, `scripts/calculate_inverse_hydraulics.py` | 1. $P_{\text{meas}}$ registrado como `null` com status `[DADO INDISPONÍVEL]`.<br>2. Multiplicador de déficit definido como `null` para evitar afirmações falsas de prova. |
| **P1-6** | Contradição na área da bacia de 2026: texto citava 65.7 hectares (0.657 km²), mas cálculo usava 65.7 km². | **CORRIGIDO** | `config/hydraulic_assumptions.yaml`, `TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md` | 1. Discrepância de unidades explicitada.<br>2. Adotada área de sub-bacia regional de 55–65 km² para o hidrograma e detalhada sensibilidade para áreas menores. |
| **P1-7** | Protocolo de auditoria afirmava que o déficit foi demonstrado matematicamente fora de erro, sem análise de sensibilidade executável. | **CORRIGIDO** | `scripts/sensitivity_analysis_hydraulics.py`, `DATA_PROVENANCE_AND_INDEPENDENT_AUDIT_PROTOCOL.md`, `data/processed/sensitivity_analysis_hydraulics.csv` | 1. Criado script `scripts/sensitivity_analysis_hydraulics.py` executando 560 simulações variando $V_{\text{bulk}}$ (±30%), $A_{\text{basin}}$ (15 a 100 km²) e chuva.<br>2. Seção 5 do protocolo atualizada demonstrando sob quais condições o déficit existe e sob quais desaparece. |
| **P1-8** | No evento 2026, a vazão de base do rio Trishuli não era subtraída do volume de água líquida antes de calcular a chuva requerida. | **CORRIGIDO** | `config/hydraulic_assumptions.yaml`, `scripts/calculate_inverse_hydraulics.py` | 1. Adicionado termo de vazão de base (180 m³/s durante 4h $\approx 2.59\text{ M m}^3$) e volume do lago ($7.54\text{ M m}^3$).<br>2. Água residual líquida exigida de chuva reduziu de 14.2M m³ para **4.07M m³**. |

---

### Grupo P2 — Afirmações Factuais e Citações Incorretas

| ID | Descrição do Defeito Original | Status | Arquivos Afetados | Ação Técnica Realizada |
|---|---|---|---|---|
| **P2-1** | Sismo de 2026 citado como "4.4 mb profundo" em contradição com o catálogo USGS FDSN. | **CORRIGIDO** | `data/processed/timeline_master.csv`, `data/raw/seismology/seismic_catalog_fdsn.csv`, relatórios técnicos | 1. Atualizado para o registro oficial USGS NEIC: evento `us7000tbwb`, 2026-08-26 02:52:10 UTC, **Ms 5.2**, magType `ms_vx`, profundidade 0 km, classificado como `landslide`.<br>2. Incluído segundo evento sísmico `us7000tc90` (Ms 4.2 landslide às 06:00:35 UTC). |
| **P2-2** | Flare solar de 2026 atribuído à região ativa AR 3792 (ativa em 2023) e classe M7.0. | **CORRIGIDO** | `timeline_master.csv`, `ESTUDO_CORRELACAO_SOLAR_RAIOS_X_JZ_HIMALAIA.md`, relatórios técnicos | 1. Região ativa corrigida para **AR 4513**.<br>2. Classificação oficial NOAA corrigida para **M6.9** (fluxo de pico $6.98\times 10^{-5}\text{ W/m}^2$ às 10:02 UTC de 25/08/2026). |
| **P2-3** | Citação falsa de Shugar et al. (Science, 2021) afirmando que o artigo "demonstrou empiricamente que $\eta \le 1\%$ para alegar déficit de água". | **CORRIGIDO** | `DATA_PROVENANCE_AND_INDEPENDENT_AUDIT_PROTOCOL.md`, `TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md`, `TECHNICAL_REPORT_HIMALAYAN_CATASTROPHES_1980_2026.md`, `LITERATURE_REGISTER_HIMALAYAN_DISASTERS.md` | 1. Falsa citação de teto de 1% removida.<br>2. Explicado que Shugar et al. demonstraram que o evento foi uma avalanche de rocha/gelo com fusão por atrito e transformação em lama hiperconcentrada sem chuva.<br>3. DOI corrigido para `10.1126/science.abh4455`. |
| **P2-4** | Alegação de que a correlação solar prova causalidade, ignorando rigidez de corte e grupo de controle. | **CORRIGIDO** | `ESTUDO_CORRELACAO_SOLAR_RAIOS_X_JZ_HIMALAIA.md`, `TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md`, `TECHNICAL_REPORT_HIMALAYAN_CATASTROPHES_1980_2026.md` | 1. Adicionada discussão explícita sobre a rigidez de corte geomagnética (~13–14 GV) do Himalaia, que deflete prótons solares abaixo de 13 GeV.<br>2. Documentado o viés de seleção da amostra de 15 eventos sem grupo de controle negativo.<br>3. Eletrodinâmica solar reclassificada como hipótese exploratória não comprovada. |
| **P2-5** | Volume da massa de colapso de 2026 fixado em 15M m³ sem indicar a incerteza da literatura (estimativas de até 200M m³). | **CORRIGIDO** | `config/hydraulic_assumptions.yaml`, relatórios técnicos | 1. Incerteza entre 15M m³ (desprendimento de crista) e 200M m³ (massa instabilizada) documentada.<br>2. Faixas de sensibilidade incluídas nos cálculos. |
| **P2-6** | Velocidade de Manning calculada em ~11.6 m/s, enquanto relatos de campo mencionavam ~50 m/s. | **CORRIGIDO** | `config/hydraulic_assumptions.yaml`, relatórios técnicos | 1. Esclarecido que 11.6 m/s representa a velocidade média de escoamento no cânion rochoso (regime supercrítico, Froude Fr ~ 1.35).<br>2. Esclarecido que relatos de 50 m/s referem-se à velocidade de queda livre na face de desprendimento da montanha e frentes de choque de ar/infrassom. |
| **P2-7** | Relatórios iniciais omitiam o balanço de perdas humanas e pontes destruídas na abertura. | **CORRIGIDO** | `TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md`, `data/processed/timeline_master.csv` | 1. Incorporado no topo dos relatórios: 1.000 a 1.400 mortos confirmados, 4.000 a 5.500 desaparecidos.<br>2. Destruição de 33 pontes rodoviárias e 68 pontes suspensas e dano a 13 hidrelétricas documentados. |

---

### Grupo P3 — Código, Reprodutibilidade e Integridade

| ID | Descrição do Defeito Original | Status | Arquivos Afetados | Ação Técnica Realizada |
|---|---|---|---|---|
| **P3-1** | Divergência de quebras de linha (CRLF vs LF) corrompia hashes SHA-256 entre Windows e Linux. | **CORRIGIDO** | `.gitattributes` | Criado `.gitattributes` com `* text=auto eol=lf` e tratamento de binários. |
| **P3-2** | Caminhos absolutos hardcoded `C:/Users/haas/...` em múltiplos scripts impediam execução em outros ambientes. | **CORRIGIDO** | `scripts/*.py` | Todos os scripts atualizados para usar caminhos relativos dinâmicos (`os.path.dirname(...)`). |
| **P3-3** | Em `process_7day_magnetometers_jz.py`, o parser de datas de Kp falhava porque a API NOAA mudou o formato para lista de dicionários. | **CORRIGIDO** | `scripts/process_7day_magnetometers_jz.py` | Parser atualizado para suportar dicionário e lista de registros com campos `time_tag` ou `datetime`. |
| **P3-4** | Scripts gravavam saídas concorrentes com o mesmo nome em locais diferentes. | **CORRIGIDO** | `scripts/model_gec_jz_parametric.py`, `scripts/process_7day_magnetometers_jz.py` | Saídas padronizadas e segregadas em `data/synthetic/` sem colisões. |
| **P3-5** | Bibliotecas críticas (`h5py`, `pyyaml`) não estavam listadas em `requirements.txt`. | **CORRIGIDO** | `requirements.txt` | Adicionados `h5py>=3.8.0` e `pyyaml>=6.0.0`. |

---

## 3. Conclusões que Não Sobreviveram

As seguintes conclusões e afirmações foram declaradas em versões anteriores do repositório, mas **perderam integralmente sustentação empírica ou factual** após a auditoria científica:

### 1. A alegação de um "Déficit Hídrico Universal de 10x a 20x" nos 15 desastres
* **O que se afirmava:** Que todos os 15 desastres himalaios desafiavam as leis da hidrologia e meteorologia com um déficit de água de 10x a 20x "fora de qualquer margem de erro".
* **O que a auditoria provou:** Essa afirmação era fruto de arbitragem manual de dados e erro físico de categoria:
  * Em **Kedarnath (2013)**, o suposto déficit decorria de colocar 35 mm no código; quando se utiliza a medição real de **325 mm** em 48h registrada por Dobhal et al. (2013), **o déficit desaparece completamente** (folga de 2.94x).
  * Em **Chamoli (2021)** e **Aru (2016)**, os eventos foram avalanches de rocha e colapsos de geleiras frias; aplicar equações de déficit pluviométrico a avalanches secas sem chuva é um erro conceitual básico.
  * No evento de **2026**, descontados o represamento do lago ($7.54\text{ M m}^3$) e a vazão de base ($2.59\text{ M m}^3$), a lâmina necessária de chuva cai para **73–87 mm**, perfeitamente plausível para um aguaceiro monçônico. Sem medições reais no repositório, o déficit é **não comprovado**.

### 2. A afirmação de "Inversão de Jz via Rede de 14 Magnetômetros Trans-Himalaios"
* **O que se afirmava:** Que a corrente vertical de tempo bom $J_z$ havia sido calculada por inversão matemática direta a partir de uma rede trans-himalaia de 14 magnetômetros com cadência de 1 segundo.
* **O que a auditoria provou:** **Nenhum arquivo magnético ou dado de magnetômetro foi lido**. O código avaliava uma função seno multiplicada por uma constante analítica ($J_z = V_I / R_c$), com um bloco condicional manual inserindo um valor forçado no dia 25/08/2026. A "inversão instrumental" era inteiramente ficcional.

### 3. A alegação de que Shugar et al. (Science, 2021) "provaram o enigma do 1% de fusão"
* **O que se afirmava:** Que Shugar et al. demonstraram um teto universal de 1% de fusão por atrito para provar a existência de água inexplicada em Chamoli.
* **O que a auditoria provou:** Shugar et al. demonstraram exatamente o contrário: que a fusão mecânica de gelo glacial arrastado na avalanche transformou o fluxo em lama fluida hiperconcentrada, sem necessidade de chuva líquida. O teto de 1% atribuído aos autores foi fabricado.

### 4. A prova de causalidade entre Erupções Solares e Colapsos no Himalaia
* **O que se afirmava:** Que as erupções solares de classe M/X eram os gatilhos físicos diretos dos desastres por acoplamento com o Circuito Elétrico Global ($J_z$).
* **O que a auditoria provou:** Trata-se de hipótese puramente exploratória e não comprovada:
  * A rigidez de corte geomagnética do Himalaia é de **~13 a 14 GV**, blindando a troposfera contra prótons solares de eventos eruptivos comuns.
  * A análise estatística sofre de severo **viés de seleção**: não houve avaliação de um grupo de controle de dias com erupções solares onde nenhum desastre ocorreu, nem de desastres que ocorreram durante o Sol calmo.

### 5. As contagens de raios anteriores a 2004
* **O que se afirmava:** Apresentavam-se tabelas com número de descargas elétricas, proporções intra-nuvem/nuvem-solo (IC/CG) e correntes de pico em kA para desastres de 1981, 1985 e 1994.
* **O que a auditoria provou:** As redes globais de monitoramento de raios em tempo real (WWLLN, GLD360) só entraram em operação após 2004. Esses dados foram gerados parametricamente e apresentados indevidamente como medições.
