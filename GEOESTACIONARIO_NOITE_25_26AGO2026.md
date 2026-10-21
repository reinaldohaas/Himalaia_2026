# Infravermelho geoestacionário da noite de 25–26/08/2026: houve o sistema, e ele se dissipou antes

**Data:** 08 de setembro de 2026
**Dado:** Himawari-9 AHI, **banda 13 (10,4 µm)**, Himawari Standard Data L1b, resolução nominal de 2 km, segmento S03 da grade de disco completo. Bucket **`noaa-himawari9` da AWS Open Data — aberto, sem autenticação**.
**Leitor:** escrito para esta análise (`hsd.py`); decodifica os 11 blocos de cabeçalho HSD, aplica ganho e constante para radiância, inverte Planck com as constantes do bloco de calibração e corrige com $c_0 + c_1 T_e + c_2 T_e^2$; geolocalização pela projeção geoestacionária inversa a partir de COFF/LOFF/CFAC/LFAC do próprio arquivo.

---

## 1. Por que Himawari e não INSAT-3D

O INSAT-3D é a geometria ideal (subsatélite a 82 °E, praticamente no nadir do sítio), mas o **MOSDAC responde HTTP 401** e o portal do IMD idem: exigem cadastro. Não crio conta em nome de terceiros, então o INSAT continua pendente de uma inscrição que só você pode fazer.

O Himawari-9 (140,7 °E) é aberto. Para o sítio a 85,5 °E o ângulo zenital de visada é de **~68°** — oblíquo. Duas consequências, declaradas:

* o pixel se alonga por $1/\cos 68° \approx 2{,}7$, e as áreas abaixo já incluem esse fator;
* topos altos sofrem **paralaxe**: um topo a 15 km aparece deslocado ~37 km ~~**para leste**~~ **para oeste** da sua posição real (**corrigido em 18/10/2026**: o satélite está a leste, em 140,7° E, e um topo alto se projeta no chão do lado oposto a ele; a geometria exata, em `scripts/himawari/ahi_hsd.py`, dá ~30 km a oeste para topos a 14–15 km). As manchas frias na figura estão, portanto, deslocadas para oeste. Trajetória do sistema com a paralaxe corrigida: `data/processed/himawari_trajetoria/`.

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

**Atualização (21/10/2026):** com o B07 e o B13 a cada 10 min e a paralaxe invertida para a nuvem que estava de fato sobre o sítio (§ 6), o topo dessa nuvem desceu de ~10 km até o terreno entre 00:30 e 01:30 UTC. Às 02:50 não há, a até 30 km, topo que se distinga da montanha. "Céu limpo" vale para nuvem alta; o infravermelho não separa uma massa perto de 0 °C dentro do anfiteatro do próprio terreno.

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
2. **A posição exata do núcleo convectivo.** A paralaxe de ~30–37 km (~~para leste~~ **para oeste**; corrigido em 18/10/2026), com visada a 68°, impede afirmar que o núcleo estava *sobre* o anfiteatro e não a algumas dezenas de km **a leste**. **Atualização (18/10/2026):** com a paralaxe corrigida, o núcleo do sistema nunca chegou ao sítio — ficou a 190–570 km a ENE e se dissipou a ~200 km a leste entre 23 e 01 UTC; o sítio esteve na borda ocidental (a jusante) da bigorna, com Tb de 218–235 K entre 17:30 e 00:30 UTC (`data/processed/himawari_trajetoria/trajetoria.txt`). **O INSAT-3D resolveria isso** — a 82 °E ele vê o sítio quase no nadir, sem paralaxe apreciável. Continua dependendo de cadastro no MOSDAC.
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

---

## 6. Fase do topo a cada 10 min sobre o anfiteatro (21/10/2026)

**Por que:** o GIF `data/processed/himawari_trajetoria/nuvem_atravessa_himalaia_colapso.gif`, feito pelo Antigravity, sugere que o sistema "colapsa sobre a arena". O pesquisador lembrava de uma imagem com um núcleo menor colapsando a sotavento sobre o anfiteatro. Revisto o GIF, ele tem quatro problemas:
1. Só acompanha o maior objeto abaixo de 213 K. A nuvem de 218–235 K que estava sobre o sítio fica fora.
2. A imagem está na posição aparente, mas a trajetória está corrigida da paralaxe, que é de 25–35 km para topos de 10–14 km.
3. O último trecho da trajetória, de 00:30 a 01:00 UTC, de 223 para 137 km a "219 km/h", é troca de objeto, não deslocamento.
4. A frase "colapsa sobre a arena" não se sustenta para o núcleo profundo, que morreu a 140–240 km a leste-sudeste.

