# Notas para o autor — artigo em formato Nature (18/10/2026)

**Arquivos:** `main.tex` (classe `nature.cls`, bibliografia `refs.bib` com `naturemag.bst`), `figures/`, `main.pdf`.
**Compilar:** `latexmk -pdf main.tex`. Com `\previewtrue` (padrão) as figuras aparecem junto das legendas. Com `\previewfalse` sai o layout de submissão da Nature: só as legendas, e as figuras vão como arquivos separados.

## O que o artigo é

Um **teste da hipótese** do artigo-base (`ARTIGO_CIENTIFICO_CATASTROFE_HIMALAIA_2026.md`). A hipótese entra como motivação, nas palavras do artigo-base: flare → Jz → anti-varredura de Tinsley → reservatório super-resfriado → liberação explosiva. Os resultados desde setembro entram como evidência:

- auditoria do balanço hídrico;
- Himawari e ERA5;
- neve e gelo em sete fontes, com orçamento de erro;
- Sentinel-1 ao longo do talvegue;
- as treze rodadas do CM1 com a anti-varredura.

A conclusão é a que os dados sustentam hoje: a fonte da água continua em aberto, e o mecanismo elétrico, como foi implementado, não fecha a conta. Se você quiser outra ênfase, a estrutura permite. A regra de não pôr número sem arquivo continua valendo.

## O que mudou em relação ao artigo-base, e por quê

A classificação veio dos documentos de auditoria do próprio repositório (AUDITORIA, VERIFICACAO_2, ANALISE_DEM, IMERG_15, MAGNETOMETROS, TORO_CM1 etc.).

| Item do artigo-base | No artigo novo | Motivo |
| :--- | :--- | :--- |
| Q = 3.376 m³/s, 20,7 Mm³, Cv 31,4 %, 14,2 Mm³ | citados como reconstrução **com entradas assumidas**; Q = 3.400–4.100 m³/s | `config/hydraulic_assumptions.yaml`: todas as entradas são `ASSUMED_BY_ANALYST`; S₀ medido no GLO-30 = 0,066 → 4.095 m³/s, Fr 1,6 |
| "Telemetria do DHM em Syabrubesi", hidrograma de 5 h, sensor a 1,62 m | retirados | sem arquivo; o hidrograma é hipotético |
| 1.000–1.400 mortos, 4.000–5.500 desaparecidos | "perda de vidas substancial, que não avaliamos" | só aparecem em "balanços públicos", sem arquivo |
| 101 pontes (33 + 68) | 25 de 33 destruídas, 3 danificadas (inventário ICIMOD) | o geojson do ICIMOD tem 33 pontes; as 68 pênseis não estão em nenhum arquivo |
| "Atribuição oficial a GLOF" | retirada | nenhuma fonte; o USGS classifica o evento como `landslide` |
| PlanetScope 3 m, NDWI < 8 ha, ALOS 12,5 m, lago de 0,8–3,5 Mm³ | "o maior corpo d'água em 914 km² tem 4,8 ha" (Sentinel-2) | não há PlanetScope nem ALOS no repositório; a conclusão (sem lago) se mantém com o Sentinel-2 |
| IMERG 15–30 mm em 24 h | 5,1 mm até o colapso na célula de 0,1°; 18,7 mm em 3 dias na caixa de 0,5° | valores calculados no repositório |
| bacias de 15/28/50 km² | áreas do GLO-30 (3,41; 24,5; 242 km²…) e os 934 km² da seção de Rasuwagadhi | ver ANALISE_DEM |
| "Déficit de 10×" | **o déficit depende da área**: sobre os 934 km² da seção, 14,2 Mm³ = 15 mm, da ordem do IMERG | é o ponto mais sensível do artigo: o paradoxo só aparece se o volume for atribuído a uma sub-bacia pequena |
| Jz 4,57 pA/m², V_I 356,4 kV | "não há medição de Jz; os valores preliminares vêm de V_I atribuído à mão"; o crochê magnético e os raios cósmicos dão ΔJz ≲ 1 % | `data/synthetic/README.md`, MAGNETOMETROS, JZ_CONSTRUIDO |
| CCN < 100 cm⁻³, LWC > 4,5 g/m³, > 500 mm em < 2 h | retirados como fato; o CM1 dá o que dá | sem medição; a ERA5 tem ~0,02–0,04 g/m³ |
| 38 descargas/h (WWLLN) | retirado | os dados do WWLLN não estão no repositório; as contagens são paramétricas |
| "O fluxo desceu o Lhende Khola" | o fluxo desceu o **Chhochen Khola** (km 3,7–8,7) e o **Chusumdo Tsangpo** (km 8–13,6) até o **Lhende Khola** (km 13–24, rio de fronteira), e dali ao Bhote Koshi em Rasuwagadhi | nomes do OpenStreetMap ao longo do talvegue do GLO-30 (`scripts/neve_anfiteatro/nomes_osm.py`, `data/processed/neve_anfiteatro/nomes_osm_talvegue.json`); o sinal de radar mais forte fica no Chhochen Khola. O nome do evento ("Lhende Khola") foi mantido no título |
| Ms 5,2, `us7000tbwb`, 02:52:10 UTC | mantido; **local corrigido para 28,271 N 85,515 E** (o do USGS) | o artigo-base dava 28,261/85,388 |
| Ondas de Rayleigh em KKN | retirado; a inversão sísmica é proposta como próximo passo | as formas de onda existem no IRIS, mas nunca foram analisadas |
| 15 Mm³ destacados | retirado; "o volume não pode ser medido com estes dados" | 15 Mm³ e 10⁸ m³ coexistem sem medição |
| Infrassom, citação do Kathmandu Post | retirados | sem dado e sem fonte |
| Geomitos (Druk) | retirados | sem fonte etnográfica; não cabem num artigo Nature |
| Referência "Briming & Haas (2026)" | retirada | não existe em nenhum outro lugar; a revista não parece existir |
| Tinsley (2000), Harrison & Ambaum (2008) | títulos corrigidos | os títulos do artigo-base não batem com os artigos reais |
| Flare "M6.9" | mantido como M6.9 (pico 6,98 × 10⁻⁵ W/m²) | é a classe da NOAA; antes eu tinha escrito "M7,0" no prompt do antigravity, arredondando o fluxo. A lista da NOAA diz M6.9 |

