# Balanço Hídrico do Evento de 26/08/2026 sob Céu Claro e Massa Sem Gelo

### Seção substitutiva do capítulo do "Toró"

**Escopo.** Esta seção refaz o balanço de massa líquida do colapso do Lhende Khola sob duas restrições observacionais que não estavam incorporadas nas versões anteriores: (i) o evento ocorreu **em dia claro, sem chuva local**; (ii) a massa destacada tinha volume da ordem de **10⁸ m³** e **conteúdo de gelo desprezível**, permanecendo o gelo do maciço em posição. Sob essas restrições, os dois mecanismos até aqui invocados — precipitação convectiva extrema e fusão por atrito de gelo arrastado — ficam ambos indisponíveis, e o balanço tem de fechar por outra via.

---

## 1. Restrições observacionais

| # | Observação | Status | Fonte |
| :-- | :--- | :--- | :--- |
| O1 | Dia claro, sem chuva no vale no momento do colapso | **Observado** | Registro do próprio projeto (`rain_status: dry_valley`; população confirma zero chuva); Stimson Center: *"This was not a rainfall-triggered event. Despite occurring during the monsoon season, the disaster unfolded on a clear day."*; DHM/Nepal não registra chuva forte imediatamente anterior |
| O2 | Colapso de rocha (± gelo) de ~10⁸ m³ a ~5.200 m, com queda > 2.000 m | **Reportado** | Relatos técnicos de acompanhamento: *"a large mass of bedrock and glacial ice with an estimated volume of almost 100 million cubic meters detached... at an elevation of around 5200 masl"*, descendo *"over 2000 meters"* |
| O3 | Conteúdo de gelo desprezível na massa destacada; gelo do maciço permanece in situ | **Premissa do PI, a documentar** | Inspeção de imagem pelo investigador principal. **Contradiz** a caracterização "bedrock and glacial ice" das fontes de O2 e exige documentação com par pré/pós de 2026 (ver §6) |
| O4 | A avalanche empurrou o rio à sua frente, ganhando água na descida | **Reportado** | *"gained water content as it descended"*, *"pushed the river ahead of it, gathering more and more water"* |
| O5 | Sismo `us7000tbwb`, Ms 5,2, `ms_vx`, tipo `landslide`, prof. 0 km, 2026-08-26T02:52:10Z; segundo deslizamento `us7000tc90`, Ms 4,2, 06:00:35Z | **Observado** | Catálogo FDSN do USGS, consulta direta |
| O6 | Elevação de nível de ~9 m em 30 min no Trishuli | **Reportado** | Relatos de campo e imprensa |

---

## 2. O que as restrições eliminam

**O1 elimina o gatilho pluvial.** Não é possível depositar 87 mm — muito menos as 500–950 mm alegadas em versões anteriores — sobre um vale seco e ensolarado no instante do colapso. O mecanismo de electro-antiscavenging (Tinsley) exige, além disso, uma nuvem com população de gotículas super-resfriadas entre −3 °C e −8 °C; céu claro não fornece esse substrato. Pela mesma razão, as contagens de descargas atribuídas ao evento são incompatíveis com a condição atmosférica observada e devem ser retiradas.

> Consistência interna: o próprio catálogo do projeto aplica a Chamoli 2021 a inferência *"céu azul, zero descargas ⇒ colapso puramente mecânico/telúrico"*. A mesma evidência em 2026 exige a mesma inferência.

**O3 elimina a fusão por atrito.** Com gelo desprezível na massa, não há reservatório a fundir, e a energia potencial — ainda que da ordem de 3.700 a 5.300 TJ para 10⁸ m³ caindo 2.000 m — não se converte em água. A energia vai para fragmentação, calor sensível na rocha e ruído sísmico/acústico, não para calor latente.

Restam, portanto, apenas fontes de **água líquida preexistente** no sistema.

---

## 3. Reconstrução do balanço

A água mobilizada não precisa ter caído do céu nem derretido: precisa ter sido **capturada**. Quatro termos, nenhum deles presente no balanço anterior de forma completa.

### [A] Água intersticial na massa de origem

Um maciço de 10⁸ m³ em ambiente periglacial, em plena monção, carrega água em juntas, fraturas, manto de alteração, talus e camada ativa. Rocha cristalina intacta tem porosidade de 0,5–2%; maciço fraturado com cobertura detrítica, bem mais.

