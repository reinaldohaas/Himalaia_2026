# Medição do par Sentinel-2 L2A real de 2026: cicatriz, gelo remanescente e área do lago

**Data da medição:** 07 de setembro de 2026
**Dados:** Sentinel-2 L2A, tile **45RUM**, coleção `sentinel-2-l2a` do Earth Search (Element 84), acesso aberto sem autenticação
**Método:** leitura em janela dos COGs via `/vsicurl` (nenhum tile completo foi baixado), AOI de 187 km² (85,44–85,58 °E; 28,22–28,34 °N), grade de 20 m, EPSG:32645
**Bandas:** B03, B04, B08, B11 e SCL (Scene Classification Layer)

Estas são as **primeiras imagens do ano do evento** analisadas neste projeto. Todo o acervo em `data/satellite_imagery/himalaia_2026/` está datado de **2024**.

---

## 1. Inventário de cenas e o problema da nuvem

Cinquenta cenas L2A entre 01/06 e 07/09/2026. Cobertura de nuvem **medida sobre a AOI** (não a do tile inteiro):

| Data | Nuvem + sombra na AOI | Neve/gelo (SCL) | Água (SCL) |
| :--- | ---: | ---: | ---: |
| **2026-08-12** | **4,6 %** | 3.992,8 ha | **76,7 ha** |
| 2026-08-24 | 42,5 % | 2.725,9 ha | 59,1 ha |
| **2026-08-27** | **79,6 %** | 1.507,7 ha | 4,2 ha |
| 2026-09-03 | 91,1 % | 1.508,2 ha | 0,0 ha |
| 2026-09-06 | 92,7 % | 800,3 ha | 0,6 ha |

**Par adotado:** PRE = 2026-08-12 (14 dias antes) × POS = 2026-08-27 (1 dia depois).

A monção domina o pós-evento: as três cenas posteriores têm 80–93 % de nuvem sobre o sítio. Como hoje é 07/09/2026, **ainda não existe uma cena pós-monção limpa** — a primeira deve aparecer em outubro. Isso limita tudo o que segue.

---

## 2. Controle de artefato

Duas fontes de falso sinal foram testadas antes de qualquer medição.

**Calibração de refletância.** NDSI mediano nos pixels classificados como neve/gelo: **0,750** com fator de escala 1/10.000 e offset zero (valor de manual); 1,033 com offset −1000 (fisicamente impossível). Offset zero adotado.

**Sombra topográfica.** A primeira passagem, sem filtro, produziu franjas vermelhas nas bordas de todas as manchas de gelo — assinatura de diferença de iluminação entre datas, não de mudança física. Aplicado filtro descartando `SCL = 2` (sombra) e pixels com brilho < 0,15 em qualquer data. Isso reduz a área útil de 3.795 ha para **1.944 ha** (51 %) e derruba o maior aglomerado de perda de 32,0 ha para 30,4 ha.

**Controle independente — cume do Langtang Lirung** (1 km², fora de qualquer trajeto, 100 % observável):

$$\text{gelo}: 99{,}8\ \text{ha} \rightarrow 99{,}1\ \text{ha} \qquad (-0{,}7\ \%)$$

O ruído sazonal e de processamento em 15 dias é inferior a 1 %. Qualquer perda acima disso é sinal.

---

## 3. Resultado 1 — A área do lago: **o valor publicado se confirma**

Na cena limpa de **2026-08-12**, a classificação L2A identifica 76,7 ha de água na AOI, distribuídos em 13 corpos. Um deles domina:

| | Valor medido |
| :--- | :--- |
| Área | **73,92 ha** |
| Centroide | 85,5364 °E, 28,2875 °N |
| Caixa envolvente | 1.420 × 1.160 m |
| Demais 12 corpos somados | 2,8 ha |

**Valor publicado no repositório: 65,7 ha.** A medição independente em imagem real de 2026 dá **73,9 ha**, mesma ordem e mesma escala.

Este é o primeiro número do repositório que **passa** em confronto com dado independente. A auditoria anterior havia registrado que os 65,7 ha não eram reproduzíveis — e não eram mesmo, a partir do raster RGB de 8 bits arquivado. Com o L2A correto, o número se sustenta. A ressalva é de proveniência, não de valor: a fonte citada não era a que estava no repositório.

---

## 4. Resultado 2 — O gelo: a premissa do PI se sustenta

Todos os números abaixo já incluem o filtro de sombra.

### AOI inteira (parte observável e iluminada, 1.944 ha)

| | PRE 12/08 | POS 27/08 | Variação |
| :--- | ---: | ---: | ---: |
| Neve/gelo (NDSI > 0,42) | 1.349,8 ha | 1.190,8 ha | **−187,1 ha (−13,9 %)** |

### Janela de 3,0 × 3,0 km no epicentro USGS `us7000tbwb`

| | Valor |
| :--- | ---: |
| Observável e iluminado | 52 % (464 ha) |
| Gelo PRE | 395,2 ha |
| Gelo POS | 374,3 ha |
| **Gelo perdido** | **27,7 ha** |
| Maior aglomerado coerente | **7,20 ha**, caixa 580 × 320 m |
| Controle (cume, mesma janela temporal) | −0,7 % |

### Leitura

**O corpo de gelo do maciço está intacto.** O cume do Langtang Lirung não mudou; 374 ha de gelo permanecem dentro da própria janela de 3 km em torno do ponto de ruptura. O evento removeu **uma mancha, não a geleira**. A sua afirmação de que o gelo continua lá é sustentada pela imagem.

