# Cartas a três pesquisadores da Tribhuvan University (Kirtipur e Amrit Campus)

**Data:** 21 de outubro de 2026

**Antes de enviar, preencher:**
* `[TITLE OF THE BOOK]`: título do livro;
* `[publisher, year]`: editora e ano;
* `[department]`: seu departamento na UFSC;
* `[e-mail]` e `[phone]`.

**Endereços:** ficam fora deste arquivo, porque o repositório é público. Estão na conversa, tirados das páginas oficiais da universidade.

**Envio:** uma carta por pessoa, sem cópia entre os três. Na carta 2, pôr Pradip Karki em cópia, porque ele trabalha com os dados GLD360 do grupo.

**Link do repositório citado nas cartas:** https://github.com/reinaldohaas/Himalaia_2026

**Antes de mandar, conferir dois pontos:**
* "Rasuwa" na carta 2. O meteorologista do DHM citado no Nepalnews (27/08) falou de céu limpo em Rasuwa e de nebulosidade densa sobre Dolakha, Sindhupalchok e o Tibete. Por isso a carta pede descargas "on the Tibetan side and over Rasuwa".
* "four orders of magnitude" na carta 3. Vale para o CM1. No WRF a diferença é de 2,5–3,5 ordens, e é assim que as cartas 1 e 3 a descrevem.

---

## Carta 1 — Dr. Dibas Shrestha (CDHM, Tribhuvan University, Kirtipur)

**Subject:** The 26 August 2026 Tsangbu Ri – Lhende Khola event: satellite and Langtang observations, and an unconventional atmospheric hypothesis

Dear Dr. Shrestha,

My name is Reinaldo Haas. I am a meteorologist at the Federal University of Santa Catarina (UFSC), Brazil. I am writing because your work on Himalayan high-mountain meteorology, satellite meteorology and the Langtang basin, including the 2025 paper on the expansion of the Lirung glacial lake, is very close to a problem I have been working on for two months: the atmosphere over the Tsangbu Ri / Langtang Lirung source in the night before the slope failure of 26 August 2026.

I should be open from the start: my hypothesis is heterodox. I think the event may have had an atmospheric component that current models do not represent.
* During the night, a large reservoir of supercooled water may have been held over the amphitheatre without raining, through an electrical "anti-scavenging" effect of the kind proposed by Tinsley.
* A vortex with strong updrafts would then have brought aerosol, triggered secondary ice production and released latent heat.
* The cloud would have collapsed onto the source, as a dense ice–water mass, before the failure.

These ideas belong to a long tradition of observations and interpretations of sudden "water from the sky" catastrophes in mountains, which I discuss in my book *[TITLE OF THE BOOK]* (in press, [publisher, year]). I know such a hypothesis has to earn its place with data, and that is what I have been trying to do.

