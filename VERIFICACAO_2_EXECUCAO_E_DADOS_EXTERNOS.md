# Verificação 2 — Execução dos modelos e confronto com dados externos

**Data:** 07 de setembro de 2026
**Estado auditado:** `main` @ `a0fe6db` (5 commits novos após `69066f3`)
**Método:** `git archive main` exportado para diretório limpo fora do repositório; scripts executados com `miniforge3/python.exe` (numpy, pandas, rasterio, PIL, yaml); consultas diretas ao serviço FDSN do USGS.

---

## 1. Sismos — **VERIFICADO E CORRETO**

Consulta ao catálogo FDSN do USGS, janela ampla (2026-08-20 a 2026-09-07, 27,0–29,5 °N / 84,0–87,0 °E), sem filtro de magnitude. Retorno completo, duas linhas:

```
2026-08-26T02:52:10.000Z,28.271,85.515,0,5.2,ms_vx,landslide,55 km NW of Kodāri̇̄ Nepal,us7000tbwb
2026-08-26T06:00:35.000Z,28.270,85.515,0,4.2,ms_vx,landslide,55 km NW of Kodāri̇̄ Nepal,us7000tc90
```

O arquivo `data/raw/seismology/seismic_catalog_fdsn.csv` do repositório reproduz ambos corretamente: id, horário, profundidade 0 km, `Ms 5.2` / `Ms 4.2`, `magType = ms_vx`, `event_type = landslide`, `source_network = USGS NEIC`. **Os sismos ocorreram, nos horários e com as magnitudes agora declarados.** O "4,4 mb" foi eliminado dos documentos.

Duas ressalvas:

1. **Coordenadas alteradas sem justificativa.** O repositório registra o segundo evento em `28.268 / 85.510`; o catálogo do USGS traz `28.270 / 85.515`. Diferença irrelevante fisicamente, mas é um valor de catálogo modificado — num repositório cujo problema central foi exatamente esse, nenhum número de fonte primária deveria ser reescrito.
2. **O "Estágio 1 precursor às 01:45 UTC" não existe em nenhum catálogo.** `TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md`, linhas 90 e 151, mantém *"STAGE 1 (Precursor Crest Detachment): 26 Aug 01:45 UTC — 1,8 M m³ a 6.200→5.200 m"*. O rótulo melhorou (de `[FIELD REPORT / MODEL]` para `[FIELD REPORT / GEOMORPHIC MODEL]`), mas o horário permanece sem base: a busca sem filtro de magnitude não devolve nada às 01:45, e o tremor precursor efetivamente reportado em campo ocorreu às **08:20 NPT = 02:35 UTC**, 50 min depois.

---

## 2. Flare solar — **VERIFICADO**

Pico no arquivo real do repositório (`goes_xrays_7day_real.json`, download genuíno da NOAA):

```
2026-08-25T10:02:00Z   6,9774e-05 W/m²   →  M7.0 por conversão direta   |  satélite GOES-18
```

A NOAA classificou oficialmente como **M6.9, AR 4513**. Ambos os valores são defensáveis — 6,977e-5 arredonda para M7,0 e a NOAA usa o valor pré-arredondamento. Os documentos principais agora usam M6.9 / AR 4513. **Correto.**

**Mas o arquivo `analise_solar_jz_tempestades_infrassom.md` (linhas 28–34) mantém quatro rótulos `DADO OBSERVADO` sobre valores que o próprio repositório contradiz ou não possui:**

| Linha | Valor publicado como `DADO OBSERVADO` | O que o repositório de fato tem |
| ---: | :--- | :--- |
| 29 | `6,90 × 10⁻⁵ W/m²`, fonte **"GOES-16 XRS"** | pico real **6,977 × 10⁻⁵**, satélite **GOES-18** |
| 28, 31 | início/fim do flare, fonte "GOES-16 XRS" | idem — satélite errado |
| 32 | prótons >10 MeV = **0,85 pfu**, "GOES-16 SEISS" | `goes_integral_protons_real.json` traz 1,77 / 0,193 / 1,63 / 0,208 naquela hora; satélite 18; **0,85 não aparece** |
| 34 | topo de nuvem **T_b = −62,0 °C**, "INSAT-3D TIR-1" | **não existe nenhum arquivo INSAT no repositório** (`find . -iname "*insat*"` → vazio) |

Este é o padrão original ainda vivo, num arquivo que a segunda rodada de correção *editou*.

---

## 3. Cálculo de Jz — **EXECUTADO. Resultado decisivo.**

`python scripts/model_gec_jz_parametric.py` roda em ambiente limpo e imprime o aviso correto (*"Dados puramente modelados — sem leitura de magnetômetros reais"*). A condicional forçada foi de fato eliminada. Estatísticas da saída (169 horas):

| Grandeza | Modelo atual (sem o valor inserido à mão) | Alegado nas versões anteriores |
| :--- | ---: | ---: |
| $V_I$ máximo | **318,4 kV** | 356,4 kV |
| $J_z$ máximo | **4,082 pA/m²** | 4,57 pA/m² |
| **Instante do pico de $J_z$** | **2026-08-24 19:00 UTC** | 2026-08-25 10:02 UTC (flare) |

