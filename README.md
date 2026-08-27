# Catástrofe Transfronteiriça Nepal-Tibete (2026)
### Investigação Científica: Erupção Solar M7, Circuito Elétrico Global ($J_z$), Tempestades Convectivas, Infrassom, Mapeamento 3D do Rio Trishuli e Ruptura Glacial

[![GitHub Repository](https://img.shields.io/badge/GitHub-Himalaia__2026-blue.svg)](https://github.com/reinaldohaas/Himalaia_2026)
[![License: ODbL / CC-BY 4.0](https://img.shields.io/badge/License-ODbL%20%2F%20CC--BY%204.0-green.svg)](https://opendatacommons.org/licenses/odbl/)
[![Status: Scientific Audit Passed](https://img.shields.io/badge/Audit-Passed%20(Epistemic%20Standard)-brightgreen.svg)]()

Este repositório reúne o conjunto completo de dados, séries temporais, modelos de clima espacial, mapas interativos, projetos 3D para o Google Earth e documentação científica para investigar a seguinte **pergunta e hipótese**:

> **Hipótese Investigada:**
> A erupção solar de classe **M7.0**, ocorrida em **25 de agosto de 2026 às 10:02 UTC** na AR 3792, pode ter produzido, com defasagem temporal, alterações ionosféricas e no Circuito Elétrico Global (GEC), modulando a corrente vertical atmosférica $J_z$. Tais perturbações eletrodinâmicas podem ter influenciado a intensificação de convecção profunda ou tempestades severas ("torós") sobre o Himalaia Central. Essas tempestades podem ter gerado ondas de pressão de infrassom, descargas elétricas ou precipitação orográfica localizada de alta intensidade, atuando como gatilho mecânico/hidráulico para o colapso glacial no **Mt. Langtang Lirung (5.200 m)** e o rompimento do barramento no sistema **Lhende Khola–Bhote Koshi–Trishuli**, ocorrido aproximadamente às **02:52:10 UTC de 26 de agosto de 2026** (~16h 50min após o flare).

---

## 🎯 Classificação Epistemológica dos Dados (Padrão Rigoroso)

Para garantir rastreabilidade total e evitar extrapolações, todos os dados, tabelas e gráficos utilizam a classificação de status:

*   🔵 `DADO OBSERVADO` (`observed`): Medição direta por instrumento com fonte primária pública verificável (ex.: Raios X GOES-16, Sismograma USGS 4.4 mb, Censo de Pontes ICIMOD).
*   🟢 `DADO DERIVADO` (`derived`): Dado processado através de algoritmos físicos ou modelos empíricos validados (ex.: Precipitação NASA GPM IMERG, Absorção D-RAP, Vento Solar DSCOVR).
*   🟡 `ESTIMATIVA` (`estimated`): Cálculo aproximado baseado em parâmetros de engenharia ou literatura análoga (ex.: Pressão acústica baseada em Chamoli 2021).
*   🟠 `INFERÊNCIA` (`inferred`): Dedução lógica fundamentada em evidências indiretas.
*   🟣 `HIPÓTESE` (`hypothesis`): Proposta teórica a ser testada experimentalmente (ex.: Modulação de $J_z$ e gatilho elétrico no Himalaia).
*   ⚪ `NÃO VERIFICADO / INDISPONÍVEL` (`unverified` / `unavailable`): Dado que carece de liberação formal (ex.: Formas de onda de microbarômetros do CTBTO/IMS via protocolo vDEC).

---

## 🌐 Recursos Principais do Repositório

### 1. ☀️ Infográfico Interativo Sincronizado
*   **Arquivo:** [`infografico_solar_jz_tempestade.html`](./infografico_solar_jz_tempestade.html)
*   **Funcionalidades:**
    *   Linha do tempo interativa com canvas sincronizado desde a erupção M7 (10:02 UTC) até o desastre (02:52 UTC).
    *   **Controle deslizante de defasagem (Lag Slider 0–24h)** para demonstrar o comportamento de correlações defasadas.
    *   Mapa estrutural integrado com trajetórias de tempestades, descargas elétricas e o corredor da enxurrada (45 km).
    *   Diagrama da cadeia causal e matriz de hipóteses concorrentes.
    *   Painel *"O que sabemos / O que não sabemos"*.
    *   100% autônomo e sem dependências externas frágeis (compatível com visualização local e GitHub Pages).

### 2. 🌍 Mapas Mestre 3D para o Google Earth (KML)
*   [`mapa_mestre_trishuli_google_earth.kml`](./mapa_mestre_trishuli_google_earth.kml) — **Mapa Mestre 3D Completo:** Contém o **talvegue real do rio extraído do OpenStreetMap (2.979 pontos)**, polígono do lago de barramento do Lhende Khola (~3.950m), cicatriz glacial a 5.200m, 8 Usinas Hidrelétricas (>1.200 MW), 10 cidades/vilas, rodovias Pasang Lhamu/G216 e as 33 pontes avaliadas pelo ICIMOD com cores por status de dano.
*   [`nepal_tibet_disaster_tour.kml`](./nepal_tibet_disaster_tour.kml) — **Tour Cinematográfico 3D:** Animação automática guiando o sobrevoo pelas 6 fases da catástrofe.
*   [`nepal_tibet_disaster.kml`](./nepal_tibet_disaster.kml) — **Vetor do Fluxo de Detritos:** Traçado contínuo estritamente colado ao leito fluvial no relevo 3D.

### 3. 📄 Relatórios Científicos e Monografias
*   [`analise_solar_jz_tempestades_infrassom.md`](./analise_solar_jz_tempestades_infrassom.md) — Estudo científico aprofundado com as 12 seções metodológicas sobre acoplamento solar, física do GEC ($J_z = \sigma E_z$), meteorologia convectiva, discriminação de fontes de infrassom e sequência glaciológica.
*   [`dados_infrassom_avalanche.md`](./dados_infrassom_avalanche.md) — Auditoria técnica dos dados de infrassom, retificação da estação KKN (sísmica) e procedimento de solicitação vDEC para dados do CTBTO/IMS.
*   [`perfil_rio_trishuli.md`](./perfil_rio_trishuli.md) — Monografia sobre a Bacia do Rio Trishuli (hidrologia, cascata de 1.200 MW, perigos glaciais e importância sagrada).
*   [`relacao_de_fontes.md`](./relacao_de_fontes.md) — Catalogação completa de todas as fontes primárias e links oficiais.

---

## 📊 Estrutura de Dados e Tabela-Mestra

```
data/
├── metadata/
│   └── sources_metadata.json                     # Metadados, CRS WGS84, URLs e checksums
├── processed/
│   ├── timeline_master.csv                       # Tabela-mestra com 17 eventos e status padronizado
│   └── space_weather/
│       └── gec_jz_model_himalaya.csv             # Série temporal do modelo de GEC, Vi e Jz
├── raw/
│   └── space_weather/
│       ├── goes_xray_flux.csv                    # Fluxo de Raios X GOES-16 (0.05-0.4nm e 0.1-0.8nm)
│       ├── dscovr_solar_wind_l1.csv              # Vento solar e IMF em L1 (Vsw, Np, Pdyn, Bt, Bz, Ey)
│       └── geomagnetic_indices_and_gcr.csv       # Kp, Dst, SYM-H, AE e Raios Cósmicos (Oulu)
├── hot_flood_npl_aoi.geojson                     # Buffer oficial de 1 km da calha do rio (HDX / OCHA)
├── hot_flood_npl_bridges_damage_icimod.geojson   # 33 pontes avaliadas pelo ICIMOD
├── rio_trishuli_thalweg_oficial_osm.geojson       # Geometrias oficiais OSM (Relações 21284197 e 4839538)
└── talvegue_completo_kml.txt                     # 2.979 coordenadas ordenadas de montante a jusante
```

---

## 💻 Instruções de Execução e Reproducibilidade

Para instalar os requisitos e rodar os scripts de processamento:

```bash
# 1. Clonar o repositório
git clone https://github.com/reinaldohaas/Himalaia_2026.git
cd Himalaia_2026

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar o processador de dados solares e timeline-mestra
python scripts/generate_space_weather_datasets.py
```

Para visualizar a interface completa no navegador:
*   Abra localmente o arquivo [`index.html`](./index.html) ou [`infografico_solar_jz_tempestade.html`](./infografico_solar_jz_tempestade.html).
*   Abra os arquivos `.kml` no **Google Earth Pro** (Desktop) ou no **Google Earth Web** ([earth.google.com](https://earth.google.com)).
