# Análise Copernicus GLO-30 e busca de lago em imagem real de 2026

**Data:** 07 de setembro de 2026
**Dados:** Copernicus DEM GLO-30 (tile `N28_00_E085_00`, TanDEM-X 2011–2015), acesso aberto sem autenticação; Sentinel-2 L2A tile 45RUM, quatro datas de 2026
**Processamento:** priority-flood com incremento ε, direções de fluxo D8, acumulação por ordem topológica, delineação de bacias por varredura de montante. Célula 27,2 × 30,7 m = 836 m²; janela de 1.682 km²

---

## 0. O que o GLO-30 não pode fazer

O GLO-30 é **de época única** — a superfície TanDEM-X de 2011–2015. Não existe um GLO-30 pós-evento, nem qualquer DEM aberto da superfície de agosto de 2026. **Diferenciação de DEM pré/pós é impossível com dados abertos hoje.** Ela exigiria par estereoscópico comercial (Pléiades Neo, WorldView-3) ou processamento InSAR dedicado.

O que o GLO-30 decide, e que foi feito aqui: delineação real das bacias, perfil longitudinal e declividade do talvegue, e cota de cada feição citada nos documentos.

---

## 1. Correção de um erro meu

No relatório anterior escrevi que os 65,7 ha do lago estavam confirmados por um corpo de 73,9 ha detectado na cena de 12/08/2026. **Estava errado, por duas razões.**

Primeira: o corpo está a **5.260 m** de cota no GLO-30, não a 3.950 m como o documento situa o lago do Lhende Khola.

Segunda, e decisiva: não é água. A assinatura espectral dos 1.917 pixels classificados como água pelo SCL:

| Grandeza | Pixels "água" do SCL | Neve/gelo na mesma cena | Água glacial típica |
| :--- | ---: | ---: | :--- |
| B11 (SWIR) | 0,0243 | 0,0885 | alta |
| B08 (NIR) | 0,1428 | 0,5347 | < 0,05 |
| **NDWI** | **+0,094** | +0,030 | **> +0,3** |
| **NDSI** | **+0,748** | **+0,750** | baixo |

NDSI idêntico ao da neve, NDWI muito abaixo do limiar de água, SWIR baixíssimo. **São pixels de neve/gelo em sombra**, que o Sen2Cor classifica como água — um erro conhecido do SCL. Apenas 2,5 % desses pixels passam no teste de NDWI.

Aceitei a classificação sem testar a assinatura. Não repito o erro abaixo.

---

## 2. Busca de lago com critério espectral estrito

Critério: `NDWI > 0,20` **e** `NIR < 0,10` **e** `NDSI < 0,60`, sobre pixels livres de nuvem. Área ampliada para **914 km²** (85,38–85,68 °E; 28,18–28,46 °N), quatro datas de 2026.

| Data | Nuvem | Água real | **Maior corpo** | "Água" pelo SCL (bruto) |
| :--- | ---: | ---: | ---: | ---: |
| 2026-06-15 | 32,4 % | 49,4 ha | **2,60 ha** | 42,5 ha |
| **2026-08-12** | **10,2 %** | 76,1 ha | **2,76 ha** | 302,8 ha |
| 2026-08-24 | 53,6 % | 37,1 ha | **4,76 ha** | 170,9 ha |
| 2026-08-27 | 83,6 % | 8,4 ha | 3,56 ha | 7,7 ha |

> **Em 914 km², em quatro datas cobrindo de 15 de junho a 27 de agosto de 2026, o maior corpo d'água detectado é de 4,76 ha.** Os 76 ha de água real na melhor cena estão dispersos em 299 corpos, nenhum acima de 2,8 ha.

O repositório adota um lago pré-evento de **65,7 ha e 5,2 M m³**, que fornece 37 % da água no balanço corrigido. **Esse lago não existe na imagem.** O maior corpo é 24 vezes menor.

E a diferença entre 302,8 ha (SCL) e 76,1 ha (teste estrito) na cena limpa mostra que a classificação automática superestima água em 4×, por neve sombreada. Qualquer área de lago derivada de SCL sem verificação espectral é suspeita.

**Isto sustenta literalmente a sua observação: não havia água lá em cima.**

---

## 3. Delineação de bacia — as áreas adotadas não existem

Traçado do escoamento a partir do ponto de colapso (85,515 °E; 28,271 °N; z = 5.590 m no GLO-30), descendo para norte:

