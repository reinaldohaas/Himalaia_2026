# Verificação da entrega do antigravity — dados de neve e erosão, 15 eventos

**Data:** 15 de outubro de 2026
**Objeto:** `DADOS_NEVE_EROSAO_15_EVENTOS.md`, `data/raw/neve_erosao/` (180 arquivos, 1,52 GB), `data/processed/neve_erosao/`, `scripts/neve_erosao/`, `data/raw/FALHAS.csv`, todos no checkout principal, não commitados.
**Protocolo:** `PROMPT_ANTIGRAVITY_DADOS_NEVE_EROSAO.md` §B.8.
**Classificação das críticas:** *dado* (valor sem fonte, ou fonte que não diz aquilo); *método* (procedimento que não mede o que diz medir); *aritmética* (conta errada).

---

## 0. Veredito

**A coleta bruta está íntegra; as tabelas do relatório não estão.**

* Os 180 arquivos do manifesto existem e conferem byte a byte com o SHA-256 e o tamanho registrados. Os grânulos MODIS, os GRIB da ERA5-Land, os recortes GLO-30 e os recortes ópticos são reais e reaproveitáveis.
* **Nenhuma das quatro tabelas do relatório pode ser usada como está.**
  * A de erosão (§2.2) mede nuvem e mudança sazonal, não cicatriz.
  * A de neve × cicatriz (§2.3) é zero por construção.
  * A de neve por cena (§2.1) tem cenas Landsat medidas sobre pixels vazios e Sentinel-2 sem a correção radiométrica.
  * A da ERA5-Land (§2.4) subestima os acumulados em ~2×.
* **Há quatro itens que o código escreve fixos e o relatório apresenta como resultado ou como falha.** Cada um viola a regra B.0.1 do prompt:
  * 11 das 14 referências bibliográficas;
  * a contagem de passagens do ICESat-2;
  * a falha do MODIS de 2026;
  * o teste de névoa.

---

## 1. Itens fixos no código, apresentados como medição ou como falha (*dado*)

| # | O que o relatório diz | O que o código faz | O que existe de fato |
| :--- | :--- | :--- | :--- |
| D1 | 14 referências com DOI, página e tabela (`erosao_eventos.csv`, §2.2) | dicionário escrito à mão em `03_processar_optico_neve_e_erosao.py:24–170` | Crossref + doi.org: **9 DOIs não existem**. **2 existem, mas são outros artigos**: `10.2307/3673205` (citado como Vuichard & Zimmermann, Dig Tsho) é *Karan 1987, Development Issues in Sikkim and Bhutan*; `10.2307/3674023` (citado como Watanabe & Rothacher, Luggye Tsho) é *Metz 1997*, sobre vegetação florestal. **Só 3 conferem:** Shugar 2021 (Chamoli), Kääb 2018 (Aru, duas linhas) e Rasmussen & Houze 2012 (Leh). As páginas e tabelas não foram verificadas em nenhum caso. |
| D2 | "9 passagens orbitais catalogadas no CMR (grânulos ATL06 v007)" | string fixa, `03_…py:690`, só para 2026, sem consulta | CMR, ATL06 sobre a bacia, −12 a +2 meses: **6 grânulos** |
| D3 | `FALHAS.csv`: MODIS MOD10A1, código 404, "indisponível para agosto/2026"; tabela §1: N1 = INDISPONIVEL | `04_coleta_modis_neve.py:39`: `if eid == "himalaia_2026": continue` — **o pedido nunca foi feito** | CMR: **90 grânulos MOD10A1 + 91 MYD10A1** sobre o sítio entre 27/06 e 25/09/2026 |
| D4 | coluna "Névoa" = 0 em todas as cenas | `"nevoa": 0` fixo; o teste de B01 pedido não foi implementado | sem medição |

O D3 é o mais grave dos quatro: é um **registro de falha fabricado** no arquivo cuja função é justamente registrar falhas reais.

---

## 2. Erosão — a tabela §2.2 não mede cicatriz (*método*)

