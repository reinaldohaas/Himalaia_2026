# Fontes Oficiais, Dados Brutos e Referências Científicas
### Mapeamento Completo de Fontes de Dados, Literatura com Peer-Review e Instituições de Monitoramento (Sem Dados Inventados)

---

## 1. Dados Brutos e Repositórios Governamentais Abertos (Utilizados no Projeto)

| Categoria de Dado | Instituição / Provedor Oficial | Identificador / URL Oficial | Formato / Status no Repositório |
| :--- | :--- | :--- | :--- |
| **Raios X Solares (GOES-18)** | **NOAA SWPC** *(Space Weather Prediction Center)* | `https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json` | **JSON Real Bruto (4,48 MB / 20.148 registros)** em `data/raw/space_weather/goes_xrays_7day_real.json` |
| **Prótons Solares Energéticos** | **NOAA SWPC / SEISS** | `https://services.swpc.noaa.gov/json/goes/primary/integral-protons-7-day.json` | **JSON Real Bruto (1,65 MB)** em `data/raw/space_weather/goes_integral_protons_real.json` |
| **Índice Geomagnético $Kp$** | **NOAA SWPC** | `https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json` | **JSON Real Bruto** em `data/raw/space_weather/noaa_planetary_k_index_real.json` |
| **Precipitação de Satélite (GPM IMERG V07)** | **NASA GES DISC / CMR** *(Goddard Space Flight Center)* | Collection `GPM_3IMERGHH_07` / `https://cmr.earthdata.nasa.gov/` | **Catálogo de Granules Real + Amostra HDF5 (8,07 MB)** baixados via Bearer Token em `data/raw/meteorology/` |
| **Censo de Danos das 33 Pontes** | **UN OCHA / ICIMOD / HDX** *(Humanitarian Data Exchange)* | Dataset: `https://data.humdata.org/dataset/hot_flood_npl` | **GeoJSON Real** em `data/hot_flood_npl_bridges_damage_icimod.geojson` |
| **Vetor do Talvegue Fluvial (2.979 nós)** | **OpenStreetMap (OSM) / Overpass Turbo** | Relação OSM `21284197` (Bhote Koshi) e `4839538` (Trishuli) | **GeoJSON Real** em `data/rio_trishuli_thalweg_oficial_osm.geojson` |
| **Catálogo Sísmico (Evento 4.4 mb)** | **USGS** *(United States Geological Survey)* | `https://earthquake.usgs.gov/fdsnws/event/1/` | Coordenadas e magnitude registradas no Himalaia. |
| **Rede Mundial de Magnetômetros** | **INTERMAGNET** *(International Real-time Magnetic Observatory Network)* | Observatórios `LZA` (Lhasa) e `SAB` (Sabhawala) / `https://intermagnet.org/` | Parâmetros de calibração magnética em 1 Hz e 1 min. |

---

## 2. Referências Científicas com Revisão por Pares (Peer-Reviewed Literature)