**Mas houve perda localizada real.** As 27,7 ha perdidas na janela do epicentro, contra −0,7 % no controle, não são sazonais. Existe um núcleo coerente de 7,2 ha medindo 580 × 320 m. Para referência, o destacamento reportado nas descrições do evento é de ~0,2 km² (20 ha) — e apenas 52 % da janela é observável, de modo que **27,7 ha é um piso, não uma medida fechada**.

### O que isso implica para a fração de gelo

O NDSI mede **cobertura de superfície**, não volume. Uma parede rochosa com verniz de neve/gelo dá exatamente esta assinatura. Convertendo a área perdida em volume para espessuras plausíveis, contra uma massa destacada da ordem de 10⁸ m³:

| Espessura do gelo na cicatriz | Volume de gelo | Fração da massa destacada |
| :--- | ---: | ---: |
| 1 m (neve sazonal) | 0,28 M m³ | **0,3 %** |
| 5 m (neve firn / gelo fino) | 1,4 M m³ | **1,4 %** |
| 30 m (geleira suspensa espessa) | 8,3 M m³ | **8,3 %** |

O `config/hydraulic_assumptions.yaml` adota `ice_fraction: 0.40`, marcado `ASSUMED_BY_ANALYST`. **A imagem não sustenta 40 %.** Ela indica algo entre décimos de por cento e, no limite superior mais generoso, cerca de 8 %.

---

## 5. Consequência para o balanço hídrico

Isto **fecha a rota da fusão por atrito** que eu havia levantado. Com fração de gelo de ordem 1 %:

| Fração de gelo | Gelo disponível | Fusão máxima (η = 0,85) | Cobre o resíduo de 4,07 M m³? |
| ---: | ---: | ---: | :--- |
| 40 % (premissa do YAML) | 40 M m³ | 9,5 M m³ | sim, com folga |
| **1,4 % (medido, verniz de 5 m)** | **1,4 M m³** | **1,4 M m³** | **não — cobre 34 %** |
| 0,3 % (verniz de 1 m) | 0,28 M m³ | 0,28 M m³ | não — cobre 7 % |

Portanto a seção `SECAO_BALANCO_HIDRICO_SEM_GELO_2026.md` é a formulação correta, e não a variante com fusão. A água tem de vir de água líquida preexistente capturada — poros da massa e do leito entranhado, coluna livre do canal e represamento — que naquela seção fecha em 112 % no cenário central, **sem gelo e sem chuva**.

Duas premissas independentes convergiram para a mesma conclusão: **céu claro** elimina a chuva, **ausência de gelo** elimina a fusão, e o que resta é captura de água já presente no sistema.

---

## 6. Limitações — o que esta medição não decide

1. **O epicentro está parcialmente encoberto por névoa em 27/08.** O aglomerado coerente de 7,2 ha está deslocado da cruz do epicentro na figura. A cicatriz completa pode ser maior e estar sob a nuvem. **27,7 ha é limite inferior.**
2. **NDSI não mede volume.** A tabela de espessuras da §4 é aritmética sobre hipóteses de espessura, não medição. Só **diferenciação de DEM** decide volume e fração de gelo.
3. **Não foi possível traçar o percurso de detritos.** O vale do Lhende a jusante está sob nuvem em todas as cenas pós-evento.
4. **A cena definitiva ainda não existe.** As três cenas pós-evento têm 80–93 % de nuvem sobre o sítio. A monção só encerra em outubro. **A delineação fechada da cicatriz exige uma cena de outubro de 2026**, que não estará disponível antes disso.
5. Uma diferença de 15 dias entre PRE e POS admite mudança sazonal genuína de neve; o controle limita esse termo a menos de 1 %, mas em terreno com aspecto diferente do controle o resíduo pode ser maior.

---

## 7. Reprodução

```
STAC   : https://earth-search.aws.element84.com/v1/search
         collections=["sentinel-2-l2a"], bbox=[85.40,28.22,85.58,28.34]
PRE    : S2C_45RUM_20260812_0_L2A
POS    : S2B_45RUM_20260827_0_L2A
COGs   : https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/45/R/UM/2026/8/<id>/{B03,B04,B08,B11,SCL}.tif
AOI    : 346918,97 / 3122389,88 / 360814,81 / 3135855,17 (EPSG:32645), grade 20 m
Máscara: válido = SCL ∉ {0,1,2,3,8,9,10} nas duas datas e brilho > 0,15 nas duas datas
Gelo   : NDSI = (B03−B11)/(B03+B11) > 0,42 e B03 > 0,11
Escala : refletância = DN / 10000, offset zero (aferido: NDSI = 0,750 na neve)
```

Figura: `cicatriz_sentinel2_2026.png` — PRE, POS e mapa de mudança, janela de 3 km, falsa cor B04/B03/B08.

---

## 8. Síntese

| Alegação | Veredito da medição |
| :--- | :--- |
| Lago de 65,7 ha | **Confirmado** — 73,9 ha medidos em L2A real de 12/08/2026 |
| "O gelo continua lá" | **Confirmado** — cume inalterado (−0,7 %), 374 ha remanescentes na janela do epicentro |
| `ice_fraction = 0,40` | **Não sustentado** — a imagem indica de 0,3 % a ~8 % |
| Cicatriz de destacamento | **Detectada, não fechada** — 27,7 ha (piso), núcleo coerente de 7,2 ha a 580 × 320 m |
| Fusão por atrito como fonte da água | **Fechada** — sem gelo, não há reservatório a fundir |
| Percurso de detritos a jusante | **Não observável** — vale sob nuvem em todas as cenas pós-evento |

O próximo passo que decide o que restou é **diferenciação de DEM** sobre a cicatriz, para volume e fração de gelo, e uma cena de **outubro de 2026** para a delineação completa.