## Caracterização do anfiteatro de erosão (acrescentada em 19/10)

Nova seção do texto principal ("A north-facing erosional headwall with almost no floor"), nova **Fig. 2** (as figuras seguintes passaram a 3, 4 e 5) e **Extended Data Table 2**. Script: `scripts/neve_anfiteatro/caracteriza_anfiteatro.py`; saída: `data/processed/neve_anfiteatro/caracterizacao_anfiteatro.json`.

- **Morfometria (GLO-30):** 3,41 km²; desnível de 3.206 m em 3,18 km (razão de relevo 1,0); declividade média de 48°, com 57 % da área acima de 45° e só 2 % (6,5 ha) abaixo de 15°; 96 % das encostas voltadas para NW–N–NE; integral hipsométrica 0,55; índice de Melton 1,74. Pelo critério de Wilford et al. (2004), o Melton está bem acima do limiar de fluxo de detritos (0,53), mas o comprimento (3,2 km) passa um pouco do limite de 2,7 km.
- **Cobertura em 12/08 (Sentinel-2):** neve e gelo acima de 6.000 m; mosaico de rocha e gelo entre 5.000 e 6.000 m; rocha e detrito entre 4.500 e 5.000 m; neve no pé da parede. Há 54 ha de geleira mapeados no OSM.
- **Correção:** a cota da localização do USGS no GLO-30 nativo é **5.590 m**; os 5.617 m anteriores vinham do modelo reamostrado na grade do Sentinel-2. Corrigido no artigo e no relatório.

## O que falta antes de submeter

1. **WRF:** terminou em 19/10 e **não passou** no critério pré-registrado. Ele forma o sistema do planalto na fase madura, com no máximo 1/7 da área observada, e não o traz para oeste. Pega a convecção noturna perto do sítio (mesma área e horário, 30–50 km ao sul) e não chove sobre o anfiteatro. Isso entrou no texto (seção da tempestade e Discussion), no Methods e na Extended Data Fig. 4.
2. **Coautoria:** o artigo está só em seu nome. A Nature não aceita IA como autora, e o uso está declarado em Methods ("Use of AI tools"). Se o Renato ou outros entrarem, é preciso ajustar o `\author` e as contribuições.
3. **Tamanho:** o `texcount` dá 4.868 palavras de texto no total (resumo, texto principal e Methods), mais 573 nas legendas. São 4 figuras, 1 tabela, 3 figuras e 1 tabela de Extended Data, e 37 referências (limite de 50). Cabe no formato de Article.
4. **Revisão de inglês** por um falante nativo; o texto segue a grafia britânica (Oxford), como a Nature pede.
5. **Carta de apresentação** (cover letter), com o resumo de 100 palavras para o público geral: ainda não foi escrita.
