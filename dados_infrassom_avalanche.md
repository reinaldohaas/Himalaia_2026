# Relatório Técnico: Monitoramento por Infrassom e Acoplamento Sismo-Acústico
### Análise das Ondas de Baixa Frequência e Discriminação de Fontes na Catástrofe Nepal-Tibete (2026)

> [!IMPORTANT]
> **Nota de Auditoria Epistemológica e Rastreabilidade de Dados:**
> Este documento foi revisado para classificar rigorosamente o status de cada afirmação, distinguindo dados observados com fontes primárias públicas de estimativas baseadas em eventos análogos (ex.: Avalanches de Chamoli 2021 e Langtang 2015) e hipóteses de trabalho.

---

## 1. Princípios Físicos: Geração de Infrassom por Fenômenos Superficiais e Atmosféricos

O **infrassom** compreende ondas acústicas longitudinais na faixa de **0.01 Hz a 20 Hz**, abaixo do limiar de audição humana. Devido ao grande comprimento de onda ($\lambda \approx 15\text{ a } 3.000\text{ m}$), o infrassom apresenta baixíssima atenuação atmosférica por viscosidade e condução térmica, permitindo propagação por milhares de quilômetros através de guias de onda troposféricos e estratosféricos.

```
                      MECANISMO DE GERAÇÃO E DISCRIMINAÇÃO SÍSMO-ACÚSTICA
  
   [COLAPSO MECÂNICO / AVALANCHE]          [CONVECÇÃO SEVERA / TORÓ]          [TERREMOTO TECTÔNICO]
                 │                                     │                                │
                 ▼                                     ▼                                ▼
     • Pistão atmosférico superficial      • Vórtices, descargas e turbulência • Ruptura em profundidade
     • Acoplamento direto no ar            • Emissão puramente acústica        • Acoplamento no solo (rocha)
     • Alta razão Infrassom / Sismo        • Sem onda sísmica de corpo         • Baixa razão Infrassom / Sismo
```

---

## 2. Auditoria dos Parâmetros e Status dos Dados

A tabela abaixo detalha o status de verificação de cada métrica citada:

| Parâmetro / Dado | Valor / Afirmação | Classificação Metodológica | Status de Verificação Primária | Fonte / Justificativa |
| :--- | :--- | :--- | :--- | :--- |
| **Sinal Sísmico do Impacto** | Magnitude **4.4 mb**, 02:52:10 UTC (26/08/2026) | `DADO OBSERVADO` | **CONFIRMADO** (USGS / ISC) | USGS Earthquake Hazards Program. Profundidade estimada em 0 km. |
| **Estação KKN (Kakani, Nepal)** | Estação sismográfica de banda larga | `DADO OBSERVADO` | **CONFIRMADO** | Estação da rede sismológica nacional do Nepal / GEOFON / IRIS. **Nota: KKN é estação sísmica, não microbarômetro**. |
| **Faixa de Frequência do Infrassom** | **0.3 Hz a 2.5 Hz** | `ESTIMATIVA TEÓRICA / ANALÓGICA` | **NÃO VERIFICADO COM DADOS PRIMÁRIOS PÚBLICOS** | Valor baseado na assinatura acústica documentada da avalanche de Chamoli (2021) e desprendimentos de blocos rochosos. |
| **Pressão Acústica de Pico ($\Delta P$)** | $\sim 1.8\text{ a } 3.2\text{ Pa}$ | `ESTIMATIVA TEÓRICA` | **NÃO VERIFICADO COM DADOS PRIMÁRIOS PÚBLICOS** | Estimativa calculada por modelos de pistão dipolar para volume de $\approx 15\times 10^6\text{ m}^3$ em queda de 1.200 m. |
| **Duração do Trem de Ondas** | **~110 segundos** | `ESTIMATIVA / INFERÊNCIA` | **NÃO VERIFICADO COM DADOS PRIMÁRIOS PÚBLICOS** | Inferido da duração do sinal sísmico emergente de alta frequência em estações regionais. |
| **Back-Azimuth ($\theta$)** | $18.4^\circ \pm 1.2^\circ$ | `HIPÓTESE GEOMÉTRICA` | **NÃO VERIFICADO COM DADOS PRIMÁRIOS PÚBLICOS** | Azimute geodésico teórico calculado a partir da posição de Katmandu em relação à face norte do Langtang Lirung. |
| **Velocidade Aparente ($v_{app}$)** | $355\text{ a } 410\text{ m/s}$ | `ESTIMATIVA DERIVADA` | **NÃO VERIFICADO COM DADOS PRIMÁRIOS PÚBLICOS** | Velocidade de traço típica de ondas acústicas troposféricas/estratosféricas em modelos de vento HWM14. |
| **Energia Acústica ($E_{ac}$)** | $10^9\text{ a } 10^{10}\text{ J}$ | `ESTIMATIVA DERIVADA` | **NÃO VERIFICADO COM DADOS PRIMÁRIOS PÚBLICOS** | Calculada aplicando um coeficiente de rendimento acústico ($\eta \approx 10^{-4}$) sobre a energia potencial gravitacional ($E_p = mgh$). |

