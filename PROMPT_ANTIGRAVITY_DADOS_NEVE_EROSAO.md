# Prompt para o antigravity — coleta de dados de NEVE e EROSÃO, 15 eventos

**Data:** 13 de outubro de 2026
**Uso:** copiar a PARTE B inteira para o antigravity. A PARTE A é para o pesquisador.

---

# PARTE A — Para o pesquisador (não enviar)

O prompt pede **só coleta e medição padronizada**: baixar, guardar, medir com limiares declarados, registrar a proveniência. Ele proíbe interpretação sobre a hipótese do toró. O motivo é o histórico das três rodadas anteriores: os números inventados apareceram justamente quando coleta e interpretação andavam juntas.

Cada número que voltar terá de apontar para um arquivo em `data/raw/` com SHA-256. A §B.8 lista o que vou checar. Quando o antigravity entregar, peça a verificação e eu rebaixo uma amostra dos arquivos para comparar.

Duas perguntas suas que o prompt prepara, sem responder:

* **Neve:** havia acúmulo de neve ou gelo (rima) sobre o anfiteatro nos dias anteriores a cada evento? A linha de neve desceu? Quanto nevou na ERA5-Land?
* **Erosão:** qual a área, o comprimento e a forma da cicatriz em cada evento? A neve foi removida dentro da cicatriz (a "mancha" abrasiva) e permaneceu fora dela?

---

# PARTE B — Prompt (copiar daqui para baixo)

---

Você vai **reunir dados de satélite e reanálise sobre neve e erosão** para os 15 eventos do repositório `Himalaia_2026`. Esta tarefa é **só de coleta e medição padronizada**. Não escreva conclusões sobre mecanismo, hipótese, toró, Jz ou eletricidade. Uma auditoria independente vai rebaixar uma amostra dos seus arquivos e recalcular uma amostra dos seus números.

## B.0 Regras invioláveis

1. **Nenhum número sem arquivo.** Todo valor que aparecer em CSV, JSON ou relatório precisa vir de um arquivo baixado e guardado em `data/raw/`, com linha no manifesto (§B.6). Se não houver arquivo, a célula fica `INDISPONIVEL`, e o motivo vai para `data/raw/FALHAS.csv` (URL, código HTTP, mensagem, data e hora).
2. **Proibido estimar, interpolar entre eventos, "completar com valores típicos" ou usar a literatura como se fosse medição.** Volume ou área de artigo entra numa coluna separada, `literatura`, com DOI e página ou tabela. Nunca na coluna `medido`.
3. **Não altere** nenhum arquivo existente do repositório, exceto para acrescentar linhas novas ao manifesto. Saídas novas vão em `data/raw/neve_erosao/`, `data/processed/neve_erosao/` e `scripts/neve_erosao/`.
4. **Credenciais:** leia apenas dos arquivos já configurados (`~/.netrc`, `~/.earthdata_token.txt`, `~/.cdsapirc`). Nunca imprima, registre em log nem grave token ou senha em arquivo do repositório. Não crie contas.
5. **Autenticação:** antes de baixar em lote, faça **uma** requisição de teste por serviço. Se vier 401 ou 403, **pare aquele serviço** e registre a falha. Repetir tentativas bloqueia a conta (já aconteceu com a Earthdata neste projeto).
6. **Datas:** o arquivo de eventos tem datas por extenso em português. Primeiro gere `data/processed/neve_erosao/eventos_iso.csv` com `id, data_iso_inicio, data_iso_fim, lat, lon, fonte_coordenada`. Eventos de duas datas (Aru 2016: 17/07 e 21/09) ficam em **duas linhas**. Kedarnath (16–17/06/2013) e Himachal (9–11/07/2023) têm intervalo, e as janelas da §B.2 contam a partir do **início**.
7. **Coordenadas:** use as de `data/himalayan_events_1980_2026.json`, campos `lat` e `lon`. Elas **não estão verificadas**. Não as corrija. Se a cicatriz visível na imagem estiver a mais de 2 km do ponto, registre a distância e a coordenada da cicatriz em `coordenada_cicatriz_obs`, sem substituir a original.
8. **Todo script tem de rodar de novo** do zero e reproduzir os mesmos números: `python scripts/neve_erosao/<script>.py`.

## B.1 Áreas de interesse (AOI)

Para cada evento, três recortes, todos em UTM da zona local e salvos em GeoJSON em `data/processed/neve_erosao/aoi/`:

* `aoi_20km`: quadrado de 20 × 20 km centrado no ponto do evento.
* `aoi_bacia`: bacia a montante do ponto, delineada no Copernicus GLO-30 (priority-flood + D8; o método já está em `ANALISE_DEM_GLO30_E_AUSENCIA_DE_LAGO.md`). Registre a área em km².
* `aoi_zona_fonte`: os pixels da bacia acima da cota do ponto de destacamento, se houver cota publicada. Se não houver, use os 20 % mais altos da bacia e **diga** que foi esse o critério.

