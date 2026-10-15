# GPM IMERG V07 nos 15 eventos — o denominador que faltava

**Data:** 08 de setembro de 2026
**Dado:** GPM IMERG V07, Final Run (calibrado por pluviômetro) para 11 eventos; Late Run para o de 2026, cujo Final ainda não foi processado (latência de ~3,5 meses).
**Método:** subsetting por OPeNDAP da janela de cada bacia (±0,25°), **144 grânulos meia-horários por evento** — o dia do evento e os dois anteriores. **Nenhuma falha: 144/144 em todos os 12 eventos com cobertura.**
**Credencial:** token Earthdata do usuário, lido de arquivo em tempo de execução.

Este é o número que o repositório afirmava ter e não tinha: o `p_meas_mm` era digitado à mão, e o único catálogo IMERG arquivado era de **2024**.

---

## 1. Resultado, ordenado por déficit

| Evento | IMERG (mm, 3 dias) | Máx. em 30 min | Lâmina requerida | **Déficit** | Mecanismo documentado |
| :--- | ---: | ---: | ---: | ---: | :--- |
| **Himachal Pradesh 2023** | **335,64** | 13,14 | 171,6 | **0,5×** | chuva extrema |
| **Kedarnath 2013** | **244,40** | 16,56 | 131,1 | **0,5×** | chuva monçônica + Chorabari |
| **Leh Ladakh 2010** | **110,33** | 24,74 | 79,3 | **0,7×** | aguaceiro |
| Melamchi 2021 | 58,09 | 11,70 | 151,8 | 2,6× | chuva + barramento |
| Parechu 2000 | 22,82 | 18,34 | 181,5 | 8,0× | barramento por deslizamento |
| Bhotekoshi 2016 | 20,83 | 8,06 | 166,7 | 8,0× | GLOF |
| South Lhonak 2023 | 13,01 | 4,20 | 262,0 | 20,1× | **GLOF** (lago drenou) |
| **Lhende / Trishuli 2026** | **18,71** | **6,96** | **510,9** | **27,3×** | **colapso rocha-gelo** |
| Aru (Tibete) 2016 | 15,69 | 11,47 | 673,7 | 42,9× | colapso de geleira fria |
| Seti 2012 | 4,42 | 1,69 | 287,6 | 65,0× | avalanche rocha-gelo |
| Chamoli 2021 | 1,38 | 0,78 | 217,7 | **158,3×** | avalanche + fusão por atrito |
| Parechu 2005 | 0,74 | 0,37 | 153,3 | **208,0×** | ruptura de represa natural |
| Zhangzangbo 1981 | — | — | — | — | anterior a 2000-06; sem IMERG |
| Dig Tsho 1985 | — | — | — | — | idem |
| Luggye Tsho 1994 | — | — | — | — | idem |

---

## 2. Os controles validam o método

Três eventos servem de calibração cega, porque o mecanismo é conhecido de forma independente:

* **Himachal 2023** — desastre pluvial documentado. IMERG dá **335,6 mm** contra 171,6 requeridos: **déficit 0,5×**, isto é, a chuva observada explica a cheia com folga de 2×. ✔
* **Chamoli 2021** — manhã seca de inverno, céu limpo, avalanche rocha-gelo. IMERG dá **1,38 mm**: "déficit" de 158×. Mas isso não é anomalia — é **erro de categoria**. A água veio da fusão por atrito do gelo arrastado, como Shugar et al. demonstraram. ✔
* **Leh 2010** — aguaceiro documentado. **110,3 mm** contra 79,3: **déficit 0,7×**. ✔

O método separa corretamente os dois regimes. Isso autoriza a leitura dos demais.

---

## 3. O que os números derrubam

### 3.1 O "déficit" de Kedarnath era artefato

O repositório publicava **déficit de 3,7×** para Kedarnath, calculado com `p_meas_mm = 35.0` digitado no código — enquanto o próprio `LITERATURE_REGISTER` citava Dobhal et al. registrando **>325 mm**.

Medição: **244,40 mm**. Requerido: 131,1 mm. **Não há déficit — há excedente de 2×.**

E 244 mm é um **piso**: o IMERG tem viés seco documentado em extremos orográficos himalaios (~400 mm/dia contra ~650 do IMD no NW-Himalaya em julho de 2026). A chuva real foi maior ainda.

### 3.2 O "déficit universal de 10× a 20×" não existe

