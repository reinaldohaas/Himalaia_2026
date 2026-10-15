# Teste solar-geomagnético com dado real e grupo-controle — 15 eventos

**Data:** 07 de setembro de 2026
**Dado primário:** GFZ Potsdam, `Kp_ap_Ap_SN_F107_since_1932.txt` — série completa de 1932-01-01 a 2026-09-07 (34.584 dias, Kp de 3 em 3 horas, ap, Ap, número de manchas, F10.7). Aberto, sem autenticação, 5,25 MB.
**Princípio:** nenhum valor digitado à mão. Toda estatística sai do arquivo. Grupo-controle e teste de hipótese declarados antes do resultado.

Esta é a análise que o repositório afirmava ter feito e não tinha: o script anterior gerava $J_z$ por fórmula e não lia magnetômetro nenhum, e nenhum teste estatístico existia.

---

## 1. Nota sobre o que $J_z$ pode e não pode ser

$J_z = V_I / R_c$ exige o potencial ionosférico $V_I$, que **não é medido rotineiramente** — não existe série temporal global de $V_I$. Ele é inferido da curva de Carnegie ou de sondagens esparsas. Qualquer "$J_z$ por evento" será, necessariamente, **modelo**, não medição. Foi exatamente essa a confusão anterior: um modelo paramétrico foi rotulado como inversão instrumental.

O que é medível e existe para os 15 eventos, com dado real:

| Grandeza | Papel físico | Fonte |
| :--- | :--- | :--- |
| **Kp / ap / Ap** | atividade geomagnética; proxy do forçamento do circuito elétrico global | GFZ, 1932– |
| **F10.7** | produtividade de flares e estado da atmosfera superior | GFZ/DRAO, 1947– |
| **Número de manchas** | fase do ciclo solar | GFZ/SILSO, 1932– |

O teste abaixo usa essas três, cada uma com o mesmo desenho de controle.

---

## 2. Kp real versus Kp alegado no repositório

Kp máximo nas 72 h anteriores ao instante de cada colapso, extraído da série de 3 horas do GFZ:

| Evento | **Kp real (72 h)** | Kp alegado | Diferença |
| :--- | ---: | ---: | ---: |
| Kedarnath 2013 | **1,67** | 4,30 | **+2,63** |
| Chamoli 2021 | 4,67 | 3,70 | −0,97 |
| Lhende/Trishuli 2026 | 3,00 | 3,70 | +0,70 |
| Aru (Tibete) 2016 | 4,00 | 4,00 | 0,00 ✔ |
| Seti 2012 | **3,00** | 5,00 | **+2,00** |
| South Lhonak 2023 | **3,67** | 5,70 | **+2,03** |
| Leh 2010 | 6,67 | 6,00 | −0,67 |
| Melamchi 2021 | 3,33 | 3,30 | −0,03 ✔ |
| Parechu 2000 | 5,33 | 6,30 | +0,97 |
| Zhangzangbo 1981 | 3,67 | 5,00 | +1,33 |
| Dig Tsho 1985 | 4,33 | 2,70 | −1,63 |
| Luggye Tsho 1994 | 5,33 | 4,30 | −1,03 |
| Bhotekoshi 2016 | 3,67 | 3,30 | −0,37 |
| Himachal 2023 | 4,00 | 4,70 | +0,70 |
| Parechu 2005 | 5,67 | 5,00 | −0,67 |

Média real 4,13; média alegada 4,47.

Três casos merecem destaque, porque o rótulo textual associado ao número afirmava um fenômeno que não ocorreu:

* **Seti 2012** — alegado *"Kp = 5,0 (Tempestade Geomagnética Menor G1)"*. Real: **3,00**. Não houve tempestade.
* **South Lhonak 2023** — alegado *"Kp = 5,7 (Tempestade Geomagnética Moderada G2)"*. Real: **3,67**. Não houve tempestade.
* **Kedarnath 2013** — alegado *"Kp = 4,3 (Condições instáveis)"*. Real: **1,67**, um dos períodos mais calmos do mês naquela década.

E dois conferem exatamente (Aru 4,00; Melamchi 3,33), o que indica que parte dos valores foi consultada e parte foi inventada.

---

## 3. Desenho do teste

**Estatística de interesse:** para cada evento, o valor da variável (Kp máx em 72 h; Ap do dia; F10.7; manchas).

