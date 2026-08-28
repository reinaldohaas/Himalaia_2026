# Estimativas Paramétricas Alternativas: Neve Derretida (Rain-on-Snow) e Geometria da Lagoa Temporária
### Modelagem de Sensibilidade Hidrológica da Bacia do Lhende Khola (Nepal-Tibete 2026)

---

## 1. Fundamentação Física dos Dois Fatores Adicionais

Ao refinar o balanço de massa do enchimento do lago em **42 minutos e 50 segundos** ($\Delta t = 2.570\text{ s}$), dois processos físicos modificam a exigência de precipitação direta:

```
                  FLUXO HÍDRICO MULTICOMPONENTE NO VALE DO LHENDE KHOLA
  
  ⛈️ Chuva Quente do Toró (4° a 8°C) ──┐
                                       ├──► [Transferência Térmica e Condensação de Vapor]
  ❄️ Manto Nival (>4.200m / 28 km²)  ──┘           │
                                                   ▼
                                       🧊 Degelo Acelerado (Rain-on-Snow: +15% a 17% de volume)
                                                   │
  💧 Rio Base (45 m³/s) ───────────────┐           │
  💥 Fusão por Fricção Mecânica ───────┼───────────┴──► 🌊 ACÚMULO NA LAGOA TEMPORÁRIA
                                       │                    • Espaço Útil: 3.5 a 8.5 M m³
                                       │                    • Tempo Limite: 42 min 50 s
```

### A. O Mecanismo Termodinâmico de Degelo por Chuva Quente (*Rain-on-Snow*)
A bacia do Lhende Khola possui $\approx 28\text{ km}^2$ de sua área situada acima de 4.200 m coberta por manto de neve sazonal úmida e isotérmica ($T_{\text{neve}} = 0^\circ\text{C}$). Durante a tempestade convectiva noturna:
1. **Calor Sensível da Chuva ($Q_p$):** A água da chuva a $+6^\circ\text{C}$ transfere calor diretamente para o gelo:
   $$Q_p = \rho_w c_w P (T_{\text{chuva}} - 0^\circ\text{C}) \approx 25.1\text{ kJ/m}^2\text{ por milímetro de chuva}$$
   Isso funde $\approx 0.075\text{ mm}$ de água de degelo por mm de chuva.
2. **Calor Latente por Condensação Turbulenta ($Q_e$):** Em tempestades tropicais/monçônicas saturadas ($UR \approx 100\%$) com vento turbulento, o vapor d'água condensa sobre a superfície gelada ($L_v = 2.50\times 10^6\text{ J/kg}$), liberando calor latente que derrete cerca de **$0.35\text{ mm}$ adicionais de gelo por mm de chuva**.
3. **Fator Multiplicador Total (*Rain-on-Snow Yield*):** Cada $1.0\text{ mm}$ de chuva direta sobre a neve gera **$+0.42\text{ mm}$ equivalentes de água líquida provenientes do degelo nival**, atuando como um poderoso amplificador natural de vazão!

### B. Variação do Espaço Efetivo e Geometria da Lagoa Temporária
O volume de armazenamento útil antes do galgamento (*free storage capacity*) varia conforme o perfil transversal da garganta e a porosidade dos detritos:
*   **Garganta Estreita em V ($3.5\times 10^6\text{ m}^3$):** Bloqueio de 35 m de altura com remanso curto (~900 m).
*   **Perfil Padrão Intermediário ($5.5\times 10^6\text{ m}^3$):** Bloqueio de 50 m com remanso de 1.400 m.
*   **Perfil Amplo Máximo ($8.5\times 10^6\text{ m}^3$):** Bloqueio de 65 m com remanso de 1.800 m.
*   **Cenário de Lago Preexistente ($2.8\times 10^6\text{ m}^3$ de sobrecarga):** O lago já continha $5.0\times 10^6\text{ m}^3$; foram necessários apenas $2.8\times 10^6\text{ m}^3$ adicionais de chuva e degelo para provocar o transbordamento imediato.

---

## 2. Comparativo dos 4 Cenários Paramétricos