### A. Dinâmica de Avalanches Glaciais e Rupturas de Lagos (GLOFs) no Himalaia:
1. **Shugar, D. H. et al. (2021)**. *A huge rock and ice avalanche caused the 2021 Chamoli disaster, Uttarakhand, India*. **Science**, 373(6552), 300-306.  
   * **DOI:** [10.1126/science.abg6027](https://doi.org/10.1126/science.abg6027)  
   * *Contribuição:* Demonstração física da conversão de energia potencial em calor por atrito, dinâmica de avalanches de rocha/gelo no Himalaia e assinatura acústica/infrassônica de colapsos maciços.
2. **Huggel, C. et al. (2002)**. *Assessment of glacial hazards in high mountain regions: an approach using remote sensing and GIS*. **Natural Hazards and Earth System Sciences**, 2(3/4), 147-159.  
   * **DOI:** [10.5194/nhess-2-147-2002](https://doi.org/10.5194/nhess-2-147-2002)  
   * *Contribuição:* Relações empíricas para cálculo de volume e área de lagos proglaciais em depressões de circo.
3. **Cook, K. L. et al. (2018)**. *Glacial lake outburst floods as drivers of fluvial erosion in the Himalaya*. **Science**, 362(6410), 53-57.  
   * **DOI:** [10.1126/science.aat4981](https://doi.org/10.1126/science.aat4981)

---

### B. Circuito Elétrico Global ($J_z$), Eletrodinâmica Ionosférica e Física de Nuvens:
4. **Tinsley, B. A. (2008)**. *The global atmospheric electric circuit and its effects on cloud microphysics*. **Reports on Progress in Physics**, 71(6), 066801.  
   * **DOI:** [10.1088/0034-4885/71/6/066801](https://doi.org/10.1088/0034-4885/71/6/066801)  
   * *Contribuição:* Modelo de eletro-coalescência de gotículas e modulação de taxas de condensação e precipitação em nuvens por variações de $J_z$.
5. **Harrison, R. G. & Carslaw, K. S. (2003)**. *Ion-aerosol-cloud processes in the lower atmosphere*. **Reviews of Geophysics**, 41(3), 1012.  
   * **DOI:** [10.1029/2002RG000114](https://doi.org/10.1029/2002RG000114)  
   * *Contribuição:* Fundamentação quantitativa da condutividade atmosférica e deposição de carga em bordas de nuvens.
6. **Rycroft, M. J., Israelsson, S., & Price, C. (2000)**. *The global atmospheric electric circuit, solar activity and climate change*. **Journal of Atmospheric and Solar-Terrestrial Physics**, 62(17-18), 1563-1576.  
   * **DOI:** [10.1016/S1364-6826(00)00112-7](https://doi.org/10.1016/S1364-6826(00)00112-7)  
   * *Contribuição:* Equações de resistência colunar ($R_c$) e acoplamento solar-ionosfera-troposfera.

---

### C. Redes de Detecção de Raios, Descargas e Efeitos Eletrostáticos:
7. **Dowden, R. L., Brundell, J. B., & Rodger, C. J. (2002)**. *VLF lightning location by time of group arrival (TOGA) at multiple sites*. **Journal of Atmospheric and Solar-Terrestrial Physics**, 64(7), 817-830.  
   * *Rede:* WWLLN *(World Wide Lightning Location Network)* - [https://wwlln.net/](https://wwlln.net/)
8. **Freund, F. (2003)**. *Rocks that crackle and glow: bizarre pre-earthquake phenomena*. **Journal of Scientific Exploration**, 17(1), 37-71.  
   * *Contribuição:* Física da emissão de luz por fratura de rochas (triboluminescência) e cargas elétricas piezoelétricas em granito/permafrost sob compressão cataclísmica.

---

### D. Relatórios Técnicos Oficiais de Infraestrutura e Hidrelétricas:
9. **Nepal Electricity Authority (NEA)**. *Annual Operations Report & Upper Trishuli Hydroelectric Projects Transmission Line Summary*. Katmandu, Nepal. [https://www.nea.org.np/](https://www.nea.org.np/)
10. **Department of Hydrology and Meteorology (DHM Nepal)**. *Flood Early Warning Systems and River Gauge Stations in Narayani & Trishuli Basins*. [https://hydrology.gov.np/](https://hydrology.gov.np/)

---

## 3. Transparência Epistemológica: O que é Dado Real vs. Modelo Dedutivo

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        CLASSIFICAÇÃO RIGOROSA DOS DADOS                         │
├────────────────────────────────┬────────────────────────────────────────────────┤
│ DADO PRIMÁRIO REAL (100% AUDITADO) │ FÓRMULA / MODELO DEDUTIVO (FÍSICA TEÓRICA)   │
├────────────────────────────────┼────────────────────────────────────────────────┤
│ • 20.148 registros GOES-18 SWPC │ • Curva de Jz = VI / Rc (Resistência de 4.000m)│
│ • Censo de 33 pontes (ICIMOD)   │ • Inversão Hidrológica Q = V / Δt (2570 s)    │
│ • 2.979 nós do rio no OSM       │ • Condutividade de Cowling Ey = ΔEEJ / 85.0    │
│ • Catálogo de Granules GPM V07 │ • Termodinâmica Rain-on-Snow (+16% degelo)     │
│ • Posições geodésicas de 8 UHEs │ • Relação Infrassônica Shugar et al. (2021)    │
└────────────────────────────────┴────────────────────────────────────────────────┘
```
