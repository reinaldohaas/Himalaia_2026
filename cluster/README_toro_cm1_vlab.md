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
| `coletar.sh` | empacota as saídas concluídas (`--leve`: só figuras, JSON, estatísticas e logs), com SHA-256 |
| `restaurar.sh` | depois de um reinício do servidor: `source restaurar.sh` no terminal (exporta `RCLONE_CONFIG`, PATH, refaz links do Claude Code, verifica Drive, `cm1.exe` e fila) |
| `relatorio.sh` | `bash relatorio.sh [--enviar]`: gera `relatorio_vlab.txt` (estado das execuções, para verificação) e o manda ao Drive |
| `gdrive.sh` | cache no Google Drive via rclone: `instalar`, `configurar`, `importar`, `estado`, `baixar`, `enviar [--completo]` |
| `devolver_github.sh` | alternativa: sobe os pacotes para um GitHub Release (via `gh`; o login é seu; público) |
| `toro_cm1_vlab.ipynb` | notebook com todas as etapas, para o Jupyter do vlab |
| `pos/` | scripts de análise e figuras (python3 + numpy + matplotlib) e o terreno do modelo |

## Onde guardar

O vlab é um contêiner rodando como `root`, com `HOME=/root`, e **`/root` pode ser apagado quando o servidor reinicia**. Os scripts carregam o `ambiente.sh`, que põe o que precisa sobreviver em **`/home/jovyan/privado`**:

| O quê | Onde |
| :--- | :--- |
| pacote, execuções, resultados | `/home/jovyan/privado/Himalaia_2026/toro_cm1_lhende/` |
| ambientes conda (gfortran `cm1`, python/rclone `cm1pos`) | `/home/jovyan/privado/conda_envs/` |
| configuração do rclone (com o token do Drive) | `/home/jovyan/privado/.config/rclone/rclone.conf` |
| login do `gh` (alternativa GitHub) | `/home/jovyan/privado/.config/gh/` |

Para usar outro lugar: `export PERSIST=/outro/caminho` antes dos scripts. Se o gfortran veio do conda, o `cm1.exe` depende das bibliotecas de `conda_envs/cm1` (registrado em `cm1/run/cm1.env`); o `rodar_caso.sh` as carrega e avisa se sumirem.

## Passo a passo (Jupyter do vlab, sem scp/rsync)

O `jupyter.vlab.ufsc.br` não oferece scp nem rsync. O fluxo usa um **cache no Google Drive**:

