# Limitações e Dados Indisponíveis — Declaração de Integridade Científica

**Projeto:** Himalaia 2026 / Catástrofes do Himalaia (1980–2026)  
**Investigador Principal:** Prof. Reinaldo Haas (Departamento de Física, UFSC)  
**Data da Auditoria:** Setembro de 2026  
**Status do Repositório:** Auditado e Corrigido (Separação Rigorosa de Dados Observacionais e Modelos Paramétricos)  

---

## 1. Princípio Epistemológico da Auditoria

Este documento formaliza, em cumprimento aos mais elevados padrões internacionais de integridade em pesquisa (COPE / ICMJE / AGU / EGU), o inventário transparente de **todos os dados instrumentais que não estão presentes no repositório local**, especificando a razão da ausência, a fonte primária externa exigida e as credenciais ou acordos institucionais necessários para obtenção futura.

> [!IMPORTANT]
> **Regra de Ouro da Integridade Científica:**
> Nunca gerar números por fórmula e rotulá-los como medições empíricas. O que não foi medido in-situ ou baixado de sensores calibrados é explicitamente catalogado como `[DADO INDISPONÍVEL]`, `[MODELO PARAMÉTRICO]` ou `[HIPÓTESE NÃO VERIFICADA]`.

---

## 2. Inventário de Dados Indisponíveis por Domínio Físico

