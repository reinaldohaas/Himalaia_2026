# Carta 06 — NSMC / CMA: FY-4A Lightning Mapping Imager (LMI)

**Para:** National Satellite Meteorological Center (NSMC), China Meteorological Administration (CMA)
**Portal:** https://satellite.nsmc.org.cn
**Contato de dados:** `nsmc_service@cma.gov.cn` · `feedback@nsmc.cma.gov.cn`
**Objeto:** dados do Lightning Mapping Imager do FY-4A para a noite de 25–26 de agosto de 2026, região do Langtang / Gyirong

> **Atualização (21/10/2026): esta carta está desatualizada quanto ao satélite.**
>
> **FY-4A:** saiu de serviço em 5/03/2024 (NSMC; ESSD 2026). Antes disso foi deslocado para 86,5 °E (05/2024–01/2025) e depois para 123,5 °E. Não há LMI do FY-4A para 2026.
>
> **FY-4B:** não carrega LMI.
>
> **FY-4C:** a opção que resta.
> * Lançado em 27/12/2025, a 133 °E, com um LMI melhorado em "modo de disco completo" (NSMC).
> * Em 12/10/2026, o OSCAR/WMO ainda o listava como "em comissionamento", sem acesso público aos dados.
> * O sítio fica a ~53° do ponto subsatélite, o que dá visada muito oblíqua e eficiência de detecção menor. Não está confirmado que 85,5 °E esteja no campo de visada efetivo.
>
> **Para o colega com contatos na China,** o pedido deve ser: **FY-4C LMI** (eventos, grupos e flashes), na mesma janela e na mesma caixa abaixo, e uma confirmação de que o produto cobre 85,5 °E / 28,3 °N.
>
> O resto desta carta (janela, caixa, finalidade) continua válido. O pedido ao Nepal está na `CARTA_07_DHM_NEPAL.md`.

---

## 1. Por que o FY-4A, e não o FY-4B

| Satélite | Carga útil | Longitude subsatelital | Serve? |
| :--- | :--- | ---: | :--- |
| **FY-4A** | AGRI, GIIRS, **LMI**, SEP | **104,7 °E** | **sim — o LMI está aqui** |
| FY-4B | AGRI, GIIRS, GHI, SEP | 133,0 °E | não carrega LMI |

Geometria de visada para o sítio (85,515 °E; 28,271 °N):

* distância angular ao ponto subsatelital do FY-4A: **33,7°**
* **ângulo zenital de visada: ~39°**

Para comparação, o Himawari-9 (140,7 °E), usado na análise de infravermelho já realizada, vê o mesmo ponto a **68°** de zênite. O FY-4A é substancialmente melhor, com paralaxe muito menor.

**A verificar no cadastro:** o LMI não imageia o disco completo — sua cobertura operacional é regional, centrada na China e arredores. É preciso confirmar que 85,5 °E / 28,3 °N cai dentro do campo de visada efetivo. Se cair fora, o produto não existe para este sítio e a busca termina aí.

---

## 2. Passo a passo do cadastro (tem de ser feito por você)

1. Acesse `https://satellite.nsmc.org.cn` e alterne para **English** no canto superior.
2. **Register** → conta de usuário. Campos exigidos: nome, instituição, e-mail institucional, país, finalidade de uso. Use o e-mail `@ufsc.br` — cadastros com e-mail institucional acadêmico costumam ser aprovados mais rápido.
3. Na finalidade, declare: *scientific research, non-commercial, transboundary Himalayan hazard analysis*.
4. Após aprovação, o acesso a dados fica em **Data Service → Data Order / Satellite Data**.
5. Selecione: satélite **FY-4A**, instrumento **LMI**, nível **L2**, produtos **LMIE (events)**, **LMIG (groups)** e **LMIF (flashes)**.
6. Janela temporal: **2026-08-25 06:00 UTC a 2026-08-26 12:00 UTC**.
7. Caixa: **84,0–87,0 °E, 27,0–29,5 °N**.

Se a interface não permitir seleção geográfica fina, peça o setor completo e recorto localmente.

---

## 3. Carta formal (caso o portal exija justificativa)

