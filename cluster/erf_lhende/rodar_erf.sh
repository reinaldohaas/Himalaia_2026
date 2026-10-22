#!/bin/bash
# ERF 26.09 no vlab: caso idealizado Lhende/Tsangbu Ri com terreno imerso (gerar_caso_erf.py, LEIA-ME_erf.md).
# Executavel compilado no WSL (gfortran/g++ 13, Open MPI 4.1.6, CPU, sem NetCDF), levado em bin_erf/; roda pelo
# mesmo kit_wrf do WRF (a unica biblioteca que faltava, libmpi_cxx.so.40, vai em bin_erf/lib e e copiada para o kit).
#
#   bash rodar_erf.sh verificar     -> o erf_exec carrega pelo kit? (copia libmpi_cxx.so.40 para o kit se faltar)
#   bash rodar_erf.sh teste         -> 500 m, 10 passos, NP=4, em erf_teste/ (tem de terminar sem erro)
#   bash rodar_erf.sh rodada        -> 200 m, 3 h, NP=80, em segundo plano, em erf_200m/
#   bash rodar_erf.sh estado        -> ultimo passo, tempo de modelo e plotfiles da rodada
# Variaveis: NP (padrao 80 na rodada), KIT_MPI (padrao ./kit_wrf), BIN (padrao ./bin_erf).
set -uo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd); cd "$AQUI"
BIN=${BIN:-$AQUI/bin_erf}
export KIT_MPI=${KIT_MPI:-$AQUI/kit_wrf}
LD="$KIT_MPI/lib/ld-linux-x86-64.so.2 --library-path $KIT_MPI/lib"
LOG="$AQUI/logs/erf.log"; mkdir -p "$AQUI/logs"
msg() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }
falha() { msg "FALHA: $*"; exit 1; }

prepara() {   # prepara <dir> <inputs> <terreno>
  mkdir -p "$1" && cd "$1" || falha "$1"
  cp "$BIN/caso/input_sounding" "$BIN/caso/$2" "$BIN/caso/$3" . || falha "faltam arquivos do caso em $BIN/caso"
}

case "${1:-}" in
  verificar)
    [ -x "$BIN/erf_exec" ] || falha "falta $BIN/erf_exec"
    if [ ! -e "$KIT_MPI/lib/libmpi_cxx.so.40" ]; then
      cp -p "$BIN/lib/libmpi_cxx.so.40" "$KIT_MPI/lib/" && msg "libmpi_cxx.so.40 copiada para o kit (so acrescentada)"
    fi
    n=$($LD --list "$BIN/erf_exec" 2>&1 | grep -c "not found")
    msg "erf_exec: $n bibliotecas faltando pelo kit; sha256 $(sha256sum "$BIN/erf_exec" | cut -c1-16)"
    [ "$n" = 0 ] || { $LD --list "$BIN/erf_exec" 2>&1 | grep "not found"; falha "bibliotecas faltando"; } ;;
  teste)
    ( prepara erf_teste inputs_teste terreno_dx500.txt
      rm -rf plt* chk*
      msg "teste ERF 500 m, 10 passos, NP=4"
      NP=4 OMP_NUM_THREADS=1 BIND=core bash "$AQUI/mpi_kit.sh" "$BIN/erf_exec" inputs_teste > erf.out 2>&1
      grep -q "Coarse STEP 10 ends" erf.out || { tail -20 erf.out; falha "teste ERF (ver erf_teste/erf.out)"; }
      grep -i -E "nan|abort" erf.out | head -3
      msg "teste ERF ok: $(grep "Coarse STEP 10 ends" erf.out)" ) || exit 1 ;;
  rodada)
    NP=${NP:-80}
    prepara erf_200m inputs_vlab terreno_dx200.txt
    [ -d plt00000 ] && falha "erf_200m ja tem saidas (nao sobrescrevo; mova a pasta antes)"
    msg "rodada ERF 200 m, 3 h, NP=$NP, em segundo plano em erf_200m"
    setsid nohup bash -c "NP=$NP OMP_NUM_THREADS=1 BIND=core bash '$AQUI/mpi_kit.sh' '$BIN/erf_exec' inputs_vlab > erf.out 2>&1; echo \"[\$(date -u +%FT%TZ)] rodada ERF terminou: \$(grep 'Coarse STEP' erf.out | tail -1)\" >> '$LOG'" > /dev/null 2>&1 < /dev/null & ;;
  estado)
    cd erf_200m 2>/dev/null || falha "sem erf_200m"
    grep "Coarse STEP" erf.out | tail -1; ls -d plt* 2>/dev/null | tr '\n' ' '; echo
    grep -i -E "nan|abort|error" erf.out | head -3 ;;
  *) echo "uso: bash rodar_erf.sh verificar|teste|rodada|estado" >&2; exit 1 ;;
esac
