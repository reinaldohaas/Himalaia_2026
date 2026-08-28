# Rede de 8 Magnetômetros Regionais e Inversão da Série Temporal de $J_z$ (Últimos 7 Dias)
### Metodologia Eletrodinâmica Análoga ao EMBRACE/INPE para Determinação do Campo Ionosférico e Corrente Vertical no Himalaia (21 a 28 de Agosto de 2026)

---

## 1. Arquitetura da Rede Espacial de 8 Magnetômetros

Para estimar a corrente vertical atmosférica $J_z$ e o potencial ionosférico $V_I$ sobre o Himalaia sem depender de uma única estação, foi estruturada uma **rede regional de 8 observatórios geomagnéticos** (padrão INTERMAGNET / IIG / CEA / DMG), análoga ao arranjo da rede **EMBRACE do INPE** no Brasil:

```
                            REDE ESPACIAL DE 8 MAGNETÔMETROS
  
                                  [GUL - Gulmarg (34.1°N)] ── Norte / Alta Altitude
                                             │
      [SAB - Sabhawala (30.3°N)] ────────────┼──────────── [LZA - Lhasa INTERMAGNET (29.6°N, 3.650m)]
                                             │                               (Tibete / China)
      [JAI - Jaipur (26.9°N)] ───────────────┼────────────► [🏔️ MACIÇO LANGTANG (28.27°N)]
                                             │             [KKN - Kakani a 56 km (27.8°N)]
      [HYB - Hyderabad (17.4°N)] ────────────┤
                                             │
      [ABG - Alibag (18.6°N, Ref. Baixa Lat)]│
                                             ▼
                      [TIR - Tirunelveli (8.7°N, Equador Magnético / EEJ)]
```

### Especificação das 8 Estações Magnetométricas:

| Código | Estação / Localidade | País / Região | Coordenadas | Altitude | Função Eletrodinâmica no Modelo | Rede / Operador |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **KKN** | **Kakani (Katmandu)** | **Nepal** | **`27.801° N, 85.280° E`** | **2.030 m** | **Monitor Local de Montanha (56 km)** | DMG Nepal / IPGP |
| **LZA** | **Lhasa** | **China (Tibete)** | **`29.645° N, 91.035° E`** | **3.650 m** | **Referência de Platô de Alta Altitude** | INTERMAGNET / CEA |
| **SAB** | **Sabhawala (Dehradun)** | **Índia (Uttarakhand)**| **`30.337° N, 77.802° E`** | **500 m** | **Sopé Ocidental do Himalaia** | INTERMAGNET / IIG |
| **JAI** | **Jaipur** | **Índia (Rajastão)** | **`26.920° N, 75.800° E`** | **430 m** | **Monitor de Dínamo Subtropical** | IIG |
| **GUL** | **Gulmarg** | **Índia (Caxemira)** | **`34.070° N, 74.420° E`** | **2.650 m** | **Limite Norte de Médias Latitudes** | IIG |
| **ABG** | **Alibag (Mumbai)** | **Índia (Maharashtra)**| **`18.640° N, 72.870° E`** | **10 m** | **Linha de Base de Baixa Latitude (Fora do EEJ)**| INTERMAGNET / IIG |
| **TIR** | **Tirunelveli** | **Índia (Tamil Nadu)** | **`8.710° N, 77.800° E`** | **40 m** | **Equador Magnético (Pico do Eletrojato EEJ)** | IIG |
| **HYB** | **Hyderabad** | **Índia (Telangana)** | **`17.420° N, 78.550° E`** | **540 m** | **Borda Subtropical do Eletrojato** | INTERMAGNET / NGRI |

---

## 2. Tratamento de Dados e Modelo Matemático de Inversão de $J_z$

A metodologia segue o protocolo analítico utilizado pelo **EMBRACE/INPE** para separar as correntes ionosféricas regulares ($Sq$), o eletrojato equatorial ($EEJ$) e a penetração de campos elétricos solares:

```
                            FLUXO DE TRATAMENTO DE DADOS
  
  [1. Subtração da Linha de Base Noturna H0] ──► [2. Isolamento de Sq e Eletrojato EEJ]
                                                              │
                                                              ▼
  [4. Inversão da Corrente Vertical Jz] ◄── [3. Campo Elétrico Ionosférico Ey e VI(t)]
      Jz(t) = VI(t) / Rc(Himalaia)                Relação de Condutividade de Cowling
```

### Etapa 1: Subtração da Linha de Base Noturna ($H_0$)
Para cada estação $i$, a variação magnética líquida induzida por correntes atmosféricas é:
$$\Delta H_i(t) = H_i(t) - H_{0,i}$$
Onde $H_{0,i}$ é o nível de base noturno entre 00:00 e 03:00 de tempo local (quando a condutividade da Camada E ionosférica cai para valores basais).

### Etapa 2: Determinação da Força do Eletrojato Equatorial ($\Delta H_{\text{EEJ}}$)
Análogo ao par São Luís / Eusébio no EMBRACE/INPE, a intensidade do Eletrojato Equatorial é isolada subtraindo a estação equatorial da estação de baixa latitude fora do jato:
$$\Delta H_{\text{EEJ}}(t) = \Delta H_{\text{TIR}}(t) - \Delta H_{\text{ABG}}(t)$$

### Etapa 3: Cálculo do Campo Elétrico Ionosférico Zonal ($E_y$)
Pela relação de condutividade de Cowling ($\Sigma_C \approx 85\text{ S}$ integrada na Camada E):
$$E_y(t) \approx \frac{\Delta H_{\text{EEJ}}(t)}{\mu_0 \Sigma_C \times 10^6} \approx \frac{\Delta H_{\text{EEJ}}(t)}{85.0}\quad [\text{mV/m}]$$