| Distância | Cota | Área de drenagem |
| ---: | ---: | ---: |
| 1,02 km | 4.209 m | 0,66 km² |
| 1,45 km | 4.010 m | **3,39 km²** ← chegada ao fundo do vale |
| 2,90 km | 3.615 m | **17,39 km²** |
| 5,80 km | 3.103 m | **32,71 km²** |
| 8,12 km | 2.776 m | **239,50 km²** ← confluência com o tronco principal |
| 11,60 km | 2.376 m | 633,40 km² |
| ~20 km | 1.800 m | **934 km²** ← Rasuwagadhi |

A queda de 5.590 m para 4.010 m em 1,45 km confirma o desnível de ordem 1.500–2.000 m reportado para o destacamento.

**Consequência direta:** a drenagem salta de 32,7 km² para 239,5 km² ao cruzar a confluência. **Não existe nenhum ponto no Lhende Khola com bacia de 55 km² nem de 65,7 km².** Também não existem os 50 km² nem os 100 km². As únicas áreas fisicamente disponíveis para um barramento no Lhende são **3,4 / 17,4 / 32,7 km²**.

Bacias delineadas nos três pontos candidatos:

| Ponto de barramento | Área | Faixa de cota | Mediana | Acima de 5.000 m |
| :--- | ---: | :--- | ---: | ---: |
| chegada ao vale (4.010 m) | 3,39 km² | 4.010–7.216 m | 5.913 m | 77 % |
| garganta a 3.615 m | 17,39 km² | 3.614–7.216 m | 5.314 m | 69 % |
| garganta a 3.103 m | 32,71 km² | 3.103–7.216 m | 4.871 m | 46 % |

---

## 4. Declividade do talvegue — um parâmetro que se confirma, e uma correção

| Trecho | Comprimento | Desnível | S₀ medido |
| :--- | ---: | ---: | ---: |
| Lhende alto (4.010 → 3.615 m) | 1,45 km | 395 m | 0,2725 |
| Lhende médio (3.615 → 3.103 m) | 2,90 km | 511 m | 0,1763 |
| Lhende inferior (3.103 → 2.376 m) | 5,80 km | 727 m | 0,1253 |
| **Garganta de Rasuwagadhi (2.376 → 1.800 m)** | 8,70 km | 576 m | **0,0662** |
| Trishuli abaixo (1.800 → 1.502 m) | 8,70 km | 298 m | 0,0342 |

O repositório adota **S₀ = 0,045** para a garganta. O valor medido é **0,0662** — a mesma ordem, o que valida a escolha como razoável, mas 47 % maior. Como $Q \propto \sqrt{S_0}$:

| | S₀ = 0,045 (adotado) | S₀ = 0,0662 (medido) |
| :--- | ---: | ---: |
| Velocidade | 11,60 m/s | **14,07 m/s** |
| $Q_{\text{pico}}$ | 3.376 m³/s | **4.095 m³/s** |
| Froude | 1,35 | **1,63** |
| Volume de água líquida | 14,20 M m³ | **17,22 M m³ (+21 %)** |

Nota: Fr = 1,63 agrava a objeção metodológica — a equação de Manning é formulação para escoamento uniforme permanente e não se aplica bem a esse regime.

---

## 5. O "déficit hídrico" é um erro de escala, agora medido

A leitura de nível ($\Delta h = 8{,}5$ m) que gera todo o volume é feita **na garganta de Rasuwagadhi**, seção que drena **934 km²**. A chuva é então exigida de uma bacia de 15 a 65 km². Dividindo o mesmo volume pelas áreas disponíveis:

**Para $V_{\text{água}} = 17{,}2$ M m³ (com a declividade medida):**

| Área de drenagem | Lâmina requerida | |
| :--- | ---: | :--- |
| 3,39 km² (chegada ao vale) | 5.977 mm | fisicamente absurdo |
| 17,39 km² | 1.165 mm | absurdo |
| 32,71 km² | 620 mm | |
| 55,0 km² *(adotado — não existe)* | 368 mm | |
| 65,7 km² *(adotado — não existe)* | 308 mm | |
| **934 km² (seção onde o nível foi lido)** | **21,7 mm** | ordinário |

> A mesma cheia exige de **21,7 mm** a **5.977 mm** de chuva, dependendo apenas de qual área se escolhe para dividir. O intervalo é de **275 vezes**. Nenhuma física distingue esses casos — só a escolha do denominador.

**É isto o "déficit de 10×".** Não é uma anomalia hidrológica: é a razão entre um volume medido numa seção de 934 km² e uma área de captação de 15–65 km² arbitrada em outro documento.