| # | Domínio | Dado Específico | Status no Repositório | Motivo da Ausência | Ação / Requisito para Obtenção |
|---|---|---|---|---|---|
| **1** | **Meteorologia / Pluviometria** | Precipitação GPM IMERG V07 (meia-hora) para 25–26/08/2026 | `[DADO INDISPONÍVEL]` | Download direto via scripts no shell falha por interceptação TLS local; requer autenticação NASA Earthdata do usuário | O usuário deve autenticar-se no portal [NASA Earthdata Login](https://urs.earthdata.nasa.gov/) e fornecer token `~/.netrc` para download automatizado via PowerShell |
| **2** | **Meteorologia / Pluviometria** | Pluviômetros in-situ no cânion do Lhende Khola (Gyirong) em 2026 | `[DADO INDISPONÍVEL]` | Inexistência de estações meteorológicas automáticas (AWS) de superfície operadas no fundo da garganta inóspita | Requer solicitação formal de cooperação bilateral com o Departamento de Hidrologia e Meteorologia do Nepal (DHM) e a Administração Meteorológica da China (CMA) |
| **3** | **Geomagnetismo / Eletrodinâmica** | Séries temporais em alta cadência (1s) de magnetômetros INTERMAGNET (LZA, SAB, BJI) | `[DADO INDISPONÍVEL]` | Nenhum arquivo binário IAGA-2002 de magnetômetros estava arquivado no repositório | Solicitação de dados brutos à rede [INTERMAGNET](https://intermagnet.org/) ou institutes nacionais (CEA / IIG) |
| **4** | **Eletricidade Atmosférica** | Medições diretas de campo elétrico vertical ($E_z$) e densidade de corrente ($J_z$) no solo ou cume | `[DADO INDISPONÍVEL]` | Não existem moinhos de campo (*electric field mills*) nem antenas de condução instaladas nos picos do Langtang Lirung | Modelado analiticamente via curva de Carnegie e modelo colunar de potencial ionosférico; classificado como modelo paramétrico teórico |
| **5** | **Descargas Atmosféricas (Raios)** | Registros brutos de sensores VLF/LF de raios das redes WWLLN e GLD360 (tempos ao microssegundo, corrente de pico em kA) | `[DADO INDISPONÍVEL]` | Acesso a dados brutos da WWLLN exige acordo de pesquisa institucional e licença comercial/acadêmica paga | Requer protocolo de colaboração acadêmica formal com o consórcio WWLLN (Universidade de Washington) ou Earth Networks |
| **6** | **Raios Pré-2004** | Descargas elétricas para os eventos de 1981 (Zhangzangbo), 1985 (Dig Tsho) e 1994 (Luggye Tsho) | `[DADO INDISPONÍVEL]` | Redes globais de localização de raios em tempo real (WWLLN, GLD360) não existiam nas décadas de 1980 e 1990 | Valores fabricados por modelo foram removidos dos arquivos de dados |
| **7** | **Infrassom** | Séries microbarométricas de 20 Hz de estações do Sistema Internacional de Vigilância (IMS/CTBTO) | `[DADO INDISPONÍVEL]` | Requer acesso autorizado via plataforma vDEC (virtual Data Exploitation Centre) da CTBTO em Viena | Requer submissão de projeto formal de pesquisa junto à [CTBTO vDEC](https://www.ctbto.org/) |
| **8** | **Topografia de Alta Resolução** | DEM LiDAR aéreo pré e pós-colapso ou estéreo-DEM sub-métrico (WorldView/Pleiades) de 2026 | `[DADO INDISPONÍVEL]` | Disponível apenas DEM Copernicus 30m público e estimativas morfológicas de satélites ópticos de média resolução | Requer aquisição de pares estereoscópicos comerciais de alta resolução (Maxar WorldView-3 / Airbus Pleiades Neo) |

---

## 3. Segregação e Catalogação de Dados Sintéticos e Modelos Paramétricos

Todos os arquivos que contêm valores gerados por código ou aproximações analíticas foram removidos das pastas de dados observacionais (`data/raw/`, `data/processed/`) e segregados em [`data/synthetic/`](./data/synthetic/README.md):

1. [`data/synthetic/jz_gec_PARAMETRIC_MODEL.csv`](./data/synthetic/jz_gec_PARAMETRIC_MODEL.csv):
   * **Natureza:** Modelo analítico teórico do Circuito Elétrico Global (GEC) baseado na curva diurna clássica de Carnegie modificada por variações hipotéticas de potencial ionosférico ($V_I$).
   * **Limitação:** Não reflete telemetria de magnetômetros in-situ. O código foi depurado para eliminar condicionais artificiais (`if date == ...`).
2. [`data/synthetic/jz_8station_PARAMETRIC_MODEL.csv`](./data/synthetic/jz_8station_PARAMETRIC_MODEL.csv):
   * **Natureza:** Simulação paramétrica de condutividade atmosférica atribuída a 8 coordenadas de observatórios geomagnéticos.
   * **Limitação:** Não contém dados magnéticos brutos IAGA-2002.
3. [`data/synthetic/goes_xray_IDEALIZED_MODEL.csv`](./data/synthetic/goes_xray_IDEALIZED_MODEL.csv):
   * **Natureza:** Perfil idealizado de decaimento de raios X solar para fins de teste computacional.
4. [`data/synthetic/dscovr_solar_wind_IDEALIZED_MODEL.csv`](./data/synthetic/dscovr_solar_wind_IDEALIZED_MODEL.csv):
   * **Natureza:** Simulação cinemática de vento solar no ponto Lagrangiano L1.
5. [`data/synthetic/geomagnetic_indices_IDEALIZED_MODEL.csv`](./data/synthetic/geomagnetic_indices_IDEALIZED_MODEL.csv):
   * **Natureza:** Série paramétrica de índices Kp, Dst e modulação simulada de raios cósmicos galácticos (GCR).
6. [`data/synthetic/lightning_points_PARAMETRIC_SYNTHETIC.json`](./data/synthetic/lightning_points_PARAMETRIC_SYNTHETIC.json):
   * **Natureza:** Nuvens de pontos de descargas geradas estocasticamente por pseudo-aleatoriedade para renderização na interface web 3D.

---

## 4. Premissas Hidráulicas e Sensibilidade

Todas as constantes de canal ($B$, $z$, $S_0$, $n$, $\Delta h$), áreas de drenagem ($A_{\text{basin}}$), coeficientes de escoamento ($C_{\text{runoff}}$) e volumes de controle foram transferidos para o arquivo declaratório aberto [`config/hydraulic_assumptions.yaml`](./config/hydraulic_assumptions.yaml).

O script reprodutível [`scripts/sensitivity_analysis_hydraulics.py`](./scripts/sensitivity_analysis_hydraulics.py) documenta a sensibilidade dessas premissas, atestando sob quais condições físicas o déficit de água líquida existe e sob quais condições desaparece completamente.