**Este é o achado central desta rodada.** Retirado o `delta_V_solar = 118.4` que havia sido digitado no código, o pico de $J_z$ deixa de coincidir com o flare e passa a cair **32 horas antes do colapso e 15 horas antes da erupção solar** — no máximo da curva de Carnegie (19h UTC), que é uma propriedade do modelo, não do evento.

Ou seja: a sincronia flare → $J_z$ → catástrofe, que era o eixo da hipótese, **era produzida pelo número inserido à mão**. Sem ele, ela não existe.

Verificação adicional: a resistência colunar implícita ($V_I \cdot 10^3 / J_z \cdot 10^{-12}$) permanece constante em **7,80 × 10¹⁶ Ω·m²** ao longo das 169 horas. $J_z$ continua sendo $V_I$ dividido por uma constante — não acrescenta nenhuma informação independente, exatamente como o campo `jz_derivation_note` do repositório agora admite.

*Nota física, à parte do código:* mesmo que $V_I$ fosse medido, não há base observacional para um flare classe M elevar o potencial ionosférico em ~50%. $V_I$ é sustentado pelos geradores de tempestades globais; os efeitos documentados de flares sobre o circuito elétrico global são de ordem percentual.

---

## 4. Balanço hídrico — **EXECUTADO**

`python scripts/calculate_inverse_hydraulics.py` roda a partir do YAML. Resultado para 2026:

```
Água líquida bruta ......... 14,20 M m³
  − lago no pico ...........  7,54 M m³
  − vazão de base ..........  2,59 M m³   (180 m³/s × 4 h)
  − fusão por atrito .......  0,11 M m³   (η = 0,030, ASSUMED_BY_ANALYST)
  = resíduo a explicar .....  4,07 M m³
  → chuva requerida ........  87,0 mm  sobre 55 km²
  medido ................... null   [DADO INDISPONÍVEL]
  déficit .................. null
```

**O déficit de 10× está eliminado**, e o repositório declara honestamente que sem medição não há déficit a afirmar. 87 mm é chuva de monção comum no Himalaia.

### 4.1 Objeção quantitativa: o repositório usa duas físicas diferentes para o mesmo tipo de evento

O YAML atribui `eta_frict = 0,85` a **Chamoli**, citando Shugar et al. (*"o atrito fundiu quase todo o gelo, resolvendo o balanço hídrico"*), e `eta_frict = 0,030` a **2026**, marcado `ASSUMED_BY_ANALYST`. Ambos são avalanches rocha-gelo de alta queda. Recalculando com $E_p = 1.255$ TJ e $L_f = 334$ kJ/kg:

| η | origem | fusão | resíduo | chuva requerida |
| ---: | :--- | ---: | ---: | ---: |
| 0,030 | 2026, assumido pelo analista | 0,11 M m³ | 3,96 M m³ | **84,6 mm** |
| 0,100 | valor intermediário | 0,38 M m³ | 3,69 M m³ | 79,0 mm |
| **0,850** | **Chamoli, no próprio YAML (Shugar)** | **3,19 M m³** | **0,87 M m³** | **18,7 mm** |

### 4.2 O limite físico duro

A massa assumida traz `ice_fraction = 0,40` sobre 4,0 × 10¹⁰ kg, ou seja **16 milhões de m³ de gelo arrastado**. O resíduo inteiro a explicar são 4,07 M m³.

> **O gelo incorporado na avalanche excede em 3,9× todo o volume de água que ainda falta explicar.**

Não é preciso invocar nenhum mecanismo novo. Há gelo de sobra para fechar o balanço por fusão, exatamente como Shugar et al. documentaram em Chamoli — e o repositório já aceita essa física, só que apenas para o outro evento.

---

## 5. Área do lago por satélite — **NÃO VERIFICÁVEL COM O DADO DO REPOSITÓRIO**

Abri `sentinel_lhende_khola_lake.tif` com `rasterio`:

```
CRS EPSG:4326 | 1376 × 768 px | 3 bandas | dtype uint8
pixel = 7,55 × 8,66 m = 65,4 m²
cena  = 10,39 × 6,65 km = 69,10 km²
```

São **3 bandas de 8 bits** — uma composição RGB de visualização, **não reflectância Sentinel-2 L2A**. Sem banda NIR, não há NDWI: água glacial e sombra de encosta são espectralmente inseparáveis em terreno de garganta. Testei quatro máscaras de severidade crescente:

| Critério | Área resultante |
| :--- | ---: |
| `b>r ∧ b>g ∧ média<90` | 2.575 ha |
| `b>r+8 ∧ b>g+4 ∧ média<70` | 1.480 ha |
| `b>r+15 ∧ b>g+8 ∧ média<60` | 673 ha |
| `b>r+25 ∧ média<50` | 215 ha |
| **Publicado no repositório** | **65,7 ha** |

Nenhum limiar plausível se aproxima de 65,7 ha; 22% da cena tem brilho médio abaixo de 30 (sombra de vale profundo).

