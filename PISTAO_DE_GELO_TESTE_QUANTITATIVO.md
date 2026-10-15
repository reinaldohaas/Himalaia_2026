# O pistão de gelo sobre o anfiteatro: teste quantitativo da cadeia completa

**Data:** 07 de setembro de 2026

A cadeia proposta, tomada inteira e não em pedaços:

> Modulação de $J_z$ (Tinsley) → electro-antiscavenging preserva população monodispersa de gotículas super-resfriadas → introdução de núcleos de congelamento → multiplicação secundária (Hallett-Mossop, estilhaçamento) → reação em cadeia → **acúmulo e colapso de um pistão de gelo sobre o anfiteatro de erosão**

Tratada assim, ela não é uma hipótese de "chuva forte". É uma hipótese de **acúmulo aéreo e descarga gravitacional concentrada** — e faz previsões quantitativas distintas, que dá para calcular. Abaixo, o que os números exigem.

---

## 1. O anfiteatro existe, e é um coletor — medido no GLO-30

Bacia a montante do ponto onde a massa alcança o fundo do vale (85,5132 °E; 28,2849 °N; 4.010 m):

| Parâmetro | Valor |
| :--- | ---: |
| Área | **3,39 km²** |
| Cota | 4.010 – 7.216 m |
| **Relevo** | **3.206 m** |
| Cota mediana | 5.913 m |
| Declividade média | **47,8°** (mediana 48,2°; p90 66,9°) |
| Área com declividade > 45° | 57 % |
| **Aspecto: voltado para NORTE** | **85,3 %** |
| Compacidade $4\pi A/P^2$ | **0,674** (forma fechada, tipo circo) |

Um circo de 3,4 km² com 3,2 km de relevo, paredes a quase 50° e 85 % da superfície voltada para o norte — frio, sombreado o ano todo, e geometricamente fechado. **É um coletor de massa.** Esta parte do modelo se confirma pela topografia.

E a capacidade é compatível com a escala do evento:

| Camada acumulada sobre o anfiteatro | Volume |
| :--- | ---: |
| 50 m | **169 M m³** |
| 100 m | 339 M m³ |
| 200 m | 677 M m³ |

O volume destacado reportado é da ordem de $10^8$ m³. **Uma camada de ~30 a 50 m sobre este anfiteatro dá exatamente essa ordem de grandeza.** Não é prova, mas é consistência dimensional, e ela não existia antes.

---

## 2. Quanto o pistão precisa ser grande — dois cálculos independentes

### 2.1 Carga de condensado

Para sustentar $14{,}2$ M m³ de água ($1{,}42\times10^{10}$ kg) como condensado suspenso:

| Carga de condensado | Volume de nuvem | Espessura sobre 15 km² | Sobre 1.000 km² |
| :--- | ---: | ---: | ---: |
| 0,5 g/m³ (estratiforme) | 28.400 km³ | 1.893 km | 28,4 km |
| 1,0 g/m³ (convectiva moderada) | 14.200 km³ | 947 km | 14,2 km |
| **3,0 g/m³ (máximo observado)** | **4.733 km³** | **316 km** | **4,7 km** |
| 5,0 g/m³ (acima do observado) | 2.840 km³ | 189 km | 2,8 km |

A tropopausa tropical fica em ~16 km. Toda linha que exija espessura maior está fisicamente fechada.

> **Confinado em 15 km²: exige nuvem de centenas de quilômetros de espessura — impossível.**
> **Espalhado por ~1.000 km² com a carga máxima já observada: ~5 km de espessura — perfeitamente possível.**

### 2.2 Suprimento de vapor

| Água precipitável disponível | Área a ser esgotada por completo |
| ---: | ---: |
| 10 mm | 1.420 km² |
| 20 mm | 710 km² |
| 30 mm | **473 km²** |

### 2.3 Convergência

Os dois cálculos, partindo de premissas independentes, convergem em **$10^2$ a $10^3$ km²**.

**Conclusão: a massa não é o problema. O confinamento é.** Um pistão capaz de entregar 14–17 M m³ tem de ser um sistema de mesoescala, não uma célula de 15 km². O calor latente de condensação envolvido é de **35.000 a 43.000 TJ** — cerca de dez vezes a energia potencial de todo o colapso rochoso de $10^8$ m³.

---

## 3. A tensão interna que isso revela

Aqui está o ponto que decide a hipótese, e ele não é um detalhe:

* O **balanço de massa** exige que o pistão tenha $10^2$–$10^3$ km².
* O **mecanismo de descarga** exige que ele desabe concentrado sobre um anfiteatro de **3,4 km²**.

São requisitos opostos. Espalhar o sistema para acomodar a massa faz com que a maior parte dela caia **fora** do anfiteatro; concentrá-lo no anfiteatro faz com que a massa não caiba na troposfera.

