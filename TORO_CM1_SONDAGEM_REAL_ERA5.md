# toro-CM1 com a atmosfera real da ERA5 e o terreno real do GLO-30 — Lhende Khola, 25–26/08/2026

**Data:** 13 de outubro de 2026 (versão 2 — substitui integralmente a versão 1 deste arquivo)
**Modelo:** `toro-CM1` (CM1 r21.1, `cm1.single.gnu.exe`, executado no WSL Ubuntu)
**Figuras:** [`toro_cm1_terreno_glo30.png`](toro_cm1_terreno_glo30.png) · [`toro_cm1_era5_real.png`](toro_cm1_era5_real.png) · [`data/processed/toro_cm1/terreno.png`](data/processed/toro_cm1/terreno.png)
**Dados, sondagens, namelists, terreno:** [`data/processed/toro_cm1/`](data/processed/toro_cm1/) · **scripts:** [`scripts/toro_cm1/`](scripts/toro_cm1/)

---

## 0. Correção da versão 1 — leia primeiro

A versão 1 deste relatório afirmava que, com as sondagens ERA5 de 12 e 18 UTC, o modelo formava uma **camada persistente de água super-resfriada a 5,4–6,3 km, que não congelava**. **Essa conclusão está retirada. Era artefato de um viés frio na sondagem.**

**Causa.** O conversor `era5_to_cm1/era5_to_sounding.py` coloca a pressão de superfície, a T2m e a Td2m da célula ERA5 na altitude pedida, sem correção hidrostática. Esses valores estão na cota da célula, 4.322 m, e na v1 pedi 4.010 m.

O CM1 calcula T = θ·(p/p₀)^κ a partir dessa pressão. Com a pressão de superfície ~23 hPa baixa demais, a coluna inteira ficou ~1,6–3 K mais fria. Por isso a umidade relativa no nível da bolha quente chegou a **98–105 %**: a nuvem nascia por saturação espúria.

**Verificação:**

| | UR média a 1,5 km acima do solo, t = 0 | T a 1,5 km | Nuvem com a bolha |
| :--- | ---: | ---: | :--- |
| v1 (base 4.010 m, viés) | **98 %** (máx. 105 %) | −2,3 °C | sim, 14 kt de água super-resfriada |
| v2 (base 4.322 m = cota da célula) | **80 %** (máx. 88 %) | −0,7 °C | **nenhuma** |

O conversor do autor **está correto quando a altitude pedida é a cota da célula ERA5**, e foi assim que o usei na v2. Para o domínio com terreno, cuja base a 3.000 m fica abaixo da célula, escrevi um conversor separado: `scripts/toro_cm1/sondagem_consistente.py`. Ele tira p, θ, qv, u e v da base do próprio perfil de níveis de pressão, com ln p interpolado no geopotencial. O arquivo do autor não foi alterado.

As saídas da v1 foram mantidas, com prefixo `v1_`, em `data/processed/toro_cm1/`.

---

## 1. A atmosfera real — o que a ERA5 mostra

Perfil da ERA5 no ponto 28,2849 N, 85,5132 E. θe é a temperatura potencial equivalente; θes, a de saturação.

| hPa | z (m) | T (°C) 12 UTC | UR 12 UTC | UR 18 UTC | UR 00 UTC | θe 12 UTC | θes 12 UTC |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 600 | 4.405 | 6,7 | 89 % | 89 % | 74 % | 351,5 | 355,1 |
| 550 | 5.116 | 3,3 | 86 % | 84 % | 76 % | 351,4 | 355,3 |
| 500 | 5.885 | **0,0** | 63 % | 86 % | 65 % | 347,8 | 357,1 |
| 450 | 6.724 | −3,6 | 54 % | 62 % | 49 % | 349,8 | 359,7 |
| 400 | 7.646 | −8,7 | 46 % | 46 % | 48 % | 351,1 | 360,2 |

