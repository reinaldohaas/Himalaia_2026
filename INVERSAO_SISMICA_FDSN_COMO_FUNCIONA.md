# Inversão de força sísmica: o que é, por que decide a massa, e o que já está disponível

**Data:** 13 de outubro de 2026

---

## 1. O que é FDSN

*Federation of Digital Seismograph Networks.* É o protocolo padrão de serviço web para pedir dados sísmicos: você monta uma URL com rede, estação, canal e intervalo de tempo, e recebe a forma de onda em miniSEED. Aberto, sem credencial.

```
https://service.iris.edu/fdsnws/dataselect/1/query?
    net=NK&sta=KKN&cha=BH?&start=2026-08-26T02:45:00&end=2026-08-26T03:15:00
```

---

## 2. Por que um deslizamento não é um terremoto

Um **terremoto** é ruptura: duas faces de uma falha deslizam uma contra a outra em segundos. O sinal é de alta frequência, com fases P e S nítidas.

Um **deslizamento de 10⁸ m³** é outra coisa: é massa acelerando ladeira abaixo. Pela terceira lei de Newton, enquanto a massa acelera para baixo e para fora, ela empurra a Terra na direção oposta com força igual. Essa força age por **dezenas a centenas de segundos**, não por segundos, e irradia ondas de **período muito longo** — 20 a 150 s — que um sismo pequeno não produz.

É exatamente por isso que o USGS catalogou este evento como `landslide` com magnitude `ms_vx` (ondas de superfície), e não como terremoto.

O próprio `ARTIGO_CIENTIFICO` do repositório já descreve isso corretamente, na linha 180:

> *"ondas de superfície de longo período (ondas de Rayleigh) com crescimento assimétrico emergente, típico de grandes colapsos de massa gravitacional de rocha e gelo"*

A descrição está certa. O que faltou foi usá-la.

---

## 3. Por que a força é recuperável — a matemática

A relação entre a força aplicada à Terra e o sismograma registrado é **linear**:

$$u(t) \;=\; G(t) \,*\, F(t)$$

| Termo | O que é | De onde vem |
| :--- | :--- | :--- |
| $u(t)$ | deslocamento registrado na estação, 3 componentes | **medido** — FDSN |
| $G(t)$ | função de Green: resposta da Terra a um impulso unitário naquele ponto, para aquela estação | **calculado** de um modelo de velocidades (PREM, ak135) |
| $F(t)$ | força que o deslizamento aplicou à Terra, vetorial | **a incógnita** |
| $*$ | convolução | |

Conhecendo $u$ e $G$, resolve-se para $F$ por mínimos quadrados regularizados no domínio da frequência. A saída é o **histórico vetorial da força**, em três componentes, segundo a segundo.

Com várias estações em azimutes diferentes, o problema fica sobredeterminado e a solução, estável.

---

## 4. E daí sai a massa, sem nenhum parâmetro arbitrado

Porque $\mathbf{F} = m\,\mathbf{a}$.

A aceleração vem da topografia, que já está delineada no GLO-30: o trajeto desce de 5.590 m para 4.010 m em 1,45 km, com declividade média de 47,8° no anfiteatro. Dois caminhos equivalentes:

1. **Ajuste de trajetória.** Integra-se $F(t)/m$ duas vezes com uma massa tentativa, obtendo a trajetória do centro de massa. Varia-se $m$ até a trajetória coincidir com o percurso observado no DEM.
2. **Razão de picos.** $m \approx F_{\max} / a_{\max}$, com $a_{\max}$ estimada da declividade e do atrito.

Nos dois casos **a massa sai da física**, não de uma premissa.

### 4.1 É o mesmo método que resolveu Chamoli

Os 27 × 10⁶ m³ que Shugar et al. (2021, *Science*) reportam para Chamoli — e que o seu repositório cita — vieram de inversão de força sísmica combinada com imagem e DEM. O mesmo procedimento está disponível para 2026, com dado aberto, e nunca foi aplicado.

### 4.2 Por que isso importa agora, e mais do que qualquer modelo

Há uma inconsistência que precede toda a modelagem atmosférica:

* massa destacada reportada: **~10⁸ m³**
* `total_bulk_m3` adotado no repositório: **20,7 × 10⁶ m³**

A fase sólida sozinha seria **cinco vezes maior** que o volume total do fluxo. Enquanto isso não fechar, os 14,2 M m³ de "água líquida" — alvo de toda a modelagem proposta — não têm base, porque saem de $V_{\text{água}} = V_{\text{bulk}} \times (1 - C_v)$ com os dois termos arbitrados.

A inversão resolve $V_{\text{bulk}}$ por medição. **Custa ordens de grandeza menos que um LES e condiciona o resultado dele.**

---

## 5. O que já está disponível — verificado

