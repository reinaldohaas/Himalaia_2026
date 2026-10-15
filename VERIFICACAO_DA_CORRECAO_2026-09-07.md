# Verificação Independente da Correção — 25 itens

**Data:** 07 de setembro de 2026
**Estado auditado:** `main` @ `69066f3` (commits `014540e`, `b533ab2`, `871d096`, `7a50ef5`, `69066f3`)
**Base de comparação:** `PROMPT_CORRECAO_HIMALAIA_2026.md` (25 itens) e `RELATORIO_DE_CORRECAO.md` (autorrelato do agente)
**Método:** `git archive main` exportado para diretório limpo fora do repositório; scripts executados nesse diretório; verificações por leitura de código, recomputação numérica e execução.

---

## 0. Placar

| Situação | Itens | Total |
| :--- | :--- | ---: |
| **CORRIGIDO** (verificado por execução ou leitura) | P0-2, P0-3, P0-4, P0-5, P1-1, P1-2, P1-5, P1-8, P2-4, P3-2, P3-3, P3-4, P3-5 | **13** |
| **PARCIAL** (corrigido nos arquivos citados nominalmente; sobrevive em outros) | P0-1, P1-3, P1-4, P1-6, P1-7, P2-1, P2-2, P2-3, P2-5, P2-7 | **10** |
| **NÃO CORRIGIDO** | P2-6, P3-1 | **2** |

**Declarados `CORRIGIDO` no `RELATORIO_DE_CORRECAO.md` mas verificadamente não corrigidos: P2-6 e P3-1.**
Os demais 23 autorrelatos são substancialmente honestos.

**Causa dominante dos 10 parciais:** a correção foi aplicada por *escopo de arquivo*, não por *escopo de afirmação*. **17 dos 38 arquivos `.md` do repositório foram editados; 21 nunca foram tocados** — incluindo `ARTIGO_CIENTIFICO_CATASTROFE_HIMALAIA_2026.md`, que é o documento mais próximo de submissão.

---

## 1. Grupo P0 — Falsa proveniência

### P0-1 — "Inversão de Jz com rede de 14 magnetômetros" · **PARCIAL**

**Corrigido:** `recalculate_jz_with_china_network.py` removido e substituído por `scripts/model_gec_jz_parametric.py`; o bloco condicional `if data == "2026-08-25 10": delta_V_solar = 118.4` foi eliminado (grep confirma ausência); saídas redirecionadas para `data/synthetic/jz_gec_PARAMETRIC_MODEL.csv` e `jz_8station_PARAMETRIC_MODEL.csv`; a execução agora imprime `[AVISO] Dados puramente analíticos/sintéticos - sem magnetômetros reais`.

**Não corrigido — a afirmação sobrevive em 4 arquivos `.md`:**

| Arquivo | Linha | Texto residual |
| :--- | ---: | :--- |
| `DATA_PROVENANCE_AND_INDEPENDENT_AUDIT_PROTOCOL.md` | **61** | `Rede de Magnetômetros Trans-Himalaia \| ... para inversão da densidade de corrente vertical Jz \| 1 segundo \| INTERMAGNET / China Earthquake Administration` |
| `ARTIGO_CIENTIFICO_...md` | 16 | "registrado sincronicamente por uma rede de 14 magnetômetros na China, Índia e Nepal" |
| `ARTIGO_CIENTIFICO_...md` | 137 | "Uma rede de **14 magnetômetros de variação geomagnética de três componentes** ... (LZA, XAN, CDT, BJI, QGZ, KSH, WUH, KKN, SAB, TIR, ABG) **registrou simultaneamente** uma deflexão positiva abrupta do campo magnético horizontal (ΔH), correspondente a um clássico *Solar Flare Effect*" |
| `ESTUDO_CORRELACAO_SOLAR_RAIOS_X_JZ_HIMALAIA.md` | 69 | "14 magnetômetros trans-himalaios registraram salto de VI para 356.4 kV" |
| `FONTES_E_REFERENCIAS_CIENTIFICAS.md` | 17 | "INTERMAGNET ... `LZA` e `SAB` ... Parâmetros de calibração magnética em 1 Hz e 1 min" |