---

## 3. Redes Globais (CTBTO/IMS) e Protocolo de Acesso a Dados

O Sistema Internacional de Monitoramento (IMS) da **CTBTO** (Organização do Tratado de Proibição Completa de Testes Nucleares) opera estações de infrassom na região da Ásia Central e Sul da Ásia (ex.: **I40PK** no Paquistão, **I31KZ** no Cazaquistão, **I34MN** na Mongólia).

> [!WARNING]
> **Restrição de Acesso a Dados do CTBTO:**
> Os dados de forma de onda bruta do IMS não são de domínio público irrestrito em tempo real. O acesso para fins de pesquisa científica depende de solicitação formal através da plataforma **vDEC (*virtual Data Exploitation Centre*)** da CTBTO ([https://www.ctbto.org/specials/vdec/](https://www.ctbto.org/specials/vdec/)) ou via Centros Nacionais de Dados (NDCs).
> **Portanto, nenhuma forma de onda de microbarômetro do CTBTO pode ser dada como observada neste estudo sem o respectivo identificador de requisição vDEC.**

---

## 4. Discriminação de Três Classes de Fontes de Infrassom

Para investigar a hipótese de que tempestades convectivas severas ("torós") possam ter antecedido e influenciado o desastre, o infrassom deve ser analisado sob três hipóteses concorrentes de origem:

```
                            HIPÓTESES DE ORIGEM DO INFRASSOM
  
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ CLASSE A: TEMPESTADE / CONVECÇÃO PRÉVIA (Precursor)                        │
  │ • Horário da fonte: ANTERIOR a 02:52:10 UTC de 26/08/2026.                  │
  │ • Frequência: 0.1 a 1.0 Hz (oscilações acústico-gravitacionais de nuvem).   │
  │ • Azimute: Apontando para os núcleos convectivos identificados por satélite.│
  └─────────────────────────────────────────────────────────────────────────────┘
                                        │
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ CLASSE B: AVALANCHE DE ROCHA-GELO (Impacto Mecânico)                       │
  │ • Horário da fonte: COINCIDENTE com 02:52:10 UTC.                           │
  │ • Frequência: 0.5 a 5.0 Hz (turbulência de massa e ar comprimido).          │
  │ • Azimute: 18° a 20° (Face Norte do Langtang Lirung / 5.200m).              │
  └─────────────────────────────────────────────────────────────────────────────┘
                                        │
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ CLASSE C: RUPTURA DE BARRAMENTO E DEBRIS FLOW (Hidráulico)                  │
  │ • Horário da fonte: POSTERIOR a 02:52:10 UTC (03:15 a 04:30 UTC).           │
  │ • Frequência: 1.0 a 8.0 Hz (colisão de megablocos e turbulência fluvial).    │
  │ • Azimute: Dinâmico, progredindo ao longo do vale do Lhende Khola e Trishuli.│
  └─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Correção do Tempo de Propagação Acústica

Para correlacionar sinais de infrassom com o horário do desastre, é obrigatório descontar o atraso de propagação atmosférica:

$$\Delta t_{prop} = \int_{\text{fonte}}^{\text{estação}} \frac{ds}{c_{\text{efetivo}}(s)}$$

Onde $c_{\text{efetivo}} = \sqrt{\gamma R T} + \vec{v}_{\text{vento}} \cdot \vec{n} \approx 330\text{ a } 345\text{ m/s}$.

*   **Para uma distância de 65 km (ex.: Katmandu):** O atraso acústico é de $\Delta t \approx \frac{65.000\text{ m}}{335\text{ m/s}} \approx 194\text{ segundos}$ (**3 minutos e 14 segundos**).
*   **Para uma estação a 500 km (ex.: I40PK):** O atraso acústico via duto estratosférico é de $\Delta t \approx \frac{500.000\text{ m}}{310\text{ m/s}} \approx 1.610\text{ segundos}$ (**~26 minutos e 50 segundos**).

---

## 6. O que é Necessário para Validação Definitiva?

Para transformar as hipóteses em dados observados comprovados, são necessários os seguintes dados primários:
1. **Requisição formal de dados vDEC da CTBTO** para os arrays I40PK e I31KZ no intervalo de 25/08/2026 18:00 UTC a 26/08/2026 06:00 UTC.
2. **Dados de microbarômetros de estações meteorológicas automáticas (AWS)** operadas pelo DHM Nepal no distrito de Rasuwa e Nuwakot.
3. **Formas de onda sísmicas completas da estação KKN** (canais BHZ, BHN, BHE) via IRIS/GEOFON para cálculo da função de correlação cruzada e estimativa empírica da força de impacto da massa.
