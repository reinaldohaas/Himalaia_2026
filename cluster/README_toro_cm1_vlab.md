# toro-CM1 — Lhende Khola, 25–26/08/2026 — pacote para o vlab (Slurm)

13 rodadas do CM1 r21.1 descritas em `TORO_CM1_SONDAGEM_REAL_ERA5.md` (repositório `Himalaia_2026`): entradas completas, código-fonte, scripts de compilação, submissão, coleta e pós-processamento.

## Conteúdo

| Pasta/arquivo | O que é |
| :--- | :--- |
| `cm1/src/` | CM1 r21.1 (cópia de `CM1/src` do autor) **já com a opção `initsfc=5`**, que lê tsk/tmn/lu/xland de `sfc_init.dat` |
| `cm1/patch/init_surface_initsfc5.patch` | o patch de 56 linhas, só para documentação; já está aplicado em `src/` |
| `tabelas/` | `RRTMG_LW_DATA`, `RRTMG_SW_DATA`, `LANDUSE.TBL` |
| `casos/<caso>/` | `namelist.input`, `input_sounding` e, quando há terreno, `perts.dat` (GLO-30) e `sfc_init.dat` (superfície) — exatamente os usados localmente |
| `casos.txt` | tabela dos casos: grupo, cpus, tempo de fila, memória, descrição |
| `compilar.sh` | compila com gfortran + OpenMP (gfortran do sistema, módulo `gcc`, ou ambiente conda `cm1`) |
| `rodar_caso.sh` | roda um caso num diretório próprio (`execucoes/<caso>`) |
| `submeter.sh` / `job_cm1.sbatch` | submetem um job Slurm por caso |
| `coletar.sh` | empacota as saídas concluídas, com SHA-256 |
| `pos/` | scripts de análise e figuras (python3 + numpy + matplotlib) e o terreno do modelo |

## Passo a passo

No seu computador:

```bash
scp toro_cm1_lhende_vlab.tar.gz vlab:~/mesoescala-montanhas/
```

No vlab:

```bash
ssh vlab
cd ~/mesoescala-montanhas && tar xzf toro_cm1_lhende_vlab.tar.gz && cd toro_cm1_lhende
sha256sum -c MANIFESTO.sha256          # confere o pacote
sinfo                                   # veja o nome da particao de CPU
bash compilar.sh                        # ~2-5 min; gera cm1/run/cm1.exe
bash submeter.sh -n todos               # mostra os sbatch, sem submeter
bash submeter.sh -t -p <particao> rad_12utc    # teste de 120 s de modelo (confere radiacao + terreno + superficie)
bash submeter.sh -p <particao> rad      # as duas rodadas com radiacao
bash submeter.sh -p <particao> todos    # ou tudo
squeue -u $USER
tail -f logs/cm1_rad_06utc-*.out
```

Se o vlab tiver disco de *scratch*, rode lá: `bash submeter.sh -e /scratch/$USER/toro_cm1 -p <particao> rad`. O `coletar.sh` e o `pos/analisar.sh` aceitam o mesmo diretório (`EXEC=...`).

Ao terminar:

```bash
bash coletar.sh                          # gera resultados_cm1_<data>.tar.gz + .sha256
bash pos/analisar.sh                     # tabelas, JSON e figuras em pos/ (opcional, no cluster)
```

E de volta no seu computador:

```bash
rsync -avP vlab:~/mesoescala-montanhas/toro_cm1_lhende/resultados_cm1_*.tar.gz* ./
```

## Os casos

| Grupo | Casos | Domínio | Custo local (WSL, referência) |
| :--- | :--- | :--- | :--- |
| `plano` | `run_{WK,pre,pico,pre_colapso}_{morrison,nssl}` (8) | 20×20×50, Δx=500 m, periódico, bolha +3 K, 2 h | ~2 min cada |
| `terreno` | `ter_{pre,pico,pre_colapso}_nssl` (3) | 80×80×64, terreno GLO-30, sem bolha, sem radiação, 3 h | ~66 min cada, 1 thread |
| `rad` | `rad_06utc` (21 h), `rad_12utc` (15 h) | terreno + RRTMG + MM5/slab + WorldCover | `rad_12utc`: 11,4 h com 8 threads, dividindo a máquina com a outra rodada; `rad_06utc` foi interrompida às 20:08 UTC de modelo após 11,7 h |

**A rodada que interessa é `rad_06utc`:** é a única que leva o estado convectivo da tarde até o colapso, às 02:52 UTC. Localmente ela foi interrompida às 20:08 UTC de modelo. Com 16 núcleos dedicados, a estimativa é de 6–10 h de parede; o limite de fila está em 48 h por segurança.

## Espaço em disco

Saídas completas, estimadas a partir das rodadas locais: `rad_06utc` ~4 GB, `rad_12utc` ~2,8 GB, cada `ter_*` ~1 GB, cada `run_*` ~90 MB. **Total de ~11 GB** sem compressão. O `coletar.sh` comprime (GrADS binário comprime ~2–3×). Se a cota da `$HOME` for pequena, use o *scratch* com `-e`.

## Testado

O pacote foi testado de ponta a ponta numa cópia limpa em Linux (Ubuntu 24.04, gfortran 13.3), simulando o cluster:
* `compilar.sh`: compilação com OpenMP;
* `submeter.sh -n todos`: os 13 comandos `sbatch` gerados;
* `rodar_caso.sh` em modo teste, nos casos `run_pre_nssl` e `rad_12utc` (este lendo `sfc_init.dat` com `initsfc=5`);
* `job_cm1.sbatch` com as variáveis do Slurm simuladas, no caso `ter_pico_nssl`;
* `coletar.sh`.

Todos terminaram com `Program terminated normally`. **Não foi testado num nó do vlab:** nome da partição, módulos e limites de fila são desconhecidos aqui. Por isso, rode primeiro o teste `-t`.

## Observações

* O executável é OpenMP, num único nó (`--ntasks=1`, `--cpus-per-task=N`). Com 80×80 pontos, mais de ~16–24 threads rende pouco.
* As entradas são **idênticas** às das rodadas locais. O código é o mesmo, recompilado; as saídas devem bater com as locais até a precisão de ponto flutuante, não bit a bit, porque o OpenMP muda a ordem das somas.
* Saída GrADS a cada 30 min (`tapfrq=1800`) nas rodadas `rad`. Para mais resolução temporal na janela do colapso, mude `tapfrq` em `casos/rad_06utc/namelist.input` **antes** de submeter e registre a mudança.
* Não desligue `output_dbz`, `output_vort` nem `output_uh` nas rodadas NSSL com terreno: nesta versão isso faz o modelo cair com falha de segmentação após ~2 min.
* `rodar_caso.sh` recusa sobrescrever um diretório que já tem saída; use `FORCAR=1` só de propósito.