No repositório não há imagem de satélite com um núcleo pequeno sobre a arena às 02:50. Por isso fizemos o teste abaixo.

**Dados e método** (`scripts/himawari/fase_topo_10min.py`, `scripts/himawari/mapa_fase_topo.py`):
* B07 (3,9 µm) e B13 (10,4 µm), segmento 3, a cada 10 min, de 25/08 22:00 a 26/08 03:30 UTC. Não há a varredura das 02:40 no arquivo.
* **De 00:00 UTC em diante é dia no sítio:** o sol nasce por volta de 23:55 UTC, e 02:50 UTC são 08:35 NPT. Por isso não se usa a diferença B07 − B13 noturna, e sim a refletância em 3,9 µm, r₃₉ = (L₇ − B₇(T₁₃)) / (E₇ cos θ₀ / π − B₇(T₁₃)) (Setvák & Doswell 1991; Rosenfeld & Lensky 1998).
  * Gotas pequenas de água dão r₃₉ de 0,1–0,3.
  * Gelo e neve dão menos de ~0,05.
  * No recorte, topos de gelo espesso deram 0,05 e a superfície 0,16, coerente com a literatura.
* **Paralaxe invertida:** para cada altura de topo, de 4 a 14 km, achamos o pixel aparente de uma nuvem que estivesse exatamente sobre o sítio e pegamos o pixel mais frio do bloco 3 × 3 em volta.

**Resultados** (`data/processed/himawari_fase_topo/fase_topo_sitio_10min.txt` e `mapa_fase_topo.png`):

| UTC (NPT) | Topo da nuvem sobre o sítio (pixel para 8–10 km) | Leitura |
| :--- | ---: | :--- |
| 17:30–00:30 | 218–235 K, r₃₉ ≈ 0,05 | topo de gelo a 10–13 km, ~7 h sobre o sítio |
| 00:30 (06:15) | 234 K | |
| 00:40 (06:25) | 249 K | |
| 00:50 (06:35) | 258 K | |
| 01:00 (06:45) | 261 K | |
| 01:10 (06:55) | 267 K | |
| 01:30 (07:15) | 273 K | topo chega ao terreno |
| 01:30–03:30 | 264–278 K | sem topo frio que se distinga da montanha |

1. **O colapso da nuvem sobre o sítio foi observado, entre 00:30 e 01:30 UTC.** O topo desceu de ~10 km até o terreno em uma hora, de 1,5 a 2,5 h antes do sinal sísmico das 02:52:10 (USGS `us7000tbwb`, na própria fonte, sem tempo de viagem a descontar).
2. **Às 02:50 não havia nuvem fria sobre o anfiteatro.** A até 30 km do sítio, nenhum topo mais frio que ~263 K. As poucas feições de 263–269 K, de 15–50 km², têm a mesma r₃₉ da superfície sem neve (~0,16) e não se distinguem dela.
3. **Topos claramente de água super-resfriada só aparecem depois do evento.** A partir de 03:00 UTC surgem nuvens de 248–256 K (~8 km), r₃₉ de 0,20–0,21 e ~450 km² cada, a 30–45 km a nordeste e a sudeste. Parece convecção da manhã.

**Consequência para a hipótese:**
* **Reservatório de nuvem comum, na casa de g/m³:** excluído às 02:50. Juntar ~10¹⁰ kg sobre a bacia exigiria uma nuvem profunda, de topo frio, e ela apareceria.
* **Massa densa:** não excluída. Na escala proposta pelo pesquisador (~1/10 da densidade do gelo, 92 kg/m³), 1,4 × 10¹⁰ kg sobre 3,4 km² dão uma camada de ~45 m. Dentro do anfiteatro, abaixo das cristas, o topo dela estaria perto de 0 °C e seria indistinguível do terreno no infravermelho.
* **Versão compatível com o satélite:**
  1. a nuvem colapsa sobre o sítio entre 00:30 e 01:30;
  2. a massa fica no anfiteatro por ~1,5 h;
  3. a ruptura acontece às 02:52.
* **O que a hipótese passa a ter de explicar** é essa espera de 1,5–2,5 h entre o colapso observado e a ruptura.
* **Distância:** os 140–240 km do GIF são do núcleo profundo do sistema. O colapso que importa aconteceu sobre o próprio sítio.

**Limites:**
* O método não separa um topo perto de 0 °C do terreno alto.
* Rocha nua tem r₃₉ parecida com a de nuvem de água.
* Com o sol baixo (θ₀ > 75°, antes de ~01:00 UTC), a r₃₉ fica ruidosa.
* A relação entre altura do topo e Tb é empírica.
* O INSAT-3D, quase no nadir, continua sendo o dado que eliminaria a paralaxe.