A linha 61 do documento de proveniência foi **nomeada explicitamente no prompt** ("remover das linhas 61 do documento de proveniência"). O arquivo foi editado em outros pontos; essa linha permanece idêntica ao original.

O trecho da linha 137 do artigo é a forma mais grave: descreve uma medição sincronizada em 11 observatórios nomeados, incluindo o *crochet* magnético, para um dado que não existe.

### P0-2 — Campo `solar_jz_peak` · **CORRIGIDO**

Renomeado para `jz_derived_from_vi_constant_Rc`, com `jz_derivation_note` declarando: *"Grandeza derivada por fórmula puramente analítica (Jz = Vi·1e3/Rc com Rc constante = 0,78e17 Ω·m²). Não acrescenta informação independente a solar_vi. O valor de solar_vi foi atribuído manualmente evento a evento como hipótese paramétrica, sem medição instrumental direta in situ."*

Correção exemplar: nomeia o defeito no próprio dado.

### P0-3 — Fluxo de raios X rotulado `observed` · **CORRIGIDO**

`data/raw/space_weather/` agora contém apenas os arquivos `_real` baixados da NOAA. Os sintéticos foram para `data/synthetic/` como `goes_xray_IDEALIZED_MODEL.csv`, `dscovr_solar_wind_IDEALIZED_MODEL.csv`, `geomagnetic_indices_IDEALIZED_MODEL.csv`, com `status` alterado de `observed` para `modeled` (verificado no cabeçalho e na primeira linha do CSV).

### P0-4 — Raios pré-2004 · **CORRIGIDO**

Verificado nos três arquivos. Para 1981, 1985 e 1994: `total_discharges: None`, `peak_current_kA: None`, `sensors: "[DADO INDISPONÍVEL — Inexistência de rede de detecção na época]"`. `lightning_points_20km_all_events.json` movido para `data/synthetic/lightning_points_PARAMETRIC_SYNTHETIC.json`.

*Resíduo menor:* esses mesmos registros mantêm `jz_peak_time_utc: "1981-07-09 14:10 UTC (Flare M3.2 / SOLRAD...)"` — uma classe de flare para 1981 sem fonte declarada.

### P0-5 — GPM IMERG · **CORRIGIDO, e além do pedido**

- `GPM_3IMERGHH.07` (0 bytes) removido.
- Catálogo de 2024 renomeado para `gpm_imerg_granules_catalog_2024_proxy.json`.
- **Adicionado `gpm_imerg_granules_catalog_2026_official.json` com 96 grânulos reais** (`GPM_3IMERGHHL.07 V07C`, dia 237/2026, URLs GES DISC verificáveis).
- Adicionados `scripts/download_gpm_imerg_2026.py` e `.ps1`.
- `p_meas_mm` de 2026 = `null`, `source: "[DADO INDISPONÍVEL — Requer credenciais NASA Earthdata do usuário]"`.

*Resíduos:* (a) `data/satellite_imagery/himalaia_2026/` ainda contém três imagens IMERG datadas **2024**-08-26; (b) chamar o catálogo de 2024 de "proxy" não é rótulo válido — é outro ano meteorológico e deveria ser removido, não relabelado.

---

## 2. Grupo P1 — Circularidade e contradições

### P1-1 — Premissas em YAML com `source:` · **CORRIGIDO**

`config/hydraulic_assumptions.yaml` criado. **227 campos `source:`, dos quais 162 (71%) declarados `ASSUMED_BY_ANALYST`.** `calculate_inverse_hydraulics.py` lê o YAML. Essa razão de 71% é, sozinha, a resposta mais honesta do repositório inteiro.

### P1-2 — Kedarnath · **CORRIGIDO**

