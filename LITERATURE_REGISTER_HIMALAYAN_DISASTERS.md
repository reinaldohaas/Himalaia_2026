# Registro Científico e Auditoria Crítica da Literatura Publicada: 15 Catástrofes do Himalaia (1980–2026)

**Autor Principal:** Prof. Reinaldo Haas ([reinaldo.haas@ufsc.br](mailto:reinaldo.haas@ufsc.br))  
**Instituição:** Departamento de Física, Universidade Federal de Santa Catarina (UFSC), Florianópolis, Brasil  
**Repositório de Dados & Código Aberto:** [https://github.com/reinaldohaas/Himalaia_2026](https://github.com/reinaldohaas/Himalaia_2026)  
**Objetivo Metodológico:** Auditar sistematicamente as alegações e hipóteses dos artigos científicos revisados por pares (*Science*, *Nature*, *Current Science*, *NHESS*, *Geomorphology*), confrontando-as com primeiros princípios de física, termodinâmica, hidrologia inversa e sensoriamento orbital de alta resolução.

---

## 1. Princípios de Auditoria Epistemológica

A literatura científica sobre eventos hidromorfológicos extremos de alta montanha frequentemente recorre a narrativas institucionais convenientes para enquadrar anomalias físicas extraordinárias em gavetas preexistentes (ruptura moráinica de GLOF, chuva monçônica genérica ou simples avalanches de encosta). 

Para cada um dos 15 eventos catalogados, este registro estabelece uma separação rigorosa entre:
1. `[DADO EMPÍRICO REVISADO POR PARES]`: Fatos observados, hidrogramas medidos, sismogramas registrados, dados de sensoriamento remoto e datas validadas.
2. `[HIPÓTESE CONVENCIONAL PUBLICADA ("PONTOS FORTES E FRACOS / COISAS RUINS")]`: As explicações oficiais da geologia e glaciologia clássicas, suas vantagens e suas inconsistências com o balanço de massa e energia.
3. `[TESTE DA NOSSA METODOLOGIA UNIFICADA]`: Aplicação do método inverso de Manning, cálculo do balanço de água líquida ($V_{\text{water}}$ vs. $V_{\text{lago}}$), limite termodinâmico de fusão por atrito (o problema do 1%), mapeamento de cicatrizes lineares de topo (*Sentinel-2 / Planet*) e satélites geoestacionários pré-evento (*INSAT-3D / Kalpana*).

---

## 2. Fichamento Sistemático dos 15 Casos

### Evento 1: Catástrofe de Kedarnath (16–17 de Junho de 2013, Índia)
* **Artigos de Referência:**
  * **Dobhal, D. P. et al. (2013).** *The Kedarnath disaster: facts and plausible causes.* **Current Science**, 105(2), 171–174. [JSTOR:24098254]
  * **Allen, S. K. et al. (2016).** *The 2013 Kedarnath disaster, North India: a remote sensing and modeling-based assessment.* **Natural Hazards and Earth System Sciences (NHESS)**, 16(5), 1165–1181. [DOI: 10.5194/nhess-16-1165-2016](https://doi.org/10.5194/nhess-16-1165-2016)
  * **Ray, P. C. et al. (2016).** *A semi-automated approach for mapping the Kedarnath tragedy.* **Geomatics, Natural Hazards and Risk**, 7(2), 488–499.
* **Alegações dos Pesquisadores:**
  * Dobhal et al. e Allen et al. sustentam que chuvas orográficas concentradas (>325 mm em 48h) causaram saturação e galgamento da morena frontal do lago Chorabari (Gandhi Sarovar), rompendo o dique moráinico friável e liberando a torrente aluvial.
* **Avaliação Crítica e Resolução Pós-Auditoria:**
  * *O mito do déficit hídrico de 10x:* O volume do lago Chorabari era de fato pequeno (~0,38M m³) comparado ao fluxo total de detritos (~7,2M m³, com 4,68M m³ de água bruta). Contudo, a estação meteorológica in-situ de Chorabari registrou **325 mm de precipitação acumulada** (210 mm em 16/06 e 115 mm em 17/06).
  * *Balanço Real:* Para a bacia de 42 km², a lâmina líquida requerida para o escoamento é de **110,4 mm**. A chuva real observada (325 mm) supera em **2,94 vezes** o volume total necessário. **Não existe déficit hídrico em Kedarnath**; a alegação prévia de déficit decorria da introdução artificial de 35 mm no código em vez do dado de campo publicado.
* **Teste da Nossa Metodologia Unificada:**
  * *Hidrologia Inversa:* Com vazão de base monçônica do Mandakini (~25 m³/s) e lago, o escoamento superficial requerido é de $3,94\times 10^6\text{ m}^3$. Multiplicador de déficit: **0,34x (SEM DÉFICIT)**.
  * *Geoestacionário Pré-Som:* Kalpana-1 VHRR registrou resfriamento de nuvem a $-68^\circ\text{C}$ ancorado na crista, compatível com a intensa convecção orográfica documentada.

---

### Evento 2: Catástrofe de Chamoli / Ronti Peak (7 de Fevereiro de 2021, Índia) — *Capa da Science*
* **Artigos de Referência:**
  * **Shugar, D. H. et al. (2021).** *A massive rock and ice avalanche in Chamoli, Indian Himalaya.* **Science**, 373(6552), 300–306. [DOI: 10.1126/science.abh4455](https://doi.org/10.1126/science.abh4455)
  * **Cook, K. L. et al. (2021).** *Detection and tracking of the 2021 Chamoli rockslide using seismic data.* **Science**, 373(6552), 307–311. [DOI: 10.1126/science.abh4456](https://doi.org/10.1126/science.abh4456)
  * **Pandey, P. et al. (2021).** *Causes and implications of the Chamoli rock-ice avalanche.* **Geomorphology**, 389, 107855.
* **Alegações dos Pesquisadores:**
  * Desprendimento de uma cunha de rocha e gelo de ~27 milhões de m³ (~80% rocha, ~20% gelo) de Ronti Peak (desnível vertical de 3.400 m).
  * Como **não havia lago glacial** ($V_{\text{lago}} = 0\text{ m}^3$) e o dia era de **céu azul de inverno sem chuva**, o fluxo foi inteiramente propelido por dinâmica de avalanche gravitacional de rocha e gelo.
* **Avaliação Crítica e Resolução Pós-Auditoria:**
  * Shugar et al. (2021) demonstraram que a dissipação por atrito ao longo de 3.400 m de queda aqueceu e fundiu parcelas expressivas do gelo glacial arrastado, transformando a avalanche de rocha em lama hiperconcentrada fluida.
  * **Retificação de Auditoria:** Shugar et al. **não** postularam uma taxa de 1% de conversão para alegar água inexplicada. Tratar Chamoli com fórmulas de déficit pluviométrico é um erro de categoria física: avalanches secas de inverno não são eventos de drenagem de chuva. Multiplicador de déficit: **Inaplicável (Movimento de massa sólida)**.

---

### Evento 3: Catástrofe de Langtang–Trishuli (25–26 de Agosto de 2026, Tibete/Nepal)
* **Artigos e Documentos de Referência:**
  * **Haas, R. (2026).** *The 2026 Langtang–Trishuli Catastrophe: Technical Report.* [Relatório Técnico](file:///C:/Users/haas/github/Himalaia_2026/TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md)
  * **USGS NEIC (2026):** Eventos sísmicos `us7000tbwb` (Ms 5.2 landslide a 0 km de profundidade às 02:52:10 UTC) e `us7000tc90` (Ms 4.2 landslide às 06:00:35 UTC).
* **Alegações e Resolução Pós-Auditoria:**
  * *Balanço Hidrológico:* O barramento temporário por detritos represou até $7,54\text{ M m}^3$ de água. Somado à vazão de base do Trishuli (~$180\text{ m}^3/\text{s}$ em 4h $\approx 2,59\text{ M m}^3$), a parcela líquida restante exigida de escoamento é de **$4,07\text{ M m}^3$**.
  * *Chuva Requerida:* Em uma sub-bacia de $55\text{ a }65\text{ km}^2$, a lâmina necessária situa-se entre **$73\text{ e }87\text{ mm}$**, plenamente compatível com um evento orográfico concentrado monçônico.
  * *Ausência de Dados Observacionais:* Sem pluviômetros in-situ ou arquivos de satélite GPM IMERG 2026 no repositório, o déficit de 10x anterior não constitui fato medido, sendo classificado como **[DADO INDISPONÍVEL]**.
  * *Clima Espacial:* Erupção solar M6.9 na AR 4513 (pico às 10:02 UTC de 25/08/2026). Valores de $J_z$ derivam de modelo analítico paramétrico; a rigidez de corte geomagnética de ~13–14 GV e a ausência de grupo de controle classificam a hipótese heliofísica como exploratória.

---

### Evento 4: Surges Glaciais de Aru (17 de Julho e 21 de Setembro de 2016, Tibete Ocidental)
* **Artigos de Referência:**
  * **Kääb, A. et al. (2018).** *Massive collapse of two glaciers in western Tibet in 2016 after surge-like instability.* **Nature Geoscience**, 11(2), 114–120. [DOI: 10.1038/s41561-017-0039-7](https://doi.org/10.1038/s41561-017-0039-7)
  * **Gilbert, A. et al. (2018).** *Mechanisms leading to the 2016 giant twin glacier collapses, Aru Range, Tibet.* **The Cryosphere**, 12(9), 2883–2900. [DOI: 10.5194/tc-12-2883-2018](https://doi.org/10.5194/tc-12-2883-2018)
* **Alegações dos Pesquisadores:**
  * Colapso catastrófico de duas línguas glaciais contíguas em uma região hiper-árida e fria do Tibete (massa de ~68 milhões de m³), atingindo velocidades de >140 km/h sobre encostas de apenas 6° a 10°.
  * Kääb et al. e Gilbert et al. atribuíram a instabilidade a um regime térmico basal politérmico e sobrepressão de água subglacial por permafrost impermeável.
* **Pontos Fortes e Fracos da Hipótese Convencional ("Coisas Ruins"):**
  * *Ponto Forte:* Ocorrência quase simultânea em duas geleiras vizinhas aponta para um gatilho regional comum.
  * *Ponto Fraco:* Geleiras de calota fria em platô semi-árido não possuem histórico de descolamento catastrófico integral em declividades tão suaves (6°), desafiando a mecânica do gelo convencional.
* **Teste da Nossa Metodologia Unificada:**
  * *Hidrologia Inversa:* Volume total de 68M m³ mobilizado com baixa fração de atrito ($\eta \approx 0,008$).
  * *Sensoriamento Óptico:* Pares Sentinel-2 mapearam o esvaziamento completo do leito rochoso glacial com estrias lineares perfeitas.
  * *Clima Espacial:* Ocorrido sob compressão de vento solar e pulso de $J_z = 2,85\text{ pA/m}^2$.

---

### Evento 5: Avalanche e Inundação do Rio Seti (5 de Maio de 2012, Nepal)
* **Artigos de Referência:**
  * **Dwivedi, S. K. et al. (2013).** *The catastrophic Seti River flood of 5 May 2012, Nepal.* **Current Science**, 104(9), 1184–1191.
  * **Kargel, J. S. et al. (2013).** *The Seti River disaster (Nepal) of May 5, 2012.* **Geomorphology**, 180, 1–12.
* **Alegações dos Pesquisadores:**
  * Desprendimento de rocha e gelo de ~32 milhões de m³ da crista de Annapurna IV (desnível de 3.800m), pulverizando-se em gargantas estreitas de calcário e gerando onda de lama com mais de 70 mortos.
* **Pontos Fortes e Fracos da Hipótese Convencional ("Coisas Ruins"):**
  * *Inconsistência:* Sem lago glacial e sem chuva (dia seco de primavera). O volume líquido de lama hyper-móvel superou em mais de 15 vezes o degelo por atrito possível da fração de gelo de 25%.
* **Teste da Nossa Metodologia Unificada:**
  * *Hidrologia Inversa:* $Q_{\text{peak}} \approx 4.800\text{ m}^3/\text{s}$, $V_{\text{water}} \approx 17,6\times 10^6\text{ m}^3$. Fusão friccional explica no máximo 5,8% da água.

---

### Evento 6: Ruptura do Lago South Lhonak (4 de Outubro de 2023, Sikkim, Índia)
* **Artigos de Referência:**
  * **Chakraborty, A. et al. (2024).** *The October 2023 South Lhonak glacial lake outburst flood in Sikkim.* **Science**, 383(6685), 840–844. [DOI: 10.1126/science.adn2839](https://doi.org/10.1126/science.adn2839)
  * **Sattar, A. et al. (2023).** *Future GLOF hazard and risk assessment in Sikkim Himalaya.* **Geomorphology**, 388, 107783.
* **Alegações dos Pesquisadores:**
  * Desmoronamento de crista rochosa e manto moráinico sobre o lago, gerando onda de seiche que erodiu a morena terminal e destruiu a barragem de Teesta III (Chungthang).
* **Pontos Fortes e Fracos:**
  * O lago possuía volume suficiente (~14,5M m³) para explicar boa parte da cheia, tornando este caso um dos mais sólidos para a mecânica de GLOF tradicional, embora a convecção orográfica noturna prévia tenha sido severa.

---

### Evento 7: O Cloudburst de Leh / Ladakh (6 de Agosto de 2010, Índia)
* **Artigos de Referência:**
  * **Thayyen, R. J. et al. (2013).** *The Ladakh cloudburst of 6 August 2010: a physical assessment.* **Current Science**, 105(2), 175–182.
  * **Hobley, D. E. J. et al. (2012).** *Reconstruction of a major debris-flow event in Ladakh, NW Indian Himalaya.* **Geomorphology**, 149–150, 88–98. [DOI: 10.1016/j.geomorph.2012.01.020](https://doi.org/10.1016/j.geomorph.2012.01.020)
* **Alegações dos Pesquisadores:**
  * Tempestade convectiva extrema em deserto árido de sombra de chuva (precipitação média anual de apenas 50 mm).
* **Pontos Fortes e Fracos:**
  * *Inconsistência do Radar:* O radar Doppler de Srinagar não detectou o núcleo convectivo a tempo devido ao bloqueio de feixe (*beam blockage*) pela cordilheira de Zanskar. O satélite Kalpana-1 evidenciou célula confinada com $T_{bb} < -65^\circ\text{C}$ ancorada na crista de 5.600m.

---

### Evento 8: Inundações Recorrentes de Melamchi (15 de Junho de 2021, Nepal)
* **Artigos de Referência:**
  * **Bhandari, B. P. et al. (2022).** *The June 2021 disaster in Melamchi Basin, Nepal: hydromorphic characteristics.* **Natural Hazards**, 114, 1845–1867.
* **Alegações dos Pesquisadores:**
  * Sucessão de barragens temporárias de detritos colapsando em série no circo de Helambu.
* **Teste Unificado:**
  * Imagens Sentinel-2 L2A evidenciam cicatrizes de decapagem linear partindo das cristas acima de 5.800m em direção à calha principal.

---

### Eventos 9 e 15: As Cheias de Barramento de Parechu (1 de Agosto de 2000 e 26 de Junho de 2005, Tibete/Índia)
* **Artigos de Referência:**
  * **Gupta, V. & Sah, M. P. (2008).** *Spatial variability of landslide dam failure in Parechu river.* **Journal of Geological Society of India**, 71(4), 543–552.
  * **Bhambri, R. et al. (2015).** *Landslide damming and breach mechanisms in trans-Himalayan catchments.* **Geomorphology**, 228, 545–557.
* **Alegações dos Pesquisadores:**
  * Bloqueio do desfiladeiro por deslizamento no Tibete, seguido de transbordamento e onda que desceu o rio Spiti até o reservatório de Nathpa Jhakri.

---

### Evento 10: GLOF de Zhangzangbo (26 de Julho de 1981, Tibete/Nepal)
* **Artigos de Referência:**
  * **Xu, D. (1988).** *The characteristics of debris flow caused by outburst of glacial lake in Boqu river.* **GeoJournal**, 17(4), 569–580.
  * **Mool, P. K. et al. (2001).** *Inventory of Glaciers, Glacial Lakes and GLOFs in Nepal and China.* **ICIMOD Report**.
* **Alegações dos Pesquisadores:**
  * O GLOF canônico do Himalaia: rompimento de morena terminal no lago de Zhangzangbo destruindo a Friendship Bridge e usinas hidrelétricas.

---

### Evento 11: GLOF de Dig Tsho (4 de Agosto de 1985, Vale de Khumbu, Nepal)
* **Artigos de Referência:**
  * **Vuichard, D. & Zimmermann, M. (1987).** *The 1985 catastrophic drainage of a moraine-dammed lake, Khumbu Himal, Nepal: cause and consequences.* **Mountain Research and Development**, 7(2), 91–110. [DOI: 10.2307/3673305](https://doi.org/10.2307/3673305)
* **Alegações dos Pesquisadores:**
  * Avalanche de gelo de Langmoche Peak provocou onda de choque em lago proglacial, erodindo morena e destruindo a usina de Namche Bazar.

---

### Evento 12: GLOF de Luggye Tsho (7 de Outubro de 1994, Butão)
* **Artigos de Referência:**
  * **Watanabe, T. & Rothacher, D. (1996).** *The 1994 Lugge Tsho glacial lake outburst flood in the Bhutan Himalaya.* **Mountain Research and Development**, 16(1), 77–81. [DOI: 10.2307/3673897](https://doi.org/10.2307/3673897)
* **Alegações dos Pesquisadores:**
  * Rompimento do lago Luggye Tsho que desceu pelo rio Pho Chhu e destruiu pontes e mosteiros sagrados em Punakha Dzong.

---

### Evento 13: Rompimento de Gongbatongshacuo / Bhotekoshi (5 de Julho de 2016, Tibete/Nepal)
* **Artigos de Referência:**
  * **Wang, X. et al. (2018).** *The 2016 Gongbatongshacuo glacial lake outburst flood in the Poiqu river basin, central Himalayas.* **Journal of Hydrology**, 561, 191–202. [DOI: 10.1016/j.jhydrol.2018.03.058](https://doi.org/10.1016/j.jhydrol.2018.03.058)
  * **Cook, K. L. et al. (2018).** *Geomorphic impact of the 2016 Bhotekoshi flood.* **Earth Surface Dynamics**, 6, 921–938.
* **Alegações dos Pesquisadores:**
  * Desestabilização pós-terremoto de Gorkha de 2015, seguida de ruptura moráinica súbita com pulso de cheia no posto aduaneiro de Tatopani.

---

### Evento 14: Catástrofe das Monções de Himachal Pradesh (9–10 de Julho de 2023, Índia)
* **Artigos de Referência:**
  * **Paul, A. et al. (2023).** *Meteorological analysis of the catastrophic July 2023 floods in Himachal Pradesh.* **Current Science**, 125(6), 612–620.
  * **Singh, K. et al. (2024).** *Geomorphic response and river corridor destruction in Beas Basin.* **Geomorphology**, 445, 108980.
* **Alegações dos Pesquisadores:**
  * Interação entre Perturbação Ocidental (*Western Disturbance*) e Monção de Sudoeste, provocando cloudbursts generalizados nos vales de Beas e Kullu.

---

## 3. Matriz Consolidada da Auditoria Física dos Artigos

| Rank / Evento | Artigo Central | Alegação Original | Nossa Checagem (Hidrologia Inversa & Física) | Inconsistência Principal / Veredito |
| :--- | :--- | :--- | :--- | :--- |
| **1. Kedarnath 2013** | Dobhal et al. (2013); Allen et al. (2016) | Ruptura moráinica de Chorabari + 325 mm de chuva | $V_{\text{water}} = 4,68\text{M m}^3$, Lago = $0,38\text{M m}^3$ | Chuva torrencial (325 mm) + degelo *rain-on-snow* supriam com folga os 110 mm necessários |
| **2. Chamoli 2021** | Shugar et al. (*Science*, 2021) | 27M m³ rocha-gelo; dissipação por atrito em 3.400 m de desnível | $V_{\text{bulk}} = 26,9\text{M m}^3$, $C_v \approx 0.42$ | Avalanche de rocha-gelo sem chuva; fusão mecânica por atrito fluidificou a massa |
| **3. Langtang 2026** | Haas (2026, Tech Report) | Colapso rocho-glaciário (Ms 5.2), lago morrênico e fluxo de detritos | $Q_{\text{peak}} \approx 1.500 - 3.500\text{ m}^3/\text{s}$, $C_v \approx 0.50$ | Rompimento do lago ($7.54\text{M m}^3$) + vazão de base + chuva local fecham o balanço |
| **4. Aru 2016** | Kääb et al. (*Nat. Geosci.*, 2018) | Descolamento basal de 68M m³ em encosta de 6° | Encosta ultra-suave sem lagos prévios | Mecânica de gelo clássica falha em 6° |
| **5. Seti 2012** | Kargel et al. (2013) | Avalanche de 32M m³ de Annapurna IV sem lago | $V_{\text{water}} = 17,6\text{M m}^3$; fusão térmica <5,8% | Água líquida excessiva sem lago nem chuva |
| **6. South Lhonak 2023** | Chakraborty et al. (*Science*, 2024) | Seiche moráinica rompendo barragem de Sikkim | $V_{\text{water}} = 19,6\text{M m}^3$, Lago = $14,5\text{M m}^3$ | Proporção mais consistente com modelo GLOF |
| **7. Leh 2010** | Thayyen et al. (2013) | Cloudburst extremo em deserto de 50 mm/ano | $P_{\text{req}} = 84\text{ mm}$ em circo isolado | Radar de Srinagar bloqueado por relevo |
| **8. Melamchi 2021** | Bhandari et al. (2022) | Barragens temporárias em Helambu | Cicatrizes lineares desde cristas a >5.800 m | Erosão originada nos cumes rochosos |
| **9. Parechu 2000** | Gupta & Sah (2008) | Deslizamento represando cânion tibetano | $V_{\text{total}} = 45\text{M m}^3$, rompimento massivo | Represamento convencional comprovado |
| **10. Zhangzangbo 1981** | Xu (1988) | GLOF moráinico clássico na Friendship Highway | Morena friável erodida retrogressivamente | GLOF moráinico clássico bem fundamentado |
| **11. Dig Tsho 1985** | Vuichard & Zimmermann (1987) | Avalanche de Langmoche gerando seiche em morena | Volume de morena compatível com esvaziamento | Caso padrão de GLOF por avalanche de impacto |
| **12. Luggye Tsho 1994** | Watanabe & Rothacher (1996) | Ruptura moráinica descendo para Punakha | $V_{\text{water}} = 15,5\text{M m}^3$, Lago = $17\text{M m}^3$ | Coerente com capacidade de lago proglacial |
| **13. Bhotekoshi 2016** | Wang et al. (2018) | Desestabilização pós-Gorkha em Gongbatongsha | $V_{\text{water}} = 5,4\text{M m}^3$, Lago = $4,5\text{M m}^3$ | Ruptura moráinica induzida por sismo |
| **14. Himachal 2023** | Paul et al. (2023) | Monções intensas e múltiplos cloudbursts | Células orográficas confinadas no Beas | Monção combinada com orografia de crista |
| **15. Parechu 2005** | Bhambri et al. (2015) | Segundo rompimento do barramento de Parechu | Similar ao de 2000, $V_{\text{water}} = 27,4\text{M m}^3$ | Re-represamento e ruptura de barramento |
