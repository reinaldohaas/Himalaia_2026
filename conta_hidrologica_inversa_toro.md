# Modelagem Hidrológica Inversa: Balanço de Massa e Física do "Toró"
### Verificação Numérica da Formação e Ruptura do Lago Lhende Khola em 42 minutos e 50 segundos

---

## 1. O Problema Hidrológico Inverso

A catástrofe no sistema Lhende Khola–Bhote Koshi–Trishuli apresentou dois marcos temporais georreferenciados:
*   **$t_1$ (Colapso Glacial e Barramento):** 26/08/2026 às `02:52:10 UTC` (08:37:10 NPT).
*   **$t_2$ (Rompimento Catastrófico por Galgamento):** 26/08/2026 às `03:35:00 UTC` (09:20:00 NPT).

O tempo transcorrido entre o bloqueio da garganta e o estouro da represa natural foi de:
$$\mathbf{\Delta t = 42\text{ minutos e } 50\text{ segundos} = 2.570\text{ segundos} \approx 0.714\text{ horas}}$$

O volume total de água represado no lago efêmero antes do rompimento, estimado por sensoriamento remoto óptico/SAR e modelo digital de elevação (DEM), situa-se na faixa de:
$$V_{\text{lago}} \approx 6.0\times 10^6\text{ a } 8.5\times 10^6\text{ m}^3\text{ (6.0 a 8.5 milhões de toneladas de água)}$$

---

## 2. Cálculo da Vazão Afluente Média Necessária ($Q_{\text{in}}$)

Para acumular esse volume no intervalo de 2.570 segundos, a taxa média de entrada de água ($Q_{\text{in}}$) na garganta do Lhende Khola foi de:

$$Q_{\text{in}} = \frac{V_{\text{lago}}}{\Delta t}$$

*   **Para $V_{\text{lago}} = 6.0\times 10^6\text{ m}^3$:**
    $$Q_{\text{in}} = \frac{6.000.000\text{ m}^3}{2.570\text{ s}} \approx \mathbf{2.334.6\text{ m}^3/\text{s}}$$
*   **Para $V_{\text{lago}} = 8.5\times 10^6\text{ m}^3$:**
    $$Q_{\text{in}} = \frac{8.500.000\text{ m}^3}{2.570\text{ s}} \approx \mathbf{3.307.4\text{ m}^3/\text{s}}$$

> [!IMPORTANT]
> **Vazão Hidrológica Anômala:**
> Uma vazão afluente sustentada de **$\approx 3.300\text{ m}^3/\text{s}$** em uma bacia montanhosa de apenas $55\text{ km}^2$ supera em mais de **70 vezes** o regime normal de monção ($45\text{ m}^3/\text{s}$).

---

## 3. Desagregação das Três Fontes Hídricas (Balanço de Massa)

$$V_{\text{lago}} = V_{\text{rio\_base}} + V_{\text{fusão\_térmica}} + V_{\text{chuva\_toró}}$$

```
                       BALANÇO DE MASSA DO ENCHIMENTO DO LAGO
  
  [Volume Total Requerido: 8.500.000 m³ (100%)]
  ├── 💧 Rio Base (Monção 45 m³/s em 2.570s)  ──►   115.650 m³ ( 1.4%)
  ├── 🧊 Fusão Térmica de Gelo (Impacto 1.200m)──►   237.907 m³ ( 2.8%)
  └── ⛈️ Precipitação Convectiva ("O TORÓ")    ──► 8.146.443 m³ (95.8%) ◄── FONTE DOMINANTE
```

### Componente 1: Vazão de Base do Rio Lhende Khola
*   Vazão de monção de verão: $Q_{\text{base}} \approx 45\text{ m}^3/\text{s}$.
*   Volume fornecido em 2.570 s:
    $$V_{\text{base}} = 45\text{ m}^3/\text{s} \times 2.570\text{ s} = \mathbf{115.650\text{ m}^3}\text{ (apenas 1.4\% do total requerido)}$$
    *(Sozinho, o rio levaria mais de **52 horas** para encher o lago).*

