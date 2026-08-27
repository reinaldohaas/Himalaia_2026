# Relação Oficial de Fontes, Bases de Dados e Referências Técnicas

Este documento reúne a catalogação detalhada de todas as fontes de dados primários, relatórios governamentais, repositórios de sensoriamento remoto, bancos de dados humanitários e publicações científicas utilizadas na elaboração dos estudos, mapas e projetos 3D.

---

## 1. Dados Humanitários, Cartografia e Avaliação de Danos

### 🏢 HDX / OCHA / HOT / ICIMOD
* **Humanitarian Data Exchange (HDX / UN OCHA):**
  * **Dataset:** *Nepal Flood 2026 Bhote Koshi and Trishuli River Corridor*
  * **URL:** [https://data.humdata.org/dataset/hot_flood_npl](https://data.humdata.org/dataset/hot_flood_npl)
  * **Recursos Utilizados:**
    * `hot_flood_npl_aoi.geojson` — Buffer de 1 km ao longo de 314 km² da calha do rio (Forte de Rasuwagadhi até Devghat).
    * `hot_flood_npl_bridges_damage_icimod.geojson` — Levantamento de 33 pontes permanentes na bacia do Trishuli.
    * `hot_flood_npl_tm_projects.geojson` — Limites das tarefas de mapeamento colaborativo do Tasking Manager.
* **ICIMOD (International Centre for Integrated Mountain Development):**
  * Censo e georreferenciamento do status estrutural das pontes (*Washed out*, *Damaged*, *Spared*), incluindo a Ponte Miteri (Ponte da Amizade) na fronteira Nepal-China.
  * Relatórios glaciológicos sobre o maciço do Langtang e avaliação de risco de GLOFs na região Hindu Kush-Himalaia (HKH).
  * **URL:** [https://www.icimod.org/](https://www.icimod.org/)
* **Humanitarian OpenStreetMap Team (HOT):**
  * Camadas vetoriais atualizadas diariamente de infraestrutura viária (`roads`), hidrografia (`waterways`) e edificações (`buildings`).
  * **URL:** [https://tasks.hotosm.org/](https://tasks.hotosm.org/)
* **Overture Maps Foundation:**
  * Base integrada de pegadas de edifícios e malha viária global (parceria Linux Foundation, Microsoft, Meta, Amazon, TomTom).
  * **URL:** [https://overturemaps.org/](https://overturemaps.org/)

---

## 2. Sensoriamento Remoto, Imagens de Satélite e Radar

### 🛰️ Agências Espaciais e Operadores de Constelações
* **Copernicus Emergency Management Service (ESA / União Europeia):**
  * **Ativação:** Mapeamento Rápido em Demanda `EMSR927` (Nepal Floods 2026).
  * **Produtos:** Delimitação da mancha de inundação (*Delineation Map*) e graduação de danos em edificações (*Damage Grading*).
  * **URL:** [https://emergency.copernicus.eu/](https://emergency.copernicus.eu/)
* **Planet Labs PBC (PlanetScope & SkySat):**
  * Constelação Dove (resolução espacial de 3 metros) e SkySat (50 cm) para comparação "Antes e Depois" do desprendimento glacial a 5.200m.
  * Dados abertos de resposta a desastres via *Source Cooperative*.
  * **URL:** [https://source.coop/](https://source.coop/) e [https://www.planet.com/](https://www.planet.com/)
* **Sentinel-1 (ESA / Copernicus):**
  * Radar de Abertura Sintética (C-SAR, Banda C / polarizações VV+VH) para análise interferométrica (InSAR) de perda de coerência e retroespalhamento no leito fluvial.
* **Sentinel-2 (ESA / Copernicus):**
  * Imagens ópticas multiespectrais (10m) para cálculo do índice NDWI (*Normalized Difference Water Index*) e turbidez nos reservatórios das usinas hidrelétricas.

---

## 3. Geofísica, Sismologia e Hidrometeorologia

### ⚡ Redes Sismográficas e Autoridades de Recursos Hídricos
* **USGS (United States Geological Survey) - Earthquake Hazards Program:**
  * Registro sísmico do evento de **magnitude 4.4 mb** às 08:37:14 (Hora do Nepal) em `28.2765° N, 85.5194° E`.
  * Análise de profundidade zero (0 km) e modelo ShakeMap de Aceleração de Pico no Solo (PGA).
  * **URL:** [https://earthquake.usgs.gov/](https://earthquake.usgs.gov/)
* **ISC (International Seismological Centre) & EMSC (Euro-Mediterranean Seismological Centre):**
  * Boletins sismológicos globais e formas de onda da estação KKN (Katmandu, Nepal).
* **DHM Nepal (Department of Hydrology and Meteorology, Governo do Nepal):**
  * Dados telemétricos das estações hidrométricas de Betrawati e Syabrubesi no Rio Trishuli.
  * **URL:** [http://www.dhm.gov.np/](http://www.dhm.gov.np/)
* **Nepal Electricity Authority (NEA):**
  * Boletins de operação e capacidade instalada das usinas da bacia do Trishuli (Rasuwagadhi 111 MW, Chilime 22 MW, Trishuli-3A 60 MW).
  * **URL:** [https://www.nea.org.np/](https://www.nea.org.np/)

---

## 4. Clima Espacial, Física Solar e Tempestades Geomagnéticas

### ☀️ Centros de Previsão de Clima Espacial e Sismologia Magnética
* **NOAA Space Weather Prediction Center (SWPC):**
  * Escalas oficiais de Clima Espacial: Escala G (Geomagnética), Escala S (Radiação Solar) e Escala R (Bloqueio de Rádio).
  * Modelagem numérica magnetohidrodinâmica WSA-Enlil para propagação de CMEs.
  * **URL:** [https://www.spaceweather.gov/](https://www.spaceweather.gov/)
* **NASA Heliophysics Science Division / SDO (Solar Dynamics Observatory) & SOHO:**
  * Instrumentos AIA, HMI e LASCO (C2/C3) para monitoramento de manchas solares, flares e ejeções de massa coronal.
  * **URL:** [https://sdo.gsfc.nasa.gov/](https://sdo.gsfc.nasa.gov/) e [https://soho.nascom.nasa.gov/](https://soho.nascom.nasa.gov/)
* **DSCOVR (Deep Space Climate Observatory) & ACE (Advanced Composition Explorer):**
  * Medições *in-situ* de vento solar no Ponto Lagrangiano L1 ($V_{sw}$, densidade $N_p$, vetor magnético $B_z$).
* **World Data Center for Geomagnetism (Universidade de Kyoto, Japão):**
  * Série temporal e cálculo do Índice Dst (*Disturbance Storm Time*) para monitoramento da Corrente de Anel (*Ring Current*).
  * **URL:** [https://wdc.kugi.kyoto-u.ac.jp/](https://wdc.kugi.kyoto-u.ac.jp/)
* **SILSO (Sunspot Index and Long-term Solar Observations, Observatório Real da Bélgica):**
  * Série histórica do número internacional de manchas solares (SSN) do Ciclo Solar 1 (1755) ao Ciclo Solar 25.
  * **URL:** [https://www.sidc.be/SILSO/](https://www.sidc.be/SILSO/)
