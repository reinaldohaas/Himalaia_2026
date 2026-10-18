# Experimentos do toró (toro_mod) — definidos antes de rodar (17/10/2026)

Base: `rad_06utc` (25/08 06 UTC → 26/08 03 UTC, 21 h), mesma sondagem, terreno, superfície e namelist da referência; só muda `tapfrq` para 900 s (saída a cada 15 min) e entra `toro_params.txt`. Tempo de modelo: 00 UTC = 64.800 s; 01:30 UTC = 70.200 s; colapso 02:52 UTC = 75.120 s; 03 UTC = 75.600 s.

Hipótese do pesquisador (Tinsley; Fundamentacao_Jz_CEAG_2024_rev9 §5.2–5.3, §2.4):
* **Estado A**: anti-varredura retém a água super-resfriada — coalescência suprimida e congelamento por contato suprimido (Bergeron não dispara).
* **Estado B**: reversão — "o aparecimento de graupel é a reversão"; levantamento/vórtice foca a convergência; a varredura liga.

Valores (não há números no documento; escolhidos como cotas, não como medidas): `fcoal = faccr = 0,1` (coalescência 10× menor), `fctfz = 0,01` (contato 100× menor) no Estado A; no Estado B, 1 (padrão) ou `fctfz_pos = 10` (varredura liga). Vórtice: ciclônico, centrado no anfiteatro (0,0), R = 2 km, sech²(h/2 km), `alpha_v` = 2,8×10⁻³ m/s² (≈10 m/s em 1 h sem atrito), de 00 UTC (rampa de 30 min) até 03 UTC.

| Experimento | Estado A | Reversão | Vórtice |
| :--- | :--- | :--- | :--- |
| `toro_A_rev_vort` | todo o período até 01:30 UTC | às 01:30 UTC; contato ×10 depois | sim |
| `toro_Ag_vort` | onde não há graupel (modo 2) | automática onde surge graupel | sim |
| `toro_vort` | — | — | sim (só dinâmica) |
| `toro_A` | todo o período | nunca | — |
| `toro_A_rev` | até 01:30 UTC | às 01:30 UTC; contato ×10 | — |
| `toro_Ag` | onde não há graupel | automática | — |

**Critérios (pré-registrados), sobre o anfiteatro (3 × 3 km) e o colapso:**
1. **Reservatório:** água líquida T < 0 °C sobre o anfiteatro às 00–02:30 UTC ≥ 10× a do controle (`rad_06utc_hib16x7`).
2. **Liberação explosiva:** taxa de chuva média no anfiteatro ≥ 50 mm/h em pelo menos uma janela de 15 min entre 01:30 e 03:00 UTC, precedida por ≥ 2 h com < 1 mm/h.
3. **Água:** volume precipitado no anfiteatro entre 00 e 03 UTC, comparado aos 14,2 × 10⁶ m³ (premissa do repositório, não medição) e à chuva do IMERG (5 mm até o colapso, na célula de 0,1°).
4. **Barulho:** proxy de raios de McCaul et al. (2009), F1 = 0,042 × fluxo de graupel a −15 °C, no raio de 10 km, 00–03 UTC; e correntes descendentes > 10 m/s a < 1 km do solo (fonte de infrassom).
5. **Satélite:** topo IR equivalente sobre o sítio às 02:30–03:00 UTC contra os 272,7 K do Himawari.

Validação antes de tudo: o executável com o patch e **sem** `toro_params.txt` tem de dar `rad_06utc_2h` bit a bit idêntica à `rad_06utc_repro` (exceto z0t/z0q). Se não der, nenhum experimento roda.
