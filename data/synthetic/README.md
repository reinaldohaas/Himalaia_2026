# Dados Sintéticos e Modelos Paramétricos (Isolamento de Auditoria)

Este diretório contém todos os arquivos e séries temporais gerados por scripts internos de modelagem, equações analíticas ou parametrizações matemáticas do projeto. 

**DECLARAÇÃO FORMAL DE AUDITORIA:**
Nenhum arquivo neste diretório é dado bruto, telemetria instrumental ou medição de estação de superfície. Todos foram segregados de `data/raw/` em cumprimento às regras de honestidade científica para eliminar qualquer falsa atribuição de proveniência.

---

## Inventário de Arquivos Sintéticos e Modelados

| Arquivo | Script Gerador | Natureza do Dado | Finalidade / Esclarecimento |
| :--- | :--- | :--- | :--- |
| `goes_xray_IDEALIZED_MODEL.csv` | `scripts/generate_space_weather_datasets.py` | Gaussiana analítica parametrizada | Modelo idealizado da curva de subida/descida do flare solar M6.9 de 25/08/2026. A coluna `status` foi corrigida de "observed" para "modeled". |
| `dscovr_solar_wind_IDEALIZED_MODEL.csv` | `scripts/generate_space_weather_datasets.py` | Séries senoidais/exponenciais sintéticas | Simulação paramétrica de vento solar ($V_{\text{sw}}$, $N_p$, $B_z$) em L1. |
| `geomagnetic_indices_IDEALIZED_MODEL.csv` | `scripts/generate_space_weather_datasets.py` | Índices modulados por fórmula | Modelação sintética de Kp, Dst e modulação simulada de raios cósmicos galácticos (GCR). |
| `jz_gec_PARAMETRIC_MODEL.csv` | `scripts/model_gec_jz_parametric.py` (antigo `recalculate_jz_with_china_network.py`) | Modelo paramétrico de condutividade global (GEC) | Série teórica de corrente $J_z = V_I / R_c$ calculada a partir de curva Carnegie e resistência colunar fixa ($R_c = 0.78 \times 10^{17}\,\Omega\cdot\text{m}^2$). **Nenhum magnetômetro real é lido.** |
| `jz_8station_PARAMETRIC_MODEL.csv` | `scripts/process_7day_magnetometers_jz.py` | Modelo analítico de Sq ionosférico | Modulação diurna simulada via função senoidal e relação de Cowling teórica. |

---

## Critério de Uso Científico
Estes arquivos representam **cenários de modelagem exploratória** e **não podem ser citados como observações instrumentais diretas** em relatórios, tabelas comparativas ou submissões a periódicos científicos.