* **A coluna livre é condicionalmente estável.** O θe de nenhum nível alcança o θes dos níveis acima. A CAPE da parcela mais instável dos primeiros 3 km é **0 J/kg** nas três horas.
* **Isoterma de 0 °C a ~5.890 m.**
* **A instabilidade está numa camada rasa de superfície.** O ar de 2 m da célula, a 4.322 m, está ~3 K mais quente e ~2 g/kg mais úmido que a coluna livre. Levantado na coluna correta, dá **974 / 1.055 / 0 J/kg** às 12 / 18 / 00 UTC. Mas essa camada tem ~80 m de espessura, entre 4.322 m e o nível de 600 hPa a 4.405 m.
* **Vento fraco em toda a troposfera média:** 0,4 a 2,8 m/s entre 4 e 8 km; 4 a 11 m/s só acima de 10 km.

---

## 2. Rodadas planas refeitas (v2)

Mesmo desenho da v1: domínio 10 × 10 km, Δx = 500 m, contornos periódicos, bolha de +3 K a 1,5 km, 2 h, Morrison e NSSL+SIP. A diferença é a sondagem, com base a 4.322 m, a cota da célula.

| Execução | w máx (m/s) | Chuva máx (mm) | Água líq. T<0 °C (kt) | Cristais, fase mista (L⁻¹) |
| :--- | ---: | ---: | ---: | ---: |
| WK · Morrison (controle) | 13,6 | 0,41 | 67,5 | 301 |
| WK · NSSL+SIP (controle) | 19,1 | 0,87 | 112,5 | 16 |
| ERA5 12 UTC · Morrison / NSSL | 0,6 / 0,6 | 0 / 0 | 0 / 0 | 0 / 0 |
| ERA5 18 UTC · Morrison / NSSL | 0,6 / 0,6 | 0 / 0 | 0 / 0 | 0 / 0 |
| ERA5 00 UTC · Morrison / NSSL | 0,9 / 0,9 | 0 / 0 | 0 / 0 | 0,1 / 0,1 |

Com a atmosfera real, a bolha de +3 K não forma nuvem em nenhuma das três horas.

**O controle WK continua sem toró:** no máximo 0,9 mm em 2 h, com pico de 10,6 mm/h. O `toro-CM1` como publicado não reproduz o fenômeno nem na atmosfera de supercélula para a qual foi configurado.

---

## 3. Rodadas com o terreno real do GLO-30

### 3.1 Configuração

| Item | Valor | Observação |
| :--- | :--- | :--- |
| Domínio | 40 × 40 km, 80 × 80 × 64, Δx = 500 m, Δz = 250 m, topo a 19 km ASL | centrado no ponto de colapso (85,515 E; 28,271 N) |
| Terreno | Copernicus GLO-30, tile `N28_00_E085_00`, janela 1.471 × 1.296 px | lido por `/vsicurl`, sem credencial |
| Reamostragem | média em blocos de 500 m + filtro 1-2-1 × 4 + borda de 4 km misturada a campo suave | o solver não aguenta 57° a 500 m |
| Relevo no modelo | 1.843 → **6.497 m** (GLO-30 em blocos: até 7.080 m; pontual: 7.271 m) | o pico perde ~580 m na suavização |
| Base do modelo | 3.000 m ASL; vales abaixo disso preenchidos (**15 %** do domínio, o Bhote Koshi/Trishuli a NO) | registrado em `terreno_meta.json` |
| Inclinação | máx. **43°**, percentil 95 de 28°; no anfiteatro (3 × 3 km), média de **32°**, cotas de 4.539 a 6.492 m | a célula mais íngreme do modelo é a do colapso |
| Sondagem | ERA5 hidrostaticamente consistente, base a 3.000 m (`sondagem_consistente.py`) | horizontalmente homogênea |
| Gatilho | **nenhum** (`iinit=0`), só perturbação aleatória fraca (`irandp=1`) | toda ascendência vem do escoamento sobre o relevo |
| Solver | `psolver=3` (compressível com divisão de passo) | o anelástico do toro-CM1 (`psolver=4`) **não aceita terreno** no CM1 (`param.F:1748`) |
| Equilíbrio | `ibalance=0` | `ibalance=2` do toro-CM1 é incompatível com terreno |
| Contornos | laterais abertos (radiativos), amortecimento de Rayleigh acima de 15 km ASL | |
| Microfísica | NSSL 2-momentos + Hallett-Mossop + estilhaçamento (`nsplinter=1000`) | |
| Duração | 3 h, saída a cada 15 min | ~66–69 min de parede por rodada |