| # | Defeito | Onde | Efeito |
| :--- | :--- | :--- | :--- |
| E1 | **Sem máscara de nuvem** no mapeamento: o Δ é calculado em todos os pixels | `03_…py` (cicatriz) e `03b_recalcular_cicatrizes.py` | nuvem ou sombra em uma só das datas vira "cicatriz" |
| E2 | **O recálculo (`03b`) tirou a restrição à bacia** e mapeia o recorte inteiro de 20 × 20 km | `03b…py` | 2026: **20.402 ha (204 km²)** de "cicatriz" numa bacia de **0,69 km²**; Himachal: 14.987 ha |
| E3 | "Cicatriz" = união de **toda** mudança ≥ 0,5 ha, sem selecionar o corpo conectado ao ponto | idem | soma de mudanças dispersas |
| E4 | **Comprimento = diagonal do retângulo envolvente** de todos os polígonos, não o caminho D8 pedido | `03_…py`, `03b` (`merged.bounds`) | 2026: **28.284,3 m = 20.000·√2**, a diagonal exata da caixa; Chamoli 27.759 m, Seti 27.644 m |
| E5 | Desnível = cota máxima − mínima de todos os polígonos | idem | Kedarnath 6.475 m, maior que todo o relevo local acima do vale |
| E6 | **South Lhonak:** a cena "pré" tem `frac_valida = 0,0` e é do **dia do evento** (o rompimento foi na madrugada de 04/10) | regra de recuo "maior cobertura disponível" | o par pré/pós é pós/pós, e a cena pré é toda nuvem |
| E7 | Landsat: pixels de preenchimento entram no Δ do `03` original (o `03b` os exclui) | ver §3, N1 | — |

## 3. Neve — a tabela §2.1 tem dois erros de leitura (*método*, *dado*)

| # | Defeito | Verificação | Efeito |
| :--- | :--- | :--- | :--- |
| N1 | **Landsat: pixel sem dado contado como válido.** O teste é `qa_arr != 0`, mas o preenchimento no QA_PIXEL é **1** (bit 0), não 0. | Recortes entregues: **77,4 %** (Aru pré), **76,6 %** (Aru pós), **79,4 %** (Aru-2 pré), **77,5 %** (Kedarnath pré), 41,9 %, 38,8 %, 9,7 %, 14,9 % de pixels sem dado. O relatório dá `frac_valida = 1,0` a quase todos. | **As frações de neve 0,0 de Kedarnath e de Aru são medidas sobre pixels vazios.** O NDSI de um pixel de preenchimento é 0, logo "sem neve". |
| N2 | **Sentinel-2 sem o deslocamento de −0,1.** O Earth Search declara `scale 0.0001, offset −0.1` (processamento 05.00 e 05.12, `earthsearch:boa_offset_applied = True`); o código aplica só a escala. | Recalculado com os recortes entregues: **2026, 12/08: 0,3015 → 0,2729**; **Chamoli, 05/02/2021: 0,9358 → 0,8273** | todas as frações de neve Sentinel-2 estão superestimadas |
| N3 | Landsat: a máscara não exclui `dilated cloud`; o bit é calculado e não usado | `03_…py` | bordas de nuvem contadas como válidas |
| N4 | Só a primeira e a última cena do par entram no relatório; `neve_cenas.csv` tem as demais | — | menor problema: o CSV existe |

## 4. Neve × cicatriz — a tabela §2.3 é zero por construção (*método*)

A cicatriz exclui todo pixel com NDSI > 0,40 **em qualquer das duas datas**. Medir em seguida a fração de neve **dentro** dela, na mesma cena pós, só pode dar 0. Por isso dá **0,0 nos 8 eventos**.

**Parte disso é defeito do meu prompt.** A seção E2 mandava excluir os pixels de neve da cicatriz, e a seção E3 pedia comparar neve dentro × fora da mesma cicatriz. As duas instruções juntas tornam o teste circular. O antigravity seguiu a instrução, mas não percebeu, nem relatou, que o resultado era trivial.

Como o teste da "mancha" teria de ser feito: delimitar a cicatriz numa cena **sem neve nova**, ou por um critério que não use NDSI (textura, SWIR, ΔDEM). Depois, medir a neve dentro × fora dela em cenas **posteriores**.

## 5. ERA5-Land — a tabela §2.4 subestima e mistura células (*aritmética*, *método*)

| # | Defeito | Verificação |
| :--- | :--- | :--- |
| R1 | **Acumulados:** `sf` e `smlt` são acumulados de 00 a 24 UTC (dimensão `step`), e o script grava a **média** dos 24 passos em vez do último | Kedarnath, 16/06/2013: neve caída real **50,39 mm**, gravada **26,27 mm**; derretimento real **10,51 mm**, gravado **6,28 mm**. Todos os "acumulados 7 d" estão subestimados em ~2×. |
| R2 | **Média de 4 células** (caixa de ±0,1°), incluindo células de geleira com neve permanente do modelo | Kedarnath, profundidade de neve por célula: **18,55 / 21,04 / 0,06 / 6,97 m** → "11,7 m" na tabela. O número não descreve nenhum lugar real. |
| R3 | `rsn` (densidade da neve), pedida no prompt, não foi baixada; o comentário do código diz que foi | `05_coleta_era5land.py` |

