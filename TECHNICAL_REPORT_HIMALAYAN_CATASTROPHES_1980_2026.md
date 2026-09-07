# The Himalayan Catastrophes (1980–2026): A Unified Physical Audit of 15 Extreme High-Mountain Disasters

**Principal Investigator:** Prof. Reinaldo Haas ([reinaldo.haas@ufsc.br](mailto:reinaldo.haas@ufsc.br))  
**Affiliation:** Departamento de Física, Universidade Federal de Santa Catarina (UFSC), Florianópolis, SC, Brazil  
**Geographic Scope:** Trans-Himalayan Arc & Tibetan Plateau (India, Nepal, Bhutan, China/Tibet)  
**Time Horizon:** 1980 to 2026 (46 Years of High-Mountain Geohazard Records)  
**Open Code & Data Repository:** [https://github.com/reinaldohaas/Himalaia_2026](https://github.com/reinaldohaas/Himalaia_2026)  
**Methodological Companion Document:** [`LITERATURE_REGISTER_HIMALAYAN_DISASTERS.md`](file:///C:/Users/haas/github/Himalaia_2026/LITERATURE_REGISTER_HIMALAYAN_DISASTERS.md)  
**Status:** Working Paper for International Peer-Reviewed Submission

---

## 1. Epistemological Framework & Unified First-Principles Methodology

Extreme high-mountain catastrophes in the Himalayas have long challenged standard hazard assessments. When a multi-million-cubic-meter slurry of mud, ice, and megablocks obliterates river gorges within minutes, post-event institutional reports routinely converge on familiar, off-the-shelf explanations:
* A conventional moraine breach of a small proglacial lake (GLOF);
* Frictional melting of ice during a rock avalanche;
* A typical seasonal monsoon cloudburst recorded by coarse-resolution regional stations.

Following an uncompromising scientific audit of all 15 events, this report strictly separates measured observational telemetry from parametric assumptions, correcting earlier false attributions:
1. **The Frictional Melting Regime in Avalanches:** In dry rock-ice avalanches with zero pre-existing lakes (such as **Chamoli 2021**), the primary driving mechanism is solid mass gravitational collapse where frictional dissipation melts entrained glacier ice into slurry (Shugar et al., *Science*, 2021). Applying liquid rainfall-runoff models to dry winter avalanches is a physical category error.
2. **Pluviometric and Lacustrine Mass Balance:** In events like **Kedarnath (2013)**, while the static capacity of Chorabari lake ($0.38\times 10^6\text{ m}^3$) was small compared to the total flow, in-situ rain gauges (Dobhal et al., 2013) recorded **325 mm of rainfall in 48 hours**. This observed precipitation easily covers the ~110 mm runoff depth required to sustain the downstream flood volume, completely resolving the apparent deficit.
3. **Mountain-Top Linear Scouring Scars:** High-resolution optical satellite pairs (Sentinel-2 10m, PlanetScope 3m) reveal continuous bedrock-stripping chutes originating on steep ridge crests ($>5,000\text{ to }7,000\text{ m}$), indicating intense summit-level geomorphic initiation.

To provide a transparent, audit-compliant assessment across the entire Himalayan arc, this report establishes a unified physical protocol applied to all 15 major events from 1980 to 2026, reading open parameters from `config/hydraulic_assumptions.yaml`.

---

## 2. Audit of Published Literature & Key Physical Distinctions

### 2.1 The Physical Dynamics of Chamoli 2021 (*Science*, Shugar et al., 2021)
In the Chamoli catastrophe of February 7, 2021, a massive rock-ice wedge (~27 million m³, ~80% rock, ~20% glacier ice) collapsed from the north face of Ronti Peak (descent from 5,600 m to 2,200 m).
* **Observed Facts (*Science*, Shugar et al., 2021):**
  * **Zero pre-existing lake:** Lake volume was $V_{\text{lake}} = 0\text{ m}^3$.
  * **Dry winter morning:** Zero precipitation in the valley or on the mountain.
  * **Massive liquid/slurry flood:** Peak discharge reached $Q_{\text{peak}} \approx 8,635\text{ m}^3/\text{s}$ (Manning cross-section reconstruction).
* **Thermodynamics and Slurry Mobilization:**
  * Shugar et al. (2021) demonstrated that frictional heating during the 3,400 m vertical descent melted significant portions of the entrained glacier ice, transforming the dry rock avalanche into a devastating, fast-moving debris slurry.
  * **Audit Clarification:** Shugar et al. did **not** state a universal 1% thermodynamic ceiling to argue for an unexplained liquid water deficit. Evaluating Chamoli against rainfall formulas is physically inappropriate because the event was purely an avalanche-driven mass movement without atmospheric precipitation involvement.

### 2.2 Volumetric Balances: Kedarnath (2013) and Langtang (2026)
* **Kedarnath 2013:**
  * Chorabari Lake static capacity: $V_{\text{lake}} = 0.38 \times 10^6\text{ m}^3$ (Dobhal et al., 2013; Allen et al., 2016).
  * Downstream flood hydrograph: $V_{\text{bulk}} = 7.2 \times 10^6\text{ m}^3$, $V_{\text{water, gross}} = 4.68 \times 10^6\text{ m}^3$.
  * In-situ measured precipitation: **325 mm** (Chorabari camp AWS: 210 mm on 16/06 and 115 mm on 17/06).
  * **Audit Resolution:** The required runoff depth over the 42 km² basin is **110.4 mm**. Because 325 mm was directly measured, **no water deficit exists in Kedarnath** (the observed rain covers the requirement with a 2.94× margin).
* **Langtang 2026:**
  * Pre-breach lake and debris blockage retention: up to $V_{\text{lake}} = 7.54 \times 10^6\text{ m}^3$.
  * River baseflow contribution: ~180 m³/s over 4 hours accounts for $2.59 \times 10^6\text{ m}^3$.
  * Net runoff required from rainfall: $V_{\text{runoff, req}} = 4.07 \times 10^6\text{ m}^3$.
  * Over a 55–65 km² headwater catchment, the required rainfall depth is **73 to 87 mm**.
  * **Audit Resolution:** No in-situ rain gauges or GPM IMERG 2026 files exist in the repository (`[DATA UNAVAILABLE]`). Therefore, the existence of an anomalous deficit cannot be asserted as an observed fact.

---

## 3. High-Resolution Optical Remote Sensing: Mountain-Top Linear Scars

A defining geomorphic signature identified in our survey is the presence of **continuous linear mountain-top scouring scars** (*bedrock stripping chutes*):
* **Morphological Characteristics:**
  * Linear, razor-straight stripping scars originating on extreme high-altitude rocky crests ($>5,000\text{ to }7,000\text{ m}$), well above the cirque glacier level.
  * Complete removal of soil, regolith, and talus mantles, exposing pristine, unweathered bedrock with drastic drops in Normalized Difference Vegetation Index (NDVI) and pronounced reflections in shortwave infrared (SWIR-1/SWIR-2).
* **Observation Strategy via Pares Antes/Depois (Sentinel-2 L2A & PlanetScope):**
  * Because optical sensors cannot penetrate dense storm cloud decks during the active convective burst, high-resolution before/after image pairs ($t_0 - 15\text{ days}$ vs. $t_0 + 15\text{ days}$) are essential.
  * In events such as Kedarnath 2013, Melamchi 2021, and Langtang 2026, the scars converge from multiple ridge summits down into the central drainage chute, confirming that the hydraulic stripping was initiated at the top of the mountain.

---

## 4. Atmospheric, Geostationary & Doppler Radar Diagnostics Prior to the Acoustic Blast

### 4.1 Rapid-Scan Geostationary Satellites (INSAT-3D/3DR, Kalpana-1, Meteosat IODC)
In the 15 to 180 minutes preceding the reported acoustic blasts ("cannon roar / military jet sounds"):
* **Cloud Top Brightness Temperature ($T_{bb}$):** Thermal infrared channels (TIR-1 10.8 µm) recorded rapid cooling rates ($>15^\circ\text{C}/\text{hour}$), with cloud tops plunging below **$-65^\circ\text{C}$ to $-75^\circ\text{C}$** directly pinned over high-altitude crests (e.g., Kedarnath Peak in 2013, Leh in 2010, Himachal in 2023).
* **Overshooting Tops (OT):** Deep convective cores penetrating the tropopause over alpine cirques, confirming highly localized, intense vertical updrafts ("hydraulic piston" mechanism).

### 4.2 Weather Radars (IMD Doppler Weather Radars) & The Orographic Beam Blockage
* India operates C-band and S-band Doppler Weather Radars (DWR) at **Mukteshwar (Kumaon/Uttarakhand)**, **Srinagar (Kashmir)**, and **Kufri (Himachal Pradesh)**.
* **The Beam Blockage Constraint:** In steep Himalayan terrain, the lowest radar elevation angles ($0.5^\circ\text{ to }1.5^\circ$) are completely obstructed by outer mountain ranges. Consequently, radar beams pass high above deep glacial valleys (often $>4,500\text{ m}$ above ground level), frequently missing isolated, ridge-trapped convective cells or underestimating precipitation echoes in the narrow cirques.

---

### 5. Solar Electrodynamic Hypothesis & Vertical Current Density ($J_z$)

Atmospheric electricity and the Global Electrical Circuit (GEC) have been proposed as a potential coupling mechanism between space weather and high-altitude cloud microphysics (Tinsley, 2008):
* **Analytical Parametric Model:** In this repository, vertical current density $J_z$ is modeled analytically using the classical Carnegie GEC curve coupled with ionospheric potential $V_I$ and an assumed column resistance $R_c = 0.78 \times 10^{17}\,\Omega\cdot\text{m}^2$. **Audit Clarification:** No raw magnetometer telemetry was used to invert $J_z$.
* **Critical Physical Limitations:**
  1. *Cutoff Rigidity:* The Himalayan arc is located at low geomagnetic latitudes with high vertical cutoff rigidity (~13–14 GV). Solar protons from ordinary solar energetic particle (SEP) events cannot penetrate the Earth's magnetic field to reach tropospheric altitudes in this region.
  2. *Selection Bias:* Associating disaster dates with preceding solar flares without evaluating a non-event control group cannot establish statistical causality. Solar-terrestrial triggering remains an unverified hypothesis.

---

## 6. Comprehensive Comparative Matrix of the 15 Catastrophes (Audited)

The table below synthesizes the results of our **unified inverse open-channel hydraulics (Manning)**, **mass balance**, and **precipitation requirements** across all 15 events, generated directly from `config/hydraulic_assumptions.yaml`:

| Rank / ID | Event Name & Date | Peak Elev (m) | $Q_{\text{peak}}$ Manning ($\text{m}^3/\text{s}$) | Total Bulk ($10^6\text{ m}^3$) | Net Liquid ($10^6\text{ m}^3$) | Lake Vol ($10^6\text{ m}^3$) | Net Runoff Req ($10^6\text{ m}^3$) | Required Rain $P_{\text{req}}$ (mm) | Measured Rain (mm) | Deficit Multiplier / Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Kedarnath (2013) | 6,940 | **2,539.2** | 7.20 | 4.68 | 0.38 | **3.94** | 110.4 | 325.0 (AWS) | **0.34x (SEM DÉFICIT — Folga de 2.94x)** |
| **2** | Chamoli (2021) | 7,816 | **8,635.5** | 26.90 | 15.60 | 0.00 | **15.60** | 298.9 | 0.0 (Winter) | **NOT APPLICABLE (Solid rock-ice avalanche)** |
| **3** | Himalaia (2026) | 7,234 | **3,376.1** | 20.70 | 14.20 | 7.54 | **4.07** | 87.0 | null | **[DADO INDISPONÍVEL — Requer dados reais]** |
| **4** | Aru (2016) | 6,200 | **10,240.0** | 68.00 | 54.40 | 0.00 | **54.40** | 818.0 | 5.0 | **NOT APPLICABLE (Cold glacier collapse)** |
| **5** | Seti (2012) | 7,525 | **8,879.0** | 32.00 | 17.60 | 0.00 | **17.60** | 287.6 | 0.0 | **NOT APPLICABLE (Rock-ice avalanche)** |
| **6** | South Lhonak (2023) | 6,710 | **5,960.0** | 28.00 | 19.60 | 14.50 | **5.10** | 72.4 | 18.0 | **4.02x (Déficit aparente vs pluviômetro local)** |
| **7** | Leh (2010) | 5,600 | **1,940.0** | 3.80 | 2.36 | 0.00 | **2.36** | 84.1 | 12.0 | **7.01x (Déficit aparente vs pluviômetro do vale)** |
| **8** | Melamchi (2021) | 5,800 | **3,391.0** | 12.50 | 8.00 | 0.00 | **8.00** | 157.4 | 28.0 | **5.62x (Déficit aparente vs pluviômetro de vale)** |
| **9** | Parechu (2000) | 5,200 | **13,767.0** | 45.00 | 32.40 | 25.00 | **7.40** | 47.0 | 8.0 | **5.87x (GLOF com contribuição de chuva)** |
| **10** | Zhangzangbo (1981) | 8,027 | **6,076.0** | 19.00 | 12.92 | 18.00 | **0.00** | 0.0 | 15.0 | **0.00x (SEM DÉFICIT — Lago cobriu 100% da água)** |
| **11** | Dig Tsho (1985) | 6,530 | **3,892.0** | 5.10 | 3.42 | 5.00 | **0.00** | 0.0 | 10.0 | **0.00x (SEM DÉFICIT — Lago cobriu 100% da água)** |
| **12** | Luggye Tsho (1994) | 7,204 | **7,844.0** | 21.00 | 15.54 | 17.00 | **0.00** | 0.0 | 16.0 | **0.00x (SEM DÉFICIT — Lago cobriu 100% da água)** |
| **13** | Bhotekoshi (2016) | 6,100 | **4,737.0** | 8.20 | 5.41 | 4.50 | **0.91** | 23.1 | 20.0 | **1.16x (Lago cobriu 83% do volume total)** |
| **14** | Himachal (2023) | 4,800 | **8,359.0** | 35.00 | 26.25 | 0.00 | **26.25** | 171.6 | 45.0 | **3.81x (Cheia regional monçônica multi-bacia)** |
| **15** | Parechu (2005) | 5,200 | **13,722.0** | 38.00 | 27.36 | 20.00 | **7.36** | 46.7 | 10.0 | **4.67x (GLOF recorrente de barramento natural)** |

---

## 7. Conventional Geotechnical Processes & Geomorphic Context

To maintain scientific objectivity, we evaluate the conventional mechanisms documented in published literature:
1. **Classical Moraine Dam Breaches (Canonical GLOFs):** In events like Zhangzangbo 1981, Dig Tsho 1985, and Luggye Tsho 1994, moraine dam failure through progressive trenching completely accounts for the flood volume ($V_{\text{lake}} \ge V_{\text{flood}}$) without requiring extreme precipitation.
2. **Rock-Ice Avalanches & Frictional Liquefaction:** In Chamoli 2021 and Seti 2012, massive rock-ice collapses mobilize without pre-existing lakes or rain. Frictional heat dissipation melts entrained glacier ice into slurry.
3. **Monsoon Cloudbursts & Orographic Convection:** In Kedarnath 2013 and Himachal 2023, extreme orographic monsoon precipitation is the verified driver. In Kedarnath, direct rain gauge data (325 mm) demonstrates that rainfall runoff fully supplied the water volume.

---

## 8. Evidentiary Categorization of Events Following Independent Audit

* **Category A: Rainfall-Driven Floods with Documented Precipitation:**
  * **Kedarnath 2013:** 325 mm rainfall directly measured in-situ; no water deficit exists.
  * **Himachal 2023:** Regional multi-day monsoon downpours across Himachal Pradesh.
* **Category B: Solid Mass Collapses (Avalanches & Glacier Surges):**
  * **Chamoli 2021:** 27M m³ rock-ice avalanche with frictional melt; rainfall models inapplicable.
  * **Aru 2016:** Twin cold glacier surges and collapses in western Tibet.
  * **Seti 2012:** 32M m³ rock-ice fall from Annapurna IV into gorge.
* **Category C: Canonical Glacial Lake Outburst Floods (GLOFs):**
  * **Zhangzangbo 1981, Dig Tsho 1985, Luggye Tsho 1994, South Lhonak 2023, Parechu 2000/2005, Bhotekoshi 2016:** Dam breach accounts for the dominant portion or entirety of the liquid flood volume.
* **Category D: Multi-Hazard Event with Inconclusive Rainfall Data:**
  * **Langtang 2026:** Multi-stage collapse and temporary landslide dam breach. Net runoff required is ~4.07M m³ (requiring 73–87 mm over 55–65 km²). Due to absence of in-situ rain gauges or 2026 satellite granules in the repo, the deficit is classified as **inconclusive / data unavailable**.

---

## 9. Conclusion & Post-Audit Scientific Assessment

This unified physical audit demonstrates that:
1. **The claim of an unexplained 10x–20x water deficit across all Himalayan disasters does not withstand empirical scrutiny.** In Kedarnath, real rainfall records show no deficit. In Chamoli and Aru, events were solid mass avalanches where rain-deficit formulas are physically invalid. In 2026, rainfall remains unobserved.
2. **Solar-terrestrial electrodynamic triggering ($J_z$) is an exploratory hypothesis**, not an established finding. The values in this repository are derived from analytical GEC formulas, not raw magnetometer measurements. High geomagnetic cutoff rigidity (~13–14 GV) and the absence of a control group remain critical scientific obstacles.
3. High-resolution satellite imagery confirms prominent bedrock-stripping chutes in steep terrain, highlighting the need for coupled geotechnical-meteorological monitoring in high-mountain basins.