### 3.2 Resultados

| Sondagem | w máx no domínio (m/s) | w máx sobre o anfiteatro (m/s) | Nuvem | Água líq. T<0 °C | Chuva máx (mm) | Chuva no anfiteatro |
| :--- | ---: | ---: | :--- | ---: | ---: | ---: |
| ERA5 25/08 12 UTC | 1,52 | 0,75 | nuvem orográfica **quente** a 4,2–5,3 km, +1,5 a +6 °C, até 38 km², LWC máx 0,34 g/m³ | **0** | 0,46 | 0 |
| ERA5 25/08 18 UTC | 2,29 | 0,42 | **nenhuma** (UR máx 94 % a 5,8 km) | **0** | 0 | 0 |
| ERA5 26/08 00 UTC | 1,25 | 0,58 | **nenhuma** (UR máx 77–78 %) | **0** | 0 | 0 |

Cota superior de deposição por impacto no anfiteatro, com eficiência de coleta 1: **0 m³** nas três, porque não há água super-resfriada para depositar.

### 3.3 Leitura

1. **Não há água super-resfriada em lugar nenhum do domínio, em nenhum instante das três rodadas.**
2. **12 UTC:** o relevo levanta ar úmido o suficiente para formar uma nuvem de encosta. Ela é **quente** e fica **abaixo do nível de 0 °C**, num vale a ~16 km a sudeste do anfiteatro, não sobre ele. Faltariam ~600 m de ascensão adicional para essa camada passar de 0 °C.
3. **18 UTC**, a hora do pico convectivo no Himawari: o ar a 5,8 km, logo acima de 0 °C (−1,5 °C), chega a **94 %** de umidade relativa, mas não condensa. É a hora em que a atmosfera real esteve mais perto do que a hipótese pede. A convecção observada às 18 UTC (8.413 km² de topos frios no Himawari) **não aparece**: o modelo sem fluxos de superfície e sem a camada quente de 2 m não tem como gerá-la.
4. **00 UTC**, 3 h antes do colapso: ar seco, sem nuvem.
5. **A ascendência sobre o anfiteatro é fraca:** 0,4 a 0,75 m/s. Com 0,6 a 0,9 m/s de vento junto ao solo, não há onda de sotavento organizada. Com U ≈ 1 m/s, N ≈ 0,01 s⁻¹ e H ≈ 2 km, o número de Froude Fr = U/NH fica em ~0,05. É escoamento bloqueado: o ar contorna o maciço em vez de transpô-lo.

---

## 4. Limitações

* **Sem radiação nem fluxos de superfície** (`radopt=0`, `isfcflx=0`, como no toro-CM1). A camada aquecida junto às encostas, a única fonte de CAPE da ERA5, **não existe** no modelo. Num CM1 com terreno, ligá-la com `sfcmodel=1` usa uma temperatura de superfície **constante** em todo o domínio. Com 3,5 km de relevo, isso aqueceria artificialmente os cumes em ~20 K. Fazer direito exige radiação e balanço de energia de superfície (`radopt=2`, `sfcmodel=2`).
* **Sondagem horizontalmente homogênea**, de um único ponto ERA5 (célula de ~28 km). O escoamento real de 25–26/08 tinha estrutura de mesoescala (dois sistemas convectivos no Himawari) que não está aqui.
* **Terreno suavizado:** o pico caiu de ~7.080 para 6.497 m. As paredes de 50–60° do circo viraram 32° em média. A ascensão forçada por paredes mais íngremes e mais altas seria maior.
* **Vales abaixo de 3.000 m preenchidos.** Isso afeta o escoamento de vale do Bhote Koshi, não o anfiteatro (4,5–6,5 km).
* **3 h de integração.** Ciclos noturnos completos, como a drenagem catabática, exigem mais tempo e radiação.

---

## 5. Conclusão

Com a atmosfera real da ERA5, corrigida, e o terreno real do GLO-30:

* o `toro-CM1` **não produz toró**;
* **não produz água super-resfriada** sobre o anfiteatro nem em parte alguma do domínio, em nenhuma das três horas;
* às 12 UTC forma só uma nuvem de encosta **quente**, longe do anfiteatro; às 18 e às 00 UTC não forma nuvem.

