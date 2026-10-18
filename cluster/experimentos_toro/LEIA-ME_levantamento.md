# Experimentos do toró, série 3 — levantar a camada armada até −5 a −15 °C (18/10/2026)

Definidos antes de rodar. Na série 2, os cristais chegaram à camada armada do `toro_Ag`, mas ela estava a 0 a −3 °C, perto do mínimo do crescimento por difusão; glaciou a ~15 %/h, sem graupel nem chuva. Pergunta: **se a camada for levantada até −5 a −15 °C, onde o crescimento por difusão e o Hallett-Mossop são eficientes, a glaciação vira cadeia e a água é liberada?**

**Levantamento controlado** (`toro_mod`, `ilift`): w relaxado (τ = 300 s) para o alvo w_l · exp(−(r/3 km)²) · sin(π(z − 4,5 km)/(10 − 4,5 km)), numa coluna sobre o anfiteatro (r < 6 km, 4,5–10 km ASL), de **01:45 a 02:45 UTC** (rampa de 10 min). Com 5,3–6 K/km de resfriamento úmido, 1 m/s por ~50 min levanta ~3 km (≈ −15 a −18 K): a camada passa pela faixa −5 a −15 °C.

| Experimento | Base | Levantamento | Gelo vindo de cima |
| :--- | :--- | :--- | :--- |
| `toro_Ag_lev` | `toro_Ag` (Estado A onde não há graupel) | w_l = 1 m/s | — |
| `toro_Ag_lev2` | `toro_Ag` | w_l = 2 m/s | — |
| `toro_Ag_lev_gelo` | `toro_Ag` | w_l = 1 m/s | como `toro_Ag_gelo10` |
| `toro_ctrl_lev` | controle (sem Estado A) | w_l = 1 m/s | — |

**Validações antes:** (1) executável novo (`2355ff92…`) sem `toro_params.txt` = bit a bit `rad_06utc_repro` (2 h); (2) com os parâmetros de `toro_Ag` = bit a bit `execucoes/toro_Ag` (2 h); (3) teste curto com tudo ligado.

**Critérios:**
* **Levantamento efetivo:** temperatura média da água super-resfriada sobre o anfiteatro (`T_SLW`) ≤ −5 °C em algum instante entre 02:00 e 02:45 UTC (no `toro_Ag`: −3 a −4 °C).
* **Reversão:** graupel sobre o anfiteatro (`graupel(t)`) acima de 10 % do reservatório depois de 01:45 UTC.
* **C2 — liberação explosiva:** taxa média no anfiteatro ≥ 50 mm/h em 15 min entre 01:30 e 03:00 UTC, depois de < 1 mm/h em 23:30–01:30.
* **Água, barulho e satélite:** como na série 1 (volume contra 14,2 × 10⁶ m³; raios F1; descendentes; topo contra 272,7 K).
* **Atribuição:** `toro_ctrl_lev` mostra o que o levantamento faz sem o reservatório; a diferença `toro_Ag_lev` − `toro_ctrl_lev` é o efeito do Estado A.