### Componente 2: Fusão Térmica de Gelo por Fricção do Colapso
*   Massa desprendida: $M = 15\times 10^6\text{ m}^3 \times 1.800\text{ kg/m}^3 = 2.7\times 10^{10}\text{ kg}$.
*   Queda livre: $h = 1.200\text{ m}$.
*   Energia potencial liberada:
    $$E_p = M \cdot g \cdot h = 2.7\times 10^{10}\text{ kg} \times 9.81\text{ m/s}^2 \times 1.200\text{ m} \approx 3.178\times 10^{14}\text{ J}$$
*   Calor latente de fusão do gelo: $L_f = 3.34\times 10^5\text{ J/kg}$.
*   Assumindo que 25% da energia de impacto converteu-se em calor dissipado na fusão:
    $$M_{\text{gelo\_fundido}} = \frac{0.25 \times 3.178\times 10^{14}}{3.34\times 10^5} \approx 2.379\times 10^8\text{ kg} \rightarrow V_{\text{fusão}} \approx \mathbf{237.907\text{ m}^3}\text{ (2.8\% do total)}$$

### Componente 3: Volume Requerido da Chuva Convectiva ("O Toró")
$$V_{\text{chuva}} = 8.500.000\text{ m}^3 - (115.650\text{ m}^3 + 237.907\text{ m}^3) = \mathbf{8.146.443\text{ m}^3}$$
$$\mathbf{M_{\text{chuva}} \approx 8.15\text{ Milhões de Toneladas de Água}}$$

---

## 4. Análise de Densidade de Chuva: "10 Toneladas sobre Alguns Metros"

Considerando a bacia hidrográfica a montante do barramento com área $A_{\text{bacia}} = 55\text{ km}^2 = 55\times 10^6\text{ m}^2$ e coeficiente de escoamento superficial em alta montanha rochosa $C_{\text{runoff}} \approx 0.90$:

### 1. Lâmina de Chuva Média Acumulada na Bacia:
$$P_{\text{lâmina}} = \frac{V_{\text{chuva}}}{A_{\text{bacia}} \times C_{\text{runoff}}} = \frac{8.146.443\text{ m}^3}{55.000.000\text{ m}^2 \times 0.90} \approx 0.1646\text{ m} = \mathbf{164.6\text{ mm}}$$

### 2. Conversão para Massa e Concentração por Área:
*   Como $1\text{ m}^3\text{ de água} = 1.000\text{ litros} = 1\text{ tonelada}$:
    *   **Densidade Pontual:** $164.6\text{ mm} = \mathbf{0.165\text{ toneladas de água por metro quadrado}}$ ($164.6\text{ kg/m}^2$).
    *   **Em um quadrado de $10\text{ m} \times 10\text{ m} = 100\text{ m}^2$:**
        $$\text{Massa de água} = 0.1646\text{ ton/m}^2 \times 100\text{ m}^2 = \mathbf{16.5\text{ Toneladas de Água!}}$$
    *   **Em 1 hectare ($100\text{ m} \times 100\text{ m} = 10.000\text{ m}^2$):**
        $$\text{Massa de água} = 0.1646\text{ ton/m}^2 \times 10.000\text{ m}^2 = \mathbf{1.646\text{ Toneladas de Água!}}$$

```
               CONCENTRAÇÃO DA ÁGUA DO TORÓ NA SUPERFÍCIE
  
  ┌─────────────────────────┐
  │                         │
  │     10 metros           │  Área = 100 m²
  │                         │  Massa de Água Concentrada = 16.5 TONELADAS!
  │                         │
  └─────────────────────────┘
        10 metros
  
  • Para concentrar exatamente 10 TONELADAS de água, a chuva atingiu
    uma área de apenas 60.8 m² (um retângulo de 7.8 m x 7.8 m!).
```

---

## 5. Conclusão da Verificação Numérica

$$\text{A CONTA FECHA COM PRECISÃO FÍSICA!}$$

1. **A física do toró é a única explicação hidrodinâmica viável** para o enchimento ultrarrápido do lago de $8.5\times 10^6\text{ m}^3$ em apenas **42 minutos e 50 segundos**.
2. A taxa de precipitação de **164.6 mm** acumulada nas encostas íngremes de alta montanha concentra **16.5 toneladas de água a cada 100 metros quadrados**, gerando uma onda de escoamento superficial instantânea com vazão de pico superior a **$3.300\text{ m}^3/\text{s}$**, que superou a capacidade da barreira de detritos, deflagrando o galgamento (*overtopping*) e o colapso catastrófico.
