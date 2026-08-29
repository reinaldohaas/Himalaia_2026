# High-Altitude Hazard Dynamics in the Langtang Basin (2026): Microphysics, Rock-Ice Collapse, and Environmental Signatures

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Status: Open for Collaboration](https://img.shields.io/badge/Collaboration-Open-brightgreen.svg)](https://github.com/reinaldohaas/Himalaia_2026)
[![Data: Reproducible](https://img.shields.io/badge/Data-100%25%20Reproducible-success.svg)](https://github.com/reinaldohaas/Himalaia_2026)

An open-source scientific research project investigating the cascading disaster of **August 25–26, 2026**, in the transboundary Langtang Lirung / Gyirong Port / Trishuli River basin (Tibet, China – Nepal border).

---

## 📖 Comprehensive Technical Report
👉 **Read the full publication-ready technical document:** [`TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md`](TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md)

---

## 🌐 Interactive 4D Web Visualizers

When running the local server (`python server_miniforge.py` or `node server.js`):
* **4D Spatiotemporal Web Viewer:** [`http://localhost:8000/viewer_4d.html`](http://localhost:8000/viewer_4d.html)  
  *Features real-time timeline playback, multi-axis Chart.js series (Jz, Lightning, Rain, X-Ray), animated lake swelling/breach, 14-station magnetometer pulses, and downstream mudflow routing.*
* **Master Infographic:** [`http://localhost:8000/index.html`](http://localhost:8000/index.html)
* **3D Earth & SAR Viewer:** [`http://localhost:8000/earth_3d_satellite_radar_viewer.html`](http://localhost:8000/earth_3d_satellite_radar_viewer.html)
* **GIS Infrastructure Damage Map:** [`http://localhost:8000/nepal_tibet_disaster_map.html`](http://localhost:8000/nepal_tibet_disaster_map.html)

---

## 🛰️ Spatial Datasets & Downloads Available in Repo
* **Sentinel-2 Natural Color KMZ (2.13 MB):** [`2026-08-12-00_00_2026-08-12-23_59_Sentinel-2_L2A_Highlight_Optimized_Natural_Color_.kmz`](2026-08-12-00_00_2026-08-12-23_59_Sentinel-2_L2A_Highlight_Optimized_Natural_Color_.kmz)
* **High-Res Lake GeoTIFF (3.17 MB):** [`sentinel_lhende_khola_lake.tif`](sentinel_lhende_khola_lake.tif)
* **Google Earth KML Master Thalweg:** [`mapa_mestre_trishuli_google_earth.kml`](mapa_mestre_trishuli_google_earth.kml)
* **Raw NOAA SWPC Telemetry:** [`data/raw/space_weather/goes_xrays_7day_real.json`](data/raw/space_weather/goes_xrays_7day_real.json) *(20,148 records)*
* **Official Bridge Damage Census:** [`data/hot_flood_npl_bridges_damage_icimod.geojson`](data/hot_flood_npl_bridges_damage_icimod.geojson) *(33 bridges / UN OCHA / ICIMOD)*

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

---

## 🤝 Open Call for Scientific Collaboration
We invite researchers and working groups specializing in **High-Altitude Hydrology**, **Atmospheric Microphysics**, **Glacial Geomechanics**, and **Remote Sensing** to contribute to this investigation.

* **GitHub Issues:** Open an issue to discuss modeling refinements, microphysical hypotheses, or data contributions.
* **Pull Requests:** Numerical routing models, high-resolution LES simulations, and InSAR deformation analyses are welcomed.
