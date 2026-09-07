# The 2026 Langtang–Trishuli Catastrophe: Solar Forcing, Inflow Incongruities, and the Physics of an Unclassified Convective-Geomorphic Hazard ("Toró")

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Status: Open for Collaboration](https://img.shields.io/badge/Collaboration-Open%20(China%20%26%20Nepal)-brightgreen.svg)](https://github.com/reinaldohaas/Himalaia_2026)
[![Contact](https://img.shields.io/badge/Contact-reinaldo.haas%40ufsc.br-blue.svg)](mailto:reinaldo.haas@ufsc.br)

An open-source, reproducible scientific investigation into the catastrophic cascading disaster of **August 25–26, 2026**, in the transboundary Langtang Lirung / Gyirong Port / Trishuli River basin (Tibet, China – Nepal border).

**Principal Investigator:** Prof. Reinaldo Haas ([reinaldo.haas@ufsc.br](mailto:reinaldo.haas@ufsc.br))  
**Affiliation:** Departamento de Física, Universidade Federal de Santa Catarina (UFSC), Florianópolis, SC, Brazil  

---

## 📖 Comprehensive Technical Reports & Independent Audit
👉 **2026 Langtang Disaster Master Report:** [`TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md`](TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md)  
👉 **15 Himalayan Catastrophes (1980–2026) Comparative Report:** [`TECHNICAL_REPORT_HIMALAYAN_CATASTROPHES_1980_2026.md`](TECHNICAL_REPORT_HIMALAYAN_CATASTROPHES_1980_2026.md)  
👉 **Relatório de Correção Pós-Auditoria (Defeitos P0–P3):** [`RELATORIO_DE_CORRECAO.md`](RELATORIO_DE_CORRECAO.md)  
👉 **Limitações e Dados Indisponíveis (Declaração de Integridade):** [`LIMITACOES_E_DADOS_INDISPONIVEIS.md`](LIMITACOES_E_DADOS_INDISPONIVEIS.md)  
👉 **Independent Audit Protocol & Data Provenance:** [`DATA_PROVENANCE_AND_INDEPENDENT_AUDIT_PROTOCOL.md`](DATA_PROVENANCE_AND_INDEPENDENT_AUDIT_PROTOCOL.md)  
👉 **Scientific Literature Register & Critical Audit:** [`LITERATURE_REGISTER_HIMALAYAN_DISASTERS.md`](LITERATURE_REGISTER_HIMALAYAN_DISASTERS.md)

### Key Pillars of the Investigation (Post-Audit Status):
1. **Hydraulic and Geomorphic Balances (Audit Evaluation):**
   * Incorporating temporary moraine damming (up to $7.54\text{ M m}^3$) and Trishuli baseflow ($2.59\text{ M m}^3$ in 4h) reduces the net required runoff from $14.2\text{ M m}^3$ to **$4.07\text{ Million m}^3$**.
   * In a realistic $55-65\text{ km}^2$ headwater catchment, an intense orographic cloudburst of $73-87\text{ mm}$ fully satisfies the flood volume without deficit.
   * Without in-situ rain gauges or validated GPM 2026 data in the repository, the previously claimed 10x deficit is not an established fact.
2. **Solar-Atmospheric Electrodynamic Hypothesis ($J_z$):**
   * Evaluates Class M6.9 solar flare (GOES-18, AR 4513, Aug 25 10:02 UTC).
   * Vertical current density $J_z$ is modeled using an **analytical parametric Carnegie GEC model** ($J_z = V_I / R_c$). Synthetic model data is strictly segregated under `data/synthetic/`.
   * High geomagnetic cutoff rigidity (~13–14 GV) and selection bias (lack of negative control days) are critical physical constraints; electrodynamic triggering is an exploratory hypothesis.
3. **The "Toró" Physical Framework (Haas, 2026):**
   * Investigates orographic secondary ice production (SIP) and high-elevation convective dumping.
4. **Geomythology & Oral Traditions:**
   * Tibetan oral lore of the *Druk* (Thunder Dragon) reflecting ancestral memory of mountain soundscapes, luminescence, and flash flooding.
5. **Rigorous Scientific Integrity:**
   * Fully reproducible open-source pipeline; parameters documented in `config/hydraulic_assumptions.yaml`; zero synthetic files labeled as telemetry.

---

## 🌐 Live Interactive Web Visualizers (GitHub Pages)

Access all interactive tools online with zero installation:
* **🚀 4D Spatiotemporal Master Viewer:** [https://reinaldohaas.github.io/Himalaia_2026/viewer_4d.html](https://reinaldohaas.github.io/Himalaia_2026/viewer_4d.html)  
  *Real-time timeline scrubber, multi-axis series (Jz, Lightning, Rain, X-Ray), animated lake swelling/breach, 14-station magnetometer dynamics, and downstream debris flow routing.*
* **🗺️ 15 Catástrofes do Himalaia (1980–2026) - Apresentação 3D:** [https://reinaldohaas.github.io/Himalaia_2026/mapa_ranking_himalaia_1980_2026.html](https://reinaldohaas.github.io/Himalaia_2026/mapa_ranking_himalaia_1980_2026.html)  
  *Navegação forense interativa em 3D, epicentros de ruptura no cume (h ≈ 0 km), intensidade MMI, sons, cheiros/gases, faíscas de atrito e inconsistências físicas documentadas na literatura.*
* **📑 Monografia de Revisão Bibliográfica de Inconsistências:** [`REVISAO_BIBLIOGRAFICA_INCONSISTENCIAS_HIMALAIA.md`](REVISAO_BIBLIOGRAFICA_INCONSISTENCIAS_HIMALAIA.md)  
  *Compilação rigorosa do Paradoxo do Déficit Hídrico (Fluência >> Chuva + Fusão) e Discrepância Cinético-Sísmica com dados de periódicos peer-reviewed (Science, Nature, GRL, NHESS).*
* **☀️ Estudo de Clima Espacial (Raios X Solar & Jz):** [`ESTUDO_CORRELACAO_SOLAR_RAIOS_X_JZ_HIMALAIA.md`](ESTUDO_CORRELACAO_SOLAR_RAIOS_X_JZ_HIMALAIA.md)  
  *Levantamento de picos de raios X (GOES), erupções Classe M/X, índice Kp e densidade de corrente Jz nas 12h a 72h anteriores a cada um dos 15 eventos históricos.*
* **⚡ Descargas Elétricas & Raios a 10 km:** [`LEVANTAMENTO_RAIOS_DESCARGAS_10KM_HIMALAIA.md`](LEVANTAMENTO_RAIOS_DESCARGAS_10KM_HIMALAIA.md)  
  *Quantificação espacial de flashes (WWLLN, TRMM LIS, INSAT-3D, FY-4), proporção IC vs. CG (+CG / -CG), líderes ascendentes de crista (Upward Lightning) e emissões de quartzo a 10 km de cada epicentro.*
* **🌩️ Descargas em 20 km (Janela Pico de Jz → Colapso):** [`LEVANTAMENTO_RAIOS_20KM_JANELA_JZ_HIMALAIA.md`](LEVANTAMENTO_RAIOS_20KM_JANELA_JZ_HIMALAIA.md)  
  *Área de 1.256,6 km² integrada desde o instante da erupção solar/salto de Jz até a quebra física, capturando a nucleação da convecção e super-raios +CG em escala de bacia hidrográfica.*
* **🔬 Protocolo de Proveniência de Dados e Auditoria Independente:** [`DATA_PROVENANCE_AND_INDEPENDENT_AUDIT_PROTOCOL.md`](DATA_PROVENANCE_AND_INDEPENDENT_AUDIT_PROTOCOL.md)  
  *Cadeia de custódia primária, fórmulas de Manning e balanço térmico de fusão por atrito, hashes SHA-256 e guia de reprodução.*
* **💻 Especificação de Software e Ambiente Computacional:** [`SOFTWARE_AND_ENVIRONMENT_SPECIFICATION.md`](SOFTWARE_AND_ENVIRONMENT_SPECIFICATION.md)  
  *Versões homologadas de interpretadores, dependências Python (`requirements.txt`), APIs abertas e padrões cartográficos.*
* **📥 KMZ Completo do Ranking (Google Earth Pro):** [`catastrofe_himalaia_1980_2026_ranking.kmz`](catastrofe_himalaia_1980_2026_ranking.kmz)
* **📊 Master Infographic & Data Portal:** [https://reinaldohaas.github.io/Himalaia_2026/](https://reinaldohaas.github.io/Himalaia_2026/) *(or index.html)*
* **🗺️ GIS Infrastructure Damage Map (33 Bridges):** [https://reinaldohaas.github.io/Himalaia_2026/nepal_tibet_disaster_map.html](https://reinaldohaas.github.io/Himalaia_2026/nepal_tibet_disaster_map.html)

---

## 🤝 Call for Scientific Collaboration (China, Nepal & Global Groups)

We warmly invite colleagues from **China** (CAS, ITPCAS, CEA, CMA) and **Nepal** (Tribhuvan University, DHM, ICIMOD, NEA), as well as international researchers in **Atmospheric Physics**, **High-Altitude Hydrology**, **Glacial Geomechanics**, and **Remote Sensing**, to collaborate with us.

### 📬 Academic Contact:
* **Principal Investigator:** Prof. Reinaldo Haas
* **Affiliation:** Departamento de Física, Universidade Federal de Santa Catarina (UFSC), Brazil
* **Institutional Email:** [reinaldo.haas@ufsc.br](mailto:reinaldo.haas@ufsc.br)
* **GitHub Issues & Discussions:** [https://github.com/reinaldohaas/Himalaia_2026/issues](https://github.com/reinaldohaas/Himalaia_2026/issues)

---

## 🚀 Quickstart & Independent Audit (Miniforge / Conda / Pip)

```bash
# 1. Clonar repositório
git clone https://github.com/reinaldohaas/Himalaia_2026.git
cd Himalaia_2026

# 2. Instalar dependências homologadas
pip install -r requirements.txt

# 3. Executar o Protocolo Mestre de Auditoria Independente (SHA-256, Hidráulica, Satélites):
python scripts/run_full_independent_audit.py

# 4. Verificar integridade criptográfica bit a bit de todos os arquivos de dados:
python scripts/verify_audit_integrity.py

# 5. Iniciar o servidor web local:
python server_miniforge.py
```
Acesse `http://localhost:8000/mapa_ranking_himalaia_1980_2026.html` ou `http://localhost:8000/viewer_4d.html` no seu navegador.