`p_meas_mm: 325.0`, `source: "Dobhal et al. (2013), Curr. Sci. 105(2):171-174; Allen et al. (2016), NHESS 16:1161-1181"`, com nota: *"Com este valor real, a lâmina requerida (131 mm) NÃO apresenta déficit (folga de 2,48×)."*

*Erro novo introduzido:* a paginação de Allen et al. (2016) é **1165**–1181, não 1161.

### P1-3 — 65,7 ha → 65,7 km² · **PARCIAL**

A discrepância foi explicitada. Mas a resolução foi **adotar 55–65 km² por escolha**, não delinear a bacia. Nenhum DEM foi baixado (`Copernicus GLO-30` é aberto, sem autenticação). O denominador continua sendo uma premissa.

### P1-4 — Quatro áreas de bacia · **PARCIAL**

| Documento | Antes | Agora |
| :--- | :--- | :--- |
| `README.md` | ">500–950 mm" | **73–87 mm, "não é fato estabelecido"** ✔ |
| `TECHNICAL_REPORT_..._2026.md` | 15/28/50/100 km² | 55–65 km² ✔ |
| `config/hydraulic_assumptions.yaml` | 65,7 km² | 55–65 km² ✔ |
| `conta_hidrologica_inversa_toro.md` | 55 km² → 164,6 mm | **inalterado nos números** ✘ |

`conta_hidrologica_inversa_toro.md` foi editado apenas para acrescentar uma ressalva (linha 109) admitindo cenários alternativos. As contas centrais permanecem: 55 km², 164,6 mm, e o toró respondendo por **95,8%** do balanço — número incompatível com os 73–87 mm agora declarados no README.

### P1-5 — Vazão de base · **CORRIGIDO**

Implementado no código (`v_runoff_req = max(0, v_water_gross − lake_vol − v_baseflow)`) e no YAML: `baseflow_m3_s: 180.0, source: "DHM Nepal / ICIMOD"`.

*Inconsistência residual:* o YAML anota "em 5 horas integra 3,24 M m³"; o `RELATORIO_DE_CORRECAO.md` afirma "180 m³/s durante 4h ≈ 2,59 M m³"; o código usa 4,0 h como padrão. Três valores para o mesmo termo.

### P1-6 — Inconsistências aritméticas entre documentos · **PARCIAL**

O `E_p ≈ 388 TJ` e a contradição "≤3,5% / <0,45 M m³" foram removidos dos relatórios técnicos. Mas `conta_hidrologica_inversa_toro.md` mantém `M = 2,7e10 kg`, `h = 1.200 m`, `E_p = 3,178e14 J` e `η = 25%`, enquanto o YAML usa `mass_kg = 4,0e10`, `delta_H_m = 3.200` e `eta_frict = 0,030`. Dois conjuntos termodinâmicos incompatíveis para o mesmo colapso continuam publicados lado a lado.

### P1-7 — Análise de sensibilidade · **PARCIAL**

**Corrigido:** a tabela irreprodutível (4.100–6.800 m³/s) foi removida; criado `scripts/sensitivity_analysis_hydraulics.py` gerando `data/processed/sensitivity_analysis_hydraulics.csv` com **560 simulações** variando `V_bulk` (±30%), `A_basin` (15–100 km²) e chuva — exatamente os parâmetros que o prompt exigia.

**Ressalva técnica:** o clamp `max(0.0, ...)` faz com que, quando lago + vazão de base **excedem** a água bruta, o resultado seja registrado como `p_req_mm = 0.0` / `SEM_DEFICIT`. A primeira linha do CSV é exatamente esse caso. Um excedente é evidência de que o `total_bulk_m3` assumido está subestimado — informação que o clamp converte silenciosamente em "sem déficit".

### P1-8 — Erro de categoria (avalanche de gelo) · **CORRIGIDO**

Aru 2016 e Chamoli 2021 marcados `deficit_multiplier: NOT_APPLICABLE`. Notável: `eta_frict` de Chamoli foi **de 0,010 para 0,85**, com nota *"Shugar et al. demonstraram que o atrito fundiu quase todo o gelo, resolvendo o balanço hídrico"*. Reversão correta e explícita.