O resultado positivo da versão 1 — nuvem super-resfriada persistente na cota do circo — era artefato do viés de pressão da sondagem e está retirado.

O que **não** está descartado, porque o modelo não o representa: a camada quente e úmida junto às encostas aquecidas, e a convecção de mesoescala que o Himawari registrou às 18 UTC. A atmosfera real ficou a ~600 m de ascensão de formar nuvem super-resfriada às 12 UTC e a 6 % de umidade de formá-la às 18 UTC. Um disparo que o modelo não tem pode ter fechado essa diferença.

## 6. Próximo passo, se for testar a parte que falta — **executado: ver §8**

* `radopt=2` (RRTMG) + `sfcmodel=2` + uso do solo real, com data, hora e latitude de 25/08/2026. Integração de 12 UTC a 03 UTC do dia 26 (15 h).
* Ou, mais barato e mais fiel à mesoescala: **WRF aninhado** até 500 m, inicializado e forçado nas bordas pela ERA5 de 12 UTC, com o mesmo critério.
* **Critério fixado antes de rodar:** água líquida com T < 0 °C sobre a janela de 3 × 3 km do anfiteatro, em qualquer instante entre 18 e 03 UTC. Se for zero, a acumulação por *riming* fica descartada para 2026 com a melhor representação disponível.

---

## 7. Reprodução

```
terreno    : python scripts/toro_cm1/terreno_glo30_cm1.py <saida>            -> perts.dat (sha256 em terreno_meta.json)
sondagens  : python scripts/toro_cm1/sondagem_consistente.py <era5_pl.nc> 3000 <saida>   (terreno)
             era5_to_cm1/era5_to_sounding.process_sounding(..., altitude=4322.1, ...)     (plano)
namelist   : python scripts/toro_cm1/merge_namelist.py <saida> $(cat data/processed/toro_cm1/ter_overrides.txt) param1.timax=10800.0 param1.tapfrq=900.0
execucao   : WSL, bash scripts/toro_cm1/rodar_um.sh <dir> 4
analise    : python scripts/toro_cm1/analisar_terreno.py ; python scripts/toro_cm1/figura_terreno.py <png>
```

---

## 8. Com radiação e fluxos de superfície (14/10/2026)

**Figura:** [`toro_cm1_radiacao_fluxos.png`](toro_cm1_radiacao_fluxos.png)

### 8.1 O que foi acrescentado ao domínio da §3

| Item | Valor | Fonte |
| :--- | :--- | :--- |
| Radiação | RRTMG (`radopt=2`), atualizada a cada 300 s, com data, hora e coordenadas reais (25/08/2026; 28,271 N, 85,515 E) | — |
| Superfície | camada superficial MM5 + solo de difusão térmica de 5 camadas (`sfcmodel=2`), atrito semi-livre (`bbc=3`) | — |
| Temperatura de pele inicial | T do ar na cota de cada célula + (skt − t2m) da célula ERA5: **+10,4 K às 06 UTC**, +1,2 K às 12 UTC | ERA5 `skt`, `t2m` |
| Solo profundo | T do ar na cota + (stl3 − t2m): −1,25 K / −0,36 K | ERA5 `stl3` |
| Neve/gelo | pele e solo limitados a 273,15 K | — |
| Uso do solo | **ESA WorldCover 2021 v200**, 10 m, por maioria em 500 m → USGS: 27 % neve/gelo, 23 % floresta, 21 % solo exposto, 20 % campo, 9 % tundra | aberto, sem credencial |
| Executável | CM1 r21.1 **recompilado de uma cópia**, com OpenMP e a opção nova `initsfc=5`, que lê tsk/tmn/lu/xland de `sfc_init.dat` | patch em `scripts/toro_cm1/patch_cm1/` |

O CM1 original inicializa a temperatura de superfície com um valor único (`tsk0`) em todo o domínio, o que com 3,5 km de relevo aqueceria os cumes em ~20 K. Por isso foi necessária a opção nova. O `CM1/src` do autor **não foi alterado**: o patch de 56 linhas está no repositório.

