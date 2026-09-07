# Especificação de Software, Dependências e Ambiente de Execução
## Reprodutibilidade Científica e Auditoria Independente — Projeto Himalaia 2026

Este documento estabelece as especificações exatas de software, bibliotecas, ferramentas de linha de comando, serviços de dados e protocolos criptográficos necessários para executar, verificar e auditar integralmente as análises do repositório **Himalaia 2026**.

---

## 1. Ambiente Computacional de Referência

O pipeline científico foi desenvolvido para operar de forma multiplataforma (Windows, GNU/Linux e macOS) sem dependência de softwares proprietários pagos (como ArcGIS Desktop ou MATLAB).

| Componente | Especificação Homologada | Notas de Compatibilidade |
| :--- | :--- | :--- |
| **Sistema Operacional** | Windows 10/11 x64, Ubuntu 22.04+ LTS, macOS Monterey+ | Testado e verificado em arquitetura x86_64 e ARM64 |
| **Linguagem Principal** | Python **3.10.x**, **3.11.x**, **3.12.x** (Referência: Python 3.12.4) | Exige suporte nativo a `urllib`, `hashlib`, `json` |
| **Ambiente Web / 3D** | Navegador moderno com suporte a WebGL e Mapbox GL JS v3+ | Chrome 120+, Firefox 120+, Edge 120+, Safari 17+ |
| **Versionamento** | Git 2.40+ | Commits assinados e rastreabilidade por SHA |

---

## 2. Dependências de Software Python (`requirements.txt`)

As bibliotecas utilizadas estão listadas em [`requirements.txt`](./requirements.txt) com seus respectivos propósitos na cadeia analítica:

```text
# Computação Numérica e Hidráulica Inversa
numpy>=1.24.0      # Álgebra linear, interpolação e vetores de vazão
scipy>=1.10.0      # Otimização paramétrica e integração numérica de vazão
pandas>=2.0.0      # Séries temporais de magnetômetros e descargas elétricas

# Processamento de Imagens, Cartografia e Banners
pillow>=10.0.0     # Composição alfa de camadas raster/vetor e tipografia cartográfica
matplotlib>=3.7.0  # Perfis longitudinais de talvegue e curvas de histerese

# Aquisição e Auditoria de Dados HTTP / APIs Orbitais
requests>=2.28.0   # Requisições REST com headers e controle de timeout
urllib3>=2.0.0     # Transporte HTTP/1.1 robusto com retentativas automáticas

# Ferramentas Opcionais de Geoprocessamento
geojson>=3.0.0     # Serialização OGC de limites de bacia e talvegues
```

### Instalação em Ambiente Isolado (Passo-a-Passo)
```bash
# 1. Clonar o repositório oficial
git clone https://github.com/reinaldohaas/Himalaia_2026.git
cd Himalaia_2026

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar o ambiente virtual
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# No Linux / macOS:
source venv/bin/activate

# 4. Instalar as dependências homologadas
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Endpoints e APIs Externas de Satélite e Dados Físicos

Para garantir que nenhum dado seja extraído erroneamente, os seguintes endpoints abertos e padronizados são utilizados pelos scripts automatizados:

### 3.1 Ortoimagens de Alta Resolução e Fronteiras Internacionais
* **Serviço Base:** Esri ArcGIS World Imagery Export REST API
  * **Endpoint:** `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export`
  * **Parâmetros:** `bboxSR=4326`, `imageSR=4326`, `size=1024,1024`, `format=png`, `f=image`
* **Serviço de Fronteiras e Topônimos:** Esri ArcGIS World Boundaries and Places MapServer
  * **Endpoint:** `https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/export`
  * **Parâmetros:** `bboxSR=4326`, `imageSR=4326`, `size=1024,1024`, `format=png32`, `transparent=true`, `f=image`
* **Metodologia de Fusão Cartográfica:** O script `scripts/download_all_satellite_images.py` efetua uma fusão por canal alfa (`alpha_composite`) entre a ortoimagem nua e a camada de fronteiras oficiais, desenhando cabeçalho cartográfico superior com as nações fronteiriças e rodapé com escala métrica calibrada e coordenadas WGS84.

### 3.2 NASA GIBS (Global Imagery Browse Services) — WMS 1.3.0
* **Endpoint:** `https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi`
* **Protocolo:** OGC WMS 1.3.0 (CRS:84 / EPSG:4326)
* **Camadas Utilizadas:**
  1. `MODIS_Terra_CorrectedReflectance_TrueColor`: Óptico diurno de 250m nos dias $t_0$ e $t_0 - 1\text{d}$.
  2. `IMERG_Precipitation_Rate_30min`: Precipitação calibrada multi-satélite e infravermelho geoestacionário a cada 30 minutos ($T-3\text{h}$, $T-1\text{h}$, $T_0$).

### 3.3 Microsoft Planetary Computer STAC API v1.0.0
* **Endpoint:** `https://planetarycomputer.microsoft.com/api/stac/v1/search`
* **Coleção:** `sentinel-2-l2a` (Copernicus Sentinel-2 Level-2A Bottom-of-Atmosphere)
* **Critério de Seleção:** `eo:cloud_cover < 40%`, ordenado por menor cobertura de nuvens dentro da janela temporal pré e pós-catástrofe.

