# High-Altitude Hazard Dynamics in the Langtang Basin (2026): Microphysics, Rock-Ice Collapse, Geomythology, and Environmental Signatures

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Status: Open for Collaboration](https://img.shields.io/badge/Collaboration-Open%20(China%20%26%20Nepal)-brightgreen.svg)](https://github.com/reinaldohaas/Himalaia_2026)
[![Contact](https://img.shields.io/badge/Contact-reinaldo.haas%40gmail.com-blue.svg)](mailto:reinaldo.haas@gmail.com)

An open-source scientific investigation into the catastrophic cascading disaster of **August 25–26, 2026**, in the transboundary Langtang Lirung / Gyirong Port / Trishuli River basin (Tibet, China – Nepal border).

---

## 📖 Comprehensive Technical Report
👉 **Read the full publication-ready technical document:** [`TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md`](TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md)

*Key Themes Investigated:*
1. **The ~10× Water Volume Anomaly:** Why conventional models (simple GLOF drainage, frictional ice-melt, and coarse satellite rainfall) fail by a factor of 10 to account for the **$14.20\text{ Million m}^3$** of net liquid water mobilized through the Trishuli gorge ($Q_{\text{peak}} \approx 3,376\text{ m}^3/\text{s}$).
2. **The "Toró" High-Altitude Microphysical Framework:** Investigating how pristine alpine atmospheres, electro-scavenging ($J_z$), and runaway secondary ice production (SIP) create explosive localized convective dumps (>500–950 mm in <2 h).
3. **Geomythology & Shifting Baselines:** How ancient Tibetan/Himalayan oral traditions (*Druk* / Thunder Dragon lore) preserved the memory of rare, high-energy atmospheric-geomorphic phenomena that modern aerosol pollution later obscured.
4. **Quantitative Inverse Hydrology:** Open-channel Manning reconstruction and numerical hydrograph integration.
5. **Trans-Himalayan 14-Station Magnetometer Inversion:** Ionospheric coupling following the August 25 Class M7.0 solar flare.

---

## 🌐 Live Interactive Web Visualizers (GitHub Pages)

Access the interactive tools online with zero installation:
* **🚀 4D Spatiotemporal Master Viewer:** [https://reinaldohaas.github.io/Himalaia_2026/viewer_4d.html](https://reinaldohaas.github.io/Himalaia_2026/viewer_4d.html)  
  *Real-time timeline scrubber, multi-axis series (Jz, Lightning, Rain, X-Ray), animated lake swelling/breach, 14-station magnetometer dynamics, and downstream debris flow routing.*
* **📊 Master Infographic & Data Portal:** [https://reinaldohaas.github.io/Himalaia_2026/](https://reinaldohaas.github.io/Himalaia_2026/) *(or index.html)*
* **🗺️ GIS Infrastructure Damage Map (33 Bridges):** [https://reinaldohaas.github.io/Himalaia_2026/nepal_tibet_disaster_map.html](https://reinaldohaas.github.io/Himalaia_2026/nepal_tibet_disaster_map.html)

---

## 🤝 Call for Scientific Collaboration (China, Nepal & Global Groups)

We warmly invite colleagues from **China** (CAS, ITPCAS, CEA, CMA) and **Nepal** (Tribhuvan University, DHM, ICIMOD, NEA), as well as international researchers in **Atmospheric Microphysics**, **High-Altitude Hydrology**, **Glacial Geomechanics**, and **Remote Sensing**, to collaborate with us.

### 📬 Direct Contact:
* **Lead Investigator:** Reinaldo Haas
* **Email:** [reinaldo.haas@gmail.com](mailto:reinaldo.haas@gmail.com)
* **GitHub Issues / Discussions:** [https://github.com/reinaldohaas/Himalaia_2026/issues](https://github.com/reinaldohaas/Himalaia_2026/issues)
* **Pull Requests:** Numerical flood routing (RAMMS / FLO-2D / HEC-RAS), high-resolution LES microphysical models (WRF), and InSAR phase analysis are actively welcomed.

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