**Duas integrações**, com sondagem ERA5 consistente (base a 3.000 m), NSSL + produção secundária de gelo e sem bolha:

* **A — início às 06 UTC** (meio-dia local), para incluir o aquecimento da tarde. **Analisada até 19 UTC** (13 h de 21 h). A rodada foi interrompida pelo pesquisador às 20:08 UTC de modelo (SIGTERM), por custo de tempo; não há saída entre 20 UTC e o colapso.
* **B — início às 12 UTC** (pôr do sol), até 03 UTC de 26/08: **completa**, 15 h.

### 8.2 Integração A (06 UTC → 19 UTC): convecção profunda à tarde

| UTC | Calor sensível no domínio (W/m²) | Topo de nuvem (km) | Água líq. T<0 °C no anfiteatro (t) | Chuva acumulada no anfiteatro (mm) |
| :--- | ---: | ---: | ---: | ---: |
| 06:30 | 206 | 5,8 | 0 | 0,00 |
| 08:00 | 203 | 8,6 | 3.594 | 0,42 |
| 09:30 | 130 | 14,1 | **5.291** | 2,65 |
| 11:00 | 73 | 14,7 | 3.716 | 10,96 |
| 13:00 | 9 | 14,5 | 4.347 | 18,60 |
| 16:00 | −4 | 15,8 | 72 | 19,01 |
| 19:00 | −12 | 15,5 | 864 | 19,10 |

* **O aquecimento das encostas dispara convecção profunda** a partir de 06:30 UTC, com topos a 14–16 km e ascendências de 16–17 m/s acima de 3 km do solo entre 10:30 e 12:30 UTC.
* **Água super-resfriada sobre o anfiteatro: até 5.300 t**, com LWC máximo de 2,9 g/m³ no domínio, entre 08 e 15 UTC. Depois das 16 UTC ela praticamente desaparece.
* **Produção secundária de gelo (Hallett-Mossop) ativa, mas moderada:** 100–165 cristais/L na faixa de −3 a −8 °C, com graupel de 2–4 g/kg, entre 9 e 13 UTC. Os picos de 2.000–10.000 L⁻¹ ocorrem perto de −36 °C, por congelamento homogêneo nas bigornas, não por reação em cadeia. Sem graupel depois das 16 UTC, a produção secundária cessa.
* **Foco de precipitação sobre o anfiteatro.** A chuva acumulada até 19 UTC é **19,1 mm** sobre o anfiteatro, contra 7,4 mm na média do domínio (razão 2,6), com máximo local de 31,8 mm. Acima de 4.500 m, encostas de 30–50° recebem 12,2 mm e as de 0–20°, 6–7 mm.
* **Contra a observação, o modelo chove demais e cedo demais:**
  * numa área equivalente à célula de 0,1° do IMERG, **12,5 mm até 19 UTC**, contra **5,09 mm** medidos pelo IMERG até o colapso — 2,5 vezes mais;
  * o pico convectivo do modelo fica entre 12 e 14:30 UTC; no Himawari, o pico com área < −60 °C foi às **18 UTC**. O modelo adianta 4–6 h, o que é típico de sondagem homogênea com aquecimento forte.
* **Artefato numérico a descontar.** Entre 13 e 14 UTC, 64–80 % dos pontos com w > 10 m/s estão a menos de 1 km do solo, sobre encostas de ~21–25°, com picos de 54–67 m/s e CFL em 1,0. Isso é erro de gradiente de pressão da coordenada que segue o terreno em encostas íngremes aquecidas, não convecção. **Parte do foco de chuva sobre o anfiteatro pode vir desse artefato**, e com este domínio não é possível separar as duas contribuições.

### 8.3 Integração B (12 UTC → 03 UTC): nuvem baixa noturna, levemente super-resfriada, sem gelo

