# Teste de estabilidade de um d04 de 333 m sobre o maciço (24/10/2026)

**Por que:** o d03 de 1 km rebaixa o maciço, com máximo de 6.438 m contra 7.216 m no GLO-30. As encostas altas (≥ 6 km), onde a hipótese revisada põe a acumulação, quase não existem no modelo. Um d04 de 333 m com o relevo do GLO-30 deve subir o maciço para perto de 7 km.

O risco é a estabilidade. O d03 já estourou com passo de 4 s sobre encostas íngremes (w-cfl 27), e o d04 terá encostas ainda mais inclinadas.

## Grade

* **d04:** filho do d03, `parent_grid_ratio = 3`, dx = 333,33 m.
* **Posição:** `i_parent_start = 67`, `j_parent_start = 66` (índices do d03, base 1); `e_we = e_sn = 91` (30 × 30 km).
* **Cantos:** SW 28,141 N / 85,374 E; NE 28,416 N / 85,676 E.
* **Relevo:** Copernicus GLO-30, média de área a 3″ (~90 m), no formato do geogrid. Está em `glo30_3s/` (`index` e um tile de 540 × 480, de 28,08 a 28,48 N e 85,30 a 85,75 E). Gerado por `scripts/wrf/glo30_geogrid.py`.

## namelist.wps (acréscimo ao de `wps_run/`)

```
&share
 max_dom = 4,
 start_date = '2026-08-25_00:00:00','2026-08-25_00:00:00','2026-08-25_00:00:00','2026-08-25_00:00:00',
 end_date   = '2026-08-25_01:00:00','2026-08-25_00:00:00','2026-08-25_00:00:00','2026-08-25_00:00:00',
/
&geogrid
 parent_id         =   1,   1,   2,   3,
 parent_grid_ratio =   1,   3,   3,   3,
 i_parent_start    =   1,  70,  61,  67,
 j_parent_start    =   1,  64,  61,  66,
 e_we              = 240, 334, 151,  91,
 e_sn              = 190, 226, 151,  91,
 geog_data_res     = 'default','default','default','glo30+default',
/
```

Para o teste, os quatro domínios começam às 00 UTC de 25/08. Na rodada real o d03 começa às 12 UTC.

## GEOGRID.TBL (cópia local; o original em `privado/WRF-Chem/WPS` não é tocado)

Na seção `name = HGT_M`, acrescentar:

```
        interp_option = glo30:average_gcell(4.0)+four_pt
        abs_path = glo30:/home/jovyan/privado/Himalaia_2026/wrf_lhende/d04/glo30_3s/
```

Apontar `opt_geogrid_tbl_path` para a pasta da cópia. A suavização do HGT_M fica como está (`smooth_option = smth-desmth_special`, `smooth_passes = 1`).

## namelist.input do teste (a partir do de A)

* `max_dom = 4`, com as quatro colunas.
* `run_hours = 0`, `run_minutes = 30`, com início às 00 UTC em todos os domínios.
* d04: `parent_time_step_ratio = 3` (dt = 1 s), `epssm = 0.9`, `zadvect_implicit = 1`; as mesmas físicas do d03, sem convecção parametrizada.
* `e_vert` igual aos outros (61).

## Critérios do teste

1. 30 min sem estourar: `SUCCESS COMPLETE WRF`, sem NaN, com o número de linhas de CFL no d04 relatado.
2. Máximo do `HGT` no `wrfinput_d04` sobre o maciço: tem de passar de ~6.900 m (no d03 é 6.438 m).
3. w máximo no d04 aos 30 min.

Se passar, o d04 entra nas rodadas E (e A, como controle), com o d03 e o d04 começando às 12 UTC.