---

## 6. Sobre a monção e "veio do céu"

Três coisas distintas foram sendo tratadas como uma só. Separadas:

**Era estação de monção.** O evento é de 26 de agosto. A fonte externa registra explicitamente: *"Despite occurring during the monsoon season, the disaster unfolded on a clear day."* Estação de monção e chuva naquela manhã são coisas diferentes; a primeira é fato de calendário, a segunda foi negada por observação.

**Não havia água armazenada lá em cima — confirmado.** Sem lago (§2), e a cabeceira do Lhende, com 32,7 km² e 46 % acima de 5.000 m, tem vazão de base de ordem de poucos m³/s no fim de agosto. Nos 43 minutos de represamento isso são milésimos de M m³. **A cabeceira não tinha como entregar 17 M m³. Você está certo.**

**Então de onde veio a onda de 9 m em Rasuwagadhi?** Da própria água do tronco principal. A seção onde o nível subiu drena 934 km² — não 33. O que a avalanche fez foi **deslocar e empurrar o rio que já estava lá**, ao longo de ~20 km de calha, exatamente como descrito na fonte externa: *"pushed the river ahead of it, gathering more and more water"*. A subida de nível é uma onda de deslocamento por detrito, não a entrega de 17 M m³ de água nova.

**E sim, a água é de origem atmosférica.** Os 934 km² a montante de Rasuwagadhi são alimentados por degelo de neve e gelo e por chuva de monção acumulada ao longo de semanas. Nesse sentido veio do céu — mas **ao longo da estação, estocada na bacia**, e não numa descarga convectiva de duas horas sob céu limpo. A discordância entre nós nunca foi sobre a origem da água; é sobre a escala de tempo da entrega.

---

## 7. Situação de cada número, medido

| Alegação do repositório | Veredito | Medido |
| :--- | :--- | :--- |
| Lago pré-evento de 65,7 ha / 5,2 M m³ | **Não existe** | maior corpo em 914 km²: 4,76 ha |
| Bacia de 55 km² ou 65,7 km² | **Não existe** | 3,4 / 17,4 / 32,7 km² são as únicas disponíveis |
| $S_0 = 0{,}045$ na garganta | **Razoável, 47 % baixo** | 0,0662 |
| $Q_{\text{pico}} = 3.376$ m³/s | **Subestimado** | 4.095 m³/s com S₀ medido |
| Destacamento a ~5.200 m, queda > 2.000 m | **Compatível** | 5.590 → 4.010 m em 1,45 km |
| Rasuwagadhi a 1.814 m | **Confirmado** | 1.800 m no GLO-30 |
| Déficit hídrico de 10× | **Artefato de escala** | 21,7 a 5.977 mm conforme a área escolhida |
| `ice_fraction = 0,40` | **Não sustentado** | verniz de 0,3 % a ~8 % (medição anterior) |

---

## 8. O que continua em aberto

1. **Volume e fração de gelo do destacamento** — só diferenciação de DEM decide, e exige par estereoscópico comercial. É a única variável de primeira ordem ainda sem medição.
2. **Delineação completa da cicatriz** — exige cena pós-monção; a primeira janela limpa será em outubro de 2026.
3. **Volume real da onda** — a reconstrução de Manning em regime supercrítico (Fr = 1,63) é frágil. Modelagem hidrodinâmica 1D/2D com o talvegue do GLO-30, que agora existe, substituiria a estimativa por cálculo.
4. **Hidrograma observado** — nenhum. As séries do DHM Nepal em Betrawati e da CMA em Gyirong resolveriam o problema por medição direta e continuam dependendo de pedido institucional.

---

## 9. Reprodução

```
DEM   : https://copernicus-dem-30m.s3.amazonaws.com/
        Copernicus_DSM_COG_10_N28_00_E085_00_DEM/Copernicus_DSM_COG_10_N28_00_E085_00_DEM.tif
janela: 85,30-85,72 E / 28,15-28,52 N  (1332 x 1512 px, 1.682 km2)
rotina: priority-flood + eps=1e-4 -> D8 -> acumulacao topologica -> varredura de montante
celula: 27,2 x 30,7 m = 836 m2 (lat 28,3)
S2    : sentinel-cogs.s3.us-west-2.amazonaws.com, tile 45RUM, B03/B08/B11/SCL
agua  : NDWI>0,20 E NIR<0,10 E NDSI<0,60, sobre pixels livres de nuvem
```
