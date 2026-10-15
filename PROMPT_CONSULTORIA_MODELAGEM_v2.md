# Prompt de consultoria em modelagem numérica — versão corrigida

**Data:** 13 de outubro de 2026
**Substitui:** o prompt produzido pelo antigravity, cujos defeitos estão listados na §A antes do texto corrigido.

---

# PARTE A — Por que o prompt anterior precisa ser substituído

## A.1 Erro de **aritmética**: a vazão citada é de outro evento

> *"uma vazão de pico estimada em mais de 8.500 m³/s"*

**8.635 m³/s é a vazão reconstruída para CHAMOLI 2021.** Para o evento de 2026 o próprio repositório calcula **3.376 m³/s** (4.095 m³/s com a declividade medida no GLO-30). O número está trocado por um fator de 2,6.

Um revisor que confira a tabela do repositório encontra a troca em um minuto, e a partir daí nada mais no texto é lido com confiança.

## A.2 Erros de **dado**: três afirmações já medidas e desmentidas

| Afirmação no prompt | O que foi medido |
| :--- | :--- |
| "chuva moderada ou insignificante (10 a 25 mm)" | **18,71 mm** no total de 3 dias — mas apenas **5,09 mm antes do colapso**, e **0,000 mm/h no instante** (IMERG meia-horário, 96 de 96 grânulos) |
| "bacia... com cotas entre 2.000 m e mais de 7.000 m" (implícita como a bacia contribuinte) | a bacia real a montante do barramento tem **3,4 a 32,7 km²** (GLO-30, priority-flood + D8). As áreas de 55 e 65,7 km² usadas no repositório **não existem em ponto nenhum** do Lhende |
| volume "superior a 15–20 milhões de m³" apresentado como observação | 20,7 M m³ é **premissa digitada**, não medição. O `config/hydraulic_assumptions.yaml` marca 71 % dos parâmetros como `ASSUMED_BY_ANALYST` |

E o prompt **omite** tudo o que já foi medido e que um consultor precisaria saber:

* **Himawari-9 B13:** sistema convectivo com 8.413 km² de topos abaixo de −60 °C às 18:00 UTC de 25/08, **dissipado a zero** entre 02:00 e 06:00 UTC de 26/08 — o colapso cai exatamente nessa janela. Um segundo sistema, maior (15.606 km²), chega 8 h depois.
* **ERA5, 48 h anteriores:** vento a 500 hPa de **2,2 m/s** (percentil 34), ascendência percentil 32, água líquida super-resfriada **0,04 kg/m²** (percentil 32). Quatro das cinco condições de onda de sotavento na mediana ou abaixo.
* **Sentinel-2 L2A real:** **nenhum lago** maior que 4,76 ha em 914 km², em quatro datas entre junho e agosto de 2026. O lago de 65,7 ha / 5,2 M m³ não existe.
* **USGS:** `us7000tbwb`, Ms 5,2 `ms_vx`, tipo `landslide`, 0 km — e um segundo deslizamento `us7000tc90`, Ms 4,2, às 06:00:35 UTC.

## A.3 Erro de **método**: o objetivo pede demonstração, não teste

> *"Meu objetivo central é demonstrar, por meio de MODELAGEM NUMÉRICA, que ocorreu um 'trombudo'"*
>
> *"como a modelagem numérica pode blindar o artigo contra essas objeções"*

Este é o defeito mais grave, e é estrutural.

Um WRF-LES configurado para produzir convecção orográfica confinada **vai produzir** convecção orográfica confinada. A escolha de domínio, de microfísica, de condição inicial e de instante de inicialização dá ao modelador graus de liberdade suficientes para gerar quase qualquer taxa de precipitação local. Um resultado assim não é evidência: é a premissa devolvida em forma de saída numérica.

E "blindar o artigo contra objeções" inverte o papel do revisor. As objeções listadas — *"foi apenas um colapso seco"*, *"foi apenas rompimento de morena sem chuva"* — não são ataques a serem repelidos. São **hipóteses concorrentes**, e no momento as medições favorecem a primeira delas.

Um consultor sênior competente, ao receber o prompt original, ou recusa o enquadramento ou entrega um plano de advocacia. Nos dois casos o tempo foi perdido.

---

# PARTE B — Prompt corrigido

> Copie daqui para baixo.

---

Atue como pesquisador sênior em Modelagem Numérica Atmosférica (WRF/LES), Hidráulica Computacional e Geofísica de Alta Montanha. Preciso de avaliação crítica de estratégia, não de validação de uma hipótese.

## 1. O evento

Colapso rocha-gelo transfronteiriço no Lhende Khola / Bhote Koshi / Trishuli (fronteira China–Nepal), **26 de agosto de 2026**.

**Fatos observacionais estabelecidos, com fonte:**