Consulta ao serviço FDSN do IRIS: **17 estações de banda larga** dentro de 12° do epicentro. Dado confirmado para a janela do colapso em quatro delas:

| Rede | Estação | Local | Distância | Azimute | miniSEED (30 min) |
| :--- | :--- | :--- | ---: | :--- | ---: |
| **NK** | **KKN** | Kakani, Nepal | **0,52° (~58 km)** | — | **492 kB** |
| **IO** | **EVN** | Pyramid Lab, Everest | 1,19° (~132 km) | leste | **1.140 kB** |
| **IN** | **SHL** | Shillong, Índia | 6,33° | sudeste | **1.346 kB** |
| **II** | **NIL** | Nilore, Paquistão | 11,53° | oeste | **360 kB** |

Sem dado na janela: IC LSA (Lhasa), K5 WANG (Butão). Outras onze estações nas redes CB (China), K5 (Butão), MM (Myanmar), CB (Qinghai) estão no catálogo e podem ser testadas.

Quatro estações com cobertura azimutal de leste, sudeste e oeste, mais uma praticamente em cima, bastam para uma primeira inversão restringindo magnitude e direção da força.

### 5.1 Sobre o KKN

O repositório contém as duas versões da mesma estação:

* `dados_infrassom_avalanche.md:34` — *"**Nota: KKN é estação sísmica, não microbarômetro**"* ✔
* `analise_solar_jz_tempestades_infrassom.md:176` — propõe *"obter as três componentes (BHZ, BHN, BHE) via IRIS para inversão de força do impacto de massa"* ✔
* `ARTIGO_CIENTIFICO:137` — lista **KKN/Kakani como magnetômetro** na rede fabricada de 14 estações ✘

A rede de magnetômetros inventada pegou o código de estação de um sismômetro real que estava documentado corretamente em outro arquivo do mesmo projeto.

---

## 6. O que falta para executar

| Item | Situação |
| :--- | :--- |
| Formas de onda | **disponíveis**, FDSN, sem credencial |
| Resposta instrumental | disponível pelo mesmo serviço (`fdsnws/station`, `level=response`) |
| Modelo de velocidades | PREM / ak135, públicos |
| Topografia para a trajetória | **já delineada** — GLO-30, priority-flood + D8 |
| `obspy` | **não instalado** neste ambiente |
| Funções de Green | `instaseis` (bancos pré-calculados) ou `pyrocko`/`fomosto`; nenhum instalado |

`obspy` é a biblioteca padrão para ler miniSEED, remover resposta instrumental e filtrar em período longo. Instalá-la altera o seu ambiente Python, então é decisão sua — `conda install -c conda-forge obspy instaseis` ou o equivalente com pip.

Fluxo de trabalho, uma vez instalada:

1. Baixar formas de onda e respostas das quatro estações, janela de −5 a +15 min em torno de 02:52:10 UTC.
2. Remover resposta instrumental; converter para deslocamento.
3. Filtrar passa-banda em **20–150 s** — a banda do sinal de massa, onde o ruído sísmico de curto período não entra.
4. Calcular funções de Green para cada par fonte–estação (Instaseis com banco PREM, ou `fomosto`).
5. Inversão linear regularizada para $F(t)$, três componentes.
6. Ajustar $m$ pela trajetória contra o DEM.

---

## 7. Observação sobre os modelos atmosféricos existentes

`toro-model` (2,2 GB, anelástico 3D com produção secundária de gelo), `eoce-model` (arXiv:2411.08219) e `toro-CM1` são infraestrutura real. Mas os três rodam, hoje, com **sondagem analítica Weisman-Klemp e hodógrafa curva de supercélula** — uma atmosfera idealizada, escolhida para suportar supercélula.

Isso é legítimo para **demonstrar que o mecanismo é fisicamente possível**. Não é capaz de mostrar que ele **ocorreu** em 26 de agosto de 2026, porque a atmosfera de entrada não é a daquele dia.

O passo que transforma esses modelos em teste do evento já existe no seu próprio ambiente: **`era5_to_cm1`**. A ERA5 das 48 h anteriores ao colapso já está baixada — `data/raw/era5/himalaia_2026_202608.nc`, 5 níveis, passo de 6 h.

A pergunta que isso responde é direta e falseável:

> Rodando `toro-CM1` com a sondagem **real** de 25–26 de agosto de 2026, em vez da Weisman-Klemp, o modelo ainda produz o toró?

Com vento de **2,2 m/s** a 500 hPa e água líquida super-resfriada no percentil 32, a resposta provável é não. Mas essa é uma previsão minha, e o modelo é seu — ele decide, não eu.

Se produzir mesmo assim, é um resultado forte e inesperado, e aí o mecanismo merece atenção séria. Se não produzir, você saberá exatamente qual condição ambiental falta, e isso vira a hipótese seguinte.