* Sem convecção: w máximo de 0,7 a 2,7 m/s e chuva máxima de 2,2 mm em 15 h; sobre o anfiteatro, ~0.
* O resfriamento radiativo noturno (−14 W/m²; pele do anfiteatro a −8 °C) forma uma **camada de nuvem líquida** de 3,4 a 5,8 km, que cresce de 0,8 km² (19 UTC) a **790 km²** (00:30 UTC).
* **O topo da camada fica de 0 a −3 °C, com água líquida super-resfriada e gelo zero** em todo o período. A camada está acima da faixa de Hallett-Mossop (−3 a −8 °C) e nunca congela.
* **No instante do colapso (02:30–03:00 UTC)**, essa água super-resfriada está **sobre o anfiteatro**: LWC de 0,10–0,36 g/m³, **10–37 t**. No corte S–N ela aparece colada à encosta sul do maciço, a 5,0–5,8 km (figura, painel inferior direito).
* **É compatível com uma observação independente.** O Himawari mediu 272,7 K (−0,4 °C) sobre o local às 02:50 UTC, interpretado em `GEOESTACIONARIO_NOITE_25_26AGO2026.md` como "superfície ou nuvem baixa". Um topo de nuvem líquida a 0 a −3 °C é compatível com essa leitura. A observação não distingue nuvem de superfície, porque a 68° de ângulo de visada o pixel mistura as duas.
* Deposição por impacto sobre o anfiteatro, cota superior com E = 1: **0 m³**. No domínio todo: 13.083 m³.

### 8.4 Comparação com o balanço do evento

| Fonte de água sobre o anfiteatro (3 × 3 km) | Modelo | Ordem de grandeza diante de 14,2 × 10⁶ m³ ¹ |
| :--- | ---: | ---: |
| Precipitação, integração A, até 19 UTC | 19,1 mm → **~1,7 × 10⁵ m³** (9 km²) | ~80× abaixo |
| Deposição por impacto, A, cota superior E = 1 | **6,2 × 10⁵ m³** (contaminada pelo artefato da §8.2) | ~23× abaixo |
| Água super-resfriada suspensa no instante do colapso, B | **10–37 t** | ~6 ordens abaixo |

¹ Os 14,2 × 10⁶ m³ são premissa do repositório, não medição (ver §1 do prompt de consultoria).

### 8.5 Leitura

1. **Com radiação e fluxos, o modelo produz o que as rodadas mecânicas não produziam:**
   * na tarde de 25/08, convecção profunda com água super-resfriada abundante, Hallett-Mossop ativo e **precipitação focada sobre o anfiteatro**;
   * na noite, uma camada de nuvem líquida super-resfriada e não glaciada, presente sobre o anfiteatro **no instante do colapso**.

   Os dois são ingredientes da sua hipótese, e o modelo os gera a partir da atmosfera e do terreno reais.
2. **Mas nenhum dos dois fecha o balanço.** O maior aporte, a precipitação da tarde, já está acima do IMERG observado em 2,5 vezes, e mesmo assim fica ~80 vezes abaixo do volume de água do repositório. A deposição por *riming*, na cota mais generosa e contaminada por artefato numérico, fica ~23 vezes abaixo.
3. **A "reação em cadeia" de produção de gelo não aparece.** O Hallett-Mossop dá ~100–165 cristais/L enquanto há graupel e desliga junto com a convecção. Os valores extremos são congelamento homogêneo nas bigornas.
4. **O que este domínio não decide:** se o foco de chuva sobre o anfiteatro é físico ou numérico, e o que aconteceu entre 19 e 03 UTC na integração A, que tinha o estado convectivo da tarde. A integração A foi interrompida às 20:08 UTC; esse intervalo fica para o WRF (`PROMPT_ANTIGRAVITY_WRF_LHENDE_2026.md`).

### 8.6 Limitações específicas

* **Radiação sem inclinação nem sombreamento:** o RRTMG do CM1 trata cada coluna como plana. A face norte do anfiteatro (85 % do circo) recebe no modelo o mesmo sol que uma face sul, então o aquecimento do circo está **superestimado**.
* **O solo não tem neve:** não há fusão nem calor latente de fusão. A pele sobre a geleira passa de 0 °C durante o dia.
* **Sondagem horizontalmente homogênea, sem forçamento de fronteira:** não entra o sistema de mesoescala que o Himawari mostrou chegando às 18 UTC.
* **Artefato de coordenada sobre encostas íngremes aquecidas**, que só se reduz com mais suavização do terreno, Δx menor ou coordenada híbrida (WRF).
