# Teste da hipótese de onda de sotavento — ERA5, 15 eventos

**Data:** 09 de setembro de 2026
**Dado:** ERA5 reanálise, níveis de pressão 400–600 hPa, passo de 6 h, caixa de ±0,5° em torno de cada sítio, ±15 dias em torno de cada evento. **15 de 15 eventos, zero falhas, 3,9 MB.** Credencial CDS do usuário, lida em tempo de execução.
**Cobertura:** a ERA5 alcança 1940, então este é o **único teste desta auditoria que cobre os três eventos anteriores a 2000** — Zhangzangbo 1981, Dig Tsho 1985 e Luggye Tsho 1994 — que ficaram de fora do IMERG e do Sentinel-2.

---

## 1. O que está sendo testado

Não é convecção profunda. É a hipótese formulada pelo investigador principal:

> nuvem entrando em sotavento da montanha, em ambiente de cisalhamento, com ascendência sustentada sobre o anfiteatro, acumulando água líquida **super-resfriada** que **não precipita** (gotículas monodispersas, evidenciadas por iridescência), até colapsar.

Nessa formulação, a ausência de chuva deixa de ser objeção e passa a ser **previsão**: precipitação seria o fracasso do mecanismo, não sua assinatura.

Cinco condições necessárias, todas mensuráveis:

| # | Condição | Métrica |
| :-- | :--- | :--- |
| 1 | escoamento cruzando a crista | vento a 500 hPa |
| 2 | cisalhamento vertical | \|V(400) − V(600)\| |
| 3 | onda aprisionada | parâmetro de Scorer, ℓ² = N²/U² |
| 4 | ascendência sobre o anfiteatro | ω a 500 hPa |
| 5 | reservatório | água líquida super-resfriada integrada, −20 °C < T < 0 °C |

**Grupo-controle interno:** para cada evento, a janela de 48 h anterior é comparada com todas as outras janelas do mesmo período de ±15 dias. Casa estação e regime sinótico por construção.

---

## 2. Resultado por evento (percentil no próprio mês)

| Evento | Vento 500 | Cisalh. | Scorer | Ascend. | SLWC |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **Kedarnath 2013** | 13,7 (**100**) | 14,6 (97) | (0) | −1,86 (**100**) | 0,32 (**100**) |
| **Himachal 2023** | 12,4 (**100**) | 14,2 (95) | (2) | −1,10 (**100**) | 0,23 (**99**) |
| **Melamchi 2021** | 8,6 (**97**) | 9,7 (67) | (9) | −0,59 (**94**) | 0,16 (**95**) |
| Parechu 2000 | 4,9 (93) | 9,1 (86) | (29) | −0,06 (81) | 0,05 (85) |
| South Lhonak 2023 | 6,6 (83) | 9,5 (53) | (23) | −0,14 (85) | 0,06 (63) |
| Bhotekoshi 2016 | 4,0 (75) | 3,0 (47) | (35) | −0,20 (62) | 0,08 (53) |
| Luggye 1994 | 6,7 (73) | 18,6 (76) | (38) | +0,06 (62) | 0,05 (68) |
| Chamoli 2021 | 8,8 (45) | 16,5 (43) | (80) | +0,57 (1) | 0,00 (13) |
| Parechu 2005 | 3,2 (40) | 7,0 (36) | (77) | +0,05 (39) | 0,00 (8) |
| **Lhende / Trishuli 2026** | **2,2 (34)** | **3,7 (53)** | **(78)** | **−0,02 (32)** | **0,04 (32)** |
| Dig Tsho 1985 | 1,6 (31) | 2,0 (19) | (73) | −0,09 (55) | 0,04 (48) |
| Aru 2016 | 2,8 (27) | 9,9 (58) | (92) | −0,06 (62) | 0,04 (84) |
| Leh 2010 | 2,4 (23) | 8,5 (63) | (81) | −0,07 (59) | 0,03 (53) |
| Seti 2012 | 3,4 (16) | 6,1 (10) | (91) | −0,06 (74) | 0,03 (48) |
| Zhangzangbo 1981 | 1,5 (16) | 5,1 (70) | (88) | −0,07 (34) | 0,05 (31) |

*(a coluna Scorer mostra 0,00 por arredondamento — os valores são de ordem 10⁻⁶ m⁻²; os percentis estão corretos)*

---

## 3. Estatística — e por que o resultado "significativo" não vale

| Métrica | Média dos percentis | z | p |
| :--- | ---: | ---: | ---: |
| Ascendência | 62,7 % | +1,70 | **0,0446** |
| Água super-resfriada | 58,7 % | +1,16 | 0,1227 |
| Cisalhamento | 58,2 % | +1,10 | 0,1365 |
| Vento a 500 hPa | 56,8 % | +0,91 | 0,1804 |
| Scorer | 53,1 % | +0,42 | 0,3376 |

A ascendência sai com p = 0,045. **Mas foram cinco testes.** O limiar de Bonferroni é 0,05/5 = 0,010, e **nenhuma das cinco sobrevive**.

Registro isso explicitamente porque é exatamente o erro que esta auditoria vem apontando: rodar várias comparações e reportar a que passou. p = 0,045 em cinco testes é o que se espera por acaso.

**As cinco médias estão acima de 50 %.** Sob independência isso teria p = 1/32. Mas elas **não são independentes** — vento, cisalhamento, ascendência e água líquida sobem juntos numa atmosfera dinamicamente ativa. O teste combinado não é válido.

---

## 4. O confundimento que decide a leitura

