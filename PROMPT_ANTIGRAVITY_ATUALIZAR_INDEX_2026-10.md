# Prompt para o antigravity — atualizar o `index.html` com os dados de outubro de 2026

**Arquivo a alterar:** só `C:\Users\haas\github\Himalaia_2026\index.html` (painel "Painel Científico Integrado: A Catástrofe do Himalaia"). Não altere nenhum outro arquivo, nem o diretório `.claude\worktrees\`.

**Onde estão os dados novos:** na branch `claude/himalaia-enchentes-auditoria-fcfdb5` do GitHub (`reinaldohaas/Himalaia_2026`), também disponível localmente, só para leitura, em `C:\Users\haas\github\Himalaia_2026\.claude\worktrees\himalaia-enchentes-auditoria-fcfdb5\`. Leia os arquivos citados abaixo antes de escrever; copie números deles, não destas instruções.

## Regras

1. **Cada número exibido leva o rótulo da sua natureza:** `OBSERVADO` (instrumento), `REANÁLISE` (ERA5), `MODELO` (CM1, WRF), `PARAMÉTRICO` (fórmula com valores atribuídos à mão) ou `HIPÓTESE`. Nada sintético ou paramétrico aparece ao lado de observações sem esse rótulo visível.
2. **Não invente números, horários, fontes nem conclusões.** Se um dado não estiver nos arquivos indicados, não o coloque.
3. **Não apague o conteúdo existente que continua válido;** corrija o que os dados novos contradizem e acrescente o resto.
4. **Mantenha o funcionamento atual** (MapLibre, Chart.js, Bootstrap, abas, linha do tempo). Teste abrindo o arquivo no navegador e confira que não há erro no console.
5. Ao terminar, escreva `RELATORIO_ATUALIZACAO_INDEX_2026-10.md` com a lista de cada mudança (antes → depois → arquivo-fonte).

## O que mudou, e onde está

### 1. Clima espacial — dados reais do GOES (`data/raw/space_weather/`)
* `goes_xrays_7day_real.json`: o flare de 25/08 foi **M7.0, pico às 10:02 UTC (15:47 NPT)** — o painel diz M6.9; corrija. Houve outros cinco flares classe M na semana (21–26/08).
* `goes_integral_protons_real.json`: **sem evento de prótons** (≥ 10 MeV abaixo de 3 pfu em 25/08; o limiar S1 é 10 pfu).
* `noaa_planetary_k_index_real.json`: **campo geomagnético calmo** (Kp 0,3–1,7 em 25–26/08).
* **Jz:** os valores 3,22 e 4,57 pA/m² são `PARAMÉTRICO` (`data/synthetic/README.md`: Jz = V_I / R_c com V_I atribuído à mão; nenhum magnetômetro lido). Mantenha-os só com esse rótulo, fora dos KPIs de observação, e diga que **não há medição de Jz para o evento**. Segundo Tinsley e Zhou (ICAE 2014, figura 1), o Jz é naturalmente alto sobre o Himalaia por causa da altitude; isso é contexto, não medição do evento.

### 2. O sistema convectivo no Himawari-9 — trajetória medida (`data/processed/himawari_trajetoria/`)
* `trajetoria.txt` / `trajetoria.json` (B13, a cada 30 min, paralaxe corrigida; figura `trajetoria.png`). `OBSERVADO`.
* Um sistema convectivo de mesoescala **no planalto tibetano, perto de Lhasa**, com 100–146 mil km² de topos < 213 K entre 09 e 13 UTC de 25/08, **andou para WSW a ~20–60 km/h** e se **dissipou a ~200 km a leste do sítio entre 23 e 01 UTC**. O centro nunca chegou ao sítio; o sítio ficou na **borda ocidental (a jusante) da bigorna**, com topo de 218–235 K entre 17:30 e 00:30 UTC, e céu limpo de nuvem alta no colapso (02:50 UTC).
* Proposta: desenhar a trajetória no mapa (linha com os horários) e acrescentar o evento à linha do tempo.
* **Correção:** a paralaxe desloca os topos para **oeste** (o documento antigo dizia leste; corrigido em `GEOESTACIONARIO_NOITE_25_26AGO2026.md`).

### 3. O sistema na ERA5 (`data/processed/era5_verificacao_mcs/era5_x_himawari.txt`)
* `REANÁLISE`: a ERA5 tem o sistema na fase madura (10–13 UTC, a 10–80 km do centro observado), mas o **dissipa às 14–16 UTC e não o propaga para oeste**; a aproximação da noite não está na ERA5.

### 4. CM1 — resultados (`TORO_CM1_SONDAGEM_REAL_ERA5.md`, §8 a §10)
* `MODELO`. Com radiação e fluxos: convecção profunda à tarde, até ~5–9 mil t de água super-resfriada sobre o anfiteatro, precipitação focada nele; ~0 de água super-resfriada no instante do colapso (§8, §9).
* **Anti-varredura de Tinsley implementada no CM1 (§10):** ela **arma** um reservatório de água super-resfriada sobre o anfiteatro às 02:00–02:30 UTC (18–25× o controle, a −8/−10 °C), mas **nenhum experimento produz liberação explosiva** — nem com vórtice imposto, nem com gelo vindo de cima, nem com levantamento forçado. A própria anti-varredura (gotículas pequenas) impede *riming*, graupel e Hallett-Mossop (§10.6).
* **Volumes:** mesmo o melhor caso fica 3–4 ordens abaixo de 14,2 × 10⁶ m³; esse volume é **premissa do repositório, não medição**.
* **Limitação declarada:** o CM1 usa sondagem única e nada entra pelas fronteiras; a tempestade real (item 2) não está nele.
* **Corrija** a frase do painel "Faltam mais de 10 milhões de m³ de água, cuja origem exige a convecção orográfica explosiva de altitude (a Física do Toró)": é `HIPÓTESE`, e os experimentos do CM1 não a reproduziram. Não a apresente como conclusão.

### 5. WRF — em andamento
* Rodada real com ERA5 (d01 9 km, d02 3 km, d03 1 km), em execução no vlab (`cluster/wrf_lhende/LEIA-ME_wrf.md`). **Ainda não há resultado:** se mencionar, diga só "em andamento" e o critério pré-registrado (o WRF só conta se reproduzir o sistema do Himawari em 18–22 UTC).

### 6. Visualizador interativo
* `viz/visualizador_cm1_lhende_2026.html`: campos do CM1 a cada 30 min sobre o anfiteatro, com Sentinel-2 reprocessado (offset −0,1 corrigido), bacia, ERA5-Land, Himawari e IMERG. Pode ser ligado a partir do painel (link relativo; copie o arquivo para a raiz do `Himalaia_2026` se for preciso).

## Lista de conferência

- [ ] Flare M7.0 às 10:02 UTC (não M6.9); sem prótons; Kp calmo.
- [ ] Todo Jz com o rótulo `PARAMÉTRICO` e a frase "não há medição de Jz para o evento".
- [ ] Trajetória do Himawari no mapa e na linha do tempo, com o rótulo `OBSERVADO`.
- [ ] Frase do "Toró" corrigida para `HIPÓTESE`, com os resultados do CM1.
- [ ] WRF descrito só como "em andamento".
- [ ] Nenhum erro no console do navegador; abas, mapa e gráficos funcionando.
- [ ] `RELATORIO_ATUALIZACAO_INDEX_2026-10.md` escrito.
