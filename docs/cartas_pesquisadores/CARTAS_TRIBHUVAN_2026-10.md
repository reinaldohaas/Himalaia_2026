# Cartas a três pesquisadores da Tribhuvan University (Kirtipur e Amrit Campus)

**Data:** 21 de outubro de 2026; **revisão de 29/10/2026:** a fonte passa a ser a bacia de 1,2 km² da ruptura no Tsangbu Ri (ponto do drone), não o anfiteatro do Langtang Lirung; a massa de gelo exigida passa a ser a de um gatilho (ver `AGUA_SUPERRESFRIADA_ANFITEATRO.md` e `TESTES_PONTO_DRONE_COLAPSO_NUVEM.md`).

**Antes de enviar, preencher:**
* `[department]`: seu departamento na UFSC;
* `[e-mail]` e `[phone]`.

**Endereços:** ficam fora deste arquivo, porque o repositório é público. Estão na conversa, tirados das páginas oficiais da universidade.

**Envio:** uma carta por pessoa, sem cópia entre os três. Na carta 2, pôr Pradip Karki em cópia, porque ele trabalha com os dados GLD360 do grupo.

**Link do repositório citado nas cartas:** https://github.com/reinaldohaas/Himalaia_2026

**Antes de mandar, conferir dois pontos:**
* "Rasuwa" na carta 2. O meteorologista do DHM citado no Nepalnews (27/08) falou de céu limpo em Rasuwa e de nebulosidade densa sobre Dolakha, Sindhupalchok e o Tibete. Por isso a carta pede descargas "on the Tibetan side and over Rasuwa".
* "four orders of magnitude" na carta 3: agora se refere só ao volume de água da cheia. Depois da revisão de 29/10, as cartas não dizem mais que os modelos ficam "ordens de grandeza abaixo" do necessário, porque para um gatilho bastam 10⁶–10⁷ kg de gelo.

---

## Carta 1 — Dr. Dibas Shrestha (CDHM, Tribhuvan University, Kirtipur)

**Subject:** The 26 August 2026 Tsangbu Ri – Lhende Khola event: satellite and Langtang observations, and an unconventional atmospheric hypothesis

Dear Dr. Shrestha,

My name is Reinaldo Haas. I am a meteorologist at the Federal University of Santa Catarina (UFSC), Brazil. I am writing because your work on Himalayan high-mountain meteorology, satellite meteorology and the Langtang basin, including the 2025 paper on the expansion of the Lirung glacial lake, is very close to a problem I have been working on for two months: the atmosphere over the Tsangbu Ri / Langtang Lirung source in the night before the slope failure of 26 August 2026.

I should be open from the start: my hypothesis is heterodox. I think the event may have had an atmospheric component that current models do not represent.
* During the night, a large reservoir of supercooled water may have been held over the source without raining, through an electrical "anti-scavenging" effect of the kind proposed by Tinsley.
* A vortex with strong updrafts would then have brought aerosol, triggered secondary ice production and released latent heat.
* The cloud would have collapsed, and its ice (graupel or hail formed at −3 to −8 °C, at 6.4–7.6 km) would have fallen into the small catchment above the scar described below. Since the failure was mostly in rock, the ice need not supply the mass of the landslide: its load and, above all, its meltwater would have been the trigger of a slope already close to failure.

These ideas come from my book *Como encontrar seu dragão* ("How to find your dragon"), now in final revision for publication in Portuguese. It deals with events of this kind that were common in Brazil in the 19th and early 20th centuries, and that led me to propose a phenomenon that Brazilian Indigenous peoples call *toró*. I know the hypothesis is heterodox. What supports it, in the book, is a list of more than 50 geomyths: traditional accounts, in Brazil and elsewhere, that describe the phenomenon and contain details that can be tested against modern explanations. That is why I take eyewitness accounts seriously. A hypothesis like this has to earn its place with data, and that is what I have been trying to do.

