# Protocolo de Solicitações Institucionais de Dados Externos

**Investigador Principal:** Prof. Dr. Reinaldo Haas (Departamento de Física, UFSC)  
**Projeto:** Himalaia 2026 — Reconstrução Física Independente da Catástrofe de 26/08/2026  
**Data:** Setembro de 2026  

---

## 1. Visão Geral das Cartas Formais de Solicitação

Para substituir definitivamente modelos paramétricos teóricos e dados ausentes por **observações instrumentais calibradas**, foram redigidas 5 cartas acadêmicas formais (em inglês padrão internacional e português protocolar).

| # | Instituição Alvo | Domínio Físico | Contato / Portal de Envio | Arquivo da Carta |
|---|---|---|---|---|
| **1** | **CTBTO vDEC** (Viena, Áustria) | Infrassom (20 Hz, estações IS31, IS52) | `vdec@ctbto.org` / [Portal vDEC](https://vdec.ctbto.org) | [`CARTA_01_CTBTO_vDEC_INFRASSOM.md`](./CARTA_01_CTBTO_vDEC_INFRASSOM.md) |
| **2** | **WWLLN** (Univ. of Washington, EUA) | Descargas Elétricas (Raios VLF) | `bobholz@uw.edu` / `wwlln@uw.edu` | [`CARTA_02_WWLLN_DESCARGAS_ELETRICAS.md`](./CARTA_02_WWLLN_DESCARGAS_ELETRICAS.md) |
| **3** | **DHM Nepal** (Governo do Nepal) | Fluviometria e Pluviometria in-situ | `info@dhm.gov.np` / `dg@dhm.gov.np` | [`CARTA_03_DHM_NEPAL_HIDROLOGIA_PLUVIOMETRIA.md`](./CARTA_03_DHM_NEPAL_HIDROLOGIA_PLUVIOMETRIA.md) |
| **4** | **ITPR / CAS & CENC** (Pequim, China) | Sismologia Regional e Estações Tibete | `itpr@itpcas.ac.cn` / `cenc@seis.ac.cn` | [`CARTA_04_CAS_ITPR_SISMOLOGIA_TIBETE.md`](./CARTA_04_CAS_ITPR_SISMOLOGIA_TIBETE.md) |
| **5** | **INTERMAGNET** (BGS / USGS) | Séries Vetoriais de Magnetômetros (1s/1min) | `info@intermagnet.org` / `data@intermagnet.org` | [`CARTA_05_INTERMAGNET_MAGNETOMETRIA.md`](./CARTA_05_INTERMAGNET_MAGNETOMETRIA.md) |

---

## 2. Instruções Práticas para Envio pelo Usuário

### Carta 1: CTBTO vDEC (Infrassom)
1. **Procedimento:** Envie um email para `vdec@ctbto.org` com o texto em inglês da Carta 1 como proposta de pesquisa preliminar, ou submeta diretamente pelo portal [vdec.ctbto.org](https://vdec.ctbto.org) (caso já tenha cadastro institucional).
2. **Assunto do Email:** `Research Proposal: Infrasound Waveform Data Request for Himalayan Catastrophic Event (26 August 2026)`
3. **Anexos:** Se desejado, anexe o sumário do evento ou o arquivo KML do projeto.

### Carta 2: WWLLN (Descargas Elétricas / Raios)
1. **Procedimento:** Envie email diretamente ao Prof. Robert Holzworth (`bobholz@uw.edu`) com cópia para `wwlln@uw.edu`.
2. **Assunto do Email:** `Academic Data Request: WWLLN lightning stroke data for Gyirong/Nepal border (25-26 Aug 2026)`
3. **Observação:** O consórcio costuma fornecer recortes pontuais para pesquisas acadêmicas sem custos ou mediante assinatura de DUA simples.

### Carta 3: DHM Nepal (Hidrologia e Meteorologia)
1. **Procedimento:** Envie email oficial com cabeçalho da UFSC para `info@dhm.gov.np` e `dg@dhm.gov.np`.
2. **Assunto do Email:** `Academic Research Request: Trishuli/Bhote Koshi Hydrometric & Rainfall Telemetry (24-28 Aug 2026)`
3. **Observação:** Se o DHM solicitar preenchimento de formulário de requisição de dados oficial do governo nepalês, solicite o formulário padrão.

### Carta 4: ITPR / CAS e CENC (Sismologia do Tibete)
1. **Procedimento:** Envie para `itpr@itpcas.ac.cn` e `cenc@seis.ac.cn`.
2. **Assunto do Email:** `Academic Collaboration & Data Request: Gyirong seismic and meteorological records (25-27 Aug 2026)`
3. **Observação:** Oferecer coautoria a pesquisadores do ITPR facilita enormemente a liberação de dados sismológicos de estações no Tibete.

### Carta 5: INTERMAGNET (Magnetometria)
1. **Procedimento:** Envie para `info@intermagnet.org` e `data@intermagnet.org`.
2. **Assunto do Email:** `Academic Data Request: High-rate geomagnetic data for Asian observatories (20-28 Aug 2026)`
3. **Observação:** Muitos dados de 1 minuto já podem ser consultados via serviço de download do portal INTERMAGNET; os dados de 1 segundo requerem requisição pontual aos observatórios.

---

## 3. Protocolo de Recepção e Incorporação de Novos Dados

Assim que os dados chegarem:
1. Salvar os arquivos originais intactos em `data/raw/<dominio>/`.
2. Registrar a procedência (email, operador, número de protocolo) no relatório de proveniência.
3. Atualizar a chave criptográfica em [`data/CHECKSUMS_SHA256.txt`](../../data/CHECKSUMS_SHA256.txt).
4. Executar os scripts de processamento instrumental para atualizar as análises.
