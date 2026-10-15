# Magnetômetros reais: o crochet medido e o limite que ele impõe sobre $J_z$

**Data:** 07 de setembro de 2026
**Dado primário:** INTERMAGNET, serviço GIN do British Geological Survey, formato IAGA-2002, **cadência de 1 minuto**, dias 24 a 27 de agosto de 2026.
Estações obtidas: **ABG (Alibag, IIG)** e **HYB (Hyderabad, NGRI)** — ambas constam da lista de estações do repositório. Arquivos completos, ABG sem uma única lacuna.
Estações sem dado: **LZH (Lanzhou)** e **BMT (Beijing Ming Tombs)** retornam `99999.00` para todo o período. `TIR` e `SAB` não são códigos INTERMAGNET.

---

## 1. Retratação parcial

Escrevi antes que "$J_z$ não é medível por evento" e que a rede de magnetômetros não entregaria nada. **Estava errado na primeira metade da frase.** A rede entrega, sim, uma medida física real e diretamente ligada ao problema — só que ela mede a **condutividade ionosférica**, não $V_I$. E essa medida, uma vez feita, impõe um limite quantitativo sobre o efeito do flare em $J_z$. É um resultado melhor do que "não dá para saber".

---

## 2. O crochet existe, e está medido

O `ARTIGO_CIENTIFICO` afirma que a rede *"registrou simultaneamente uma deflexão positiva abrupta do campo magnético horizontal ($\Delta H$), correspondente a um clássico Solar Flare Effect (crochet magnético)"*. A frase foi escrita sem dado. Testando com dado real:

Métrica: $H$ médio em 09:30–09:55 UTC (antes) contra o máximo em 10:00–10:40 UTC (depois), no dia do flare e em três dias de controle vizinhos.

### ABG — Alibag (hora local = UTC + 4h51 → flare às 14:53 LT, lado dia)

| Dia | H antes (nT) | H pico (nT) | Δ (nT) | instante do pico |
| :--- | ---: | ---: | ---: | ---: |
| 2026-08-24 | 38 371,74 | 38 370,20 | −1,54 | 10:06 |
| **2026-08-25** | **38 394,87** | **38 397,70** | **+2,83** | **10:03** |
| 2026-08-26 | 38 390,50 | 38 388,90 | −1,60 | 10:00 |
| 2026-08-27 | 38 376,65 | 38 375,40 | −1,25 | 10:00 |

Controle: −1,47 ± 0,19 nT. Dia do flare: +2,83 nT → **z = +23,0**.

### HYB — Hyderabad (UTC + 5h14 → 15:16 LT)

| Dia | Δ (nT) | instante |
| :--- | ---: | ---: |
| 2026-08-24 | −1,37 | 10:06 |
| **2026-08-25** | **+2,56** | **10:03** |
| 2026-08-26 | −1,94 | 10:00 |
| 2026-08-27 | −1,72 | 10:00 |

Controle: −1,68 ± 0,29 nT → **z = +14,8**.

### Perfil minuto a minuto em 25/08 (desvio a partir de 09:45 UTC)

| UTC | ABG | HYB |
| :--- | ---: | ---: |
| 09:45 | 0,00 | 0,00 |
| 09:55 | −1,00 | −0,85 |
| 10:00 | +1,80 | +1,66 |
| **10:05** | **+3,10** | **+2,61** |
| 10:10 | +0,40 | −0,53 |
| 10:20 | −2,50 | −4,00 |
| 10:45 | −7,30 | −9,06 |

Subida de ~4 nT em dez minutos, pico em **10:03 UTC — um minuto após o pico de raios X do GOES-18 às 10:02** — e decaimento. É a morfologia de livro-texto de um SFE, em duas estações independentes, com sincronia ao minuto.

**O crochet é real.** A frase do artigo estava certa por acaso; agora está certa por medição.

---

## 3. O que o crochet mede: realce de condutividade

Comparando a amplitude do crochet com a amplitude diurna do Sq nos dias de controle:

| Estação | Amplitude Sq | Crochet | Razão |
| :--- | ---: | ---: | ---: |
| ABG | 39,7 nT | 4,30 nT | **10,8 %** |
| HYB | 38,6 nT | 4,24 nT | **11,0 %** |

Duas estações independentes, separadas por ~700 km, concordam em **~11 %**. A corrente Sq é proporcional à condutividade integrada da região E; logo, o flare M6.9 elevou a condutividade da região E em cerca de **11 %** sobre o setor diurno asiático.

Este é um número medido, com barra de erro implícita pela concordância entre estações. É o primeiro número de eletrodinâmica deste projeto que não saiu de uma fórmula.

---

## 4. O limite que isso impõe sobre $J_z$

$$J_z = \frac{V_I}{R_c}, \qquad R_c = \int_0^{h_{\text{ion}}} \frac{dz}{\sigma(z)}$$

