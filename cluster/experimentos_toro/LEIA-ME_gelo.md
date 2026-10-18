# Experimentos do toró, série 2 — gelo vindo de cima na camada armada (18/10/2026)

Definidos antes de rodar. Base: `toro_Ag` (Estado A onde não há graupel), cuja camada de água super-resfriada sobre o anfiteatro chega a 1,2–2,6 mil t entre 02:00 e 02:30 UTC, sem nada que a dispare. Pergunta: **se cristais de gelo caírem sobre essa camada (a bigorna do sistema de mesoescala que o Himawari mostrou chegando), a reversão dispara e a água é liberada de forma explosiva?**

**Gelo injetado como gatilho, não como fonte de água:** cristais de gelo de nuvem (`qi`, `cci`; índices 4 e 11 do vetor de hidrometeoros da NSSL ptype 27), num cilindro de 4 km de raio centrado no anfiteatro, entre 5,5 e 7,5 km ASL, de **01:45 a 02:45 UTC** (71.100–74.700 s de modelo).

| Experimento | Base | Cristais | Massa injetada em 1 h (ordem) |
| :--- | :--- | :--- | :--- |
| `toro_Ag_gelo` | `toro_Ag` | 19 /kg/s (≈ 10 L⁻¹ a cada 15 min), 1,9 × 10⁻¹⁰ kg/kg/s | ~40 t (reservatório: ~2.600 t) |
| `toro_Ag_gelo10` | `toro_Ag` | 10× | ~400 t |
| `toro_ctrl_gelo` | controle (sem Estado A) | como `toro_Ag_gelo` | ~40 t |

**Validações antes:** (1) executável novo sem `toro_params.txt` = bit a bit `rad_06utc_repro` (2 h); (2) executável novo com os parâmetros de `toro_Ag` = bit a bit `execucoes/toro_Ag` (2 h), o que prova que o código da semeadura é inerte quando desligado; (3) teste curto com tudo ligado, inclusive a semeadura.

**Critérios (os mesmos da série 1, `LEIA-ME.md`), com foco em:**
* **C2 — liberação explosiva:** taxa média no anfiteatro ≥ 50 mm/h em 15 min entre 01:30 e 03:00 UTC, depois de < 1 mm/h em 23:30–01:30.
* **Reversão:** aparecimento de graupel na camada sobre o anfiteatro depois de 01:45 UTC.
* **Água:** volume precipitado no anfiteatro e em 10 km, 00–03 UTC, contra o reservatório (~2,6 × 10³ t) e os 14,2 × 10⁶ m³ (premissa).
* **Barulho:** raios (F1 de McCaul) e correntes descendentes junto ao solo.
* **Satélite:** topo IR sobre o sítio às 02:30–03:00 contra 272,7 K.