A hipótese só sobrevive se existir um mecanismo de **focalização** — algo que colete o condensado de $10^2$–$10^3$ km² e o descarregue sobre $10^0$ km². Convergência orográfica em circo fechado é candidata plausível e conhecida, mas o fator de concentração exigido é de **100 a 1.000×**, e isso precisa ser demonstrado, não assumido.

Este é o problema central a ser resolvido, e ele é bem posto: tem um número associado, e o número é testável em modelo de nuvem resolvido (WRF-LES ou equivalente) com microfísica de duas fases e SIP ativa.

---

## 4. Estado da verificação observacional

**MODIS Terra, 2026-08-26, ~05:00 UTC** (duas horas após o colapso), caixa 26,0–30,5 °N / 83,0–88,0 °E: nuvem de monção encostada na vertente sul e sobre a planície gangética; **lado tibetano em grande parte limpo**; nenhuma bigorna de sistema convectivo profundo identificável sobre o sítio. Bigornas persistem por horas, então uma ausência duas horas depois é informativa — mas não conclusiva.

**MODIS banda 31 noturna:** obtida, porém **não interpretável sem calibração**. O planalto tibetano a 5.000 m está, ele próprio, a temperaturas de topo de nuvem à noite; sem escala calibrada não se separa solo frio de nuvem fria. Não uso esta imagem como evidência em nenhuma direção.

**O que decidiria:** infravermelho geoestacionário com cadência de 15–30 min ao longo da noite de 25 para 26 de agosto, com temperatura de brilho calibrada. Um sistema de $10^3$ km² com topos abaixo de −60 °C seria inconfundível, e a sua ausência fecharia a hipótese.

| Sensor | Longitude subsatelital | Adequação | Acesso |
| :--- | :--- | :--- | :--- |
| **INSAT-3D / 3DR** | 82 °E | **ideal** — quase no nadir do sítio | MOSDAC (registro gratuito) |
| Meteosat-9 IODC | 45,5 °E | boa | EUMETSAT (registro gratuito) |
| FY-4B AGRI | 105 °E | boa | NSMC/CMA (registro) |
| Himawari-9 | 140,7 °E | ângulo alto, marginal | JAXA/NOAA (aberto) |

O repositório já afirmava ter usado INSAT-3D. **Não existe nenhum arquivo INSAT nele** (`find . -iname "*insat*"` retorna vazio). Este é, portanto, um dado que nunca foi obtido e que é decisivo.

---

## 5. O que muda na leitura do evento

A hipótese do pistão **não é incompatível** com o que já foi medido — e isso merece ser dito com clareza, porque as duas leituras vinham sendo tratadas como excludentes.

O que a imagem Sentinel-2 real mostrou foi que o **corpo de gelo do maciço permanece** (cume inalterado em −0,7 %). Isso descarta que a massa destacada fosse a geleira preexistente. Mas **não descarta** que fosse massa **acumulada recentemente** sobre o anfiteatro — que é justamente o que o pistão prevê. Gelo novo depositado e colapsado deixaria o gelo antigo intacto, exatamente como se observa.

E há a consistência dimensional da §1: 30–50 m acumulados sobre 3,39 km² dão os $10^8$ m³ reportados.

Portanto a hipótese continua viva, mas agora com um requisito numérico explícito: **fator de focalização de 100 a 1.000×**, e a exigência de um sistema de mesoescala visível na noite de 25–26 de agosto.

---

## 6. O que fazer, em ordem

1. **Obter INSAT-3D/3DR** da noite de 25–26/08/2026, TIR-1 calibrado, cadência de 30 min. Decide a existência do sistema de mesoescala. Registro gratuito no MOSDAC.
2. **ERA5** (chave gratuita do CDS): água precipitável, CAPE, velocidade vertical e conteúdo de gelo em nuvem, horários, sobre a região. Quantifica o suprimento de vapor e a convergência disponível.
3. **Modelo de nuvem resolvido** com SIP ativa, testando o fator de focalização orográfica em circo fechado. É aqui que a hipótese passa ou não passa.
4. **Monitores de nêutrons** para os 15 eventos: decréscimos de Forbush contra o mesmo controle já usado para o Kp. É a última via eletrodinâmica em aberto.

---

## 7. Reprodução

```
DEM      : Copernicus GLO-30, bacia delineada por priority-flood + D8 (ver ANALISE_DEM_GLO30)
anfiteatro: montante de 85,5132E / 28,2849N (z=4010 m)
imagens  : https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi
           LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor, TIME=2026-08-26
           BBOX=26.0,83.0,30.5,88.0
calculos : piston.py (carga de condensado e suprimento de vapor), anfiteatro.py (geometria)
```