| Grandeza | Valor | Fonte |
| :--- | :--- | :--- |
| Sismo principal | Ms 5,2 `ms_vx`, tipo **landslide**, prof. 0 km, 02:52:10 UTC | USGS `us7000tbwb` |
| Segundo deslizamento | Ms 4,2, 06:00:35 UTC | USGS `us7000tc90` |
| Destacamento | ~0,2 km² a ~5.200 m, queda > 2.000 m; estimativas de massa mobilizada de ordem 10⁸ m³ | relatos técnicos (preliminar) |
| Céu no momento | **claro, sem chuva**; DHM/Nepal não registra chuva forte prévia | relatos de campo |
| Precipitação | **5,09 mm** acumulados até o colapso; **0,000 mm/h** no instante; 12,66 mm no total de 25+26/08 | GPM IMERG V07 Late, 96/96 grânulos, subsetting OPeNDAP |
| Convecção profunda | 8.413 km² com topo < −60 °C às 18:00 UTC de 25/08; **zero** entre 02:00 e 06:00 UTC de 26/08; 15.606 km² às 12:00 UTC de 26/08 | Himawari-9 AHI B13, 18 instantes |
| Ambiente 48 h antes | vento 500 hPa 2,2 m/s (pct 34); ascendência pct 32; água líq. super-resfriada 0,04 kg/m² (pct 32) | ERA5, controle interno de ±15 dias |
| Lago pré-evento | **nenhum** corpo d'água > 4,76 ha em 914 km², em 4 datas | Sentinel-2 L2A, NDWI>0,20 ∧ NIR<0,10 ∧ NDSI<0,60 |
| Gelo do maciço | cume do Langtang Lirung inalterado (−0,7 %) entre 12/08 e 27/08 | Sentinel-2 L2A, NDSI |
| Bacia a montante do barramento | **3,4 / 17,4 / 32,7 km²** conforme o ponto | Copernicus GLO-30, priority-flood + D8 |
| Declividade do talvegue na garganta | **S₀ = 0,0662** | GLO-30 |
| Nível a jusante | subida de ~9 m em 30 min em Rasuwagadhi (seção que drena **934 km²**) | relatos |

**Grandezas que são premissa, não observação** — e devem ser tratadas como livres no modelo:

* volume total do fluxo (20,7 M m³), concentração de sólidos (C_v = 0,314), e portanto a "água líquida" de 14,2 M m³;
* rugosidade de Manning (n = 0,060) e elevação de nível (Δh = 8,5 m);
* fração de gelo e eficiência de fusão por atrito da massa destacada.

No `config/hydraulic_assumptions.yaml` do projeto, **71 % dos parâmetros estão marcados `ASSUMED_BY_ANALYST`**.

## 2. A questão científica

A onda de 9 m em Rasuwagadhi foi gerada por:

* **H1 — deslocamento por massa.** O colapso empurrou e entranhou a água já presente na calha de 934 km², sem aporte atmosférico relevante.
* **H2 — fusão por atrito.** O gelo incorporado à massa fundiu na descida e forneceu a fase líquida.
* **H3 — acumulação orográfica prévia.** Nuvem de sotavento com gotículas monodispersas acumulou água super-resfriada e depositou por rima sobre o circo nas horas anteriores, carregando a massa, que falhou depois sob céu limpo.
* **H4 — aguaceiro confinado.** Precipitação extrema sobre < 15 km², invisível ao IMERG a 0,1°.

**Quero saber qual estratégia de modelagem melhor DISCRIMINA entre as quatro**, não qual delas confirma uma.

## 3. O que peço

**3.1** Para cada uma das quatro hipóteses: qual **assinatura observável distinta** o modelo produziria, e qual observação disponível a falsearia. Interessa especialmente onde H3 e H4 divergem, já que as duas invocam a atmosfera.

**3.2** Quadro comparativo das abordagens — WRF/LES aninhado; hidráulica inversa (HEC-RAS 2D, BASEMENT, Telemac); glacio-hidrologia acoplada (WRF-Hydro, balanço de energia nival); fluxo de detritos (RAMMS, r.avaflow, D-CLAW) — com resolução exigida, custo computacional, e **o que cada uma pode e não pode discriminar**.

**3.3** **Grau de liberdade do modelador.** Para a configuração que você recomendar: quantos parâmetros livres existem, e o que impede que o modelo produza o resultado desejado por escolha de configuração? Que pré-registro de configuração, ou que validação independente, tornaria o resultado defensável?

**3.4** Um WRF-LES a 333 m alimentado por ERA5 que mostre 2,2 m/s a 500 hPa tem condição de gerar > 100 mm/h local? Se não, isso por si falseia H4 naquele evento?

**3.5** Dados de entrada e validação obrigatórios, distinguindo os que **restringem** o modelo daqueles que apenas o **alimentam**.

**3.6** Que resultado faria você **abandonar** H3 e H4?

## 4. Restrições

* Nada de "blindar contra objeções". As hipóteses concorrentes são concorrentes, não ataques.
* Se a sua conclusão for que a modelagem não consegue discriminar com os dados existentes, essa é uma resposta aceitável e preferível a um plano que produza uma conclusão predeterminada.
* Se algum dado da §1 lhe parecer mal medido, diga — a cadeia de proveniência está documentada e pode ser reauditada.

---

# PARTE C — Observação sobre o que a modelagem deveria resolver primeiro

Antes de qualquer WRF, há uma inconsistência aritmética mais barata de resolver e que condiciona todo o resto:

Se a massa destacada foi de ordem **10⁸ m³**, ela é **cinco vezes maior** que o `total_bulk_m3 = 20,7 × 10⁶` adotado. A fase sólida sozinha excederia o volume total do fluxo. Ou o bulk está subestimado por um fator ≥ 5, ou a maior parte do material depositou no vale alto sem alcançar a seção de controle.

Enquanto isso não fechar, os 14,2 M m³ de "água líquida" — que são o alvo de toda a modelagem proposta — não têm base. **Inversão da força do deslizamento a partir de formas de onda FDSN** resolve a massa de forma independente, é dado aberto, e custa ordens de grandeza menos que um LES.
