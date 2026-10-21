# Linha do tempo do evento de 25–26/08/2026 (Lhende Khola / Kyirong–Rasuwa), com fonte e fuso de cada horário

**Data:** 21 de outubro de 2026
**Fusos:** NPT = UTC+5:45 (Nepal). BJT = UTC+8 (hora de Pequim, oficial em toda a China, inclusive no Tibete). BJT − NPT = 2h15. Todos os horários da tabela estão em **UTC**. A coluna "como escrito" mantém o horário e o fuso da fonte.
**Confiança:**
* **A:** registro instrumental ou fonte oficial primária.
* **M:** fonte secundária confiável.
* **B:** fonte única, vaga ou contraditada.

**Como foi feito:**
* duas buscas na web (notícias e boletins oficiais em inglês, chinês e nepali; catálogos sísmicos consultados direto nas APIs);
* as análises do Himawari deste repositório.

Os textos `levantamento_relatos_som_descargas_eletricas.md` e `relatorio_avalanche_inundacao_nepal_tibete.md` **não foram usados como fonte**: os horários deles não têm origem verificável.

---

## 1. Linha do tempo

| UTC | Como escrito (fuso) | Onde | O quê | Fonte | Conf. |
| :--- | :--- | :--- | :--- | :--- | :---: |
| fim de 2025 → ago/2026 | — | geleira suspensa acima da zona de ruptura | Velocidade sobe de ~7,4 para ~55 m/ano (aceleração precursora) | Wang et al., *Landslides*, via Petley, [Landslide Blog](https://eos.org/thelandslideblog/nepal-landslide-precursory-behaviour) | M |
| 2 semanas antes | — | região da fonte | "Mais de 60 eventos sísmicos menores" nas duas semanas anteriores | [GEO3BCN-CSIC](https://www.geo3bcn.csic.es/news-and-media/news/reconstruyen-con-datos-sismologicos-como-se-produjo-la-riada-mortal-en-el-himalaya/) (Adhikari et al. 2026) | M |
| 25/08 07:15–08:15 | "25 Aug 13:00–14:00" (NPT) | "perto de Deding", ~5.000 m | Massa se desprende e barra o Bhote Koshi; água represada "~18–19 h" | IRDR, via [ADRC](https://www.adrc.asia/publications/disaster_report/pdf/2026/ADRC_FL_NPL_Rasuwa_20260826_EN.pdf) | B: contradito pelo sismo de 26/08 e pela falta de evento em 25/08 |
| 25/08 09:00–13:00 | — | planalto, perto de Lhasa | Sistema convectivo de mesoescala, 100–146 mil km² abaixo de 213 K | Himawari-9 (este repositório, `trajetoria.txt`) | A |
| 25/08 15:25 | "9:10pm" (NPT) | Phalakhu Khola, Betrawati | Afluente passa do nível de alerta (chuva local, fora da fonte) | [Nepali Times, 31/08](https://nepalitimes.com/nepal-disaster-was-a-warning-to-fix-its-early-warning-system) | M |
| 25/08 17:30 → 26/08 00:30 | — | **sobre o sítio** (paralaxe invertida) | Nuvem com topo de 218–235 K (10–13 km), fase de gelo, ~7 h | Himawari-9, `GEOESTACIONARIO_NOITE_25_26AGO2026.md` § 6 | A |
| 26/08 00:30 → 01:30 | — | **sobre o sítio** | **Topo da nuvem desce de ~10 km ao terreno** (234 → 261 → 273 K) | idem | A |
| 02:15 | "8:00am" (NPT) | DHM | Boletim rotineiro de previsão de cheia (não é precursor) | Nepali Times, 31/08 | M |
| 02:30 | "8月26日10时30分许", sem fuso (Reuters: "10:30 AM (0230 GMT)") | Porto de Kyirong | Primeiro horário oficial chinês do fluxo | [Xinhua](https://www.news.cn/20260826/ae1b8e34e4c94c2cbe342f62367644ee/c.html), [MEM](https://www.mem.gov.cn/xw/yjglbgzdt/202608/t20260826_708718.shtml) | A como declaração; B como horário físico (22 min antes do sismo) |
| horas antes | — | perto da fonte | "Vários eventos nas horas anteriores com formas de onda semelhantes às do ML 2,5" (detecção por modelo de forma de onda; horários a publicar em outro estudo) | Adhikari et al. 2026 | M |
| **02:35:12** | "17 min 4 s before the mass movement" (origem 02:52:16 UTC); "8:20 am" (NPT, The Week) | **~28,21 N / 85,58 E** (lido na Fig. 2 do artigo), **~9,7 km a SSE da cicatriz**; profundidade ~9 km (mal resolvida) | **Evento sísmico precursor ML 2,5**, localizado com P e S pela rede NEMRC. Os autores julgam origem tectônica "menos provável" do que um "slide-quake" raso ligado ao movimento gravitacional. | [Adhikari et al. 2026, *Seismica* 5(2)](https://doi.org/10.26443/seismica.v5i2.3433), § 3.1; [The Week, 27/08](https://www.theweek.in/news/world/2026/08/27/tragic-10-hours-inside-the-timeline-of-the-cross-border-flood-that-hit-nepal.html) ("M2,6") | A |
| 02:50 | "8:35 am" (NPT) | Porto de Kyirong | Última travessia no sistema de imigração do Nepal | BBC, 01/09 (via en.wikipedia) | M |
| 02:50 | — | sítio | Nenhum topo de nuvem que se distinga da montanha a até 30 km | Himawari-9, § 6 | A |
| **02:52:10–02:52:23** | USGS 02:52:10Z; "北京时间10时52分12秒" (BJT); CENC 10:52:20 (BJT); GFZ 02:52:23Z | flanco norte entre o Langtang Lirung e o Tsangbu Ri | **Ruptura principal**, sinal de "deslizamento" (Ms 5,2 USGS; M 5,1 CENC; Mw 5,7 GFZ). O sinal dura ~18,5 min; fase da avalanche ~88 s. | [USGS us7000tbwb](https://earthquake.usgs.gov/earthquakes/eventpage/us7000tbwb); CENC; [GFZ](https://geofon.gfz.de/eqinfo/event.php?id=gfz2026qrfy); SKLGP/CDUT via [The Paper](https://www.thepaper.cn/newsDetail_forward_33972765); Chen Ningsheng via [QQ](https://news.qq.com/rain/a/20260914A0BW4500) | A |
| 02:52:16 | — | chegada P de alta frequência | Melhor início da onda P (resíduos USGS mediana +6,45 s; retroprojeção de período longo) | USGS QuakeML; Adhikari et al. | A |
| 02:55 | "8:40am" (NPT) | Syabrubesi | Última leitura do limnímetro: 1,62 m | [Kathmandu Post, 27/08](https://kathmandupost.com/national/2026/08/27/how-the-bhotekoshi-flood-unfolded-over-10-hours); NDRRMA | A |
| 02:59 | "10时59分" (BJT) | Porto de Kyirong | Fluxo de detritos atinge o porto, gravado por câmera | Shigatse via [CDSB](https://static.cdsb.com/micropub/Articles/202608/a35cc0dbc8b20fe086b45db6a81449d9.html); [CGTN](https://english.cctv.cn/2026/08/29/ARTIMtLTn5VunoUue932YjVW260829.shtml) | A |
| 03:00 → | — | 30–45 km a NE e SE do sítio | Primeiras nuvens com topo de água super-resfriada (248–256 K, ~450 km²) | Himawari-9, § 6 | A |
| 03:05 | "8:50am" (NPT) | Syabrubesi | Limnímetro para de transmitir | KP; NDRRMA | A |
| 03:15 | "around 9:00 am" (NPT) | Bhote Koshi | O FFD é avisado por telefone; o nível começa a subir rápido | [Himalayan Times](https://thehimalayantimes.com/ampArticle/1040002); ICIMOD | A |
| 03:30–03:31 | "9:15–9:16am" (NPT) | Rasuwa, Nuwakot, Dhading, Chitwan | 679.295 alertas por SMS | KP; NDRRMA | A |
| 04:43 | "10:28 hrs" (NPT) | Galchhi | Cheia chega a Galchhi | NDRRMA | A |
| **05:59–06:00:35** | 06:00:35Z (USGS); "~05:59 UTC" (Adhikari); ADRC "11:45" (NPT) | **28,3281 N, 85,4798 E (7,2 km a NNW)**, posto por imagem | **Segundo deslizamento**, Ms 4,2, ~10⁷ m³ (uma ordem abaixo do principal); "criou uma barragem e um lago temporários" | [USGS us7000tc90](https://earthquake.usgs.gov/earthquakes/eventpage/us7000tc90); Adhikari et al. 2026 | A |
| 10:15 | "4pm" (NPT) | Devghat | Pico de 6,57 m, ~5.850 m³/s | KP; NDRRMA | A |

---

## 2. "Algo uma hora antes, talvez em outro lugar"

Não há registro verificável de um evento **uma hora** antes. Há cinco candidatos:

1. **O evento sísmico precursor das 02:35:12 UTC (08:20 NPT), 17 min 4 s antes.** É o único instrumental e foi **em outro lugar**.
   * Adhikari et al. (rede NEMRC) dão ML 2,5, localizado com fases P e S, a menos de 10 km a sudeste da fonte. Na Fig. 2 do artigo ele está em ~28,21 N / 85,58 E, ~9,7 km a sul-sudeste da cicatriz, do outro lado da crista do Tsangbu Ri, no vale ao sul. A profundidade é de ~9 km sob o Langtang Lirung, mas mal resolvida.
   * Os autores acham origem tectônica "menos provável" do que um tremor raso de deslizamento ("slide-quake"). Ele seria ligado ao movimento gravitacional, porque se repetiu nos dias anteriores perto da fonte. Avisam que coincidência no tempo e no espaço não prova causa.
   * The Week o descreve como "M2,6 perto da fronteira de Rasuwagadhi".
   * O mesmo artigo diz que a detecção por modelo de forma de onda achou **mais de 60 eventos menores nas duas semanas anteriores**, "incluindo vários nas horas anteriores", com formas de onda parecidas com a do ML 2,5. Os horários desses eventos ficaram para um estudo separado. É o que mais se aproxima de "algo uma hora antes".
2. **O "10:30" da Xinhua.** Lido em BJT, é 02:30 UTC, 22 min antes do sismo; não é confusão de fuso inteiro. Convertido para o Nepal dá 08:15, e é daí que veio o boato de que "a China sabia às 8:15". Os horários chineses posteriores (10:52 e 10:59 BJT) batem com o sismo e com a câmera do porto.
3. **O desprendimento em 25/08 à tarde, "perto de Deding" (IRDR).** São 19 h antes, e nenhum catálogo sísmico registra nada em 25/08. O ICIMOD diz que a questão está "em aberto".
4. **Santosh Nepal (Onlinekhabar, 28/08).** Escreve que a massa atingiu o chão "por volta das 9:38", exatamente 1 h depois de 8:37–8:38. Provavelmente é um erro de digitação, mas foi publicado assim.
5. **O segundo deslizamento, às 06:00:35 UTC.** Foi **em outro lugar** (7,2 km a NNW) e **3 h depois**, não antes.

A Universidade de Wuhan fala em "vários sinais anômalos na fonte horas antes do evento principal", sem estação nem horário. É a única menção a algo horas antes, e não foi verificada.

---

## 3. Onde foi a fonte (o sismo não está "no" anfiteatro)

| Localização | Lat / lon | Distância ao ponto USGS | Dentro do anfiteatro (3,41 km²)? | O que é |
| :--- | :--- | ---: | :---: | :--- |
| USGS us7000tbwb (final) | 28,271 / 85,515 | 0 | sim | **Posta à mão a partir de imagens de satélite** (0 fases usadas; "estimated from satellite images") |
| USGS inicial (substituída) | 28,5495 / 85,5378 | 31 km N | não | Solução sísmica com fases tardias do sinal longo |
| GFZ | 28,30 / 85,50 | 3,5 km | não | Epicentro fixado; só o tempo foi resolvido |
| CENC | 28,20 / 85,58 | 10 km SE | não | Relocada com estações do Nepal |
| IDC (CTBTO) | 28,1706 / 85,3895 | 17 km SW | não | Elipse de 27 × 12 km que contém o sítio |
| **Retroprojeção de período longo** (Adhikari et al.) | 28,2604 / 85,5057 | 1,5 km SW | sim | Coerência de forma de onda de período longo; grade de ~1 km, incerteza maior que a grade |
| **Primeiras chegadas de alta frequência, NonLinLoc** (Adhikari et al.) | 28,298 / 85,566 | 5,8 km ENE | não | Origem 02:52:16 UTC; incerteza realista de ~5 km; 19 estações, lacuna azimutal de 133°, estação mais próxima a 63 km. Fica 3,9 km a E da zona de ruptura de Petley. |
| **Zona de ruptura mapeada** (Petley, 07/09) | 28,2921 / 85,5271 | 2,6 km NNE | **não (1,6 km fora)** | Coroa a ~5.140 m, base a ~3.990 m, ~2 km de comprimento, superfície de ruptura **em rocha**, ~10⁸ m³ |
| Segundo deslizamento (us7000tc90) | 28,3281 / 85,4798 | 7,2 km NNW | não | Também posto por imagem de satélite |

**A zona de ruptura coincide com a mancha de queda do radar de 28,3 ha** (`data/processed/neve_anfiteatro/manchas_s1_exutorio.geojson`):
* a mancha tem centro em 28,2878 N / 85,5278 E e vai de 28,283 a 28,294 N e de 85,523 a 85,531 E;
* o ponto de Petley cai dentro dela, a ~0,5 km do centro;
* ela fica logo a leste do exutório do anfiteatro (4.024 m), onde começa o sinal do Sentinel-1 ao longo do talvegue.

A **cicatriz verificada em campo** na Fig. 2 de Adhikari et al. (linha vermelha, de ~28,283 N / 85,522 E a ~28,295 N / 85,530 E) cai sobre a mesma mancha. O relatório de neve e gelo a tinha como candidata ambígua. Com o mapeamento de Petley, ela passa a ser a **localização mais provável da ruptura**.

Adhikari et al. dão nome à fonte: **flanco norte do Tsangbu Ri (6.781 m)**, perto do Langtang Lirung. Segundo eles, o volume é da ordem de 10⁸ m³, "principalmente rocha, com uma parte menor de gelo". Pelas imagens de satélite, não havia lago glacial na origem.

**Consequência:** a ruptura foi no flanco logo a nordeste do exutório, entre ~4.000 e ~5.140 m, e não dentro da bacia de 3,41 km² que caracterizamos (4.000–7.200 m). O anfiteatro fica a montante e a sudoeste dela. O ponto do USGS e a retroprojeção caem no anfiteatro, mas o primeiro foi posto a olho e a segunda não resolve 2–3 km.

---

## 4. Fusos horários

* **Nenhum horário de catálogo tem desvio igual a um fuso.**
  * 10:52:20 BJT (CENC) = 02:52:20 UTC = 08:37 NPT.
  * O próprio USGS escreve "8:37 AM local (10:52 AM China Standard Time)".
* **Há dois grupos de horário de origem que não são de fuso:**
  * 02:52:10–02:52:23, do início do sinal (USGS final, CENC, GFZ, Adhikari);
  * 02:52:44–02:52:47, das chegadas mais fortes e tardias (USGS inicial, EMSC, IDC, MOS).
* **As confusões reais são três:**
  * o "10:30" da Xinhua (22 min antes do sismo);
  * o "10:30 a.m. local" de um fotógrafo na CNN, que é 02:30 UTC se for BJT e 04:45 UTC se for NPT;
  * o "9:38" de Santosh Nepal (+1 h).
* **Divergências menores entre fontes nepalesas:**
  * a mesma leitura de 1,62 m aparece às 8:23 em "Rasuwagadhi" (The Week) e às 8:40 em Syabrubesi (KP, NDRRMA);
  * a chegada a Malekhu varia em 30 min.

---

## 5. O que isso muda para a hipótese do pesquisador

**O que fica de pé:**
* Houve nuvem espessa sobre o sítio por ~7 h.
* O topo dela desceu até o terreno entre 00:30 e 01:30 UTC.
* Isso aconteceu ~1,5 h antes de um precursor sísmico (02:35) e ~1,5–2,5 h antes da ruptura (02:52).
* A sequência "colapso da nuvem, depois colapso da montanha" é compatível com os horários.

**O que pesa contra um gatilho só atmosférico:**
* A ruptura foi **em rocha**, com ~10⁸ m³ (Petley, ICIMOD: 100–200 M m³), numa encosta cuja geleira suspensa vinha **acelerando havia meses** (7,4 → 55 m/ano).
* Houve dezenas de pequenos sismos nas duas semanas anteriores e um precursor 17 min antes.
* Qualquer massa entregue pela nuvem seria uma fração pequena desse volume. No máximo, um carregamento final sobre uma encosta que já estava em ruptura progressiva.

**O que falta para fechar:**
1. **Os horários e locais dos "vários eventos nas horas anteriores"** que Adhikari et al. detectaram por modelo de forma de onda. Eles prometem publicá-los em outro estudo; pode-se pedir aos autores (NEMRC). Interessa saber se algum caiu entre 00:30 e 01:30 UTC, durante a descida da nuvem. O artigo (lido em 21/10/2026) dá a hora do ML 2,5 (02:35:12 UTC) e a localização NonLinLoc do principal (28,298 / 85,566 ± 5 km). A posição do ML 2,5 só aparece na Fig. 2, de onde foi lida: ~28,21 N / 85,58 E.
2. **A inversão da história de força do sinal de período longo** (Ekström), que daria massa, direção e tempo.
3. **O INSAT-3D**, que vê o sítio quase no nadir, para o colapso da nuvem sem paralaxe.
4. **Relatos com horário de quem estava perto da fonte entre 00:30 e 02:35 UTC.** As notícias até agora não trazem nenhum.

---

## 6. Cicatriz, depósito e o "lago temporário", no Sentinel-2 (21/10/2026)

**Por que:** o pesquisador desconfia dos 10⁸ m³ de Adhikari et al. Duas razões: "não há tanta diferença na geleira" e "o cálculo da água não continha tanta rocha". Também acha estranho o "lago temporário" atribuído ao segundo deslizamento.

**Método** (`scripts/neve_anfiteatro/cicatriz_e_lago.py`, saídas em `data/processed/cicatriz_lago/`):
* Sentinel-2 L2A, na mesma órbita (passagem das ~04:47 UTC) e na mesma época do ano: 13 e 18/10/2025 (antes) contra 13 e 18/10/2026 (depois). Iluminação e neve sazonal são as mesmas.
* O par de 2025 entre si dá o ruído de cada teste.
* A cicatriz de referência é a linha de campo da Fig. 2 de Adhikari et al.

**Resultados:**

1. **A geleira acima da cicatriz quase não mudou.**
   * A até 2 km da cicatriz, a área que era neve/gelo nas duas cenas de antes e não é nas duas de depois soma **14 ha**. O ruído do par de 2025 é de 27 ha, então a perda não se distingue dele.
   * A maior mancha contínua de perda tem 2,4 ha, em 28,293 N / 85,529 E, sobre a cicatriz.
   * A observação do pesquisador se confirma. A massa que rompeu era sobretudo rocha (é também o que o artigo diz), e a geleira por cima ficou.
   * Na cena de antes (out/2025) já havia, abaixo da cicatriz, um corredor de rocha exposta de ~2 km, uma trilha antiga de avalanche ou detritos.
2. **O depósito é grande e está no vale, não no rio.**
   * Solo exposto ou detrito novo sobre o que era vegetação nas duas cenas de antes: **511 ha (5,1 km²)** em manchas de 5 ha ou mais. A maior mancha contínua tem 218 ha. O mesmo teste no par de 2025 dá **0 ha**.
   * O depósito sai do pé da cicatriz para noroeste, ~6 km até o Lhende Khola, e segue o vale para oeste além da borda do recorte (85,45 E).
   * Os 5,1 km² não contam a parte alta do corredor, que já era rocha antes. A área real é maior.
3. **O volume depende da espessura, que o Sentinel-2 não mede:**

   | Espessura média do depósito | Volume sobre 5,1 km² |
   | ---: | ---: |
   | 2 m | ~10 M m³ |
   | 5 m | ~26 M m³ |
   | 10 m | ~51 M m³ |
   | 20 m | ~100 M m³ |

   * **O lado do depósito não exclui os 10⁸ m³.** Para isso bastaria um depósito de ~20 m de espessura média, comum em avalanches de rocha.
   * **Isso corrige a crítica anterior,** que se baseava na mancha de 28 ha do radar como área da fonte. A zona de ruptura de Petley tem ~2 km de comprimento. Com 1–2 km² e 50–100 m de profundidade, 10⁸ m³ fica possível.
   * O número de 10⁸ m³ continua **não medido**: vem de uma calibração de amplitude sísmica que os próprios autores chamam de muito incerta. Para decidir é preciso um modelo de elevação pós-evento por estereoscopia (ASTER, por exemplo), comparado com o GLO-30.
4. **Rocha e água não andaram juntas.**
   * A rocha ficou, em grande parte, no depósito de ~6 km entre a cicatriz e o Lhende Khola.
   * O que desceu o Bhote Koshi e o Trishuli foi sobretudo água com sedimento.
   * Isso é compatível com o cálculo de água do repositório, que não continha tanta rocha. Os dois números (10⁷–10⁸ m³ de rocha parada e ~10⁷ m³ de água que passou por Rasuwagadhi) não se contradizem.
5. **Não há lago visível no ponto do segundo deslizamento.**
   * Teste de água estrito: NDWI > 0,15, NIR baixo, SWIR1 < 0,04 e SWIR2 < 0,03, para não confundir com sombra de relevo.
   * Ele dá **0 ha de água** a até 1,5 km do ponto do us7000tc90 em todas as cenas utilizáveis depois do evento: 08/09 (34% de nuvem no local), 28/09, 03/10, 13/10 e 18/10.
   * No vale do Lhende Khola inteiro (28,30–28,36 N, 85,45–85,52 E), o máximo é ≤ 0,24 ha, igual ao de antes.
   * As cenas de 14 e 24/08 são anteriores ao evento, e a de 03/09 é 100% nuvem. Entre 26/08 e 08/09 não há cena óptica utilizável.
   * O ponto do us7000tc90 fica junto à ponta inferior do depósito, onde ele encontra o Lhende Khola. Se houve barragem e lago, eles se esvaziaram antes de 08/09.
   * O Sentinel-1, que vê através de nuvem, pode testar a janela de 26/08 a 08/09. Feito no item 7.

6. **ASTER: o modelo de elevação pós-evento existe, mas está sobre nuvem** (`scripts/neve_anfiteatro/aster_dh.py`, `data/processed/cicatriz_lago/aster_dh.json`).
   * O LP DAAC tem modelos AST14DEM (30 m) de 27/05, 16/06 e 11/07/2026 (antes) e de **30/08/2026** (quatro dias depois). Não há aquisição ASTER posterior até 21/10.
   * O de 30/08 cobre todo o depósito, mas fica em média **4.458 m acima do terreno** do GLO-30. Em nenhum pixel do depósito a diferença é menor que 50 m. É o topo das nuvens da monção (~7,6 km), não o chão. As cenas tinham 41–53% de nuvem, e sobre o sítio ela era total.
   * O de 16/06, de controle, alinhado ao GLO-30 (deslocamento de −60/+30 m), dá no depósito **mediana de −1,5 m** e dispersão de 12–20 m. Esse é o ruído do método: sem evento, nada muda. O de 11/07 não cobre a área.
   * **Resultado:** o ASTER não mede a profundidade da cicatriz nem a espessura do depósito. Não há ICESat-2 nem GEDI cruzando a área entre julho e outubro de 2026.
   * Para medir o volume falta um par estéreo pós-evento sem nuvem. As opções são todas por solicitação: Pléiades, WorldView ou SkySat (comerciais), ou um modelo TanDEM-X (DLR).
7. **Sentinel-1: nenhum lago acima de ~1 ha no ponto do segundo deslizamento a partir de 28/08** (`scripts/neve_anfiteatro/s1_lago.py`, `data/processed/cicatriz_lago/s1_lago.json`).
   * Teste: VV antes > −15 dB, para descartar sombra de relevo e água antiga; VV depois < −18 dB; queda > 5 dB na mesma órbita. Três órbitas, com o par de antes do evento como ruído.

   | Órbita | Par | "Água nova" a até 2 km do tc90 | Maior mancha contínua |
   | :--- | :--- | ---: | ---: |
   | 121 | 07/08 → 19/08 (ruído) | 0,20 ha | 0,04 ha |
   | 121 | 19/08 → 31/08 | 0,36 ha | 0,08 ha |
   | 121 | 19/08 → 12/09 | 0,48 ha | 0,24 ha |
   | 19 | 12/08 → 24/08 (ruído) | 0,08 ha | 0,04 ha |
   | 19 | 24/08 → 05/09 | 0,88 ha | 0,48 ha |
   | 19 | 24/08 → 17/09 | 1,16 ha | 0,72 ha |
   | 85 | 04/08 → 16/08 (ruído) | 0,20 ha | 0,04 ha |
   | 85 | 16/08 → **28/08** | 2,00 ha | 0,60 ha |
   | 85 | 16/08 → 09/09 | 1,52 ha | 0,28 ha |

   * Há um pouco mais de "água nova" que no ruído, mas espalhada em pixels soltos, com a maior mancha abaixo de 1 ha. O mesmo padrão aparece na neve alta ao sul, onde é neve molhada, não lago.
   * A primeira passagem é de 28/08 às 12:21 UTC, ~2,3 dias depois do segundo deslizamento. **Se houve barragem e lago no Lhende Khola, eles tinham menos de ~1 ha ou já se tinham esvaziado** nesse prazo. Um lago de 1 ha com 5–10 m de profundidade guardaria só ~0,05–0,1 M m³.
   * Limite: num vale estreito e íngreme, a geometria do radar (sombra e inversão de relevo) pode esconder uma faixa de água estreita.
   * O "lago temporário" do texto do USGS continua sem nenhuma confirmação independente.

**Arquivos de trabalho das buscas** (fora do repositório, no scratchpad da sessão): respostas brutas dos catálogos em `scratchpad\seis\`; textos do ADRC e do NDRRMA em `scratchpad\adrc\` e `scratchpad\ndrrma\`.