A condutividade atmosférica cresce de forma quase exponencial com a altura — de ~$10^{-14}$ S/m junto ao solo a ~$10^{-8}$ S/m aos 60 km, seis ordens de grandeza. Como $R_c$ é a integral de $1/\sigma$, ela é **dominada pelos primeiros quilômetros da troposfera**. A camada acima de 60 km contribui com uma fração da ordem de $10^{-6}$ de $R_c$.

O flare ioniza as regiões D e E, isto é, exatamente a parte que quase não pesa em $R_c$. Portanto:

$$\frac{\Delta J_z}{J_z} \;\approx\; 0{,}11 \times \frac{R_c(\text{acima de 60 km})}{R_c} \;\sim\; 10^{-7}$$

**Ordem de $10^{-5}$ por cento.**

O modelo anterior do repositório impunha, por causa deste mesmo flare, um salto de $V_I$ de 238 para **356,4 kV — mais 47 %**, e daí $J_z$ de 3,05 para 4,57 pA/m². O crochet medido não autoriza nada nem remotamente próximo disso. A discrepância entre o que o dado permite e o que o modelo impunha é de **cerca de sete ordens de grandeza**.

---

## 5. O que este resultado **não** fecha

O limite acima vale para a **via direta e imediata**: raios X do flare → ionização D/E → $R_c$ → $J_z$. Essa via está medida e é desprezível.

Restam duas vias indiretas, que o crochet não toca:

1. **Partículas energéticas solares (SEP)** ionizando a troposfera superior nos dias seguintes. Aqui vale a objeção da rigidez de corte: Gyirong/Langtang está a ~13–14 GV, entre as maiores do planeta, e prótons solares de dezenas a centenas de MeV são integralmente defletidos. Esta via já está fechada por geometria.
2. **Modulação de raios cósmicos galácticos (decréscimos de Forbush)**, que é o mecanismo que Tinsley de fato propõe. Os GCR de rigidez acima de 13 GV **penetram** no Himalaia, e um decréscimo de Forbush reduz a ionização troposférica, aumentando $R_c$ e reduzindo $J_z$. Efeito documentado, de poucos por cento.

**A via 2 é testável com dado aberto** e é a única que resta em pé. Monitores de nêutrons publicam séries horárias contínuas — inclusive de estações de alta rigidez, próximas da geometria correta. O teste seria: houve decréscimo de Forbush nas 24–72 h anteriores a cada um dos 15 eventos, comparado ao mesmo controle casado por sazonalidade e ciclo solar já usado para o Kp?

Este é o teste que fecharia a hipótese eletrodinâmica de forma definitiva — a favor ou contra.

---

## 6. Estações chinesas

`LZH` (Lanzhou) e `BMT` (Beijing Ming Tombs) estão no GIN mas retornam `99999.00` em todo o período de 24 a 27/08/2026 — dado não publicado. As sete estações chinesas listadas no repositório (LZA, XAN, CDT, BJI, QGZ, KSH, WUH) não são obteníveis pelo GIN nesta janela. Para incluí-las é preciso pedido formal à Administração de Terremotos da China — a carta `CARTA_04` já está redigida no repositório.

Nada disso invalida o resultado: **duas estações independentes bastaram** para medir o crochet com z de +23 e +15.

---

## 7. Reprodução

```
servico : https://imag-data.bgs.ac.uk/GIN_V1/GINServices
consulta: ?Request=GetData&format=IAGA2002&observatoryIagaCode=ABG
          &samplesPerDay=minute&publicationState=Best+available
          &dataStartDate=2026-08-25&dataDuration=1
estacoes: ABG (Alibag), HYB (Hyderabad).  LZH e BMT retornam 99999.
metrica : H medio 09:30-09:55 UTC  x  H maximo 10:00-10:40 UTC
controle: mesmos horarios em 24, 26 e 27 de agosto de 2026
Sq      : maximo diurno (04-12 UTC) menos media noturna (18-02 UTC), dias de controle
```

Script: `sfe.py` (crochet), `sq.py` (amplitude Sq e razão).

---

## 8. Síntese

| Questão | Resposta, agora medida |
| :--- | :--- |
| A rede de magnetômetros registra o flare? | **Sim.** Crochet de +2,8 nT (ABG) e +2,6 nT (HYB), pico às 10:03 UTC, z = +23 e +15 |
| Qual grandeza física isso mede? | Realce de ~**11 %** na condutividade integrada da região E |
| Isso permite calcular $V_I$? | **Não.** A corrente do circuito elétrico global é ~1–2 kA contra ~10⁵ A do Sq: não tem assinatura magnética detectável |
| Qual o efeito do flare sobre $J_z$? | **Ordem de 10⁻⁵ %** — porque $R_c$ mora na baixa troposfera, não na ionosfera |
| O salto de $V_I$ de +47 % do modelo anterior se sustenta? | **Não.** Excede o permitido pelo dado em ~7 ordens de grandeza |
| Sobra alguma via eletrodinâmica testável? | **Sim**, uma: decréscimos de Forbush em raios cósmicos galácticos. Dado aberto, teste montável |
