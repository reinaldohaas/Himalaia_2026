# Observatórios Geomagnéticos Próximos ao Himalaia e Estimativa de $J_z$
### Mapeamento de Estações, Redes INTERMAGNET/IIG/DMG e Fundamentação Eletrodinâmica

---

## 1. Mapeamento dos Observatórios Geomagnéticos na Região

Embora não exista um sensor direto de corrente vertical de tempo bom ($J_z$) na garganta do Lhende Khola, existem **observatórios geomagnéticos e estações magnetotelúricas de alta precisão** operando na região do Himalaia e do Platô Tibetano:

```
                          DISTRIBUIÇÃO GEOGRÁFICA DAS ESTAÇÕES
  
                    [LZA - Lhasa INTERMAGNET (3.650m)] ── 561 km a Leste (Tibete/China)
                                      ▲
                                      │
  [SAB - Sabhawala (Dehradun)] ───────┼───────► [🏔️ Maciço Langtang / Lhende Khola (28.27°N, 85.48°E)]
        (779 km a Oeste / Índia)      │
                                      ▼
                    [KKN - Kakani (DMG/IPGP)] ───────── 56 km ao Sul (Nepal)
```

### Tabela de Estações e Redes Científicas:

| Código | Observatório / Local | País / Região | Coordenadas | Altitude | Distância ao Desastre | Rede / Instrumentação |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **KKN** | **Kakani (Katmandu)** | **Nepal** | **`27.801° N, 85.280° E`** | **2.030 m** | **56,2 km** | **DMG Nepal / IPGP (França)**<br>Variômetro de indução e potencial telúrico ($E_x, E_y$). |
| **LZA** | **Lhasa** | **China (Tibete)** | **`29.645° N, 91.035° E`** | **3.650 m** | **561,2 km** | **INTERMAGNET / CEA / IGGCAS**<br>Magnetômetro triaxial Fluxgate (1 Hz) + Prótons. |
| **SAB** | **Sabhawala (Dehradun)** | **Índia (Uttarakhand)**| **`30.337° N, 77.802° E`** | **500 m** | **779,1 km** | **INTERMAGNET / IIG**<br>Observatório padrão-ouro do sopé do Himalaia. |
| **JAI** | **Jaipur** | **Índia (Rajastão)** | **`26.920° N, 75.800° E`** | **430 m** | **965,7 km** | **IIG (Indian Inst. of Geomagnetism)**<br>Fluxgate e monitor de variações $Sq$. |
| **GUL** | **Gulmarg** | **Índia (Caxemira)** | **`34.070° N, 74.420° E`** | **2.650 m** | **1.233 km** | **IIG (Estação de Alta Altitude)**<br>Monitoramento de correntes aurorais/médias latitudes. |

---

## 2. Como os Magnetômetros Ajudam a Estimar e Restringir $J_z$?

Os magnetômetros não medem diretamente a corrente vertical atmosférica $J_z$ (que requer um eletrômetro de prato coletor ou moinho de campo $E_z$), mas registram **três fenômenos eletrodinâmicos acoplados à ionosfera e ao Circuito Elétrico Global (GEC)**:

```
                            ACOPLAMENTO ELETRODINÂMICO GEC - IONOSFERA
  
  [Vento Solar / Flare M7] ──► [Magnetosfera] ──► [Campo Elétrico Penetrante (PPEF)]
                                                        │
                                                        ▼
  [Magnetômetro em Solo (LZA / KKN)] ◄── [Corrente Ionosférica na Camada E (110 km)]
  • Variação ΔH e dB/dt                        │  (Mede a densidade da corrente horizontal)
                                               ▼
                                      [Potencial Ionosférico VI(t)]
                                               │
                                               ▼
                                      [Corrente Vertical Jz = VI / Rc]
                                      (Flui pelo topo do Himalaia a 4.000m)
```

### 1. Variação do Potencial Ionosférico ($V_I$) via Corrente Ionosférica Horizontal ($Sq$ e $EEJ$):
A componente horizontal do campo magnético ($\Delta H$) medida em Lhasa (`LZA`) e Sabhawala (`SAB`) é proporcional à densidade total de corrente que flui na ionosfera sobre a região:

$$J_{\text{ionosfera}} \approx \frac{2}{\mu_0} \Delta H$$

Picos anômalos em $\Delta H$ após um flare solar refletem o aumento imediato de condutividade ionosférica ($\Delta \sigma$) induzido por raios X/EUV na Camada D e E.

### 2. Campo Elétrico de Penetração Rápida (*Prompt Penetration Electric Field - PPEF*):
Quando o campo magnético do vento solar ($B_z$) gira para o sul, campos elétricos magnetosféricos penetram instantaneamente na ionosfera de baixa/média latitude, alterando o potencial global $V_I(t)$ que alimenta a corrente vertical de descida:

$$J_z(t) = \frac{V_I(t)}{R_c}$$

### 3. Indução Eletromagnética de Faraday ($\frac{dB}{dt}$):
Variações rápidas no campo magnético ($\frac{\partial \mathbf{B}}{\partial t}$) registradas no variômetro de Kakani (`KKN`) e Lhasa induzem campos elétricos locais na superfície da Terra e nas camadas atmosféricas condutoras pela Lei de Faraday-Maxwell:

$$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$$

---

## 3. Onde Consultar e Baixar os Dados Reais dessas Estações

1. **Rede Mundial INTERMAGNET (Dados 1-minuto e 1-segundo abertos):**
   * Portal Oficial: [https://intermagnet.org/](https://intermagnet.org/)
   * Download de Séries Temporais: [https://intermagnet.org/data-download](https://intermagnet.org/data-download) *(Selecione as estações `LZA` e `SAB`)*.
2. **World Data Center for Geomagnetism, Kyoto (WDC Kyoto):**
   * Portal Oficial: [http://wdc.kugi.kyoto-u.ac.jp/](http://wdc.kugi.kyoto-u.ac.jp/)
   * Índices geomagnéticos rápidos ($Dst$, $SYM-H$, $AE$).
3. **Indian Institute of Geomagnetism (IIG):**
   * Portal de Dados: [https://iigm.res.in/](https://iigm.res.in/) *(Dados dos observatórios de Sabhawala e Jaipur)*.

---

## 4. Conclusão Científica sobre o Uso de Magnetômetros para $J_z$

* **O que os magnetômetros fornecem:** Medição contínua e fidedigna do estado da ionosfera sobre o Himalaia e o Tibete, permitindo verificar com precisão se houve penetração de campos elétricos solares ($PPEF$) ou sobretensão ionosférica $\Delta V_I$ nas 16h50min que antecederam o desastre.
* **O que ainda falta:** A medição local exata de $J_z$ exige um eletrômetro de campo elétrico atmosférico ($E_z$) instalado no Parque Nacional de Langtang. Os magnetômetros atuam como um **excelente proxy indireto da fronteira superior (ionosférica) do Circuito Elétrico Global**.
