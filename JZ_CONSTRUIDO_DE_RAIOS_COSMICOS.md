# $J_z$ construído a partir de dado medido — raios cósmicos galácticos, 15 eventos

**Data:** 08 de setembro de 2026
**Dado primário:** NMDB (`nmdb.eu`), monitores de nêutrons, contagem horária corrigida por eficiência. Aberto, sem credencial.
**Estações:** OULU (0,81 GV, série desde 1964), Atenas ATHN (8,53 GV), Cidade do México MXCO (8,20 GV).

---

## 1. Por que esta é a via certa, e a única que restava

Duas vias eletrodinâmicas já haviam sido fechadas por medição:

* **Raios X do flare** → o crochet medido em ABG e HYB deu +11 % de condutividade na região E, o que limita o efeito sobre $J_z$ a ordem de $10^{-5}$ %, porque $R_c$ mora na baixa troposfera e não na ionosfera.
* **Prótons solares (SEP)** → fechada por geometria: a rigidez de corte do sítio (~13–14 GV) deflete integralmente prótons de dezenas a centenas de MeV.

Restava a via que **Tinsley de fato propõe**: modulação de raios cósmicos galácticos, que penetram acima de 13 GV, alterando a ionização troposférica.

A cadeia é fechada e não contém nenhum valor arbitrado:

$$\text{GCR} \rightarrow q \;\;\Rightarrow\;\; n=\sqrt{q/\alpha} \;\Rightarrow\; \sigma = n e \mu \propto \sqrt{q} \;\;\Rightarrow\;\; R_c \propto q^{-1/2} \;\;\Rightarrow\;\; J_z = \frac{V_I}{R_c} \propto V_I\sqrt{\text{GCR}}$$

$$\boxed{\;\frac{\Delta J_z}{J_z} \;=\; \tfrac{1}{2}\,\frac{\Delta \text{GCR}}{\text{GCR}}\;}$$

**Método:** anomalia da contagem nas 72 h anteriores a cada evento, em % da mediana dos 27 dias precedentes (uma rotação de Carrington), excluída a própria janela.

**Teste de rigidez, sem assumir expoente:** três estações de rigidez de corte diferente. Se o sinal existe em OULU (0,81 GV) e desaparece em Atenas e México (~8,2–8,5 GV), ele não alcança o sítio, que está mais alto ainda.

---

## 2. Resultado — OULU (0,81 GV), 15 de 15 eventos

| Evento | GCR média (%) | GCR mínima (%) | **$\Delta J_z$ média (%)** |
| :--- | ---: | ---: | ---: |
| Kedarnath 2013 | +1,55 | +0,63 | **+0,78** |
| Chamoli 2021 | −0,81 | −1,62 | −0,40 |
| **Lhende / Trishuli 2026** | **+1,85** | +0,80 | **+0,92** |
| Aru 2016 | −1,55 | −2,55 | −0,77 |
| Seti 2012 | +0,74 | −0,59 | +0,37 |
| South Lhonak 2023 | +1,62 | +0,41 | +0,81 |
| **Leh Ladakh 2010** | **−1,79** | **−4,13** | **−0,89** |
| Melamchi 2021 | −0,00 | −1,11 | −0,00 |
| Parechu 2000 | +1,89 | +0,34 | +0,94 |
| Zhangzangbo 1981 | +1,94 | +0,57 | +0,97 |
| Dig Tsho 1985 | −0,42 | −1,24 | −0,21 |
| Luggye Tsho 1994 | −1,56 | −2,93 | −0,78 |
| Bhotekoshi 2016 | +0,77 | +0,02 | +0,38 |
| Himachal 2023 | −0,83 | −2,20 | −0,42 |
| Parechu 2005 | +0,74 | −0,13 | +0,37 |

Cobertura completa: os três eventos anteriores a 2000 (Zhangzangbo, Dig Tsho, Luggye Tsho), que não têm IMERG nem satélite, **têm** dado de nêutrons — a série de OULU começa em 1964.

---

## 3. Significância e teste de rigidez

| Estação | Rigidez | n | Média | dp | EP | z | p (unilateral) | Positivos |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| OULU | 0,81 GV | 15 | **+0,276 %** | 1,360 | 0,351 | +0,79 | **0,216** | 8/15 (binom. 0,50) |
| ATHN | 8,53 GV | 10 | +0,145 % | 0,693 | 0,219 | +0,66 | 0,254 | 5/10 (binom. 0,62) |
| MXCO | 8,20 GV | 11 | +0,238 % | 0,831 | 0,251 | +0,95 | 0,171 | 7/11 (binom. 0,27) |

