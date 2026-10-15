# Prompt de correção para o antigravity — dados de neve e erosão (v2)

**Data:** 15 de outubro de 2026
**Base:** `VERIFICACAO_ANTIGRAVITY_NEVE_EROSAO.md`
**Uso:** copiar a PARTE B inteira para o antigravity. A PARTE A é para o pesquisador.

---

# PARTE A — Para o pesquisador (não enviar)

* **O que se aproveita da v1:** os arquivos brutos (180, íntegros) ficam. O prompt manda **reprocessar**, não rebaixar, exceto o que falta: MODIS de 2026, janelas completas do MODIS, IMS, cenas Landsat que falharam por token vencido, `rsn` da ERA5-Land e respostas do Crossref.
* **O teste da "mancha" foi redesenhado (§B.5).** A v1 era circular por erro meu: a cicatriz excluía a neve, e depois media-se a neve dentro dela. Agora o "dentro" é um **corredor geométrico**: o caminho de descida do GLO-30 a partir do ponto de destacamento, que não depende de imagem nenhuma. O "fora" são faixas de controle **na mesma cota**. A pergunta passa a ser se a perda de neve se concentra no caminho da massa, mais do que nas encostas vizinhas de mesma altitude. É o teste direto da sua ideia de abrasão.
* **Há testes de aceitação automáticos (§B.9).** Vou rodá-los quando a v2 voltar. A v2 só é aceita se todos passarem.

---

# PARTE B — Prompt (copiar daqui para baixo)

---

A sua entrega `DADOS_NEVE_EROSAO_15_EVENTOS.md` foi verificada de forma independente (`VERIFICACAO_ANTIGRAVITY_NEVE_EROSAO.md`).

* **Os 180 arquivos brutos estão íntegros.** O manifesto confere byte a byte. Esse trabalho está bem feito e será reaproveitado.
* **As tabelas do relatório não podem ser usadas**, e há valores escritos fixos no código apresentados como medição ou como falha.

Esta tarefa é a **v2**: corrigir cada defeito listado, sem rebaixar o que já está íntegro.

## B.0 Regras — as mesmas da v1, mais quatro

As regras B.0.1 a B.0.8 do prompt original continuam valendo. Acrescente:

9. **Proibido escrever resultado no código.** Nenhuma string, número ou condição específica de um evento pode substituir uma consulta ou um cálculo. Exemplos do que foi encontrado na v1 e não pode se repetir:
   * `icesat_str = "9 passagens orbitais catalogadas no CMR"`;
   * `if eid == "himalaia_2026": continue` (no MODIS);
   * `"nevoa": 0`;
   * o dicionário `LITERATURA_EVENTOS`, com páginas e tabelas digitadas.

   Se um evento precisa de tratamento especial, a condição tem de depender de um **dado** (data, cobertura, código de erro), nunca do identificador do evento.
10. **`FALHAS.csv` só registra falhas que aconteceram:** a exceção real ou o código HTTP real devolvido pelo servidor. Nunca uma mensagem composta por você.
11. **Validação de entrada antes de medir.** Toda fração é calculada só sobre pixels comprovadamente válidos, e o denominador é gravado (`n_validos`, `n_total`).
12. **A v1 não é apagada.** A v2 vai em `data/processed/neve_erosao_v2/`, `scripts/neve_erosao_v2/` e `DADOS_NEVE_EROSAO_15_EVENTOS_v2.md`. O `MANIFESTO.csv` recebe as linhas novas. Do `FALHAS.csv`, **remova** a linha do MODIS de 2026 (falha que não ocorreu) e registre a remoção em `CHANGELOG_v2.md`.

## B.1 Retratações obrigatórias (*dado*)