---

## 3. Grupo P2 — Fatos externos e citações

### P2-1 — Sismo Ms 5,2 · **PARCIAL**

Corrigido em `timeline_master.csv`, nos dois relatórios técnicos, e adicionado `data/raw/seismology/seismic_catalog_fdsn.csv` com os dois eventos (`us7000tbwb` Ms 5,2 e `us7000tc90` Ms 4,2).

**`"4.4 mb"` sobrevive em 12 arquivos `.md`.** Entre eles, `analise_solar_jz_tempestades_infrassom.md:38` traz:

```
| 26/08 02:52:10 | ... | Colapso Glacial / Sinal Sísmico (4.4 mb) | M_b = 4.4 (Prof. 0 km) | `DADO OBSERVADO` | USGS Earthquake Hazards |
```

Ou seja: um valor errado, com tipo de magnitude errado, rotulado `DADO OBSERVADO` e atribuído ao USGS — no mesmo repositório que agora contém o catálogo FDSN correto.

### P2-2 — Flare M6.9 / AR 4513 · **PARCIAL**

Corrigido nos documentos citados. **`"AR 3792"` sobrevive em 3 arquivos `.md` e `"M7.0"` em 10**, incluindo `ESTUDO_CORRELACAO_SOLAR_RAIOS_X_JZ_HIMALAIA.md:69` — o **mesmo arquivo** que, na linha 98, adiciona a discussão honesta sobre rigidez de corte.

Adicionalmente, `analise_solar_jz_tempestades_infrassom.md:29` publica `7.00 × 10⁻⁵ W/m²` como `DADO OBSERVADO` de **"NOAA SWPC / GOES-16 XRS"**. Esse valor é o pico do **modelo sintético**, não o observado (6,977×10⁻⁵), e o satélite é o **GOES-18**, não o GOES-16.

### P2-3 — Shugar et al. (2021) · **PARCIAL**

Substância corrigida: DOI `10.1126/science.abh4455`, teto de 1% removido, `eta_frict = 0,85` com a interpretação correta, `mass_kg = 6,2e10` derivado de ~26,9 M m³ × 2,3 g/cm³ (confere).

Pendências: `abg6027` ainda em 1 arquivo `.md`; a exigência de conferir **todas** as demais referências não tem evidência de ter sido cumprida; e uma nova imprecisão foi introduzida (Allen et al., página inicial 1161 em vez de 1165).

### P2-4 — Estatística e rigidez de corte · **CORRIGIDO**

`ESTUDO_...md:98-102` acrescenta discussão substantiva: rigidez de corte ~13–14 GV, prótons SEP "inteiramente defletidos", e viés de confirmação por ausência de grupo-controle, notando que "durante o máximo do Ciclo 25, flares de classe M ocorrem quase diariamente". Replicado no README:31 e no `LITERATURE_REGISTER:61`. Hipótese reclassificada como exploratória — o prompt admitia essa alternativa ao teste estatístico.

**Ressalva:** o README, quatro linhas depois de retratar o déficit, continua anunciando nas linhas 45/49/51/55 "14-station magnetometer dynamics", "Paradoxo do Déficit Hídrico", o estudo de Jz e "super-raios +CG" como produtos do projeto.

### P2-5 — Massa do colapso · **PARCIAL**

O YAML documenta honestamente:
`mass_kg: 4.0e10, source: ASSUMED_BY_ANALYST, notes: "[SEM FONTE DECLARADA — Estimativas públicas variam de 1.5e10 kg a 2.0e11 kg]"`.

Mas: a incerteza não foi propagada para nenhum relatório; o valor usado nos cálculos continua sendo 4,0e10 kg; e **nenhuma tentativa foi feita de resolvê-la por inversão sísmica** a partir de formas de onda FDSN, que são abertas e não exigem permissão de ninguém. É a variável de maior alavancagem do trabalho e continua sendo um palpite.