| Porosidade efetiva $n$ | Saturação $S$ | Descrição | Água |
| ---: | ---: | :--- | ---: |
| 0,020 | 0,80 | maciço cristalino fraturado, pouco alterado | **1,60 M m³** |
| 0,050 | 0,85 | rocha muito fraturada + manto de alteração | **4,25 M m³** |
| 0,100 | 0,90 | inclui talus, morena e camada ativa periglacial | **9,00 M m³** |

### [B] Água no material de leito entranhado

O fluxo escavou o talvegue. Aluvião e morena saturados ($n \approx 0{,}30$, $S \approx 0{,}95$) liberam sua água intersticial ao serem incorporados.

| Percurso | Largura | Prof. de escavação | Material | Água |
| ---: | ---: | ---: | ---: | ---: |
| 20 km | 40 m | 3 m | 2,40 M m³ | 0,68 M m³ |
| 20 km | 80 m | 6 m | 9,60 M m³ | 2,74 M m³ |
| 45 km | 80 m | 6 m | 21,60 M m³ | 6,16 M m³ |

### [C] Água livre no canal, varrida pela frente

Este é o termo estruturalmente ausente das versões anteriores. O balanço antigo integrava $Q \cdot t$ **numa única seção**, o que contabiliza apenas o que passa por um ponto — e ignora que a frente varre a coluna d'água **armazenada ao longo de todo o percurso**. Com seção molhada de 45–88 m² em regime de monção:

| Percurso | $A$ = 45 m² | $A$ = 60 m² | $A$ = 88 m² |
| ---: | ---: | ---: | ---: |
| 20 km | 0,90 M m³ | 1,20 M m³ | 1,76 M m³ |
| 45 km | 2,02 M m³ | 2,70 M m³ | 3,96 M m³ |

Este termo é a formalização quantitativa de O4.

### [D] Lago represado e afluência durante o evento

Represamento no pico: **7,54 M m³** (ou 5,20 M m³ para o lago pré-evento, valor não verificável — ver §6). Afluência de base do Trishuli superior: 180 m³/s × 4 h = **2,59 M m³**.

---

## 4. Resultado

Volume de água líquida a explicar, conforme a reconstrução hidráulica corrente: **14,20 M m³**.

| Cenário | [A] poros origem | [B] leito entranhado | [C] canal varrido | [D] lago + afluência | **Total** | Cobertura | Chuva ainda necessária |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Baixo** | 1,60 | 0,68 | 0,90 | 5,66 | **8,84** | 62,3% | 115 mm |
| **Central** | 4,25 | 2,05 | 1,80 | 7,79 | **15,89** | **111,9%** | **0 mm** |
| **Alto** | 9,00 | 6,16 | 3,87 | 11,14 | **30,17** | 212,5% | 0 mm |

> **No cenário central, o balanço fecha com 112% — sem uma gota de chuva e sem um grama de gelo fundido.**

O cenário baixo deixa 5,4 M m³ em aberto, equivalentes a 115 mm sobre 55 km². É aí, e apenas aí, que um resíduo genuíno poderia existir — e ele depende inteiramente da porosidade efetiva do maciço e da profundidade de escavação do talvegue, duas grandezas mensuráveis.

---

## 5. Consequência para o método anterior

A reconstrução expõe uma incompatibilidade aritmética que precede todo o resto:

$$V_{\text{água}} = V_{\text{bulk}} \times (1 - C_v), \qquad V_{\text{bulk}} = 20{,}7\ \text{M m}^3,\ C_v = 0{,}314$$

Se a massa destacada foi da ordem de **10⁸ m³** (O2), a fase sólida sozinha é **cinco vezes maior** que o bulk total adotado. Ou o bulk estava subestimado por um fator ≥ 5, ou a maior parte do material depositou no vale alto e nunca alcançou a seção de controle. Nos dois casos, aplicar um $C_v$ fixo a 20,7 M m³ e chamar 68,6% disso de água não descreve o evento.

**Recomendação metodológica:** abandonar a derivação da água a partir do bulk. Estimar os termos [A]–[D] independentemente e comparar a soma com a vazão reconstruída — que é o que esta seção faz. Um "déficit hídrico", se existir, deve emergir dessa comparação, não de uma partição imposta.

