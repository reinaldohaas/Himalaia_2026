# Infravermelho geoestacionário da noite de 25–26/08/2026: houve o sistema, e ele se dissipou antes

**Data:** 08 de setembro de 2026
**Dado:** Himawari-9 AHI, **banda 13 (10,4 µm)**, Himawari Standard Data L1b, resolução nominal de 2 km, segmento S03 da grade de disco completo. Bucket **`noaa-himawari9` da AWS Open Data — aberto, sem autenticação**.
**Leitor:** escrito para esta análise (`hsd.py`); decodifica os 11 blocos de cabeçalho HSD, aplica ganho e constante para radiância, inverte Planck com as constantes do bloco de calibração e corrige com $c_0 + c_1 T_e + c_2 T_e^2$; geolocalização pela projeção geoestacionária inversa a partir de COFF/LOFF/CFAC/LFAC do próprio arquivo.

---

## 1. Por que Himawari e não INSAT-3D

O INSAT-3D é a geometria ideal (subsatélite a 82 °E, praticamente no nadir do sítio), mas o **MOSDAC responde HTTP 401** e o portal do IMD idem: exigem cadastro. Não crio conta em nome de terceiros, então o INSAT continua pendente de uma inscrição que só você pode fazer.

O Himawari-9 (140,7 °E) é aberto. Para o sítio a 85,5 °E o ângulo zenital de visada é de **~68°** — oblíquo. Duas consequências, declaradas:

* o pixel se alonga por $1/\cos 68° \approx 2{,}7$, e as áreas abaixo já incluem esse fator;
* topos altos sofrem **paralaxe**: um topo a 15 km aparece deslocado ~37 km **para leste** da sua posição real. As manchas frias na figura estão, portanto, deslocadas nesse sentido.

Nenhum dos dois efeitos impede detectar um sistema de $10^3$ km². Eles apenas limitam a precisão de posição.

---

## 2. O resultado

Caixa de 150 km em torno de 28,271 °N / 85,515 °E. Limiares: convecção profunda tem topo abaixo de **213 K (−60 °C)**; cumulonimbus maduro abaixo de 220 K.

| Instante UTC | BT no sítio | BT mín. (150 km) | Área < 240 K | Área < 220 K | **Área < 213 K** |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **25/08 18:00** | 235,3 K | 200,3 K | 32.886 km² | 13.025 km² | **8.413 km²** |
| 25/08 21:00 | 225,3 K | 203,2 K | 43.816 km² | 15.196 km² | **4.892 km²** |
| 26/08 00:00 | 222,1 K | 210,3 K | 26.719 km² | 7.160 km² | **810 km²** |
| **26/08 02:50 — colapso** | **272,7 K** | 215,7 K | 10.811 km² | 1.534 km² | **0 km²** |
| 26/08 04:00 | 275,6 K | 215,3 K | 9.817 km² | 842 km² | **0 km²** |

Contexto regional no instante do colapso (caixa 83–88 °E, 25,5–31,5 °N, ~274 mil km²): apenas **0,2 %** da caixa com topo abaixo de −60 °C, mínima de 210,4 K, e **nada abaixo de 200 K**.

Figura: `himawari_noite_25_26ago2026.png` — cinco painéis, magenta = topo abaixo de −60 °C.

---

## 3. Leitura

### 3.1 O sistema existiu, e na escala certa

Às **18:00 UTC de 25 de agosto havia 8.413 km² com topos abaixo de −60 °C** na vizinhança do sítio, e 32.886 km² abaixo de −33 °C. Isso é um sistema convectivo de mesoescala maduro.

Esse número importa: o cálculo do balanço de massa exigia que qualquer pistão capaz de entregar 14–17 M m³ tivesse entre **$10^2$ e $10^3$ km²**. O sistema observado tem **8.400 km²** de núcleo profundo. **A escala exigida não só é possível como foi observada.** O lado do suprimento da hipótese deixa de ser especulativo.

### 3.2 Mas ele se dissipou antes do colapso

A sequência é monotônica e inequívoca: 8.413 → 4.892 → 810 → **0** km². No instante do colapso, às 02:50 UTC, **não havia um único pixel abaixo de −60 °C em 150 km**, e a temperatura de brilho sobre o sítio era de 272,7 K (−0,4 °C) — superfície ou nuvem baixa, não topo convectivo.

Isso é consistente, e de forma independente, com tudo o que já havia sido apurado: o céu claro relatado, a ausência de chuva registrada pelo DHM, e o `rain_status: dry_valley` do próprio repositório.