---

## 4. Padrão Estrito de Nomenclatura e Rastreabilidade Criptográfica

### 4.1 Formato de Nomes de Arquivo
Nenhum arquivo do repositório possui denominação vaga ou anônima. Todas as imagens seguem a sintaxe ISO:
```
<ANO-MES-DIA>_<SENSOR>_<DESCRITOR-DO-ESTÁGIO>.<extensão>
```
* **Exemplos Reais em `data/satellite_imagery/`:**
  * `2021-02-07_ArcGIS_10m_highres_basin_borders.png` (Ortoimagem com fronteiras internacionais e escala)
  * `2021-02-07_NASA-GIBS_MODIS-Terra_event-day.jpg` (Refletância ótica no dia do desastre)
  * `2021-02-06_NASA-GIBS_MODIS-Terra_pre-event-1d.jpg` (Véspera do desastre)
  * `2021-02-07_T0151_GPM-IMERG_geostationary_-3h.png` (Quadro geoestacionário 3 horas antes)
  * `2021-02-07_T0351_GPM-IMERG_geostationary_-1h.png` (Quadro geoestacionário 1 hora antes)
  * `2021-02-07_T0451_GPM-IMERG_geostationary_T0.png` (Quadro geoestacionário no momento do colapso)
  * `2021-01-31_Sentinel-2-L2A_pre-event.jpg` (Cena multiespectral pré-evento)
  * `2021-02-25_Sentinel-2-L2A_post-event.jpg` (Cena multiespectral pós-evento)

### 4.2 Verificação Criptográfica SHA-256
Para assegurar que nenhum dado tenha sido alterado ou corrompido, o arquivo [`data/CHECKSUMS_SHA256.txt`](./data/CHECKSUMS_SHA256.txt) contém as assinaturas criptográficas SHA-256 de **111 arquivos** de dados do repositório.

Qualquer perito ou auditor pode rodar a verificação imediata:
```bash
python scripts/verify_audit_integrity.py
```
Saída esperada:
```text
Verified Files: 111 / 111 (100% MATCH)
STATUS: DATA INTEGRITY AUDIT PASSED - ALL ASSETS CRYPTOGRAPHICALLY SECURE.
```

---

## 5. Script Mestre de Execução e Auditoria Integral

Para auditar o projeto de ponta a ponta em menos de 5 segundos, execute:
```bash
python scripts/run_full_independent_audit.py
```
Este comando executa e valida em sequência:
1. A integridade criptográfica SHA-256 de todos os arquivos de dados.
2. O recálculo das equações de Manning e balanço térmico de fusão por atrito.
3. A extração dos forçamentos solares (raios-X GOES) e cálculo do decaimento da corrente ionosférica $J_z$.
4. A conformidade do catálogo de 68 imagens de satélite locais com fronteiras e carimbos de data.