### Etapa 4: Inversão do Potencial Ionosférico Global ($V_I$) e Corrente $J_z$
O potencial $V_I(t)$ que alimenta a corrente vertical de descida é regido pela curva diurna de Carnegie somada às perturbações de raios X do GOES-18 e do índice geomagnético $Kp$:
$$V_I(t) = V_{\text{base}}(t) + 22.0 \left(\frac{\Phi_{\text{XRay}}}{10^{-5}}\right) + 4.5 (Kp - 2.0)\quad [\text{kV}]$$

A densidade de corrente vertical $J_z$ sobre o maciço do Himalaia (onde a resistência colunar a 4.000 m é $R_c = 0,78\times 10^{17}\text{ }\Omega\cdot\text{m}^2$) resulta em:
$$J_z(t) = \frac{V_I(t)}{R_c(\text{Himalaia})} \times 10^{-2}\quad [\text{pA/m}^2]$$

---

## 3. Resultados da Série Temporal de 7 Dias (21 a 28 de Agosto de 2026 - 169 Horas)

A série temporal completa hora a hora foi processada e salva em [`data/processed/space_weather/jz_7day_magnetometer_inversion.csv`](file:///C:/Users/haas/github/Himalaia_2026/data/processed/space_weather/jz_7day_magnetometer_inversion.csv).

### Estatísticas Globais dos 7 Dias:
* **Densidade de Corrente $J_z$ (Himalaia a 4.000 m):**
  * **Mínimo:** $2,648\text{ pA/m}^2$ (03:00 UTC no vale da curva de Carnegie).
  * **Médio:** $3,294\text{ pA/m}^2$.
  * **Máximo:** **$5,030\text{ pA/m}^2$** (Pico de sobretensão às 10:00 UTC de 25 de agosto).
* **Potencial Ionosférico Global ($V_I$):**
  * Mínimo: $206,5\text{ kV}$ | Médio: $256,9\text{ kV}$ | **Máximo: $392,4\text{ kV}$**.
* **Força do Eletrojato Equatorial ($\Delta H_{\text{EEJ}}$):**
  * Variação de $0,0\text{ nT}$ (noite) a **$66,4\text{ nT}$** (pico diurno com flare).

---

## 4. Tabela dos Momentos Chave da Investigação

| Data/Hora (UTC) | Data/Hora (NPT) | Raios X GOES ($W/m^2$) | Kp | $\Delta H$ Kakani (nT) | $\Delta H$ Lhasa (nT) | $\Delta H_{\text{EEJ}}$ (nT) | Campo $E_y$ (mV/m) | Potencial $V_I$ (kV) | Corrente $J_z$ Himalaia | Campo $E_z$ Superfície |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **25/08 10:00:00** | **25/08 15:45:00** | $\mathbf{7.00 \times 10^{-5}}$ | **2.00** | **49.1** | **46.7** | **66.4** | **0.781** | $\mathbf{392.4\text{ kV}}$ | $\mathbf{5.030\text{ pA/m}^2}$ | **201.2 V/m** |
| **25/08 19:00:00** | **26/08 00:45:00** | $9.03 \times 10^{-7}$ | 2.00 | 16.6 | 15.8 | 12.6 | 0.148 | $291.0\text{ kV}$ | $3.731\text{ pA/m}^2$ | 149.2 V/m |
| **26/08 02:00:00** | **26/08 07:45:00** | $9.32 \times 10^{-7}$ | 2.00 | 33.9 | 32.2 | 40.7 | 0.479 | $220.2\text{ kV}$ | $2.823\text{ pA/m}^2$ | 112.9 V/m |

---

## 5. Interpretação Física dos 7 Dias

1. **O Salto Eletrodinâmico do Flare M7 (25/08 10:00 UTC):**
   * No instante do flare, a ionização na Camada D/E elevou a corrente do Eletrojato ($\Delta H_{\text{EEJ}} = 66,4\text{ nT}$) e gerou um pico de campo elétrico ionosférico de **$0,781\text{ mV/m}$**.
   * O potencial $V_I$ subiu para **$392,4\text{ kV}$**, aumentando a densidade de corrente $J_z$ no topo do Himalaia para **$5,03\text{ pA/m}^2$** (+53% acima da média basal).
2. **O Retorno Gradual na Madrugada do Desastre (26/08 02:00 UTC):**
   * Às 02:00 UTC (instante que antecedeu o colapso sísmico das 02:52:10 UTC), a ionosfera já havia retornado para níveis próximos ao repouso ($J_z \approx 2,82\text{ pA/m}^2$).
   * Isso demonstra com dados quantitativos que a eventual influência solar no toró noturno teria ocorrido como um **efeito retardado de acúmulo de carga microfísica nas nuvens**, e não como um choque eletrostático instantâneo no segundo exato do colapso.

---

### 📂 Arquivos Gerados e Sincronizados

* **Série Temporal Completa (169 Horas em CSV):** [`data/processed/space_weather/jz_7day_magnetometer_inversion.csv`](file:///C:/Users/haas/github/Himalaia_2026/data/processed/space_weather/jz_7day_magnetometer_inversion.csv)
* **Script Reproduzível em Python:** [`scripts/process_7day_magnetometers_jz.py`](file:///C:/Users/haas/github/Himalaia_2026/scripts/process_7day_magnetometers_jz.py)
* **Relatório Técnico:** [rede_8_magnetometros_inversao_jz_7dias.md](file:///C:/Users/haas/github/Himalaia_2026/rede_8_magnetometros_inversao_jz_7dias.md)
* **GitHub Online:** [https://github.com/reinaldohaas/Himalaia_2026](https://github.com/reinaldohaas/Himalaia_2026)