A alegação era que **todos** os 15 eventos partilhavam um déficit hídrico de 10–20×. Medido: os déficits vão de **0,5× a 208×**, e a distribuição não é aleatória — ela **rastreia o mecanismo**:

| Faixa | Eventos | O que são |
| :--- | :--- | :--- |
| **≤ 1×** | Himachal, Kedarnath, Leh | eventos pluviais: a chuva explica |
| **2–8×** | Melamchi, Parechu 2000, Bhotekoshi | mistos; o viés seco do IMERG pode fechar boa parte |
| **> 20×** | South Lhonak, **2026**, Aru, Seti, Chamoli, Parechu 2005 | **falha de massa ou ruptura de lago** — a água não veio de chuva |

O "déficit" é grande exatamente onde a fonte da água **não é** precipitação: um lago que drenou, gelo arrastado que fundiu, ou um rio represado que foi liberado. Não é anomalia física: é o método detectando corretamente que chuva não era a fonte.

---

## 4. O evento de 2026

**18,71 mm medidos, 510,9 requeridos, déficit 27,3×.** Isso o coloca no grupo das falhas de massa, ao lado de South Lhonak (GLOF, 20×) e Aru (colapso de geleira, 43×) — **não** no grupo pluvial.

Três ressalvas, todas importantes:

1. **É Late Run**, não Final: sem calibração por pluviômetro. O Final sairá por volta de dezembro de 2026.
2. **18,71 mm é a média numa caixa de 0,5°** (~2.700 km²). O anfiteatro tem **3,39 km²** — três ordens de grandeza menor que o pixel de amostragem. O IMERG a 0,1° não resolve um núcleo convectivo confinado. O máximo de meia hora foi 6,96 mm, o que confirma que houve convecção na caixa.
3. **Isto é consistente com o Himawari-9**, que mostrou 8.413 km² de topos abaixo de −60 °C às 18:00 UTC de 25/08, dissipando-se antes do colapso. Houve convecção real na região; o IMERG a vê como ~19 mm de média de caixa. Quanto caiu sobre os 3,4 km² do anfiteatro, este dado não decide.

Ou seja: o número **não** sustenta a lâmina de 510 mm exigida pela reconstrução hidráulica, mas **também não** exclui precipitação relevante sobre o anfiteatro. Ele exclui uma coisa mais estreita e mais útil: que a chuva de escala de bacia tenha sido a fonte.

---

## 5. Limitações declaradas

1. **Três eventos sem cobertura.** Zhangzangbo 1981, Dig Tsho 1985 e Luggye Tsho 1994 precedem o início do IMERG (2000-06-01). Exigiriam reanálise ERA5 (que alcança 1940) ou pluviômetro histórico. Ficam em branco — não estimados.
2. **Viés seco orográfico.** Todos os valores são **piso**, não medida fechada. Onde o déficit é 2–8×, a correção de viés pode fechá-lo sozinha.
3. **Resolução.** 0,1° (~10 km) contra bacias de 3 a 210 km². Para as menores, o IMERG amostra, não mede.
4. **A lâmina requerida herda as premissas do balanço inverso** — áreas de bacia e volumes que a auditoria mostrou serem, em vários casos, arbitrados. Para o evento de 2026, a área real delineada no GLO-30 é de 3,4 a 32,7 km², e 55 ou 65,7 km² **não existem** em ponto nenhum do Lhende.

---

## 6. Reprodução

```
colecoes: GPM_3IMERGHH (Final, 2000-06 em diante) / GPM_3IMERGHHL (Late, eventos recentes)
descoberta: CMR da NASA (aberto, sem credencial)
subsetting: OPeNDAP .ascii, precipitation[0][lon][lat], janela de +/-0,25 grau
janela temporal: dia do evento + 2 anteriores = 144 granulos meia-horarios
credencial: token Earthdata, lido de ~/.earthdata_token em tempo de execucao
script: scripts/imerg_15_eventos.py --catalogo | --baixar
saida : data/processed/imerg_15_eventos.csv
```

Salvaguardas embutidas após a primeira execução ter produzido zeros com aparência de dado: sonda única em série antes de qualquer paralelismo; aborto imediato em erro de autenticação (tentativas repetidas travam a conta no URS); e `FALHA / SEM DADO` explícito quando `n = 0`, nunca `0,00 mm`.
