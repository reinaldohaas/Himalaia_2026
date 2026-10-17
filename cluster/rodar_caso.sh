#!/bin/bash
# Roda UM caso do CM1 num diretorio proprio.
# Uso:  bash rodar_caso.sh <caso>             (ex.: rad_06utc)
#       TESTE=1 bash rodar_caso.sh <caso>     (so 120 s de modelo, em <caso>_teste)
#       EXEC=/scratch/$USER/cm1 bash rodar_caso.sh <caso>
#       EXE_ALT=caminho/cm1.exe SUFIXO=_repro bash rodar_caso.sh <caso>   (outro executavel, outro diretorio)
#       FORCAR=1 ...                          (permite reaproveitar um diretorio ja usado)
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
CASO=${1:?informe o caso (ver casos.txt)}
SRC="$AQUI/casos/$CASO"
[ -d "$SRC" ] || { echo "ERRO: caso '$CASO' nao existe em $AQUI/casos" >&2; exit 1; }
EXE=${EXE_ALT:-$AQUI/cm1/run/cm1.exe}                # EXE_ALT: outro executavel (ex.: reproducao/cm1_estatico.exe)
[ -x "$EXE" ] || { echo "ERRO: $EXE nao existe; rode antes: bash compilar.sh" >&2; exit 1; }
if [ -f "$AQUI/cm1/run/cm1.env" ]; then source "$AQUI/cm1/run/cm1.env"; export LD_LIBRARY_PATH="$ENV_PREFIX/lib:${LD_LIBRARY_PATH:-}"; fi
if [ -z "${CM1_RUNNER:-}" ] && ldd "$EXE" | grep -q "not found"; then
  echo "ERRO: o cm1.exe nao acha bibliotecas (o ambiente do compilador sumiu?). Recompile: bash compilar.sh" >&2
  ldd "$EXE" | grep "not found" >&2; exit 1; fi

EXEC=${EXEC:-$AQUI/execucoes}
NOME=$CASO${SUFIXO:-}; [ "${TESTE:-0}" = "1" ] && NOME=${NOME}_teste     # SUFIXO: ex. _repro
DIR="$EXEC/$NOME"
if ls "$DIR"/cm1out_* >/dev/null 2>&1 && [ "${FORCAR:-0}" != "1" ]; then
  echo "ERRO: $DIR ja tem saida. Use FORCAR=1 ou outro EXEC." >&2; exit 1
fi
mkdir -p "$DIR"
cp "$SRC"/* "$DIR"/
cp "$AQUI"/tabelas/* "$DIR"/
cp "$EXE" "$DIR"/cm1.exe
if [ "${TESTE:-0}" = "1" ]; then
  sed -i -E 's/^( timax +=).*/\1 120.0,/; s/^( tapfrq +=).*/\1 60.0,/' "$DIR/namelist.input"
fi

cd "$DIR"
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-${SLURM_CPUS_PER_TASK:-8}}
export OMP_STACKSIZE=${OMP_STACKSIZE:-512M}
export OMP_PLACES=${OMP_PLACES:-cores} OMP_PROC_BIND=${OMP_PROC_BIND:-close}
ulimit -s unlimited 2>/dev/null || true
{
  echo "caso=$CASO  dir=$DIR  host=$(hostname)  threads=$OMP_NUM_THREADS  inicio=$(date -u +%FT%TZ)"
  echo "exe sha256=$(sha256sum cm1.exe | cut -d' ' -f1)  runner=${CM1_RUNNER:-sistema}"
  grep -E "^ (timax|tapfrq|ptype|terrain_flag|radopt|initsfc|nx|ny|nz) " namelist.input | tr -s ' '
} > execucao.info
s=$(date +%s)
set +e
${CM1_RUNNER:-} ./cm1.exe > cm1.print.out 2>&1      # CM1_RUNNER: carregador do kit de reproducao (glibc embutida)
rc=$?
set -e
echo "fim=$(date -u +%FT%TZ)  rc=$rc  parede=$(( $(date +%s) - s ))s  ultima_linha=$(tail -1 cm1.print.out)" >> execucao.info
cat execucao.info
grep -q "Program terminated normally" cm1.print.out || { echo "AVISO: o CM1 NAO terminou normalmente (ver $DIR/cm1.print.out)" >&2; exit 2; }