---

## 6. Testes que decidem, em ordem de poder discriminante

| Teste | O que decide | Dado necessário | Acesso |
| :--- | :--- | :--- | :--- |
| **1. Par Sentinel-2 pré/pós de 2026 (B3, B8, NDSI)** | Se havia gelo na cicatriz e se o gelo do maciço permanece — **a premissa O3** | L2A de julho e setembro de 2026 | **Aberto**, STAC Earth Search, sem autenticação |
| **2. Diferenciação de DEM (Copernicus GLO-30 ou estéreo)** | Volume real destacado; testa os 10⁸ m³ | DEM pré e pós | GLO-30 **aberto**; estéreo submétrico é comercial |
| **3. Inversão da força do deslizamento** | Massa e trajetória de forma independente da imagem | Formas de onda banda larga, ±1 h | **Aberto**, FDSN/IRIS, sem autenticação |
| **4. InSAR Sentinel-1 (coerência)** | Extensão da área remobilizada e da escavação de talvegue | GRD/SLC pré e pós | Registro gratuito (ASF / Copernicus) |
| **5. IMERG V07 de 2026 + correção de viés orográfico** | Fecha O1 quantitativamente | 96 grânulos já catalogados no repositório | Credencial NASA Earthdata |

O teste 1 é o mais urgente, porque **O3 é hoje a única restrição do balanço que não tem documentação anexada** e porque contradiz as descrições publicadas do evento.

---

## 7. Limitações declaradas

1. **O acervo de imagens do evento de 2026 no repositório é do ano errado.** Todos os arquivos em `data/satellite_imagery/himalaia_2026/` estão datados de **2024** — `2024-07-30_Sentinel-2-L2A_pre-event.jpg`, `2024-08-26_..._event-day.jpg`, e as três grades IMERG de `2024-08-26`. Nenhuma imagem do evento real está arquivada. Em consequência, **nem a presença de gelo, nem a área do lago de 65,7 ha, nem o veredito de "pluma convectiva confinada" são sustentáveis pelo acervo atual.**
2. O raster `sentinel_lhende_khola_lake.tif` é composição RGB de 8 bits, não reflectância L2A; sem banda NIR, água e sombra de encosta são inseparáveis. Máscaras plausíveis devolvem de 215 a 2.575 ha contra os 65,7 ha publicados. O valor não é reproduzível a partir do que está arquivado.
3. Os termos [A], [B] e [C] são paramétricos. Nenhum foi medido; todos são calculados a partir de intervalos de porosidade, geometria de canal e profundidade de escavação declarados acima. São **verificáveis** pelos testes 2 e 4, mas hoje são premissas.
4. O volume de ~10⁸ m³ (O2) provém de relatos técnicos de acompanhamento, não de publicação revisada por pares. Deve ser tratado como preliminar até o teste 2 ou 3.
5. O valor de 14,20 M m³ herda os parâmetros de Manning ($n = 0{,}060$, $S_0 = 0{,}045$, $\Delta h = 8{,}5$ m), todos declarados `ASSUMED_BY_ANALYST`. A reconstrução dá $Fr \approx 1{,}35$, regime supercrítico, onde a formulação de Manning tem aplicabilidade limitada.

---

## 8. Síntese

Sob céu claro e sem gelo, o evento de 26/08/2026 é descrito de forma consistente como um **colapso rochoso de escala 10⁸ m³ que capturou a água já presente no sistema** — intersticial na massa e no leito entranhado, livre na coluna do canal, e represada no lago efêmero. Nessa leitura o balanço fecha, e nenhum mecanismo atmosférico ou eletrodinâmico é requerido.

Isto não é um recuo: é o alinhamento do caso com a linha que a literatura de alta montanha vem consolidando — a de que estes eventos são **eventos de detrito, não eventos de água**, em que o volume que desce excede em muito o volume que rompeu, por entranhamento ao longo do percurso.

O resíduo eventualmente remanescente — entre 0 e 5,4 M m³ conforme a parametrização — é a única quantidade que ainda comportaria uma explicação não convencional. Estabelecê-lo exige os testes 1 a 4, todos com dados abertos, e é a única rota pela qual uma hipótese heterodoxa sobre este evento poderia ser defendida em revisão por pares.