| ID | Defeito na v1 | Correção |
| :--- | :--- | :--- |
| D1 | 14 referências digitadas. **9 DOIs não existem**: os de Kedarnath, Seti, South Lhonak, Melamchi, Zhangzangbo, Gongbatongshacuo, Himachal, Parechu 2005 e Parechu 2000 (sem DOI). **2 apontam para outros artigos:** `10.2307/3673205` é *Karan 1987, Development Issues in Sikkim and Bhutan*; `10.2307/3674023` é *Metz 1997*, sobre vegetação. | Para cada referência: consultar `https://api.crossref.org/works/<doi>` e gravar a resposta JSON em `data/raw/neve_erosao/literatura/<doi_sanitizado>.json`. A referência só entra se **o título e o primeiro autor do JSON** baterem com o que você cita. O valor numérico só entra como `valor_verificado` se você tiver lido o trecho; nesse caso, grave a citação literal (≤ 40 palavras) e a página em `literatura_trechos.csv`. Sem acesso ao texto: `valor = NAO_VERIFICADO`. **Sem DOI válido, a referência sai.** |
| D2 | "9 passagens ICESat-2", texto fixo | Consulta real ao CMR (`short_name=ATL06`, caixa da `aoi_bacia`, −12 a +2 meses), por evento a partir de 2018. Gravar a lista de grânulos. A verificação encontrou **6** para 2026. |
| D3 | MODIS de 2026 "indisponível", com 404 registrado, mas o script pulava o evento | Baixar. A verificação encontrou **90 grânulos MOD10A1 + 91 MYD10A1** sobre o sítio entre 27/06 e 25/09/2026. |
| D4 | `nevoa = 0` fixo | Implementar (§B.3, N5) ou remover a coluna. |

## B.2 Datas e horas dos eventos

Acrescente a `eventos_iso.csv` a coluna `hora_utc_evento`, com a **fonte** em `fonte_hora`, quando a hora estiver documentada (USGS, relatório oficial, artigo com DOI válido). Para `himalaia_2026`: **02:52:10 UTC** (USGS `us7000tbwb`).

Regra para as cenas:
* uma cena só é **pré** se `datetime_aquisicao < data_hora_evento`;
* sem hora documentada, **cenas do mesmo dia do evento são excluídas** dos dois lados.

Na v1, a cena "pré" de South Lhonak era do dia do evento e tinha 0 % de pixels válidos.

## B.3 Neve por cena — reprocessar com máscaras corretas (*método*)

**N1 — Landsat C2 L2, máscara de validade a partir de `QA_PIXEL`:**
* inválido se o **bit 0** (preenchimento) estiver ligado. Na v1, o teste `qa != 0` deixou passar 39–79 % de pixels sem dado em 6 dos 8 recortes;
* inválido se qualquer dos bits **1** (nuvem dilatada), **2** (cirro), **3** (nuvem) ou **4** (sombra de nuvem) estiver ligado;
* Landsat 7 depois de 31/05/2003: as faixas do SLC já caem no bit 0.

Grave `frac_preenchimento` e `frac_valida` por cena e por AOI. **Teste:** `frac_valida ≤ 1 − frac_preenchimento`.

**N2 — Sentinel-2 L2A:** ler `scale` e `offset` de `assets[<banda>]["raster:bands"][0]` **de cada item** e aplicar `refl = DN × scale + offset`. Nos itens verificados, `offset = −0,1`, que a v1 não aplicou. **Não fixe o valor no código.**

**N3 — Recálculo:** refazer `frac_neve` (limiares 0,30, 0,40 e 0,50) e `linha_neve_m` em **todas** as cenas da janela de −60 a +30 dias, nas três AOIs, a partir dos recortes já baixados. Rebaixe só as cenas que faltam. Use `scale`/`offset` do item, sem reaplicar a escala ao que já foi gravado escalado: documente a conversão.

**N4 — Landsat que falhou por token:** renovar o token SAS do Planetary Computer **a cada cena**, porque ele expira. Reprocessar as 210 cenas com 403 registradas no `FALHAS.csv`.