**Nenhuma significativa.** Oito de quinze positivos em OULU é exatamente o esperado por acaso.

**A dependência de rigidez aparece nos dados**: o desvio-padrão cai de 1,36 % (0,81 GV) para 0,69 % (8,53 GV) — a modulação de GCR encolhe ao subir a rigidez, como a física prevê. O sítio está a **13–14 GV**, acima das três estações. O que já é pequeno a 8,5 GV é menor ainda lá.

**Nota de justiça à hipótese:** o sinal médio é **positivo** nas três estações. Se o mecanismo de Tinsley opera por $J_z$ elevado favorecendo eletrocongelamento, a *direção* é a que a hipótese pediria. O problema não é o sinal — é a magnitude.

---

## 4. A escala do efeito

| Grandeza | Valor |
| :--- | ---: |
| $\Delta J_z$ médio medido (15 eventos, OULU) | **+0,138 %** |
| $\Delta J_z$ do evento mais forte (Leh 2010, tempestade real de Kp 6,67) | −0,89 % (média), −2,07 % (pico) |
| $\Delta J_z$ que o modelo anterior do repositório impunha | **+49,8 %** (3,05 → 4,57 pA/m²) |
| **Razão entre o exigido e o medido** | **361 vezes** |

Mesmo o evento com tempestade geomagnética genuína — Leh 2010, o único dos quinze com Kp real de 6,67, percentil 98 no controle — produz $\Delta J_z$ de ~2 % no pico. Não 50 %.

---

## 5. Fechamento da questão eletrodinâmica

Com esta análise, as três vias possíveis estão quantificadas com dado medido:

| Via | Mecanismo | $\Delta J_z$ medido | Status |
| :--- | :--- | ---: | :--- |
| Raios X do flare | ionização D/E → $R_c$ | ~$10^{-5}$ % | fechada (crochet em ABG/HYB) |
| Prótons solares (SEP) | ionização troposférica | ~0 | fechada (rigidez de corte 13–14 GV) |
| **GCR / Forbush** | ionização troposférica → $\sigma$ → $R_c$ | **+0,14 % (média), até ~2 % (extremo)** | **medida; ordem de grandeza insuficiente** |

Nenhuma das três chega perto dos ~50 % que a hipótese exigia. A diferença não é de interpretação: é de **duas a sete ordens de grandeza**, conforme a via.

Isto **não** refuta o mecanismo de Tinsley, que é ciência revisada por pares e opera na escala de poucos por cento — exatamente a escala aqui medida. O que fica excluído é que ele produza, no Himalaia, uma variação de $J_z$ capaz de reorganizar a microfísica de uma nuvem a ponto de disparar um colapso de $10^8$ m³.

---

## 6. O que este resultado não afeta

A cadeia física que **sobreviveu** a toda a auditoria continua de pé, e não depende de $J_z$:

> Sistema convectivo de mesoescala na noite de 25/08 (8.413 km² de topos abaixo de −60 °C, medidos no Himawari-9) → deposição sobre o anfiteatro de 3,39 km², face norte, 47,8° de declividade → dissipação do sistema → colapso ~9 h depois sob céu limpo.

O que o presente resultado remove é apenas a alegação de que a **eletrodinâmica solar** organizou aquele sistema. O sistema existiu, foi medido, e sua organização é explicável por convecção orográfica de monção sem nenhum ingrediente heliofísico.

---

## 7. Reprodução

```
fonte : https://www.nmdb.eu/nest/draw_graph.php  (output=ascii, tresolution=60,
        dtype=corr_for_efficiency, tabchoice=revori)
estacoes: OULU (0,81 GV), ATHN (8,53 GV), MXCO (8,20 GV)
anomalia: media da janela de 72 h antes do evento, em % da mediana dos 27 dias
          precedentes, excluida a janela
conversao: dJz/Jz = 0,5 * dGCR/GCR   (sigma ~ sqrt(q); Rc ~ q^-0,5)
script  : scripts/jz_de_raios_cosmicos.py
```

Limitação declarada: PSNM (Doi Inthanon, 16,8 GV) seria a estação de geometria ideal — rigidez acima da do sítio — mas não tem dado publicado no NMDB para 2026. Com ela, o teste de rigidez ficaria fechado por cima em vez de extrapolado.