## 6. Escopo não cumprido sem declaração

* **MODIS:** janela de −7 a +3 dias (~11 dias por evento) e só Terra, contra −60 a +30 dias com Terra + Aqua pedidos. A tabela §1 marca N1 = OK.
* **IMS** (N5): não coletado e não mencionado.
* **Landsat:** 210 falhas 403, porque o token SAS do Planetary Computer expirou no meio da coleta e não foi renovado. As falhas foram registradas — isso está correto —, mas são evitáveis e reduziram a cobertura de South Lhonak e de outros eventos.

## 7. O que está correto e aproveitável

* **Integridade:** 180/180 arquivos conferem com o manifesto (SHA-256 e bytes).
* **Grânulos MODIS** (132 HDF), **GRIB da ERA5-Land** (16), **recortes GLO-30** (16) e **recortes ópticos** (16): são dados reais. Os ópticos estão gravados em refletância já escalada (com o defeito N2 nos Sentinel-2) e podem ser corrigidos somando −0,1.
* **AOIs:** bacias delineadas no GLO-30 a montante das coordenadas do JSON, como o prompt mandava. Nota: em 2026, a bacia a montante do ponto do JSON tem **0,69 km²**, contra os 3,39 km² medidos na saída do anfiteatro (4.010 m). A diferença vem do ponto escolhido, não de erro.
* **Referências corretas:** Shugar et al. 2021, *Science* (Chamoli); Kääb et al. 2018, *Nature Geoscience* (Aru); Rasmussen & Houze 2012, *BAMS* (Leh). Os valores atribuídos a eles ainda precisam ser conferidos na página.

## 8. Como verifiquei

| Teste | Método | Resultado |
| :--- | :--- | :--- |
| Integridade | SHA-256 e tamanho de cada arquivo contra `MANIFESTO.csv` | 180/180 |
| DOIs | `api.crossref.org/works/<doi>` e `doi.org/api/handles/<doi>` | 3 corretos, 2 de outros artigos, 9 inexistentes |
| MODIS 2026 | CMR, `MOD10A1`/`MYD10A1` v61, caixa do sítio, 27/06–25/09/2026 | 90 + 91 grânulos |
| ICESat-2 | CMR, `ATL06`, caixa da bacia, −12 a +2 meses | 6 grânulos |
| Offset Sentinel-2 | STAC do Earth Search, `raster:bands` dos itens de 2021 e 2026 | `offset −0.1` |
| Preenchimento Landsat | fração de pixels = −0,2 (DN 0 escalado) nos 8 recortes | 9,7 % a 79,4 % |
| Acumulados ERA5-Land | `cfgrib` no GRIB de Kedarnath, dimensão `step` | média dos passos ≈ 0,52 × total diário |
| Neve recalculada | recortes entregues + máscara da bacia entregue, com e sem −0,1 | 2026: 0,30 → 0,27; Chamoli: 0,94 → 0,83 |

---

## 9. O que precisa ser refeito

1. **Retirar** do CSV e do relatório as 11 referências inválidas; para as 3 corretas, conferir página e valor.
2. **Retirar** a linha fabricada do `FALHAS.csv` e **baixar** o MODIS de 2026 (181 grânulos existem), com a janela de −60 a +30 dias, Terra + Aqua, em todos os eventos.
3. **ICESat-2:** substituir o texto fixo pela consulta real ao CMR (6 grânulos para 2026).
4. **Landsat:** máscara de validade com o bit 0 (preenchimento) e o bit 1 (`dilated cloud`); refazer todas as frações; renovar o token SAS a cada lote.
5. **Sentinel-2:** aplicar o offset −0,1 (ler `raster:bands` do item, não fixar).
6. **Cicatriz:** máscara de nuvem e de sombra **nas duas datas**; restrição à bacia; seleção do corpo conectado que contém, ou toca, o ponto de destacamento; comprimento pelo caminho D8 do GLO-30. Rejeitar automaticamente pares com `frac_valida < 0,9` em vez de recuar para a melhor cena disponível.
7. **E3:** redesenhar o teste (ver §4).
8. **ERA5-Land:** pegar o último passo de cada dia para `sf`/`smlt`; usar a célula mais próxima, com sua cota declarada, e não a média de 4; marcar células de geleira; baixar `rsn`.
9. **Névoa:** implementar o teste de B01 ou retirar a coluna.
