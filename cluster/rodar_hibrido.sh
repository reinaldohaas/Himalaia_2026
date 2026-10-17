#!/bin/bash
# Teste hibrido MPI x OpenMP no vlab: rad_06utc nas 2 primeiras horas, NP ranks x T threads, com o kit_mpi
# (executavel hibrido + OpenMPI 4.1.6 + glibc do computador de referencia, tudo pelo carregador do kit).
# Depois compara, byte a byte e variavel a variavel, com execucoes/rad_06utc_repro (a reproducao no vlab
# que ja e identica a referencia local).
#
# Ja verificado no computador de referencia: 16 ranks x 1 thread (decomposicao 4x4) da campos identicos
# byte a byte aos da referencia OpenMP de 8 threads; so os diagnosticos z0t/z0q diferem (memoria nao
# inicializada; nao realimentam). O cm1out_stats.dat NAO serve para comparar MPI: as medias do dominio
# somam por rank (outra ordem de soma).
#
# Uso:  bash rodar_hibrido.sh                 (16 x 7, padrao)
#       NP=16 T=7 bash rodar_hibrido.sh
#       TESTE=1 bash rodar_hibrido.sh         (120 s de modelo, para ver se o kit sobe)
#       bash rodar_hibrido.sh comparar        (so a comparacao, depois que a rodada terminar)
#       CASO=rad_06utc bash rodar_hibrido.sh  (rodada COMPLETA, 21 h; compara as 43 saidas)
#       CASO=rad_06utc bash rodar_hibrido.sh comparar
#       bash rodar_direto.sh estado           (acompanhar)
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
NP=${NP:-16}; T=${T:-7}
CASO=${CASO:-rad_06utc_2h}                     # rad_06utc_2h (teste de 2 h) ou rad_06utc (21 h)
case "$CASO" in rad_06utc_2h|rad_06utc) ;; *) echo "ERRO: CASO deve ser rad_06utc_2h ou rad_06utc" >&2; exit 1;; esac
NOME=${CASO}_hib${NP}x${T}
REF="$AQUI/execucoes/rad_06utc_repro"
PY=$(command -v python3 || true)
[ -x /home/jovyan/privado/conda_envs/cm1pos/bin/python3 ] && PY=/home/jovyan/privado/conda_envs/cm1pos/bin/python3

if [ "${1:-}" = "comparar" ]; then
  D="$AQUI/execucoes/$NOME"
  grep -q "Program terminated normally" "$D/cm1.print.out" || { echo "ERRO: $D ainda nao terminou (ou falhou)" >&2; exit 1; }
  [ -f "$REF/cm1out_s.dat" ] || { echo "ERRO: falta a reproducao $REF" >&2; exit 1; }
  mkdir -p "$AQUI/logs"
  "$PY" "$AQUI/comparar_bits.py" "$D" "$REF" | tee "$AQUI/logs/comparacao_${NOME}.txt"
  rc=${PIPESTATUS[0]}
  export RCLONE_CONFIG=${RCLONE_CONFIG:-/home/jovyan/privado/.config/rclone/rclone.conf}
  if command -v rclone >/dev/null && rclone copy "$AQUI/logs/comparacao_${NOME}.txt" gdrive:vlab_cache/Himalaia_2026/saida/toro_cm1_lhende/relatorios/ 2>/dev/null; then
    echo "comparacao enviada ao Drive: relatorios/comparacao_${NOME}.txt"
  else echo "AVISO: nao consegui enviar a comparacao ao Drive (rode: source restaurar.sh e repita)"; fi
  exit "$rc"
fi

K="$AQUI/kit_mpi"
[ -f "$K/cm1.exe" ] || { echo "ERRO: falta $K (extraia kit_mpi_hibrido.tar.gz aqui)" >&2; exit 1; }
( cd "$K" && sha256sum -c --quiet MANIFESTO_kit.sha256 ) || { echo "ERRO: kit_mpi corrompido (sha256)" >&2; exit 1; }
if [ "$CASO" = rad_06utc_2h ]; then
[ -d "$AQUI/casos/rad_06utc_2h" ] || { cp -r "$AQUI/casos/rad_06utc" "$AQUI/casos/rad_06utc_2h"
  sed -i -E 's/^( timax +=).*/\1 7200.0,/' "$AQUI/casos/rad_06utc_2h/namelist.input"; }
grep -q "timax *= *7200.0" "$AQUI/casos/rad_06utc_2h/namelist.input" || { echo "ERRO: casos/rad_06utc_2h sem timax 7200" >&2; exit 1; }
# o rodar_direto.sh so aceita casos do casos.txt; grupo proprio ("teste") para nao entrar no grupo "rad"
grep -q "^rad_06utc_2h " "$AQUI/casos.txt" || \
  printf '%-27s %-8s %4s  %-11s  %-4s %s\n' rad_06utc_2h teste 16 04:00:00 8G "teste hibrido: rad_06utc so 2 h (rodar_hibrido.sh)" >> "$AQUI/casos.txt"
fi

mkdir -p "$AQUI/logs"
NC=$(nproc)
[ "$NC" -lt $((NP * T)) ] && echo "AVISO: $NC nucleos visiveis < $NP x $T = $((NP * T)); vai rodar, mas mais devagar (o resultado nao muda)"
# teste rapido do lancador: com amarracao a nucleos; se o conteiner nao deixar, sem amarracao
export BIND=core
if ! NP=$NP OMP_NUM_THREADS=$T timeout 60 bash "$AQUI/mpi_kit.sh" /bin/true >/dev/null 2>"$AQUI/logs/mpi_teste_bind.err"; then
  echo "AVISO: amarracao a nucleos falhou (ver logs/mpi_teste_bind.err); usando BIND=none"; export BIND=none
  NP=$NP OMP_NUM_THREADS=$T timeout 60 bash "$AQUI/mpi_kit.sh" /bin/true >/dev/null 2>"$AQUI/logs/mpi_teste_nobind.err" \
    || { echo "ERRO: o orterun do kit nao sobe (ver logs/mpi_teste_nobind.err)" >&2; exit 1; }
fi
{
  echo "hibrido  $(date -u +%FT%TZ)  host=$(hostname)  caso=$CASO  NP=$NP  T=$T  BIND=$BIND  nucleos=$NC  teste=${TESTE:-0}"
  echo "exe: $(sha256sum "$K/cm1.exe")"
  cat "$K/KIT.info"
  lscpu 2>/dev/null | grep -E "Model name|Socket|Thread|Core" || true
} | tee "$AQUI/logs/hibrido_${NOME}.info"
export NP EXE_ALT="$K/cm1.exe" SUFIXO=_hib${NP}x${T} CM1_RUNNER="bash $AQUI/mpi_kit.sh"
TESTE=${TESTE:-0} bash "$AQUI/rodar_direto.sh" -j "$T" $( [ "${TESTE:-0}" = 1 ] && echo -t ) "$CASO"
echo "Quando terminar:  CASO=$CASO bash rodar_hibrido.sh comparar"