Os três eventos com as condições mais fortes são **Kedarnath 2013, Himachal 2023 e Melamchi 2021** — percentis de 94 a 100 em vento, ascendência e água super-resfriada.

Os três são **desastres pluviais documentados**.

Ou seja: o que as métricas detectam não é onda de sotavento. É **atmosfera úmida com ascendência sinótica ativa** — que é a definição de chuva. A reanálise a 28 km não distingue "onda de sotavento com água super-resfriada" de "depressão monçônica com precipitação", e o sinal positivo vem inteiramente dos casos de chuva.

Isso torna o teste **não diagnóstico** para o mecanismo proposto, e eu deveria ter previsto essa degenerescência ao desenhá-lo.

---

## 5. O evento de 2026, especificamente

| Métrica | Valor | Percentil |
| :--- | ---: | ---: |
| Vento a 500 hPa | 2,23 m/s | **34** |
| Cisalhamento | 3,69 m/s | 53 |
| Ascendência | −0,02 Pa/s | **32** |
| Água líquida super-resfriada | 0,04 kg/m² | **32** |

**Quatro das cinco métricas na mediana ou abaixo.** O ambiente das 48 h anteriores ao colapso foi mais fraco que o típico daquele mês, não mais forte.

Ondas de sotavento aprisionadas exigem escoamento cruzando a crista da ordem de 10–15 m/s no nível de cume. Mediram-se **2,2 m/s**.

### 5.1 E isto conecta de volta ao cálculo de fluxo

Na mensagem anterior eu calculei que uma nuvem lenticular estacionária poderia acumular 1 a 10 M m³ em 12–36 h — o que cobria o resíduo de 4,07 M m³. Aquele cálculo usou LWC de **0,2 a 1,0 g/m³**, valores típicos de literatura.

A coluna medida no evento de 2026 é de 0,04 kg/m². Distribuída numa nuvem de 1 a 2 km de espessura, isso dá **0,02 a 0,04 g/m³** — **cinco a cinquenta vezes abaixo** do que eu havia assumido.

Refazendo o fluxo com o valor medido (0,02 g/m³, vento 25 m/s, seção de 6 km²):

$$3{,}0\ \text{m}^3/\text{s} \;\rightarrow\; 0{,}13\ \text{M m}^3 \text{ em 12 h} \;\rightarrow\; \mathbf{0{,}39\ \text{M m}^3 \text{ em 36 h}}$$

Contra os **4,07 M m³** do resíduo: **déficit de 10 vezes**.

O mecanismo de acumulação por fluxo é fisicamente correto — foi um avanço real sobre a minha objeção de armazenamento. Mas com o reservatório que a reanálise mede naquele evento, ele entrega um décimo do necessário.

---

## 6. Limitações declaradas

1. **Resolução.** ERA5 a 0,25° (~28 km) não resolve a onda de sotavento nem o anfiteatro de 3,39 km². Mede o ambiente, não o fenômeno. Uma nuvem lenticular confinada sobre o circo pode ter LWC local muito acima da média de caixa — o valor de 0,04 kg/m² é média sobre ~2.700 km².
2. **O proxy de Scorer é fraco.** Calculei ℓ² = N²/U² num nível. O critério físico de aprisionamento é ℓ² **decrescer com a altura**, o que exige o perfil completo. A coluna Scorer desta tabela deve ser lida como indicativa, não como teste.
3. **Passo de 6 h.** Oito amostras na janela de 48 h. Um episódio de onda de duração de poucas horas pode passar entre amostras.
4. **A caixa de ±0,5°** inclui terreno muito heterogêneo; as médias diluem gradientes locais fortes.

Estas quatro limitações apontam todas na mesma direção: **o teste é conservador contra a hipótese**. Ele pode não ver um mecanismo que exista em escala pequena.

---

## 7. Situação

**O que este teste estabeleceu:** as condições de onda de sotavento não distinguem os 15 desastres do seu próprio contexto mensal, e o único resultado nominalmente significativo não sobrevive à correção para cinco comparações. O sinal positivo vem dos eventos de chuva, o que torna a métrica não diagnóstica.

**O que ele não estabeleceu:** que o mecanismo não existe. A resolução da reanálise é grosseira demais para vê-lo, por construção.

**O que decidiria:** simulação de mesoescala não-hidrostática (WRF ou equivalente) com grade de 1 km ou menos aninhada sobre o anfiteatro, alimentada pela ERA5, com microfísica de dupla-momento e produção secundária de gelo ativa. Só isso resolve a onda, a distribuição de tamanhos de gotícula e a taxa de deposição por rima. Os dados de contorno para rodar isso são exatamente os que acabaram de ser baixados.

---

## 8. Reprodução

```
dado   : reanalysis-era5-pressure-levels, CDS (cds.climate.copernicus.eu/api)
vars   : temperature, u, v, vertical_velocity, specific_cloud_liquid_water_content
niveis : 400, 450, 500, 550, 600 hPa      horarios: 00, 06, 12, 18 UTC
janela : evento +/- 15 dias    area: +/-0,5 grau em torno do sitio
credencial: ~/.cdsapirc  (nao impressa, nao transmitida a outro destino)
script : scripts/era5_onda_sotavento.py --baixar | --analisar
dados  : data/raw/era5/<evento>_<AAAAMM>.nc  (31 arquivos, 3,9 MB)
```

Nota de execução: a primeira tentativa falhou com HTTP 403 "cost limits" nos 15 eventos. Causa: o CDS expande `year × month × day` no produto cartesiano, e pedir uma janela que cruza dois meses dobra os dias. Corrigido com uma requisição por mês e redução de 7 para 5 variáveis e de 8 para 5 níveis.