> **To:** National Satellite Meteorological Center, China Meteorological Administration
>
> **Subject:** Request for FY-4A LMI data — 25–26 August 2026, Gyirong / Langtang border region
>
> Dear Colleagues,
>
> I am writing to request access to Lightning Mapping Imager (LMI) data from FengYun-4A for a scientific investigation of the transboundary cascading disaster of 26 August 2026 in the Lhende Khola / Bhote Koshi / Trishuli basin, on the China–Nepal border.
>
> The event began with a rock-and-ice detachment at approximately 5,200 m elevation, recorded by the USGS as a surface-wave magnitude Ms 5.2 landslide-type seismic event (`us7000tbwb`) at 2026-08-26 02:52:10 UTC.
>
> Using open Himawari-9 AHI band-13 data, we have established that a mesoscale convective system with 8,413 km² of cloud tops colder than −60 °C was present over the region at 18:00 UTC on 25 August, and that it had dissipated by the time of the collapse. Ground reports and Nepal's DHM confirm clear skies and no rainfall at the moment of failure.
>
> The open question is the electrical state of that convective system during its mature phase. No open lightning dataset covers 85 °E for August 2026: ISS LIS was decommissioned in November 2023, and GOES GLM does not view this longitude. The FY-4A LMI, at 104.7 °E, views the site at approximately 39° zenith angle and is the only instrument providing continuous lightning observation over this region.
>
> **Requested data**
> - Instrument: FY-4A LMI, Level 2 — events (LMIE), groups (LMIG), flashes (LMIF)
> - Period: 2026-08-25 06:00 UTC to 2026-08-26 12:00 UTC
> - Region: 84.0–87.0 °E, 27.0–29.5 °N
>
> We would also be grateful for confirmation of whether this region falls within the LMI operational field of view.
>
> All data will be used exclusively for non-commercial scientific research. NSMC and CMA will be fully credited in any resulting publication, following the FengYun data citation policy. We would welcome collaboration with CMA and CAS colleagues, given that the source area lies within Chinese territory.
>
> With thanks and regards,
>
> **Prof. Reinaldo Haas**
> Departamento de Física, Universidade Federal de Santa Catarina (UFSC)
> Florianópolis, Brasil — `reinaldo.haas@ufsc.br`

---

## 4. O que fazer com o dado quando chegar

A pergunta que ele responde **não** é sobre $J_z$ de tempo bom. É sobre a eletrificação do sistema convectivo que já foi medido no Himawari.

Especificamente:

1. **Taxa de descargas ao longo da noite**, com resolução de minutos, entre 06:00 UTC de 25/08 e 12:00 UTC de 26/08.
2. **Coincidência com o pico convectivo** medido às 18:00 UTC de 25/08 (8.413 km² abaixo de −60 °C).
3. **Estado elétrico no instante do colapso** (02:52:10 UTC de 26/08). Se a taxa já era nula, confirma que o sistema estava eletricamente morto — coerente com o céu limpo observado.
4. **Fração de descargas positivas nuvem-solo (+CG)**, se o produto permitir. Sistemas com +CG dominante têm estrutura de carga invertida e são associados a granizo e correntes de gerador anômalas.

Nota metodológica registrada: os dados de descargas hoje presentes no repositório para os 15 eventos são **paramétricos**, não observacionais, e foram movidos para `data/synthetic/`. Os registros anteriores a 2004 foram removidos, porque nenhuma rede capaz de produzi-los existia. O produto do LMI seria a **primeira medição real de descargas** deste projeto.

---

## 5. Alternativas, se o NSMC não liberar

| Fonte | Cobertura de 85 °E em ago/2026 | Acesso |
| :--- | :--- | :--- |
| ISS LIS | **não** — desativado em 2023-11-16 | Earthdata (já disponível) |
| GOES GLM | **não** — não vê esta longitude | aberto |
| MTG-I1 Lightning Imager | limite de campo em ~70 °E; marginal | EUMETSAT (cadastro) |
| WWLLN | sim | acordo de pesquisa (Univ. of Washington) |
| GLD360 / Earth Networks | sim | comercial |

A WWLLN é a alternativa mais realista se o NSMC não responder — a `CARTA_02` deste diretório já está redigida para ela.