**Grupo-controle:** todos os dias do **mesmo mês calendário**, dentro de **± 5 anos** do evento, excluindo ± 10 dias em torno dele. Isso casa simultaneamente a **sazonalidade** (monção, inverno) e a **fase do ciclo solar** — os dois fatores que poderiam gerar correlação espúria. O controle tem entre 170 e 2.650 amostras por evento.

**Estatística de teste:** o percentil de cada evento dentro do seu próprio controle. Sob a hipótese nula de nenhuma relação, os 15 percentis são uniformes em [0, 100], com média esperada 50 % e erro-padrão $28{,}87/\sqrt{15} = 7{,}45$ pontos.

**Testes:** binomial exato (quantos acima da mediana) e permutação com 200.000 reamostragens.

---

## 4. Resultados

### 4.1 Kp máximo nas 72 h anteriores

| Evento | Kp máx | Percentil no controle |
| :--- | ---: | ---: |
| Kedarnath 2013 | 1,67 | **5,2 %** |
| Chamoli 2021 | 4,67 | 79,5 % |
| Lhende/Trishuli 2026 | 3,00 | 33,0 % |
| Aru 2016 | 4,00 | 71,6 % |
| Seti 2012 | 3,00 | 43,8 % |
| South Lhonak 2023 | 3,67 | 42,5 % |
| Leh 2010 | 6,67 | **98,0 %** |
| Melamchi 2021 | 3,33 | 47,6 % |
| Parechu 2000 | 5,33 | 78,2 % |
| Zhangzangbo 1981 | 3,67 | 29,2 % |
| Dig Tsho 1985 | 3,33 | 15,1 % |
| Luggye Tsho 1994 | 5,33 | 70,2 % |
| Bhotekoshi 2016 | 3,67 | 60,5 % |
| Himachal 2023 | 4,00 | 68,9 % |
| Parechu 2005 | 4,67 | 76,7 % |

> **Média dos percentis: 54,7 %** (esperado 50 %). z = +0,63. Acima da mediana: 8 de 15.
> **Binomial: p = 0,50. Permutação: p = 0,267.**

### 4.2 As quatro variáveis

| Variável | Média dos percentis | z | p (permutação) | Conclusão |
| :--- | ---: | ---: | ---: | :--- |
| Kp máx (72 h) | 54,7 % | +0,63 | **0,267** | não significativo |
| **Ap do dia** | **44,9 %** | **−0,68** | 0,753 | não significativo, e **em sentido contrário** |
| F10.7 | 55,4 % | +0,72 | **0,239** | não significativo |
| Manchas solares | 52,7 % | +0,36 | 0,363 | não significativo |

**Nenhuma das quatro variáveis distingue os dias de desastre do controle casado.**

Dois detalhes que o teste expõe:

* O evento de **26/08/2026** — o caso central do repositório — teve **Ap = 2,0**, percentil **2,9 %**: um dos dias geomagneticamente **mais calmos** do seu mês em ±5 anos.
* **Leh 2010** é o único com tempestade genuína (Kp 6,67, percentil 98 %). Um caso em quinze é o que se espera por acaso.

---

## 5. Poder do teste — o que este resultado não diz

Com n = 15 e erro-padrão de 7,45 pontos, o teste só atinge $p < 0{,}05$ unilateral se a média dos percentis chegar a **62,3 %**. Observou-se 54,7 %.

Portanto o enunciado correto é: **não há evidência de efeito**, e não "o efeito está refutado". Um efeito real, porém modesto — deslocando a média para 55–60 % — seria indistinguível do acaso nesta amostra. Para detectá-lo seriam necessários da ordem de **60 a 200 eventos**, não 15.

Isto é uma limitação de desenho, não um veredito contra a hipótese. Mas também significa que **um catálogo de 15 casos não pode sustentar uma alegação de causalidade**, e que qualquer afirmação nesse sentido precisa ser retirada até que a amostra cresça.

Caminho para aumentar o poder, com dados abertos: usar catálogos inteiros de deslizamentos e GLOFs do Himalaia (NASA Global Landslide Catalog, ICIMOD, GLOF databases publicadas) em vez de 15 casos escolhidos. Isso também elimina o viés de seleção — hoje os 15 foram escolhidos *depois* de conhecidos, o que enviesa qualquer teste.

---