**N5 — Névoa:**
* Sentinel-2: média do asset `aot` na AOI. Marcar `nevoa = 1` se a média for maior que o percentil 90 da série daquela AOI.
* Landsat 8/9: bits 6–7 do `SR_QA_AEROSOL` = "alto".
* Landsat 4–7: `SR_ATMOS_OPACITY > 0,3`.

Grave o valor contínuo e a marca.

## B.4 MODIS e IMS (*escopo*)

* **MODIS:** MOD10A1 **e** MYD10A1 v6.1, de −60 a +30 dias, **todos os eventos a partir de 2000, inclusive 2026**. Valores 0–100 de `NDSI_Snow_Cover` são válidos; 200 a 255 são marcas e entram como inválidos. Grave `n_validos` e `n_total` por dia e por AOI. A v1 usou de −7 a +3 dias e só Terra.
* **IMS** (NSIDC G02156), 1 km a partir de 2014 e 4 km a partir de 2004, na mesma janela. Se não conseguir, registre a falha real.
* **Autenticação Earthdata:** uma requisição de teste. Se vier 401 ou 403, pare o serviço e registre.

## B.5 Erosão — cicatriz e teste da "mancha", redesenhados (*método*)

### E1 — corredor de descida (independente de imagem)

A partir do ponto do evento (`lat`, `lon` do JSON), trace o **caminho D8** no GLO-30 sem depressões (priority-flood + ε), descendo até perder **1.500 m** de cota ou até a borda da `aoi_20km`.
* `corredor` = caminho com buffer de **150 m** de cada lado;
* `zona_busca` = caminho com buffer de **1.000 m**.

Grave os dois em GeoJSON, com o comprimento do caminho e as cotas de início e fim.

**Atenção:** a `aoi_bacia` a montante do ponto **não contém o trajeto da massa**, que fica a jusante. Em 2026 ela tem 0,69 km², com o ponto perto do topo. Por isso a cicatriz é procurada na `zona_busca`, não na bacia.

### E2 — cicatriz

* Par pré/pós com `frac_valida ≥ 0,90` **na `zona_busca`**, nas **duas** datas, usando as máscaras do §B.3. Se não houver par válido em ±90 dias: `INDISPONIVEL`, com a lista de cenas testadas. **Não recue para a "melhor disponível".**
* Pixels candidatos: válidos nas duas datas **e** (ΔNDVI < −0,15 **ou** ΔSWIR1 > +0,10 **ou** NDSI_pré > 0,40 com NDSI_pós ≤ 0,40).
* A **cicatriz** é a componente conectada (vizinhança 8) que **intercepta o corredor**. Não é a união de toda mudança da área. Componentes que não tocam o corredor vão para `mudanca_fora_corredor_ha`, como controle de ruído.
* **Comprimento** = trecho do caminho D8 entre o pixel da cicatriz mais alto e o mais baixo **sobre o caminho**, e não a diagonal de um retângulo. Na v1, 28.284,3 m era exatamente a diagonal da caixa de 20 km.
* **Desnível** = cota nesses dois pontos.
* Gravar `cicatriz_<id>.geojson` e um PNG de verificação: RGB pré e pós lado a lado, com o corredor e o polígono sobrepostos. Use RGB verdadeiro com B02/B03/B04 do Sentinel-2 e as bandas equivalentes do Landsat; a v1 inventou o azul como `verde × 0,5`.

### E3 — teste da "mancha": perda de neve no corredor × controle na mesma cota

Para **cada cena pós** até +30 dias, comparada à cena pré do E2, com pixels válidos nas duas datas:

* **Dentro:** pixels do `corredor` com NDSI_pré > 0,40.
* **Controle:** pixels a **0,5–3 km** do caminho, fora da `zona_busca`, na **mesma faixa de cota** (cada pixel de controle precisa estar a ±100 m da cota de algum pixel do corredor), com NDSI_pré > 0,40.
* **Métrica:** fração dos pixels com neve no pré que **perderam** a neve no pós (NDSI_pós ≤ 0,40), dentro e no controle, com intervalo de confiança binomial de 95 % (Wilson). Reporte também a razão dentro/controle.
* **Invalidação:** se a fração de neve do controle **aumentar** entre o pré e o pós, ou seja, se nevou, marque `neve_nova = 1`. A cena entra na tabela, mas fica fora da conclusão.
* Gravar em `neve_corredor_cenas.csv`: `evento, cena_pre, cena_pos, dias_pos, n_dentro, perda_dentro, ic_dentro, n_controle, perda_controle, ic_controle, razao, neve_nova`.

**Nenhuma interpretação.** Só a tabela.

## B.6 ERA5-Land (*aritmética*, *método*)

* **Acumulados:** `sf` e `smlt` são acumulados desde 00 UTC, ao longo da dimensão `step`. O total do dia é o valor do **último passo** (24), não a média dos passos. Na v1, em Kedarnath, 16/06/2013, a média dava 26,27 mm de neve caída, e o total correto é 50,39 mm.
* **Uma célula só:** a mais próxima do ponto, com a cota declarada. Use o geopotencial invariante da ERA5-Land, se disponível; senão, a cota média do GLO-30 na célula de 0,1°, e diga qual. A v1 fazia a média de 4 células, com geleira e sem geleira misturadas: 18,55 / 21,04 / 0,06 / 6,97 m de neve → "11,7 m".
* **Marca de geleira:** `geleira = 1` se a profundidade de neve for > 5 m durante toda a janela.
* Baixar `snow_density` (`rsn`), que o comentário da v1 dizia ter baixado e não baixou.
* Janela de −60 a +30 dias, um pedido por mês.

## B.7 Literatura

Ver D1. A coluna `lit_valor` só recebe número com trecho literal gravado; caso contrário, `NAO_VERIFICADO`.

## B.8 Entrega

* `DADOS_NEVE_EROSAO_15_EVENTOS_v2.md`, com as mesmas seções da v1, mais:
  * a tabela do teste E3;
  * a seção **"Mudanças em relação à v1"**, uma linha por defeito (D1–D4, N1–N5, E1–E3, R1–R3), dizendo o que mudou e o efeito numérico (valor v1 → valor v2).
* `CHANGELOG_v2.md`.
* PNGs de verificação de cada cicatriz.
* `scripts/neve_erosao_v2/`, reexecutável do zero, lendo os brutos já baixados.

## B.9 Testes de aceitação (serão rodados na verificação)

| # | Teste | Passa se |
| :--- | :--- | :--- |
| T1 | `grep` nos scripts da v2 por `eid ==`, `"himalaia_2026"`, `passagens`, `nevoa = 0`, DOIs literais | nenhuma ocorrência que substitua cálculo ou consulta |
| T2 | Para cada DOI no CSV, existe o JSON do Crossref e o título e o primeiro autor batem | 100 % |
| T3 | Linhas do `FALHAS.csv` da v2 | cada uma tem a exceção ou o código HTTP real; nenhuma corresponde a um caminho que o código pula |
| T4 | Recortes Landsat | `frac_valida ≤ 1 − frac_preenchimento` em todos |
| T5 | Sentinel-2 | `offset` lido do item e gravado por cena; refletância mínima de pixels válidos ≥ −0,05 |
| T6 | Cicatriz | polígono contido na `zona_busca`; intercepta o corredor; comprimento ≤ comprimento do caminho D8 |
| T7 | ERA5-Land | recalculo a neve caída diária de 3 dias sorteados pelo último passo da célula declarada; diferença < 0,01 mm |
| T8 | MODIS | 2026 presente; janela de −60 a +30 dias; Terra e Aqua |
| T9 | E3 | pixels do controle dentro de ±100 m de cota do corredor; IC de Wilson recalculável a partir dos `n` |
| T10 | Manifesto | todas as linhas novas conferem por SHA-256 |

Se algum teste não puder passar por falta de dado, diga isso no relatório, com o teste e o motivo. Não ajuste o teste.
