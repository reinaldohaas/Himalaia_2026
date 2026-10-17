#!/bin/bash
# Roda casos do CM1 SEM Slurm, em segundo plano, na propria sessao do Jupyter do vlab
# (o servidor do Jupyter ja e um no de computacao; la nao existe sbatch).
#
# Uso:  bash rodar_direto.sh recursos                 # nucleos/memoria que a sessao realmente tem
#       bash rodar_direto.sh [-j N] [-t] <selecao>     # selecao: caso(s) ou grupo plano|terreno|rad|todos
#       bash rodar_direto.sh estado                    # o que esta rodando e o andamento
#       bash rodar_direto.sh parar                     # interrompe a fila em execucao
#   -j N : threads OpenMP (padrao: nucleos disponiveis, ate 16)
#   -t   : teste curto (120 s de modelo) em <caso>_teste
# Os casos rodam um depois do outro, na ordem de casos.txt. Log em logs/direto_<data>.log.
#
# ATENCAO: o processo vive enquanto o SEU servidor do Jupyter estiver ligado. Se o JupyterHub
# desligar servidores ociosos ou voce clicar em "Stop My Server", a rodada para.
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$AQUI/logs"
PIDF="$AQUI/logs/direto.pid"
EXEC=${EXEC:-$AQUI/execucoes}

nucleos() {
  local n q p
  n=$(nproc 2>/dev/null || echo 1)
  if [ -r /sys/fs/cgroup/cpu.max ]; then                        # cgroup v2
    read -r q p < /sys/fs/cgroup/cpu.max || true
    [ "${q:-max}" != "max" ] && [ -n "${p:-}" ] && n=$(( (q + p - 1) / p < n ? (q + p - 1) / p : n ))
  elif [ -r /sys/fs/cgroup/cpu/cpu.cfs_quota_us ]; then          # cgroup v1
    q=$(cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us); p=$(cat /sys/fs/cgroup/cpu/cpu.cfs_period_us)
    [ "$q" -gt 0 ] 2>/dev/null && n=$(( (q + p - 1) / p < n ? (q + p - 1) / p : n ))
  fi
  echo "$n"
}


# tempo de modelo, %, ritmo e previsao a partir de cm1out_stats (1 registro por statfrq; 1a variavel = mtime)
progresso() {
  local d=$1 ctl="$1/cm1out_stats.ctl" dat="$1/cm1out_stats.dat" nv rec n mt tmax ini agora dt fim fimt
  [ -f "$ctl" ] && [ -f "$dat" ] || return 0
  nv=$(sed -n '/^vars/,/^endvars/p' "$ctl" | grep -vcE '^(vars|endvars)')
  rec=$((nv * 4)); n=$(( $(stat -c %s "$dat") / rec )); [ "$n" -ge 1 ] || return 0
  mt=$(od -An -t f4 -j $(( (n - 1) * rec )) -N 4 "$dat" 2>/dev/null | tr -d ' ')
  tmax=$(grep -E '^ *timax' "$d/namelist.input" | head -1 | tr -dc '0-9.,' | cut -d, -f1)
  ini=$(grep -oE 'inicio=[0-9T:-]+Z' "$d/execucao.info" 2>/dev/null | cut -d= -f2)
  agora=$(date -u +%s)
  fimt=$(grep -oE 'fim=[0-9T:-]+Z' "$d/execucao.info" 2>/dev/null | cut -d= -f2)
  [ -n "$fimt" ] && agora=$(date -u -d "$fimt" +%s)          # concluida: mede ate o fim, nao ate agora
  dt=0; [ -n "$ini" ] && dt=$(( agora - $(date -u -d "$ini" +%s) ))
  fim=$(grep -c 'Program terminated normally' "$d/cm1.print.out" 2>/dev/null || true)
  awk -v mt="$mt" -v tm="$tmax" -v dt="$dt" -v fim="${fim:-0}" -f "$AQUI/progresso.awk"
}