## B.2 Bloco NEVE

Janela: de **−60 a +30 dias** do evento (os produtos diários) e **todas as cenas ópticas** da janela.

| # | Produto | Acesso | Variável | Para quais eventos |
| :--- | :--- | :--- | :--- | :--- |
| N1 | **MODIS MOD10A1 + MYD10A1 v6.1**, 500 m, diário | NSIDC / Earthdata (CMR) | `NDSI_Snow_Cover`, `NDSI_Snow_Cover_Basic_QA` | 2000 em diante |
| N2 | **Sentinel-2 L2A** | Earth Search STAC (aberto) | B03, B08, B11, SCL; metadado de elevação solar | 2016 em diante |
| N3 | **Landsat 5/7/8/9 Collection 2 Level-2** | USGS / Planetary Computer STAC (aberto) | SR verde, NIR, SWIR1; QA_PIXEL | todos com cena; essencial antes de 2016 |
| N4 | **ERA5-Land horária**, ponto do evento | CDS (uma requisição por mês) | `sd` (profundidade de neve), `sf` (neve caída), `smlt` (fusão), `rsn` (densidade), `t2m` | 1981 em diante (ERA5-Land começa em 1950) |
| N5 | **IMS** 1 km (de 2014) / 4 km (de 2004), diário | NSIDC G02156 | máscara de neve | 2004 em diante |
| N6 | Sentinel-1 GRD IW, VV/VH (neve úmida) | ASF / Earthdata | σ⁰ | opcional, 2015 em diante |

**Medidas obrigatórias por cena óptica (N2, N3)**, para cada uma das três AOIs:

* `frac_valida`: fração de pixels sem nuvem nem sombra de nuvem, **medida dentro da AOI**. A nebulosidade da cena inteira não serve.
* `frac_neve`: fração de pixels válidos com NDSI > 0,40 **e** NIR > 0,11. Grave também a fração com os limiares 0,30 e 0,50, para medir a sensibilidade.
* `linha_neve_m`: a cota (GLO-30) acima da qual ≥ 50 % dos pixels válidos são neve, em faixas de 100 m.
* `elev_solar_graus`: elevação solar, do metadado da cena.

**Cuidados já aprendidos neste projeto. São obrigatórios:**

* A camada SCL do Sentinel-2 **classifica neve em sombra topográfica como água** (classe 6). Uma "área de lago" de 73,9 ha já foi publicada por esse erro. Não use SCL = 6 como água em pixels com NDSI > 0,40 ou com sombra topográfica (calcule o *hillshade* com o ângulo solar da cena).
* **Névoa e neblina rebaixam o NDSI.** Uma "perda de gelo" de 27,7 ha já foi medida assim. Cena com B01 (aerossol) acima do percentil 90 da série da AOI fica marcada como `nevoa=1` e entra em separado.
* Não compare cenas com elevação solar diferente em mais de 10° sem marcar isso.

**Saídas:**

* `data/processed/neve_erosao/neve_cenas.csv`: uma linha por evento × cena × AOI.
* `data/processed/neve_erosao/neve_modis_diario.csv`: uma linha por evento × dia × AOI.
* `data/processed/neve_erosao/era5land_<id>.csv`: série horária de cada evento.

## B.3 Bloco EROSÃO

Para cada evento:

**E1 — Par pré/pós.** Escolha a cena válida **mais próxima antes** e **mais próxima depois**, com `frac_valida` ≥ 0,90 na `aoi_bacia`. Grave os recortes (GeoTIFF, todas as bandas usadas) e um PNG RGB com nome `<id>_<S2|L8|...>_<AAAA-MM-DD>_<pre|pos>.png`. Se não houver par válido em ±90 dias, registre `INDISPONIVEL` com a lista de cenas testadas e a `frac_valida` de cada uma.

**E2 — Cicatriz.** Mapeie a mudança do pré para o pós com **limiares declarados no código**:

* ΔNDVI < −0,15 **ou** Δ(brilho no SWIR1) > 0,10;
* exclua pixels que são neve em qualquer das duas datas (NDSI > 0,40). Esses vão para uma classe separada, `mudanca_em_neve`;
* exclua corpos d'água estáveis;
* remova polígonos menores que 0,5 ha.

Exporte em `data/processed/neve_erosao/cicatriz_<id>.geojson`. Meça:

* `area_cicatriz_ha`;
* `comprimento_m`: ao longo do caminho D8 do GLO-30, do pixel mais alto ao mais baixo da cicatriz;
* `desnivel_m`;
* `largura_media_m` = área / comprimento;
* `area_mudanca_em_neve_ha`: neve presente no pré e ausente no pós, **dentro** e **fora** da cicatriz, em colunas separadas.