**Conclusão honesta:** isto não prova que 65,7 ha esteja errado. Prova que **o número não é reproduzível a partir do que está arquivado**, e que a descrição "imagem multiespectral Sentinel-2" não corresponde ao produto que está no repositório. Para uma medição defensável seria necessário L2A com as bandas B3 e B8 (abertas, sem autenticação, via STAC Earth Search).

---

## 6. Integridade criptográfica — **AINDA FALHA (26 arquivos)**

```
FAILURES: 26, MISSING: 0
RESULTADO FINAL: AUDITORIA APONTOU INCONSISTÊNCIAS.
```

Listei os 26. **Todos são arquivos criados ou modificados pelas próprias rodadas de correção:** `himalayan_events_1980_2026.json`, os dois `lightning_data_*`, `timeline_master.csv`, `sensitivity_analysis_hydraulics.csv`, `seismic_catalog_fdsn.csv`, `gpm_imerg_granules_catalog_2026_official.json`, e **todo o conteúdo de `data/synthetic/`**.

Diagnóstico: **o manifesto `CHECKSUMS_SHA256.txt` nunca foi recomputado após as correções.** É a falha mais trivial de todas as pendências — um comando — e o `RELATORIO_DE_CORRECAO.md` continua afirmando *"o pipeline mestre foi executado com 100% de aprovação"*. Terceira verificação consecutiva em que esse autorrelato é desmentido pela execução.

---

## 7. Resíduos remanescentes

| Item | Onde | Estado |
| :--- | :--- | :--- |
| DOI errado de Shugar (`abg6027`) | `FONTES_E_REFERENCIAS_CIENTIFICAS.md:25` | ainda presente |
| `M7.0` sem a classificação oficial M6.9 | `REFERENCIAS_CIENTIFICAS_E_RELATOS_TESTEMUNHAIS_HIMALAIA.md` | ainda presente |
| Infrassom `104,1 dB SPL` atribuído à estação **I43US** da CTBTO | `ARTIGO_CIENTIFICO...md:19, 184, 194` | ainda presente, em contradição direta com o item 7 de `LIMITACOES_E_DADOS_INDISPONIVEIS.md`, que declara o infrassom da CTBTO `[DADO INDISPONÍVEL]`. O sufixo de duas letras em identificadores IMS é o código do país anfitrião; "I43US (Índia)" é incoerente. |
| Balanço humano (≈1.000–1.400 mortos, ≈4.000–5.500 desaparecidos) | `README.md` = **0 menções**; `ARTIGO_CIENTIFICO` = **0 menções** | não corrigido |
| Frase quebrada pela edição automática | `ARTIGO_CIENTIFICO...md:19` | *"registrado instrumentalmente pelo USGS como um colapso de encosta registrado pelo USGS NEIC como sismo Ms 5.2"* — a substituição textual deixou duplicação gramatical |
| Imagens IMERG datadas **2024** dentro de `data/satellite_imagery/himalaia_2026/` | 3 arquivos | ainda presentes |
| Área da bacia por DEM | — | nunca feita; 55–65 km² continua sendo escolha, não delineação (Copernicus GLO-30 é aberto) |
| Massa do colapso por inversão sísmica | — | nunca tentada; formas de onda FDSN são abertas e resolveriam a incerteza de 1,5e10 a 2,0e11 kg |

---

## 8. Conclusão

**O que está certo agora.** Os sismos são reais e estão corretamente catalogados. O flare é real e está corretamente classificado nos documentos principais. O balanço hídrico foi refeito com vazão de base e lago no pico, e resulta em 87 mm — declarado, com honestidade, como não comparável por falta de medição. Os dados sintéticos estão segregados e rotulados. O modelo de Jz roda com aviso explícito de que não lê magnetômetro nenhum.

**O que a execução revelou de novo.** Retirado o valor inserido à mão, **o pico de Jz migra para 24/08 às 19:00 UTC** — 32 h antes do colapso. A coincidência temporal que sustentava a hipótese eletrodinâmica era um produto do código, e desaparece quando o código é corrigido. Este é um resultado que só aparece rodando, e nenhum dos relatórios do repositório o menciona.

**O que ainda falta, em ordem de importância.**

1. Aplicar ao evento de 2026 a mesma física de fusão por atrito que o repositório já aceita para Chamoli. Com η = 0,85 a chuva requerida cai para **18,7 mm**, e os 16 M m³ de gelo arrastado excedem em 3,9× todo o resíduo. Não sobra anomalia a explicar.
2. Recomputar `CHECKSUMS_SHA256.txt` e parar de afirmar aprovação sem executar.
3. Retirar do `ARTIGO_CIENTIFICO` os 104,1 dB da CTBTO e o "Estágio 1 às 01:45 UTC", e incluir as vítimas nele e no README.
4. Corrigir os quatro rótulos `DADO OBSERVADO` de `analise_solar_jz_tempestades_infrassom.md`.
5. Delimitar a bacia por DEM e estimar a massa do colapso por inversão sísmica — ambos com dados abertos, sem permissão de ninguém.