case "${1:-}" in
  recursos)
    echo "host: $(hostname)"
    echo "nproc: $(nproc)   nucleos efetivos (cgroup): $(nucleos)"
    free -g 2>/dev/null | head -2 || true
    for f in /sys/fs/cgroup/memory.max /sys/fs/cgroup/memory/memory.limit_in_bytes; do
      [ -r "$f" ] && echo "limite de memoria ($f): $(cat "$f")"; done
    df -h "$AQUI" | tail -1
    command -v sbatch >/dev/null && echo "sbatch: disponivel (use submeter.sh)" || echo "sbatch: NAO disponivel nesta sessao -> use rodar_direto.sh"
    exit 0 ;;
  estado)
    if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then echo "fila RODANDO (pid $(cat "$PIDF"))"; else echo "nenhuma fila rodando"; fi
    L=$(ls -t "$AQUI"/logs/direto_*.log 2>/dev/null | head -1 || true); [ -n "$L" ] && { echo "== $L"; tail -n 8 "$L"; }
    for d in "$EXEC"/*/; do [ -d "$d" ] || continue
      n=$(basename "$d"); s="$d/cm1out_stats.dat"
      if grep -qs "Program terminated normally" "$d/cm1.print.out"; then st="concluido"
      elif [ -f "$s" ]; then st="rodando/parado ($(( $(date +%s) - $(stat -c %Y "$s") )) s desde a ultima saida)"
      else st="ainda sem saida"; fi
      printf '  %-28s %s\n' "$n" "$st"
      progresso "$d"
    done
    exit 0 ;;
  parar)
    [ -f "$PIDF" ] || { echo "nenhuma fila"; exit 0; }
    P=$(cat "$PIDF"); kill -TERM -- "-$P" 2>/dev/null || kill -TERM "$P" 2>/dev/null || true
    pkill -TERM -f "$AQUI/execucoes/.*/cm1.exe" 2>/dev/null || pkill -TERM -x cm1.exe 2>/dev/null || true
    rm -f "$PIDF"; echo "fila interrompida"; exit 0 ;;
esac

J=""; TESTE=0
while getopts "j:t" o; do case $o in j) J=$OPTARG;; t) TESTE=1;; *) exit 1;; esac; done
shift $((OPTIND-1))
[ $# -ge 1 ] || { sed -n '2,16p' "$0"; exit 1; }
[ -x "$AQUI/cm1/run/cm1.exe" ] || { echo "ERRO: compile antes: bash compilar.sh" >&2; exit 1; }
if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then
  echo "ERRO: ja ha uma fila rodando (pid $(cat "$PIDF")). Veja: bash rodar_direto.sh estado" >&2; exit 1; fi
[ -n "$J" ] || { J=$(nucleos); [ "$J" -gt 16 ] && J=16; }

SEL=" $* "; CASOS=()
while read -r caso grupo resto; do
  [ -n "${caso:-}" ] || continue
  [[ "$SEL" == *" todos "* || "$SEL" == *" $grupo "* || "$SEL" == *" $caso "* ]] && CASOS+=("$caso")
done < <(grep -v '^#' "$AQUI/casos.txt")
[ ${#CASOS[@]} -ge 1 ] || { echo "ERRO: nenhum caso corresponde a: $*" >&2; exit 1; }

LOG="$AQUI/logs/direto_$(date +%Y%m%d_%H%M%S).log"
echo "casos: ${CASOS[*]}   threads: $J   teste: $TESTE   log: $LOG"
setsid nohup bash -c '
  AQUI=$1; J=$2; TESTE=$3; EXEC=$4; shift 4
  for c in "$@"; do
    echo "[$(date -u +%FT%TZ)] inicio $c"
    OMP_NUM_THREADS=$J TESTE=$TESTE EXEC=$EXEC bash "$AQUI/rodar_caso.sh" "$c" && r=0 || r=$?
    echo "[$(date -u +%FT%TZ)] fim $c rc=$r"
  done
  echo "[$(date -u +%FT%TZ)] fila concluida"
  rm -f "$AQUI/logs/direto.pid"
' _ "$AQUI" "$J" "$TESTE" "$EXEC" "${CASOS[@]}" > "$LOG" 2>&1 < /dev/null &
echo $! > "$PIDF"
echo "rodando em segundo plano (pid $(cat "$PIDF")). Acompanhe: bash rodar_direto.sh estado"