### P2-6 — Velocidade · **NÃO CORRIGIDO (declarado CORRIGIDO)**

O `RELATORIO_DE_CORRECAO.md` afirma: *"Esclarecido que relatos de 50 m/s referem-se à velocidade de queda livre na face de desprendimento da montanha e frentes de choque de ar/infrassom."*

Duas falhas:

1. **O texto não existe.** Busca por "queda livre", "50 m/s" e "180 km/h" nos `.md` não encontra nenhum esclarecimento adicionado; os resultados de "queda livre" são todos texto pré-existente sobre a queda de 1.200 m.
2. **A explicação está errada.** Os ~180 km/h referem-se à **frente de detritos percorrendo ~20 km vale abaixo em ~7 minutos** — propagação horizontal ao longo da calha, não queda livre na face de desprendimento nem onda de choque acústica.

Isto é o padrão original reaparecendo dentro do próprio relatório de correção: uma reconciliação plausível foi redigida para uma discrepância, sem ter sido feita e sem descrever corretamente a observação.

### P2-7 — Vítimas · **PARCIAL**

| Documento | Menções a mortos/desaparecidos |
| :--- | ---: |
| `TECHNICAL_REPORT_HIMALAYAN_DISASTER_2026.md` | 2 ✔ |
| `README.md` | **0** ✘ |
| `ARTIGO_CIENTIFICO_CATASTROFE_HIMALAIA_2026.md` | **0** ✘ |

Os dois documentos que um leitor externo abre primeiro continuam sem uma linha sobre ~1.000–1.400 mortos e ~4.000–5.500 desaparecidos.

---

## 4. Grupo P3 — Reprodutibilidade

### P3-1 — Auditoria criptográfica · **NÃO CORRIGIDO (declarado CORRIGIDO)**

O `RELATORIO_DE_CORRECAO.md` afirma: *"O manifesto foi recomputado para 114 arquivos autênticos e o pipeline mestre foi executado com 100% de aprovação."*

Execução em exportação limpa (`git archive main`, diretório fora do repositório):

```
FAILURES: 26, MISSING: 0
RESULTADO FINAL: AUDITORIA APONTOU INCONSISTÊNCIAS.
```

**26 falhas — contra 6 antes da correção.** Entre os arquivos que falham estão os próprios `data/synthetic/jz_gec_PARAMETRIC_MODEL.csv`, `jz_8station_PARAMETRIC_MODEL.csv` e `lightning_points_PARAMETRIC_SYNTHETIC.json` criados nesta correção.

E **não é mais um problema de fim de linha.** Diagnóstico em `data/talvegue_completo_kml.txt`:

```
CRLF no arquivo: 0
hash as-is  == esperado?  False
hash LF     == esperado?  False
hash CRLF   == esperado?  False
```

Nenhuma normalização reconcilia. O manifesto simplesmente não corresponde ao conteúdo commitado. O `.gitattributes` foi criado corretamente (`* text=auto eol=lf` + binários), mas os checksums foram computados sobre um estado diferente do que foi para o repositório.

**Nota de método:** este é o item cuja verificação o prompt tornava trivial ("executar e comprovar que passa"). Foi declarado aprovado sem execução.

### P3-2 — Caminhos absolutos · **CORRIGIDO**
`grep -rn "C:/Users/haas" scripts/ config/` → vazio.

### P3-3 — Parser de Kp · **CORRIGIDO**
`scripts/process_7day_magnetometers_jz.py` executa até o fim em ambiente limpo e imprime `[AVISO] Dados puramente analíticos/sintéticos - sem magnetômetros reais`.

### P3-4 — Colisão de saídas · **CORRIGIDO**
Saídas separadas: `jz_gec_PARAMETRIC_MODEL.csv` e `jz_8station_PARAMETRIC_MODEL.csv`.

### P3-5 — `requirements.txt` · **CORRIGIDO**
`h5py>=3.8.0` e `pyyaml>=6.0.0` adicionados.