**E3 — Neve dentro × fora da cicatriz.** Para a pergunta da "mancha": em todas as cenas pós-evento até +30 dias, calcule `frac_neve` dentro do polígono da cicatriz e numa faixa de 500 m ao redor dele, **na mesma faixa de cota**. Tabela por cena.

**E4 — Modelos digitais de elevação.**

* **Copernicus GLO-30** é a base, mas é **pré-evento só para os eventos depois de 2015** (as aquisições do TanDEM-X são de 2011–2015). Registre isso por evento.
* Para eventos antes de 2011, liste se existe DEM anterior: SRTM (fevereiro de 2000), ASTER GDEM. **Não** faça diferença de DEMs de datas desconhecidas.
* **Não existe DEM aberto pós-2026** para a região. Não fabrique um. Liste as passagens do **ICESat-2 ATL06** que cruzam a `aoi_bacia` de −12 a +2 meses do evento (granule ID, data, número de pontos dentro da AOI), sem calcular volume.

**E5 — Literatura.** Para cada evento, até 3 referências com área ou volume erodido, depositado ou mobilizado: DOI, página, tabela ou figura, valor, unidade e método (campo, DEM, sísmica, óptico). Coluna `literatura`, nunca `medido`. **Se não encontrar o DOI, não inclua a referência.**

**Saída:** `data/processed/neve_erosao/erosao_eventos.csv`, uma linha por evento, com as colunas acima mais `cena_pre`, `cena_pos`, `dias_pre`, `dias_pos`.

## B.4 Casos que exigem atenção

* **2026 (Lhende Khola):** já existe o par Sentinel-2 L2A `2026-08-12` × `2026-08-27`, tile **45RUM** (ver `MEDICAO_SENTINEL2_2026_CICATRIZ_E_LAGO.md`). A conclusão de "lago confirmado" desse relatório **foi corrigida depois**: era neve sombreada (ver `ANALISE_DEM_GLO30_E_AUSENCIA_DE_LAGO.md`). Rebaixe as cenas, não reutilize as áreas daquele relatório e procure cenas válidas de setembro e outubro de 2026.
* **Eventos de 1981, 1985, 1994 e 2000:** só Landsat 4/5 (16 dias, falhas) e eventualmente nada. `INDISPONIVEL` é resposta aceitável e esperada.
* **Landsat 7 depois de 31/05/2003:** falha do SLC. Os pixels com faixa ausente contam como inválidos.
* **Chamoli 2021 (fevereiro):** inverno, sombra forte. Marque a elevação solar.

## B.5 O que NÃO fazer

* Não escrever seção de "Discussão", "Implicações" ou "Mecanismo".
* Não ordenar os eventos por "força" ou "evidência".
* Não preencher lacunas com valores de outro evento.
* Não usar imagens do Google Earth, prints de notícia ou vídeo como dado.
* Não rodar o modelo atmosférico nem o hidráulico.
* Não alterar `config/hydraulic_assumptions.yaml` nem os JSON de eventos.

## B.6 Manifesto (obrigatório)

`data/raw/neve_erosao/MANIFESTO.csv`, uma linha por arquivo baixado:

```
arquivo_local, sha256, bytes, fonte, url_ou_id_granulo, data_aquisicao_produto, data_hora_download_utc, evento_id, script
```

O SHA-256 é calculado **sobre o arquivo como baixado**, antes de qualquer conversão. Se você recortar o arquivo no próprio download (OPeNDAP, GDAL `/vsicurl`), grave o recorte e diga isso na coluna `fonte`.

Também obrigatórios:

* `data/raw/FALHAS.csv`: toda requisição que falhou;
* `scripts/neve_erosao/AMBIENTE.txt`: versões de Python, GDAL, numpy, pystac-client e das bibliotecas usadas.

## B.7 Entrega

Um relatório `DADOS_NEVE_EROSAO_15_EVENTOS.md` só com:

1. a tabela de disponibilidade por evento × produto (`OK` / `PARCIAL` / `INDISPONIVEL`), com o motivo;
2. as tabelas-resumo de `neve_cenas.csv` (só a cena pré mais próxima e a pós mais próxima) e de `erosao_eventos.csv`;
3. a lista de PNGs gerados;
4. a contagem de arquivos e bytes do manifesto.

**Sem interpretação.** Cada número da tabela tem de ser rastreável a uma linha do CSV, e cada linha do CSV a arquivos do manifesto.

## B.8 Como a entrega será verificada

* Sorteio de 5 linhas do manifesto: o arquivo é rebaixado da URL registrada e o SHA-256 comparado.
* Sorteio de 3 medidas de `neve_cenas.csv` e 2 de `erosao_eventos.csv`: recálculo independente a partir do raw.
* Os PNGs pré/pós são conferidos contra a data no metadado da cena.
* Qualquer número que não tenha arquivo correspondente invalida a tabela inteira em que aparece.
