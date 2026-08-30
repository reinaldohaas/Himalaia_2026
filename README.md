# The 2026 Langtang–Trishuli Catastrophe: Solar Forcing, Inflow Incongruities, and the Physics of an Unclassified Convective-Geomorphic Hazard ("Toró")

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Status: Open for Collaboration](https://img.shields.io/badge/Collaboration-Open%20(China%20%26%20Nepal)-brightgreen.svg)](https://github.com/reinaldohaas/Himalaia_2026)
[![Contact](https://img.shields.io/badge/Contact-reinaldo.haas%40ufsc.br-blue.svg)](mailto:reinaldo.haas@ufsc.br)

An open-source, reproducible scientific investigation into the catastrophic cascading disaster of **August 25–26, 2026**, in the transboundary Langtang Lirung / Gyirong Port / Trishuli River basin (Tibet, China – Nepal border).

**Principal Investigator:** Prof. Reinaldo Haas ([reinaldo.haas@ufsc.br](mailto:reinaldo.haas@ufsc.br))  
**Affiliation:** Departamento de Física, Universidade Federal de Santa Catarina (UFSC), Florianópolis, SC, Brazil  

---

## 📖 Comprehensive Technical Report
👉 **Read the full publication-ready technical document:** [`TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md`](TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md)

### Key Pillars of the Investigation:
1. **Confronting Official Incongruities (The ~10× Water Deficit):**
   * Pre-event lake volume ($5.2\text{ M m}^3$) accounts for $<35\%$ of the surge.
   * Frictional ice-melt ($388\text{ TJ}$) yields $<0.45\text{ M m}^3$ ($<3\%$).
   * Coarse GPM satellite rain ($15-30\text{ mm}$) yields only $\sim 0.84\text{ M m}^3$.
   * Channel hydraulic reconstruction ($8.5\text{ m}$ stage rise, $Q_{\text{peak}} \approx 3,376\text{ m}^3/\text{s}$) demands **$14.20\text{ Million m}^3$** of net liquid water, revealing a **$\sim 10$-fold deficit** in standard explanations.
2. **Solar-Atmospheric Electrodynamic Forcing ($J_z$):**
   * Real-time telemetry from NOAA GOES-18 (Class M7.0 solar flare on Aug 25, 10:02 UTC) driving an ionospheric jump ($V_I = 356.4\text{ kV}$, $J_z \approx 4.57\text{ pA/m}^2$) inverted across a 14-station Trans-Himalayan magnetometer network (China + South Asia).
3. **The "Toró" Physical Framework (Haas, 2026; Tinsley, 1991, 2008):**
   * Electro-antiscavenging preserving uniform supercooled droplet spectra, followed by runaway secondary ice production (SIP / Hallett-Mossop) and an explosive "hydraulic piston" convective dump (>500–950 mm in <2 h over $<15\text{ km}^2$).
4. **Geomythology & Shifting Environmental Baselines:**
   * Tibetan oral lore of the *Druk* (Thunder Dragon) as an indigenous physical memory of infrasound acoustic shocks, quartz piezoelectric luminescence, and destructive high-velocity debris flows.
5. **Cutting-Edge Science with Heterodox Hypotheses:**
   * Grounded in first-principles physics, mass conservation, numerical hydrograph integration, and open reproducible code.

---

## 🌐 Live Interactive Web Visualizers (GitHub Pages)

Access all interactive tools online with zero installation:
* **🚀 4D Spatiotemporal Master Viewer:** [https://reinaldohaas.github.io/Himalaia_2026/viewer_4d.html](https://reinaldohaas.github.io/Himalaia_2026/viewer_4d.html)  
  *Real-time timeline scrubber, multi-axis series (Jz, Lightning, Rain, X-Ray), animated lake swelling/breach, 14-station magnetometer dynamics, and downstream debris flow routing.*
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

## 🚀 Quickstart & Reproducibility (Miniforge / Conda)

```bash
# 1. Clone repository
git clone https://github.com/reinaldohaas/Himalaia_2026.git
cd Himalaia_2026

# 2. Run the Inverse Hydrological Balance calculation:
python scripts/inverse_hydrology_balance.py

# 3. Run the 14-station Trans-Himalayan Jz electrodynamic inversion:
python scripts/recalculate_jz_with_china_network.py

# 4. Launch the local web server:
python server_miniforge.py
```
Open `http://localhost:8000/viewer_4d.html` in your browser.