| Parâmetro Hidrológico | Cenário 1: Garganta Estreita | Cenário 2: Bacia Média | Cenário 3: Lago Amplo Máximo | Cenário 4: Lago Preexistente |
| :--- | :---: | :---: | :---: | :---: |
| **Volume Total do Lago ($V_{\text{lago}}$)** | **$3.5\times 10^6\text{ m}^3$** | **$5.5\times 10^6\text{ m}^3$** | **$8.5\times 10^6\text{ m}^3$** | **$2.8\times 10^6\text{ m}^3$** (Sobrecarga) |
| **Vazão Afluente Média ($Q_{\text{in}}$)** | $1.361.9\text{ m}^3/\text{s}$ | $2.140.1\text{ m}^3/\text{s}$ | $3.307.4\text{ m}^3/\text{s}$ | $1.089.5\text{ m}^3/\text{s}$ |
| **Contribuição da Neve (*Rain-on-Snow*)** | **$0.55\text{ M m}^3$ (15.8%)** | **$0.91\text{ M m}^3$ (16.5%)** | **$1.44\text{ M m}^3$ (16.9%)** | **$0.43\text{ M m}^3$ (15.4%)** |
| **Volume de Chuva Direta** | $2.59\text{ M m}^3$ (74.1%) | $4.24\text{ M m}^3$ (77.1%) | $6.71\text{ M m}^3$ (79.0%) | $2.02\text{ M m}^3$ (72.0%) |
| **Rio Base + Fusão Mecânica** | $0.35\text{ M m}^3$ (10.1%) | $0.35\text{ M m}^3$ (6.4%) | $0.35\text{ M m}^3$ (4.2%) | $0.35\text{ M m}^3$ (12.6%) |
| **Lâmina de Chuva Requerida ($P$)** | **$52.4\text{ mm}$** | **$85.7\text{ mm}$** | **$135.6\text{ mm}$** | **$40.7\text{ mm}$** |
| **Lâmina de Degelo Adicional da Neve** | $+22.0\text{ mm}$ | $+36.0\text{ mm}$ | $+56.9\text{ mm}$ | $+17.1\text{ mm}$ |
| **Lâmina Total Equivalente de Água** | **$74.4\text{ mm}$** | **$121.7\text{ mm}$** | **$192.5\text{ mm}$** | **$57.8\text{ mm}$** |
| **Densidade do Toró (ton/100m²)** | **$5.2\text{ ton / 100 m}^2$** | **$8.6\text{ ton / 100 m}^2$** | **$13.6\text{ ton / 100 m}^2$** | **$4.1\text{ ton / 100 m}^2$** |
| **Área para Concentrar 10 Toneladas** | $191.0\text{ m}^2$ ($13.8\times 13.8\text{ m}$) | $116.7\text{ m}^2$ ($10.8\times 10.8\text{ m}$) | $73.8\text{ m}^2$ ($8.6\times 8.6\text{ m}$) | $245.6\text{ m}^2$ ($15.7\times 15.7\text{ m}$) |

---

## 3. Principais Conclusões das Novas Estimativas

1. **O Degelo Nival Alivia a Exigência de Chuva Extrema:**
   * Sem considerar a neve, eram necessários $165\text{ mm}$ de chuva pura.
   * Com a inclusão termodinâmica do efeito *Rain-on-Snow*, a **neve derretida fornece entre $550.000\text{ e } 1.440.000\text{ m}^3$ de água líquida**, reduzindo a chuva direta necessária para a faixa perfeitamente viável de **$52\text{ a } 85\text{ mm}$** em eventos convectivos de monção.
2. **Influência da Geometria da Lagoa Temporária:**
   * Se o espaço de represamento da garganta era mais confinado ($3.5\text{ M m}^3$), bastou uma chuva convectiva rápida de **$52.4\text{ mm}$** ($5.2\text{ toneladas a cada } 100\text{ m}^2$) para encher e estourar a barragem em $42\text{ min } 50\text{ s}$.
   * Se havia um lago glacial proglacial preexistente, uma precipitação de apenas **$40.7\text{ mm}$** somada a **$17.1\text{ mm}$** de neve derretida foi suficiente para disparar o galgamento e a enxurrada de detritos de 45 km pelo Rio Trishuli.