| Lado | Onde |
| :--- | :--- |
| seu computador | `G:\Meu Drive\vlab_cache\Himalaia_2026\` (Google Drive para desktop, já sincronizando): `entrada\` → vlab, `saida\` ← vlab |
| vlab | `rclone` com o remoto `gdrive:`. O login é feito **no Windows** (`rclone config create gdrive drive scope=drive`); o `rclone.conf` sobe pelo Jupyter para `privado/` e `bash gdrive.sh importar` o instala (ver `bash gdrive.sh configurar`) |

Na **primeira vez** o pacote vem do GitHub (público), porque o `gdrive.sh` ainda não está no vlab. Depois: ponha versões novas em `G:\Meu Drive\vlab_cache\Himalaia_2026\entrada\` e rode `bash gdrive.sh baixar` no vlab; para devolver, `bash gdrive.sh enviar`.

**Opção A — notebook:** baixe `toro_cm1_vlab.ipynb` (está em `cluster/` no repositório e dentro deste pacote), suba-o pelo botão *Upload* do Jupyter e rode as células em ordem.

**Opção B — terminal do Jupyter** (*File → New → Terminal*):

```bash
mkdir -p /home/jovyan/privado/Himalaia_2026 && cd /home/jovyan/privado/Himalaia_2026
URL=https://raw.githubusercontent.com/reinaldohaas/Himalaia_2026/refs/heads/claude/himalaia-enchentes-auditoria-fcfdb5/cluster/toro_cm1_lhende_vlab.tar.gz
wget -O toro_cm1_lhende_vlab.tar.gz "$URL" && wget -O toro_cm1_lhende_vlab.tar.gz.sha256 "$URL.sha256"
sha256sum -c toro_cm1_lhende_vlab.tar.gz.sha256
tar xzf toro_cm1_lhende_vlab.tar.gz && cd toro_cm1_lhende
sha256sum -c --quiet MANIFESTO.sha256
sinfo -s                                       # nome da particao de CPU
bash compilar.sh                               # gera cm1/run/cm1.exe
bash submeter.sh -t -p <particao> rad_12utc    # teste de 120 s de modelo
bash submeter.sh -p <particao> rad             # rad_06utc e rad_12utc (ou: todos)
squeue -u $USER
```

Se o branch for incorporado ao `main`, troque `refs/heads/claude/himalaia-enchentes-auditoria-fcfdb5` por `refs/heads/main` na URL.

Ao terminar:

```bash
bash pos/analisar.sh          # figuras e JSON em pos/ (cria o ambiente conda cm1pos se faltar numpy/matplotlib)
bash coletar.sh --leve        # resultados_cm1_leve_<data>.tar.gz, poucos MB
bash gdrive.sh enviar         # -> G:\Meu Drive\vlab_cache\Himalaia_2026\saida\toro_cm1_lhende\<data>\  no seu computador
# alternativa sem Drive:  gh auth login && bash devolver_github.sh   (GitHub Release, publico)
```

O pacote leve também pode ser baixado direto pelo navegador: no painel de arquivos do Jupyter, botão direito → *Download*.

Para devolver as saídas 3D completas (~11 GB): `bash coletar.sh` e `bash gdrive.sh enviar --completo` (consome cota do Drive). Pelo GitHub Release, `bash devolver_github.sh --completo` divide em partes de 1,9 GB (limite de 2 GB por arquivo); para remontar:

```bash
gh release download <tag> --repo reinaldohaas/Himalaia_2026
cat resultados_cm1_*.tar.gz.parte* > resultados_cm1.tar.gz
```

O Release herda a visibilidade do repositório: **é público**.

Se o vlab tiver disco de *scratch*, rode lá: `bash submeter.sh -e /scratch/$USER/toro_cm1 ...`, e use `EXEC=/scratch/$USER/toro_cm1` no `coletar.sh` e `bash pos/analisar.sh /scratch/$USER/toro_cm1`.

## Os casos

| Grupo | Casos | Domínio | Custo local (WSL, referência) |
| :--- | :--- | :--- | :--- |
| `plano` | `run_{WK,pre,pico,pre_colapso}_{morrison,nssl}` (8) | 20×20×50, Δx=500 m, periódico, bolha +3 K, 2 h | ~2 min cada |
| `terreno` | `ter_{pre,pico,pre_colapso}_nssl` (3) | 80×80×64, terreno GLO-30, sem bolha, sem radiação, 3 h | ~66 min cada, 1 thread |
| `rad` | `rad_06utc` (21 h), `rad_12utc` (15 h) | terreno + RRTMG + MM5/slab + WorldCover | `rad_12utc`: 11,4 h com 8 threads, dividindo a máquina com a outra rodada; `rad_06utc` foi interrompida às 20:08 UTC de modelo após 11,7 h |

**A rodada que interessa é `rad_06utc`:** é a única que leva o estado convectivo da tarde até o colapso, às 02:52 UTC. Localmente ela foi interrompida às 20:08 UTC de modelo. Com 16 núcleos dedicados, a estimativa é de 6–10 h de parede; o limite de fila está em 48 h por segurança.

## Espaço em disco

Saídas completas, estimadas a partir das rodadas locais: `rad_06utc` ~4 GB, `rad_12utc` ~2,8 GB, cada `ter_*` ~1 GB, cada `run_*` ~90 MB. **Total de ~11 GB** sem compressão. O `coletar.sh` comprime (GrADS binário comprime ~2–3×). Se a cota da `$HOME` for pequena, use o *scratch* com `-e`. Pelo navegador, traga só o pacote `--leve`.

## Testado

O pacote foi testado de ponta a ponta numa cópia limpa em Linux (Ubuntu 24.04, gfortran 13.3), simulando o cluster:
* `compilar.sh`: compilação com OpenMP;
* `submeter.sh -n todos`: os 13 comandos `sbatch` gerados;
* `rodar_caso.sh` em modo teste, nos casos `run_pre_nssl` e `rad_12utc` (este lendo `sfc_init.dat` com `initsfc=5`);
* `job_cm1.sbatch` com as variáveis do Slurm simuladas, no caso `ter_pico_nssl`;
* `coletar.sh` (normal e `--leve`).

Todos terminaram com `Program terminated normally`. **Não foi testado num nó do vlab:** nome da partição, módulos e limites de fila são desconhecidos aqui. Por isso, rode primeiro o teste `-t`.

## Observações

* O executável é OpenMP, num único nó (`--ntasks=1`, `--cpus-per-task=N`). Com 80×80 pontos, mais de ~16–24 threads rende pouco.
* As entradas são **idênticas** às das rodadas locais. O código é o mesmo, recompilado; as saídas devem bater com as locais até a precisão de ponto flutuante, não bit a bit, porque o OpenMP muda a ordem das somas.
* Saída GrADS a cada 30 min (`tapfrq=1800`) nas rodadas `rad`. Para mais resolução temporal na janela do colapso, mude `tapfrq` em `casos/rad_06utc/namelist.input` **antes** de submeter e registre a mudança.
* Não desligue `output_dbz`, `output_vort` nem `output_uh` nas rodadas NSSL com terreno: nesta versão isso faz o modelo cair com falha de segmentação após ~2 min.
* `rodar_caso.sh` recusa sobrescrever um diretório que já tem saída; use `FORCAR=1` só de propósito.