By "the source" I mean the rupture on the north flank of Tsangbu Ri, about 13 km east of Rasuwagadhi: the scar mapped by Adhikari et al. (2026, *Seismica*) and by D. Petley, at about 28.29°N, 85.53°E, with its crown at about 5,140 m and the failure surface in rock. A drone video recorded at the moment of failure points to a small catchment just above it: 1.2 km² between 4,500 and 5,600 m, draining west to the Chhochen Khola and on to the Lhende Khola, on the Nepal–China border. The whole catchment lies above the freezing level (0 °C at about 5.8 km that night in ERA5). It is separate from the larger north-face amphitheatre of Langtang Lirung (3.4 km², 4,000–7,200 m) just to the south-west, where my first analyses had placed the source, following the automatic USGS location.

**What I have done so far** (code, data and reports are open at https://github.com/reinaldohaas/Himalaia_2026):
* **Satellite.** Himawari-9 every 10 minutes, with each pixel moved to its parallax-corrected position. The coldest core of the evening convection (210–220 K) stood over the source until about 00:30 UTC. Its top then descended to the terrain between 00:30 and 01:30 UTC, 1.5–2.5 h before the seismic onset (02:52:16 UTC; Adhikari et al. 2026). After sunrise, compared pixel by pixel with the clear morning of 25 August, supercooled liquid tops held at most 5 × 10⁶ kg of water within 10 km and none within 5 km at 02:50 UTC. The 1.6-µm band shows a thin supercooled liquid layer over the snow of Langtang Lirung just after the collapse of the cloud.
* **Optical and radar.** Sentinel-2 shows no loss of snow or ice above the scar beyond the noise, and a new deposit of at least 5 km² down to the Lhende Khola. Himawari's 500-m visible band shows no ice cover over most of the catchment once it was sunlit; a deposit concentrated in a gully would be smaller than a pixel.
* **Models**, from CM1 at 500 m to WRF at 9/3/1 km nested domains:
  * WRF reproduces the plateau system only in part and deposits no solid precipitation on the massif; its 1-km terrain is too smooth there.
  * A "supercooled mode" and an imposed vortex in WRF concentrate supercooled water up to about 5 × 10⁷ kg within 30 km and 4 × 10⁶ kg within 5 km. For a trigger, 10⁶–10⁷ kg of ice may be enough, so the question is no longer the size of the reservoir but whether ice reached the ground in the catchment.
  * I am now testing a 333-m inner domain over the massif.

**Where I am stuck:**
1. There is no direct observation near the source of the supercooled water or of the cloud base during the night.
2. The satellite cannot see inside the convective core that stood over the source, and a small ice deposit would be below its resolution. Witnesses on the Tibetan side describe fog over the massif just before the collapse.
3. The models do not yet deliver ice to the ground on the massif, and I cannot tell whether this is a limit of the resolution, of the physics or of the hypothesis.

I would value your view on any of this. I would be especially grateful for two things:
* your reading of the satellite sequence;
* any help to obtain the hourly records of the Kyanjin station for 20–27 August 2026. DHM showed in its WMO webinar that it recorded only about 1 mm in the 24 h to 08:45 on 26 August. I have also written to DHM.

I would gladly share all my material and would welcome any form of collaboration.

With kind regards,

Reinaldo Haas
Federal University of Santa Catarina (UFSC), [department], Florianópolis, Brazil
[e-mail] · [phone]

---

## Carta 2 — Dr. Shriram Sharma (Department of Physics, Amrit Campus, Tribhuvan University)

**Subject:** Lightning and atmospheric electricity on the night of 25–26 August 2026 near Langtang (Rasuwa)

Dear Dr. Sharma,

My name is Reinaldo Haas. I am a meteorologist at the Federal University of Santa Catarina (UFSC), Brazil. I am writing because your group is, as far as I can find, the reference for lightning and atmospheric electricity in Nepal. Your papers on lightning occurrence in Nepal (2022) and on lightning and meteorological parameters (2026) use exactly the kind of data that could test a question I cannot answer alone.

I study the atmosphere over the Tsangbu Ri / Langtang Lirung source in the hours before the slope failure of 26 August 2026 (seismic onset 02:52:16 UTC). My hypothesis is unconventional, and I want to say so openly.
* I think an electrical "anti-scavenging" effect of the kind proposed by Tinsley may have held a large reservoir of supercooled water over the source without rain during the night.
* Its later release, through secondary ice production and the collapse of the cloud, would have delivered ice and meltwater to a small catchment above the scar, as the trigger of a slope already close to failure.

These ideas come from my book *Como encontrar seu dragão* ("How to find your dragon"), now in final revision for publication in Portuguese. It deals with events of this kind that were common in Brazil in the 19th and early 20th centuries, and that led me to propose a phenomenon that Brazilian Indigenous peoples call *toró*. I know the hypothesis is heterodox. What supports it, in the book, is a list of more than 50 geomyths: traditional accounts, in Brazil and elsewhere, that describe the phenomenon and contain details that can be tested against modern explanations. That is why I take eyewitness accounts seriously.

By "the source" I mean the rupture on the north flank of Tsangbu Ri, about 13 km east of Rasuwagadhi: the scar mapped by Adhikari et al. (2026, *Seismica*) and by D. Petley, at about 28.29°N, 85.53°E, with its crown at about 5,140 m and the failure surface in rock. A drone video recorded at the moment of failure points to a small catchment just above it: 1.2 km² between 4,500 and 5,600 m, draining west to the Chhochen Khola and on to the Lhende Khola, on the Nepal–China border. The whole catchment lies above the freezing level (0 °C at about 5.8 km that night in ERA5). It is separate from the larger north-face amphitheatre of Langtang Lirung (3.4 km², 4,000–7,200 m) just to the south-west, where my first analyses had placed the source, following the automatic USGS location.

**What I have found so far** (open at https://github.com/reinaldohaas/Himalaia_2026):
* **Satellite.** In Himawari-9, with parallax corrected, the coldest core of the evening convection (210–220 K) stood over the source until about 00:30 UTC. Its top descended to the terrain between 00:30 and 01:30 UTC.
* **Models.** My cloud-resolving (CM1) and regional (WRF) simulations, including versions with imposed electrical suppression of coalescence and an imposed vortex, build supercooled water near the source but do not yet deposit ice on the ground there.
* **Lightning.** What I do not have at all is lightning data.
  * Lightning would be strong evidence of mixed-phase convection with graupel near the source, and its absence would also be informative.
  * Before about 01:00 UTC the cloud tops were cold enough for lightning, and later they were not.
  * Eyewitnesses describe thunder-like sounds only at the moment of the collapse, and none describe flashes.
  * The DHM sensors installed in 2017 seem to have been largely out of service. The Chinese satellite LMI data are not yet public.

**My request.** Does your group have, or have access to, any lightning record for 25 August 17:00 UTC to 26 August 03:00 UTC within about 100 km of 28.29°N, 85.53°E? GLD360, your field-mill or electric-field records in Kathmandu, or the South Asian Lightning Network would all help, especially on the Tibetan side and over Rasuwa.

I would also be very interested in your opinion, as a specialist in atmospheric electricity, on whether a Tinsley-type mechanism could matter at this scale.

I would gladly share all my material, acknowledge your group in any publication, and contribute to any analysis you find worthwhile.

With kind regards,

Reinaldo Haas
Federal University of Santa Catarina (UFSC), [department], Florianópolis, Brazil
[e-mail] · [phone]

---

## Carta 3 — Dr. Binod Pokharel (CDHM, Tribhuvan University, Kirtipur)

**Subject:** Supercooled water and secondary ice over Langtang before the 26 August 2026 slope failure — a request for your view

Dear Dr. Pokharel,

My name is Reinaldo Haas. I am a meteorologist at the Federal University of Santa Catarina (UFSC), Brazil. I am writing because of your background in the microphysics of orographic clouds, in particular your work at Wyoming on shallow orographic clouds with large supercooled droplets and glaciogenic seeding. It touches the centre of a hypothesis I am testing for the 26 August 2026 Tsangbu Ri – Lhende Khola event.

I want to be clear that the hypothesis is heterodox. It has three steps:
1. During the night of 25–26 August, a large reservoir of supercooled water would have been held over the source (described below) without precipitating, through an electrical suppression of collection of the kind proposed by Tinsley.
2. A vortex with strong updrafts would then have brought ice-nucleating aerosol and triggered rime splintering and other secondary ice production, with a large release of latent heat.
3. The cloud would have collapsed and its ice, as graupel or hail, would have fallen into a small catchment above the scar that lies wholly above the freezing level. Because the failure was mostly in rock, the ice would only have to trigger it: its load and meltwater on a slope already close to failure.

These ideas come from my book *Como encontrar seu dragão* ("How to find your dragon"), now in final revision for publication in Portuguese. It deals with events of this kind that were common in Brazil in the 19th and early 20th centuries, and that led me to propose a phenomenon that Brazilian Indigenous peoples call *toró*. I know the hypothesis is heterodox. What supports it, in the book, is a list of more than 50 geomyths: traditional accounts, in Brazil and elsewhere, that describe the phenomenon and contain details that can be tested against modern explanations. That is why I take eyewitness accounts seriously.

By "the source" I mean the rupture on the north flank of Tsangbu Ri, about 13 km east of Rasuwagadhi: the scar mapped by Adhikari et al. (2026, *Seismica*) and by D. Petley, at about 28.29°N, 85.53°E, with its crown at about 5,140 m and the failure surface in rock. A drone video recorded at the moment of failure points to a small catchment just above it: 1.2 km² between 4,500 and 5,600 m, draining west to the Chhochen Khola and on to the Lhende Khola, on the Nepal–China border. The whole catchment lies above the freezing level (0 °C at about 5.8 km that night in ERA5). It is separate from the larger north-face amphitheatre of Langtang Lirung (3.4 km², 4,000–7,200 m) just to the south-west, where my first analyses had placed the source, following the automatic USGS location.

**What I have done** (all open at https://github.com/reinaldohaas/Himalaia_2026):
* **CM1 at 500 m** on the real terrain, with NSSL two-moment microphysics. When coalescence is suppressed, the model holds a reservoir of only a few thousand tonnes of supercooled water. That is about four orders of magnitude below the water volume of the flood, but of the order that a trigger might need. The reservoir is never released.
* **WRF at 9/3/1 km nested domains:**
  * Suppressing the heterogeneous ice paths barely increases the supercooled water. It also weakens the convection, because the latent heat of freezing is lost.
  * An imposed vortex (13–14 m/s at 2–6 km) concentrates supercooled water to about 5 × 10⁷ kg within 30 km of the source and 4 × 10⁶ kg within 5 km. The water stays at about −2 °C, there is no freezing burst, and no solid precipitation reaches the ground on the massif.
  * A new run moves the vortex to mid-levels (maximum at 7.5 km) over the source and restricts the secondary nucleation to −8 to −3 °C, with a 333-m inner domain over the massif.
* **Satellite.** Himawari-9 shows, after sunrise, at most 5 × 10⁶ kg of supercooled liquid water in cloud tops within 10 km of the source, and a thin supercooled liquid layer over the snow of Langtang Lirung just after the collapse of the cloud.

**Where I am stuck, and where your experience would help most:**
1. Could an orographic convective cell over a 5-km ridge deposit 10⁶–10⁷ kg of graupel or hail on a 1.2-km² catchment that lies at 0 to +6 °C, and would it survive long enough to accumulate?
2. Can secondary ice production be strong and fast enough to turn such a supercooled reservoir into graupel within an hour, and to release enough latent heat to drive a collapse?
3. With the water at about −2 °C, rime splintering is outside its active range of −3 to −8 °C. Which other mechanisms would you test?

I would be very grateful for your view, even a short one. I would gladly share every configuration and result, and I would welcome a collaboration if you find the problem interesting.

With kind regards,

Reinaldo Haas
Federal University of Santa Catarina (UFSC), [department], Florianópolis, Brazil
[e-mail] · [phone]
