# Protocolo de Proveniência de Dados, Metodologia Científica e Guia de Auditoria Independente

**Investigação:** 15 Catástrofes Hidromorfológicas do Himalaia (1980–2026)  
**Autor Principal:** Prof. Reinaldo Haas ([reinaldo.haas@ufsc.br](mailto:reinaldo.haas@ufsc.br))  
**Afiliação:** Departamento de Física, Universidade Federal de Santa Catarina (UFSC), Florianópolis, SC, Brasil  
**Repositório Oficial de Código e Dados:** [https://github.com/reinaldohaas/Himalaia_2026](https://github.com/reinaldohaas/Himalaia_2026)  
**Padrão de Conformidade:** *FAIR Data Principles (Findable, Accessible, Interoperable, Reusable)* para Auditoria por Pares Externa.

---

## 1. Propósito Deste Documento

Este documento serve como **guia exaustivo de auditoria independente e rastreabilidade de dados**. Qualquer revisor científico, perito geotécnico ou pesquisador externo pode, a partir destas diretrizes:
1. Rastrear a origem primária de cada dado físico, sismológico, meteorológico e orbital;
2. Reproduzir as equações analíticas de hidrologia inversa, balanço de massa líquida e termodinâmica de atrito;
3. Executar os scripts automatizados que geram os conjuntos de dados estruturados;
4. Auditar a análise de sensibilidade e incerteza paramétrica que comprova os déficits de 10x–20x e a limitação de 1% na fusão por atrito.

---

## 2. Proveniência e Fontes Primárias de Dados (Data Provenance)

### 2.1 Sensoriamento Remoto Óptico de Alta Resolução (Pares Antes/Depois)
Para mapear as cicatrizes lineares de decapagem desde as cristas de cume (*bedrock stripping chutes*) e delimitar as alterações geomorfológicas:

| Sensor / Missão | Agência Operadora | Resolução Espacial | Bandas Utilizadas | Repositório de Acesso Aberto | Janela Temporal dos Dados |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sentinel-2A/B (MSI)** | ESA / Copernicus | $10\text{ m}$ (VNIR), $20\text{ m}$ (SWIR) | B02, B03, B04, B08, B11, B12 | Copernicus Data Space Ecosystem / Planetary Computer STAC | 2015–presente ($t_0 \pm 30\text{ dias}$) |
| **PlanetScope** | Planet Labs | $3.0\text{ m}$ (PSB.SD / 8 bandas) | RGB, NIR, RedEdge | Planet Explorer / Education & Research License | 2016–presente ($t_0 \pm 10\text{ dias}$) |
| **Landsat 8/9 (OLI/TIRS)** | USGS / NASA | $15\text{ m}$ (Pancromática), $30\text{ m}$ (Multiespectral) | Bandas 1 a 7 | USGS EarthExplorer / AWS Open Data | 2013–presente |
| **Landsat 4/5/7 (TM/ETM+)** | USGS / NASA | $30\text{ m}$ | VNIR + SWIR | USGS EarthExplorer (Collection 2 Level-2) | 1982–2012 |
| **Imagens de Satélite Históricas (Corona)** | USGS / CIA (Declassified) | $1.8\text{ m} \text{ a } 2.7\text{ m}$ | Filme pancromático digitalizado | USGS EarthExplorer (Declassified Data) | 1960–1972 (Linha de base histórica de Zhangzangbo) |

* **Modelos Digitais de Elevação (DEM):**
  - **Copernicus GLO-30:** Resolução de 30m, datum vertical EGM2008 (usado para declividades de talvegue $S_0$ e cotas de cume).
  - **SRTM 1 Arc-Second Global (30m):** Linha de base topográfica pré-2000 da NASA/NGA.
  - **ALOS World 3D (AW3D30 - JAXA):** Modelo digital de superfície de 30m para confirmação de cristas agudas.

---

### 2.2 Satélites Geoestacionários e Radares (Minutos e Horas Anteriores ao Som)

| Sistema / Sensor | Operador | Canal Espectral | Resolução Temporal | Resolução Espacial | Parâmetro Extraído |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INSAT-3D / INSAT-3DR (Imager & Sounder)** | ISRO / IMD (Índia) | TIR-1 ($10.8\text{ }\mu\text{m}$), TIR-2 ($12.0\text{ }\mu\text{m}$), WV ($6.8\text{ }\mu\text{m}$) | $15\text{ a }30\text{ min}$ contínuo | $4.0\text{ km}$ no nadir | Taxa de resfriamento de topo de nuvem convectiva ($T_{bb} < -65^\circ\text{C}$) |
| **Kalpana-1 (MetSat-1 VHRR)** | ISRO (Índia) | Infravermelho Térmico ($10.5\text{–}12.5\text{ }\mu\text{m}$) | $30\text{ min}$ | $8.0\text{ km}$ | Célula orográfica confinada pré-colapso (Leh 2010, Kedarnath 2013) |
| **Meteosat IODC (Meteosat-7/8)** | EUMETSAT | Infravermelho Térmico e Vapor d'Água | $30\text{ min}$ | $5.0\text{ km}$ | Cobertura transfronteiriça do Oceano Índico e Himalaia |
| **GPM IMERG Final Run (v06/v07)** | NASA / JAXA | Micro-ondas passivas + IR calibrado | $30\text{ min}$ | $0.1^\circ \times 0.1^\circ$ (~$10\text{ km}$) | Precipitação de grade grossa regional ($P_{\text{meas}}$) |
| **Radares Meteorológicos Doppler (DWR)** | IMD (Índia) | Banda C e Banda S | Volume scan a cada $10\text{–}15\text{ min}$ | $1.0^\circ$ de feixe, alcance de $250\text{ km}$ | Ecos de refletividade (dBZ) em Mukteshwar, Srinagar e Kufri; identificação de *beam blockage* orográfico |

---

### 2.3 Clima Espacial, Heliofísica e Eletrodinâmica Global ($J_z$)

| Conjunto de Dados | Plataforma de Coleta | Parâmetro Físico | Cadência | Repositório Oficial |
| :--- | :--- | :--- | :--- | :--- |
| **Fluxo de Raios-X Solar (XRS)** | Satélites NOAA GOES (GOES-2 a GOES-18) | Irradiância em $0.1\text{–}0.8\text{ nm}$ (canal longo) e $0.05\text{–}0.4\text{ nm}$ (canal curto) | $1\text{ min}$ | NOAA National Centers for Environmental Information (NCEI) / SWPC |
| **Vento Solar & Campo Interplanetário** | Base NASA OMNIWeb (Satélites ACE, Wind, IMP-8) | Densidade de prótons ($N_p$), velocidade do vento solar ($V_{\text{sw}}$), $B_z$ (GSM), Pressão dinâmica ($P_{\text{dyn}}$) | $1\text{ min}$ e $1\text{ hora}$ | NASA Goddard Space Flight Center (SPDF OMNIWeb) |
| **Índice Geomagnético Planeta Kp / Dst** | GFZ Helmholtz Centre Potsdam / WDC Kyoto | Perturbação do campo magnético global (Kp 0 a 9) | $3\text{ horas}$ | German Research Centre for Geosciences (GFZ) |
| **Potencial Ionosférico ($V_I$)** | Circuito Elétrico Global (GEC) | Potencial elétrico da camada condutora em relação à Terra ($250\text{–}380\text{ kV}$) | Diária / Horária | Modelagem física via Tinsley (2008), Rycroft et al. (2008) |
| **Rede de Magnetômetros Trans-Himalaia** | Estações da China (Tibet) e Índia (IIG / INTERMAGNET) | Variações do campo $H$, $D$, $Z$ para inversão da densidade de corrente vertical $J_z$ | $1\text{ segundo}$ | INTERMAGNET / China Earthquake Administration |

---

### 2.4 Sismologia e Infrassom de Ruptura Mecânica Superficial

| Parâmetro Sismológico | Fonte Primária | Método de Extração | Observável Físico |
| :--- | :--- | :--- | :--- |
| **Magnitude de Superfície ($M_L$ / $M_b$)** | USGS National Earthquake Information Center (NEIC), ISC, Wadia Institute (WIHG) | Inversão espectral de ondas superficiais (Rayleigh/Love) | Ruptura mecânica de cume com profundidade focal $h \approx 0\text{ km}$ (descompressão gravitacional) |
| **Duração do Tremor Sísmico** | Estações regionais de banda larga (ex.: KKN, LSA, SHL) | Envoltória de sinal contínuo (envelope amplitude) | Tempo de trânsito da avalanche e atrito de megablocos no cânion ($10\text{ a }70\text{ min}$) |
| **Sinal Infrassônico de Choque** | Matrizes IMS / CTBTO e microbarômetros de pesquisa | Espectrograma acústico ($0.5\text{–}10\text{ Hz}$) | Deslocamento súbito de coluna de ar e onda de choque prévia à onda de lama |

---

## 3. Metodologia Analítica e Equações Físicas

### 3.1 Hidrologia Inversa de Canal Aberto (Equação de Manning)
Para cada evento, a seção transversal de garganta mais estreita a jusante foi modelada como um canal trapezoidal com base na topografia e marcas de cheia registradas em campo:

$$A = (B + z \cdot \Delta h) \cdot \Delta h$$

$$P = B + 2 \cdot \Delta h \cdot \sqrt{1 + z^2}$$

$$R_h = \frac{A}{P}$$

$$v = \frac{1}{n} \cdot R_h^{2/3} \cdot S_0^{1/2}$$

$$Q_{\text{peak}} = A \cdot v$$

* **Onde:**
  * $B$: Largura de fundo do cânion rochoso ($\text{m}$);
  * $z$: Inclinação das ombreiras rochosas ($1\text{V}:z\text{H}$);
  * $\Delta h$: Elevação da linha de água máxima gravada por marcas de deposição e lama nas encostas ($\text{m}$);
  * $S_0$: Declividade média do talvegue extraída do DEM Copernicus 30m ($\text{m/m}$);
  * $n$: Coeficiente de rugosidade de Manning, calibrado entre $0.045$ e $0.065$ para gargantas rochosas de alta montanha com megablocos (Chow, 1959; Barnes, 1967).

---

### 3.2 Separação de Fase Sólido-Líquido e Balanço de Água Pura
As cheias de detritos do Himalaia comportam-se como fluxos hiperconcentrados não-newtonianos:

$$V_{\text{solids}} = V_{\text{total}} \cdot C_v$$

$$V_{\text{water}} = V_{\text{total}} \cdot (1 - C_v)$$

* **Onde:**
  * $V_{\text{total}}$: Volume total do pulso hidro-sedimentar medido por diferenciação de DEM pré e pós-evento no vale ($\text{m}^3$);
  * $C_v$: Concentração volumétrica média de sólidos, aferida entre $0.20$ e $0.45$ por granulometria de depósitos e literatura clássica;
  * $V_{\text{water}}$: Volume líquido efetivo que precisou ser alimentado para sustentar o hidrograma ($\text{m}^3$).

---

### 3.3 Termodinâmica de Primeiro Princípio (Fusão por Atrito Mecânico)
Para verificar a alegação comum de que avalanches de rocha geram sua própria água através do calor de atrito durante a queda:

$$E_p = m_{\text{total}} \cdot g \cdot \Delta H$$

$$m_{\text{melt, max}} = \frac{\eta \cdot E_p}{L_f}$$

$$V_{\text{melt, max}} = \frac{m_{\text{melt, max}}}{\rho_{\text{water}}}$$

$$\text{Contribuição Percentual} = \frac{V_{\text{melt, max}}}{V_{\text{water}}} \times 100\%$$

* **Constantes e Parâmetros:**
  * $g = 9.80665\text{ m/s}^2$ (aceleração gravitacional);
  * $\Delta H$: Desnível vertical total percorrido pelo centro de massa ($\text{m}$);
  * $L_f = 3.34 \times 10^5\text{ J/kg}$ (calor latente de fusão do gelo a $0^\circ\text{C}$);
  * $\rho_{\text{water}} = 1.000\text{ kg/m}^3$;
  * $\eta$: Eficiência térmica de conversão de energia potencial em fusão de gelo.
  * **Nota Crítica de Auditoria sobre Shugar et al. (Science, 2021):** Shugar et al. demonstraram que o desastre de Chamoli foi causado por uma avalanche maciça de rocha e gelo (~27 milhões de m³, com ~20% de gelo) originada no pico Ronti, na qual a dissipação por atrito ao longo de 3.400 m de desnível fundiu frações volumosas de gelo, transformando o fluxo em lama hiperconcentrada sem qualquer necessidade de chuva líquida. O artigo **não** estabeleceu um teto de 1% para alegar anomalias hídricas; aplicar fórmulas de déficit pluviométrico a avalanches secas de rocha-gelo de inverno é um erro físico de categoria.

---

### 3.4 Lâmina Pluviométrica Localizada Necessária ($P_{\text{req}}$)
O volume de água líquida $V_{\text{water}}$ não explicado por lagos ($V_{\text{lake}}$) exige uma precipitação orográfica localizada de crista calculada por:

$$P_{\text{req}} = \frac{V_{\text{water}}}{A_{\text{basin}} \cdot C_{\text{runoff}}} \times 1000\text{ mm}$$

$$\text{Defasagem / Déficit Multiplier} = \frac{P_{\text{req}}}{P_{\text{meas}}}$$

* **Onde:**
  * $A_{\text{basin}}$: Área de drenagem da bacia confinada acima do ponto de estrangulamento ($\text{m}^2$);
  * $C_{\text{runoff}}$: Coeficiente de escoamento superficial (adotado entre $0.75$ e $0.90$ para encostas rochosas íngremes e periglaciais de altitude);
  * $P_{\text{meas}}$: Precipitação registrada por pluviômetros de vale ou satélites de grade grossa (GPM IMERG).

---

## 4. Roteiro Passo-a-Passo de Reprodução (Guia do Auditor)

Para auditar e reproduzir 100% dos resultados de forma automatizada no ambiente local, consulte adicionalmente a especificação detalhada de ambiente em [`SOFTWARE_AND_ENVIRONMENT_SPECIFICATION.md`](./SOFTWARE_AND_ENVIRONMENT_SPECIFICATION.md).

### Passo 1: Clonar o Repositório e Instalar Dependências Homologadas
```bash
git clone https://github.com/reinaldohaas/Himalaia_2026.git
cd Himalaia_2026

# Instalar dependências declaradas em requirements.txt
pip install -r requirements.txt
```

### Passo 2: Executar a Auditoria Criptográfica de Integridade (SHA-256)
Para garantir que nenhum arquivo foi corrompido, adulterado ou selecionado erroneamente:
```bash
python scripts/verify_audit_integrity.py
```
* **Saída Verificável:** Validação bit a bit de **111 arquivos de dados** contra o manifesto oficial [`data/CHECKSUMS_SHA256.txt`](./data/CHECKSUMS_SHA256.txt).

### Passo 3: Executar a Auditoria Hidráulica e Termodinâmica
```bash
python scripts/calculate_inverse_hydraulics.py
```
* **Saída Verificável:** Gera `data/catchment_hydraulics/inverse_hydraulics_all_events.json`.
* **Validação do Auditor:** Inspecione os campos `q_peak_m3_s`, `lake_deficit_ratio`, `frictional_water_pct_of_flood` e `deficit_multiplier` para conferir a consistência matemática direta com a Tabela da Seção 6 do Relatório Técnico.

### Passo 4: Executar a Extração de Clima Espacial e Forçamento Solar
```bash
python scripts/extract_solar_forcing.py
```
* **Validação do Auditor:** Confere a datação do flare solar GOES, o valor de $J_z$ do modelo analítico paramétrico (baseado na curva de Carnegie e potencial ionosférico com $R_c$ fixo, sem telemetria de magnetômetros in-situ) e o intervalo temporal até o desastre.

### Passo 5: Baixar e Auditar o Acervo de Satélite com Datas, Fronteiras e Geoestacionários
```bash
python scripts/download_all_satellite_images.py
```
* **Saída Verificável:** 
  * Diretório `data/satellite_imagery/<event_id>/` contendo **68 imagens padronizadas** com prefixo ISO de data (`YYYY-MM-DD_...`).
  * Ortoimagens de alta resolução de 10m com fusão de fronteiras internacionais oficiais (Esri World Boundaries), barras de escala métrica e carimbos de cume.
  * Série temporal geoestacionária rápida (GPM IMERG 30-min calibrado) nos intervalos $T-3\text{h}$, $T-1\text{h}$ e $T_0$ pré-colapso.
  * Manifesto completo de auditoria `data/satellite_imagery/local_imagery_manifest.json` catalogando SHA-256 de cada imagem.

### Passo 6: Execução em Comando Único do Protocolo Mestre de Auditoria
Para validar a integridade de ponta a ponta em uma única instrução:
```bash
python scripts/run_full_independent_audit.py
```
Retorna certificado de aprovação: `STATUS: 100% REPRODUZÍVEL`.

---

## 5. Análise de Sensibilidade Paramétrica e Incerteza (Error Budget)

A alegação anterior de que os desastres apresentavam déficits pluviométricos de 10× a 20× demonstrados "fora de qualquer margem de erro" foi submetida à auditoria independente e refutada como conclusão irrefutável. A existência ou o desaparecimento de déficit é estritamente condicionada aos parâmetros de entrada e às fontes observacionais utilizadas:

### 5.1 Execução da Análise de Sensibilidade
O script reprodutível [`scripts/sensitivity_analysis_hydraulics.py`](./scripts/sensitivity_analysis_hydraulics.py) avalia 560 combinações paramétricas variando o volume total de detritos $V_{\text{bulk}}$ (±30%), a área efetiva da bacia $A_{\text{basin}}$ (15 a 100 km²) e a precipitação de referência:

```bash
python scripts/sensitivity_analysis_hydraulics.py
```
A tabela completa de sensibilidade é gerada em [`data/processed/sensitivity_analysis_hydraulics.csv`](./data/processed/sensitivity_analysis_hydraulics.csv).

### 5.2 Resultados Críticos e Cenários Onde o Déficit Desaparece

#### Caso 1: Catástrofe de Kedarnath (2013)
* **Premissa anterior:** O código utilizava $P_{\text{meas}} = 35.0\text{ mm}$ arbitrado manualmente, gerando um déficit artificial de ~3.15× a 4.73×.
* **Dado Observacional Real:** Dobhal et al. (2013) e Allen et al. (2016) publicaram a medição direta da estação de Chorabari: **325 mm acumulados em 48h** (210 mm em 16/06 e 115 mm em 17/06).
* **Resultado Físico:** A lâmina de escoamento necessária ($P_{\text{req}}$) para drenar a bacia de 42 km² é de **110.4 mm**. Com a chuva real de 325 mm, **o déficit hídrico desaparece completamente** (folga de 2.94× a favor da precipitação observada).

#### Caso 2: Catástrofe de Chamoli (2021)
* **Premissa anterior:** Calculava-se $P_{\text{req}} = 298.9\text{ mm}$ e comparava-se com $P_{\text{meas}} = 0\text{ mm}$ de um dia de inverno seco, alegando "infinito déficit pluviométrico".
* **Realidade Física:** Trata-se de um erro de categoria. Shugar et al. (2021) demonstraram que Chamoli foi uma avalanche seca de rocha e gelo. Não houve chuva e a dinâmica não depende de precipitação orográfica.

#### Caso 3: Catástrofe de 2026 (Lhende Khola / Trishuli)
* Com a incorporação do volume do lago rompido ($7.54\times 10^6\text{ m}^3$) e a vazão de base monçônica do rio Trishuli (~$180\text{ m}^3/\text{s}$ durante 4h $\approx 2.59\times 10^6\text{ m}^3$), o volume líquido excedente a ser explicado por escoamento superficial cai de $14.20\times 10^6\text{ m}^3$ para **$4.07\times 10^6\text{ m}^3$**.
* A chuva requerida varia drasticamente conforme a delimitação espacial da bacia:
  * Em sub-bacia regional de $100\text{ km}^2$: $P_{\text{req}} = 47.9\text{ mm}$ (qualquer chuva de monção moderada supre integralmente o evento).
  * Na bacia de Gyirong/Lhende de $55\text{ km}^2$: $P_{\text{req}} = 87.0\text{ mm}$.
  * No núcleo estrito de montante ($28\text{ km}^2$): $P_{\text{req}} = 170.9\text{ mm}$.
* **Conclusão:** Sem dados pluviométricos reais in-situ ou telemetria GPM validada para 26/08/2026 no repositório, **não é possível provar cientificamente a existência de um déficit anômalo**. O déficit permanece uma hipótese não testada por falta de observação direta.

---

## 6. Mapeamento de Rastreabilidade Cruzada dos 15 Casos

A tabela a seguir consolida a cadeia de custódia e rastreabilidade para os 15 eventos:

| Rank | ID do Evento | Coordenadas Auditadas | Cume de Referência | Sensor de Satélite Antes/Depois | Dataset de Saída | Artigo de Referência Principal |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `kedarnath_2013` | $30.745^\circ\text{ N}, 79.067^\circ\text{ E}$ | Mt. Kedarnath ($6.940\text{ m}$) | Landsat-8 / Kalpana-1 TIR | `inverse_hydraulics_all_events.json` | Dobhal et al. (2013); Allen et al. (2016) |
| **2** | `chamoli_2021` | $30.378^\circ\text{ N}, 79.732^\circ\text{ E}$ | Nanda Devi ($7.816\text{ m}$) | Sentinel-2 L2A / PlanetScope | `inverse_hydraulics_all_events.json` | Shugar et al. (*Science*, 2021); Cook et al. (2021) |
| **3** | `himalaia_2026` | $28.274^\circ\text{ N}, 85.483^\circ\text{ E}$ | Langtang Lirung ($7.234\text{ m}$) | Sentinel-2 L2A / GOES-18 | `inverse_hydraulics_all_events.json` | Haas (2026, Technical Report) |
| **4** | `aru_2016` | $34.045^\circ\text{ N}, 82.285^\circ\text{ E}$ | Aru Range ($6.200\text{ m}$) | Sentinel-2 / Landsat-8 | `inverse_hydraulics_all_events.json` | Kääb et al. (*Nature Geosci.*, 2018); Gilbert et al. (2018) |
| **5** | `seti_2012` | $28.542^\circ\text{ N}, 84.152^\circ\text{ E}$ | Annapurna IV ($7.525\text{ m}$) | Landsat-7 / ASTER GDEM | `inverse_hydraulics_all_events.json` | Dwivedi et al. (2013); Kargel et al. (2013) |
| **6** | `south_lhonak_2023`| $27.905^\circ\text{ N}, 88.205^\circ\text{ E}$ | Lhonak Peak ($6.710\text{ m}$) | Sentinel-2 L2A / INSAT-3D | `inverse_hydraulics_all_events.json` | Chakraborty et al. (*Science*, 2024) |
| **7** | `leh_2010` | $34.152^\circ\text{ N}, 77.577^\circ\text{ E}$ | Ladakh Range ($5.600\text{ m}$) | Kalpana-1 / TRMM LIS | `inverse_hydraulics_all_events.json` | Thayyen et al. (2013); Hobley et al. (2012) |
| **8** | `melamchi_2021` | $28.095^\circ\text{ N}, 85.612^\circ\text{ E}$ | Helambu Cirque ($5.800\text{ m}$) | Sentinel-2 L2A / PlanetScope | `inverse_hydraulics_all_events.json` | Bhandari et al. (2022); Petley (2021) |
| **9** | `parechu_2000` | $32.028^\circ\text{ N}, 78.536^\circ\text{ E}$ | Spiti Rim ($5.200\text{ m}$) | Landsat-7 ETM+ / IRS LISS-III | `inverse_hydraulics_all_events.json` | Gupta & Sah (2008) |
| **10** | `zhangzangbo_1981`| $28.175^\circ\text{ N}, 86.045^\circ\text{ E}$ | Shishapangma ($8.027\text{ m}$) | Landsat-3 MSS / Corona | `inverse_hydraulics_all_events.json` | Xu (1988); Mool et al. (2001) |
| **11** | `dig_tsho_1985` | $27.870^\circ\text{ N}, 86.600^\circ\text{ E}$ | Langmoche Peak ($6.530\text{ m}$) | Landsat-5 TM / Topomapas | `inverse_hydraulics_all_events.json` | Vuichard & Zimmermann (1987) |
| **12** | `luggye_tsho_1994`| $28.080^\circ\text{ N}, 90.300^\circ\text{ E}$ | Kangphu Kang ($7.204\text{ m}$) | Landsat-5 TM | `inverse_hydraulics_all_events.json` | Watanabe & Rothacher (1996) |
| **13** | `bhotekoshi_2016` | $28.026^\circ\text{ N}, 85.965^\circ\text{ E}$ | Gongbatongsha ($6.100\text{ m}$) | Sentinel-2 L2A / Landsat-8 | `inverse_hydraulics_all_events.json` | Wang et al. (2018); Cook et al. (2018) |
| **14** | `himachal_2023` | $31.985^\circ\text{ N}, 77.150^\circ\text{ E}$ | Pir Panjal ($4.800\text{ m}$) | Sentinel-2 L2A / Radar Kufri | `inverse_hydraulics_all_events.json` | Paul et al. (2023); Singh et al. (2024) |
| **15** | `parechu_2005` | $31.956^\circ\text{ N}, 78.558^\circ\text{ E}$ | Parechu Gorge ($5.200\text{ m}$) | Landsat-7 ETM+ / ASTER | `inverse_hydraulics_all_events.json` | Bhambri et al. (2015); Gupta & Sah (2008) |

---

## 7. Termo de Responsabilidade e Contato para Auditoria Científica

Este protocolo foi desenhado para atender aos padrões de escrutínio das publicações mais rigorosas da geofísica internacional. Dúvidas técnicas sobre a reprodução de códigos, calibração de dados brutos ou solicitação de arquivos binários não comprimidos devem ser encaminhadas ao Investigador Principal:

* **Contato Acadêmico:** Prof. Reinaldo Haas
* **Email Institucional:** [reinaldo.haas@ufsc.br](mailto:reinaldo.haas@ufsc.br)
* **Repositório GitHub:** [https://github.com/reinaldohaas/Himalaia_2026](https://github.com/reinaldohaas/Himalaia_2026)
* **Rastreabilidade de Código:** Todos os commits são assinados e registrados no branch `main`.
