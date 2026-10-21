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

**Arquivos de trabalho das buscas** (fora do repositório, no scratchpad da sessão): respostas brutas dos catálogos em `scratchpad\seis\`; textos do ADRC e do NDRRMA em `scratchpad\adrc\` e `scratchpad\ndrrma\`.