**What I have done so far** (code, data and reports are open at https://github.com/reinaldohaas/Himalaia_2026):
* **Satellite.** Himawari-9 every 10 minutes, with the parallax inverted for a cloud directly over the source. A thick ice-topped cloud stayed over the source from about 17:30 to 00:30 UTC. Its top then descended from about 10 km to the terrain between 00:30 and 01:30 UTC, 1.5–2.5 h before the seismic onset (02:52:16 UTC; Adhikari et al. 2026, *Seismica*). At 02:50 UTC no cloud top distinguishable from the terrain lay within 30 km.
* **Optical and radar.** Sentinel-2 shows no loss of snow or ice above the scar beyond the noise, and a new deposit of at least 5 km² down to the Lhende Khola.
* **Models**, from CM1 at 500 m to WRF at 9/3/1 km nested domains:
  * WRF reproduces the plateau system only in part and gives no rain over the amphitheatre.
  * A "supercooled mode" and an imposed vortex in WRF concentrate supercooled water up to about 5 × 10⁷ kg within 30 km. That is still 2.5–3.5 orders of magnitude below what the hypothesis requires.
  * I am now considering ERF, for its immersed-boundary terrain and super-droplet microphysics on very steep slopes.

**Where I am stuck:**
1. There is no direct observation near the source of the supercooled water or of the cloud base during the night.
2. Infrared from Himawari cannot separate a near-0 °C cloud inside the amphitheatre from the terrain. Witnesses on the Tibetan side describe fog over the massif just before the collapse.
3. The models cannot hold or concentrate a reservoir of the required size, and I cannot tell whether this is a limit of the physics or of the hypothesis.

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
* Its later release, through secondary ice production and the collapse of the cloud, would have reached the slope.

This idea is part of a long tradition of accounts of sudden atmospheric catastrophes in mountains, which I discuss in my book *[TITLE OF THE BOOK]* (in press, [publisher, year]).

**What I have found so far** (open at https://github.com/reinaldohaas/Himalaia_2026):
* **Satellite.** In Himawari-9, a thick cloud with tops at 218–235 K (10–13 km) stayed over the source for about seven hours. Its top descended to the terrain between 00:30 and 01:30 UTC.
* **Models.** My cloud-resolving (CM1) and regional (WRF) simulations, including versions with imposed electrical suppression of coalescence and an imposed vortex, do not produce a reservoir of the required size.
* **Lightning.** What I do not have at all is lightning data.
  * Lightning would be strong evidence of mixed-phase convection with graupel near the source, and its absence would also be informative.
  * Before about 01:00 UTC the cloud tops were cold enough for lightning, and later they were not.
  * Eyewitnesses describe thunder-like sounds only at the moment of the collapse, and none describe flashes.
  * The DHM sensors installed in 2017 seem to have been largely out of service. The Chinese satellite LMI data are not yet public.

**My request.** Does your group have, or have access to, any lightning record for 25 August 17:00 UTC to 26 August 03:00 UTC within about 100 km of 28.27°N, 85.52°E? GLD360, your field-mill or electric-field records in Kathmandu, or the South Asian Lightning Network would all help, especially on the Tibetan side and over Rasuwa.

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
1. During the night of 25–26 August, a large reservoir of supercooled water would have been held over the source amphitheatre without precipitating, through an electrical suppression of collection of the kind proposed by Tinsley.
2. A vortex with strong updrafts would then have brought ice-nucleating aerosol and triggered rime splintering and other secondary ice production, with a large release of latent heat.
3. The cloud would have collapsed and funnelled onto the source as a dense ice–water mass, perhaps one tenth of the density of ice, before the failure.

This line of thought belongs to a long tradition of accounts of sudden atmospheric catastrophes in mountains, which I discuss in my book *[TITLE OF THE BOOK]* (in press, [publisher, year]).

**What I have done** (all open at https://github.com/reinaldohaas/Himalaia_2026):
* **CM1 at 500 m** on the real terrain, with NSSL two-moment microphysics. When coalescence is suppressed, the model holds a reservoir of only a few thousand tonnes of supercooled water, about four orders of magnitude too small.
* **WRF at 9/3/1 km nested domains:**
  * Suppressing the heterogeneous ice paths barely increases the supercooled water. It also weakens the convection, because the latent heat of freezing is lost.
  * An imposed vortex (13–14 m/s at 2–6 km) concentrates supercooled water to about 5 × 10⁷ kg within 30 km of the source. The water stays at about −2 °C, and there is no freezing burst and no release.
  * A new run is now restricting the secondary nucleation to points with updrafts above 2 m/s.
* **ERF next.** I am considering ERF, for its immersed-boundary terrain on slopes of 45° and more, and its super-droplet microphysics. There, an electrical effect could be represented as a change in collision efficiency rather than as switching processes off.

**Where I am stuck, and where your experience would help most:**
1. Is there any physical way, in your view, for an orographic cloud to accumulate supercooled water on the order of 10¹⁰ kg over a few km² without precipitating? Or is the limit I keep hitting in the models physical?
2. Can secondary ice production be strong and fast enough to freeze such a reservoir within an hour, and to release enough latent heat to drive a collapse?
3. With the water at about −2 °C, rime splintering is outside its active range of −3 to −8 °C. Which other mechanisms would you test?

I would be very grateful for your view, even a short one. I would gladly share every configuration and result, and I would welcome a collaboration if you find the problem interesting.

With kind regards,

Reinaldo Haas
Federal University of Santa Catarina (UFSC), [department], Florianópolis, Brazil
[e-mail] · [phone]