**A versão da hipótese em que o pistão desaba do céu no instante do evento está excluída pela observação.** Não havia pistão no ar às 02:52 UTC.

### 3.3 A versão que sobrevive — e ela é melhor

O que os dados suportam é uma cadeia deslocada no tempo:

> Sistema convectivo de mesoescala sobre a região na noite de 25/08, com pico por volta das 18:00 UTC e 8.400 km² de núcleo profundo → deposição de neve e gelo sobre o anfiteatro de 3,39 km², e umedecimento/carregamento do maciço → **dissipação do sistema** → **colapso ~9 horas depois, sob céu limpo**, às 02:52 UTC.

Esta versão reconcilia, sem forçar nada, todas as observações que vinham em conflito:

| Observação | Como se encaixa |
| :--- | :--- |
| Céu claro no colapso | o sistema já se dissipara há horas |
| "A água veio do céu" | veio — na noite anterior, não no instante |
| Nenhum lago em 914 km² | a água estava como neve/gelo fresco no anfiteatro, não represada |
| Gelo do maciço intacto (−0,7 %) | o que desabou foi material **novo**, não a geleira antiga |
| Anfiteatro: 3,39 km², 85 % face norte, 47,8° | coletor frio e sombreado, geometria de acumulação |
| ~10⁸ m³ destacados | camada de 30–50 m sobre 3,39 km² = 169–339 M m³ |
| Sismo Ms 5,2 tipo `landslide` | falha de massa, não terremoto |

O elemento que eu vinha tratando como fatal — o céu limpo — deixa de ser objeção quando a cadeia é deslocada em nove horas. E o elemento que você insistia — a origem atmosférica — passa a ter suporte observacional direto.

---

## 4. O que isso não resolve

1. **Quanto o sistema precipitou sobre a bacia.** O IR mede topo de nuvem, não precipitação. Sem isso não se sabe se as 8.400 km² de convecção entregaram 10 mm ou 200 mm sobre o anfiteatro. **É o GPM IMERG de 2026** — os 96 grânulos já estão catalogados no repositório e exigem apenas a sua credencial NASA Earthdata. Agora há um motivo concreto e específico para querê-los.
2. **A posição exata do núcleo convectivo.** A paralaxe de ~37 km para leste, com visada a 68°, impede afirmar que o núcleo estava *sobre* o anfiteatro e não a algumas dezenas de km a oeste. **O INSAT-3D resolveria isso** — a 82 °E ele vê o sítio quase no nadir, sem paralaxe apreciável. Continua dependendo de cadastro no MOSDAC.
3. **O elo de Tinsley.** Nada aqui testa se a modulação de $J_z$ teve papel na organização daquele sistema. O que já se mediu é que o flare M6.9 alterou $J_z$ em ordem de $10^{-5}$ % — desprezível. Se a eletrodinâmica atuou, terá sido por outra via, e a única ainda aberta são os decréscimos de Forbush em raios cósmicos.
4. **O mecanismo de focalização.** Continua de pé o problema numérico: 8.400 km² de sistema contra 3,4 km² de anfiteatro. Deposição de neve ao longo de horas é um mecanismo de concentração muito mais plausível do que descarga instantânea — mas o fator ainda precisa ser quantificado.

---

## 5. Reprodução

```
bucket : https://noaa-himawari9.s3.amazonaws.com/AHI-L1b-FLDK/<AAAA/MM/DD/HHMM>/
arquivo: HS_H09_<AAAAMMDD>_<HHMM>_B13_FLDK_R20_S0310.DAT.bz2   (~2,5 MB por instante)
segmento S03 cobre 20,6 a 37,1 N; o sitio cai na linha 283, coluna 639
leitura: hsd.py  (cabecalho HSD de 11 blocos, Planck inverso, projecao geoestacionaria inversa)
serie  : hima_serie.py    figura: hima_fig.py
area por pixel: 2 x 2 km x 2,7 (correcao de obliquidade a 68 graus de zenite)
```

Validação do leitor: banda 13 a 10,407 µm, grade 550 × 5500, sub_lon 140,7°, COFF = LOFF = 2750,5, CFAC = LFAC = 20466275 — todos lidos do próprio arquivo e consistentes com a especificação do JMA. O pixel geolocalizado para o sítio cai em 85,510 °E / 28,257 °N, a menos de 2 km do alvo.