## 6. Erosão nos demais eventos — situação

### 6.1 Disponibilidade Sentinel-2 L2A verificada

| Evento | Cenas na janela ±60 d | Melhor PRE | Melhor POS |
| :--- | ---: | :--- | :--- |
| **Chamoli 2021** | 53 | 2021-01-21 (**0 %** nuvem) | 2021-03-02 (**0 %**) |
| **South Lhonak 2023** | 101 | 2023-09-16 (1 %) | 2023-11-18 (**0 %**) |
| **Himachal 2023** | 48 | 2023-05-19 (2 %) | 2023-09-06 (8 %) |
| Melamchi 2021 | 103 | 2021-04-20 (7 %) | 2021-07-29 (53 %) |
| Aru 2016 | — | sem cobertura L2A | — |
| Bhotekoshi 2016 | — | sem cobertura L2A | — |

Os eventos de 2016 e anteriores exigem Sentinel-2 **L1C** ou **Landsat** (5/7/8), ambos abertos, com processamento adicional.

### 6.2 O experimento natural de calibração

Três casos com mecanismo conhecido de forma independente formam um teste cego do método:

| Caso | Mecanismo documentado | Assinatura esperada |
| :--- | :--- | :--- |
| **Himachal 2023** | chuva extrema (centenas de mm) | erosão **distribuída** — muitos focos, várias vertentes |
| **Chamoli 2021** | avalanche rocha-gelo, dia seco | erosão **concentrada** — um trajeto |
| **South Lhonak 2023** | GLOF | erosão **concentrada** — um trajeto |

Se a métrica separa corretamente esses três, ela pode ser aplicada ao evento de 2026 quando a cena de outubro existir — e aí sim a morfologia da cicatriz vira evidência sobre o mecanismo.

### 6.3 Primeira execução: resultado insuficiente

A primeira passagem usou perda de vegetação (NDVI > 0,25 → < 0,10) numa janela de 11 × 11 km centrada na origem. Resultado: Chamoli 1,6 ha em 21 grupos; South Lhonak 0,0 ha; Himachal falhou por desalinhamento de grade.

**A métrica está errada para este terreno.** As áreas de origem estão acima do limite da vegetação — não há vegetação para perder —, e o trajeto erosivo se estende por dezenas de quilômetros vale abaixo, fora da janela. Chamoli devastou o Rishiganga e o Dhauliganga muito além dos 11 km amostrados.

Correções necessárias antes de repetir: janela seguindo o talvegue traçado no DEM em vez de quadrado centrado na origem; métrica de mudança de superfície que não dependa de vegetação (variação de brilho e de razões de bandas sobre solo/rocha); e reamostragem comum entre bandas de 10 m e 20 m. É trabalho de uma sessão dedicada, não de um script.

---

## 7. Situação

| Item | Estado |
| :--- | :--- |
| Kp real dos 15 eventos | **Feito.** Série GFZ, sem valores digitados |
| Comparação com os valores alegados | **Feito.** 3 casos afirmam tempestades que não ocorreram |
| Grupo-controle casado por sazonalidade e ciclo solar | **Feito.** 170–2.650 amostras por evento |
| Teste de hipótese (Kp, Ap, F10.7, manchas) | **Feito.** Nenhum significativo |
| Análise de poder | **Feita.** n = 15 é insuficiente; são precisos 60–200 eventos |
| Catálogo de flares por evento (1981–2026) | Pendente — endpoints NCEI testados retornaram 404; requer localizar o arquivo histórico |
| Erosão comparativa | **Iniciada.** Pares identificados; métrica precisa ser refeita para terreno sem vegetação |

---

## 8. Reprodução

```
Kp/Ap/F10.7/SN : https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt
estatistica    : Kp maximo em janela movel de 24 slots (72 h) terminando no instante do evento
controle       : mesmo mes calendario, |ano - ano_evento| <= 5, |dia - dia_evento| >= 10
teste          : percentil no controle -> binomial exato + permutacao (200.000 reamostragens)
S2 disponivel  : https://earth-search.aws.element84.com/v1/search  (collections=sentinel-2-l2a)
```

Scripts: `jz_real.py` (Kp real x alegado), `jz_ctrl.py` (controle e teste), `jz_f107.py` (Ap/F10.7/manchas), `erosao.py` (calibração de erosão, a refazer).