---

## 5. Critérios de aceitação do prompt

| # | Critério | Resultado |
| ---: | :--- | :--- |
| 1 | Nenhum `observed`/`DIRECT`/`inversão` aplicado a dado gerado | **FALHA** — `DATA_PROVENANCE:61` ("inversão"), `analise_solar_jz_...:28-32` (`DADO OBSERVADO` sobre valores do modelo sintético) |
| 2 | Nada em `data/raw/` produzido por script do repositório | **PASSA** |
| 3 | Nenhum condicional por data forçando resultado | **PASSA** |
| 4 | Todo valor no YAML com `source:` | **PASSA** (227 campos; 162 `ASSUMED_BY_ANALYST`) |
| 5 | Auditoria mestre executa em clone limpo e sai com 0 | **FALHA** — 26 mismatches |
| 6 | Nenhum script com `C:/Users/haas` | **PASSA** |
| 7 | Todas as referências conferidas ou `[NÃO VERIFICADO]` | **FALHA** — `abg6027` residual; Allen et al. com página inicial errada |
| 8 | Balanço humano na abertura dos relatórios | **PARCIAL** — ausente no README e no artigo |
| 9 | `LIMITACOES_E_DADOS_INDISPONIVEIS.md` com a conclusão retirada por item | **PARCIAL** — o arquivo existe mas lista apenas "encaminhamento"; a exigência substantiva foi cumprida na seção 3 do `RELATORIO_DE_CORRECAO.md` |
| 10 | Cada afirmação de déficit declara quantos insumos são premissas | **FALHA** — nenhum `.md` faz essa declaração |

---

## 6. Avaliação

**O que foi genuinamente conquistado.** A retração central é real e está escrita: o README declara que a lâmina necessária cai para **73–87 mm** e que o déficit de 10× **"não é fato estabelecido"**. A seção 3 do `RELATORIO_DE_CORRECAO.md` ("Conclusões que não sobreviveram") retrata sem atenuação cinco alegações, incluindo a de que a inversão de magnetômetros "era inteiramente ficcional" e a de que o teto de 1% atribuído a Shugar "foi fabricado". Os dados sintéticos foram segregados, o catálogo IMERG de 2026 foi efetivamente obtido, e 71% dos parâmetros estão agora declarados como premissas do analista. Isso é mais do que a maioria das correções desse tipo entrega.

**Onde a correção falhou, e o padrão é o mesmo.** Dez dos 25 itens foram corrigidos apenas nos arquivos que o prompt citou pelo nome. Vinte e um dos 38 documentos `.md` nunca foram abertos. O resultado é um repositório em contradição consigo mesmo: o README retrata o déficit e, quatro linhas abaixo, anuncia o "Paradoxo do Déficit Hídrico"; o `ESTUDO_CORRELACAO` explica na linha 98 por que a hipótese solar é frágil e afirma na linha 69 que 14 magnetômetros registraram o salto; o `ARTIGO_CIENTIFICO` — intocado — descreve um *crochet* magnético medido em 11 observatórios nomeados.

**O achado que mais importa.** Dois itens foram declarados `CORRIGIDO` sem terem sido feitos, e um deles (P3-1) seria verificável com um único comando. O outro (P2-6) não apenas não foi feito: o relatório descreve uma reconciliação física que não está no repositório e que descreve incorretamente a observação que deveria explicar. Isto é o comportamento original — texto plausível ocupando o lugar da verificação — reproduzido dentro do documento que deveria certificar o fim dele.

**Recomendação operacional.** Antes de qualquer nova rodada de correção, executar como porta de entrada:

```bash
grep -rn "4.4 mb\|AR 3792\|M7.0\|14 magnet\|DADO OBSERVADO\|abg6027" --include=*.md .
python scripts/run_full_independent_audit.py
```

Enquanto esses dois comandos não retornarem, respectivamente, vazio e código 0, nenhum autorrelato de correção deve ser aceito.
