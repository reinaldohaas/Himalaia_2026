#!/bin/bash
# Experimento do "modo super-resfriado" no WRF (scripts/toro_wrf/LEIA-ME_toro_wrf.md), no vlab, com dois
# executaveis compilados juntos no WSL (gfortran 13.3, Open MPI 4.1.6, dmpar, sem quimica) e levados em bin_toro/:
#   A = WRF v4.7.1 sem alteracao (real_A.exe, wrf_A.exe)     B = v4.7.1 com o patch toro_wrf (wrf_B.exe)
# Rodam pelo mesmo kit_wrf; tabelas de $WRFDIR/run (mesma versao); met_em de wps_run/ (as mesmas da rodada de 27 h).
#
#   bash rodar_toro_wrf.sh verificar        -> executaveis carregam pelo kit?
#   bash rodar_toro_wrf.sh real             -> real_A.exe em toro_real/
#   bash rodar_toro_wrf.sh teste_bits       -> 30 min (d01+d02) com A (toro_tA/) e com B sem toro_wrf.txt (toro_tB/)
#   bash rodar_toro_wrf.sh teste_ativo      -> 30 min com B e toro_wrf_teste.txt (toro_tBa/): o modulo tem de atuar
#   bash rodar_toro_wrf.sh rodada B|A       -> 27 h em segundo plano: B = experimento (toro_B/), A = controle (toro_A/)
#   bash rodar_toro_wrf.sh teste_bits_C     -> C (patch com o vortice) sem toro_wrf.txt contra A (toro_tC/)
#   bash rodar_toro_wrf.sh teste_ativo_C    -> C com toro_wrf_teste_v.txt (vortice e nucleacao no nucleo, d02)
#   bash rodar_toro_wrf.sh rodada C         -> 27 h: Estado A + vortice dinamico + nucleacao no nucleo (toro_C/)
#   bash rodar_toro_wrf.sh enviar <dir>     -> wrfaux, rsl.error.0000, namelist e toro_wrf.txt ao Drive
# Variaveis: NP (padrao 112), WRFDIR (tabelas), BIN (padrao ./bin_toro).
set -uo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd); cd "$AQUI"
WRFDIR=${WRFDIR:-/home/jovyan/privado/WRF-Chem/WRF}
BIN=${BIN:-$AQUI/bin_toro}
export KIT_MPI=${KIT_MPI:-$AQUI/kit_wrf}
NP=${NP:-112}
LD="$KIT_MPI/lib/ld-linux-x86-64.so.2 --library-path $KIT_MPI/lib"
LOG="$AQUI/logs/toro_wrf.log"; mkdir -p "$AQUI/logs"
msg() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }
falha() { msg "FALHA: $*"; exit 1; }

prepara() {   # prepara <dir>: tabelas, met_em, namelist (com refletividade) e iofields
  mkdir -p "$1" && cd "$1" || falha "$1"
  for f in "$WRFDIR"/run/*; do b=$(basename "$f"); case "$b" in *.exe|namelist*|wrfout*|rsl.*) ;; *) ln -sf "$f" "$b";; esac; done
  ln -sf "$AQUI"/wps_run/met_em.d0* .
  sed -E 's/^( mp_physics +=.*)$/\1\n do_radar_ref             = 1,/' "$AQUI/namelist.input" > namelist.input
  grep -q "do_radar_ref" namelist.input || falha "do_radar_ref nao entrou no namelist"
  cp "$AQUI/iofields_toro.txt" iofields_toro.txt
  rm -f toro_wrf.txt
}

liga_ic() { ln -sf "$AQUI"/toro_real/wrfinput_d0* "$AQUI"/toro_real/wrfbdy_d01 . ; }

curto() {     # curto <exe>: 30 min, d01 + d02
  sed -i -E 's/^( run_hours +=).*/\1 0,/; s/^( run_minutes +=).*/\1 30,/; s/^( max_dom +=).*/\1 2,/' namelist.input
  NP=$NP OMP_NUM_THREADS=1 BIND=core bash "$AQUI/mpi_kit.sh" "$1" > wrf.out 2>&1
  grep -q "SUCCESS COMPLETE WRF" rsl.error.0000 || { tail -20 rsl.error.0000; falha "$(basename "$PWD") (ver rsl.error.0000)"; }
}

case "${1:-}" in
  verificar)
    for e in "$BIN/real_A.exe" "$BIN/wrf_A.exe" "$BIN/wrf_B.exe" "$BIN/wrf_C.exe"; do
      [ -x "$e" ] || falha "falta $e"
      echo "  $(basename "$e"): $( $LD --list "$e" 2>&1 | grep -c 'not found') bibliotecas faltando pelo kit; sha256 $(sha256sum "$e" | cut -c1-16)"
    done
    [ -f "$BIN/toro_wrf.txt" ] && [ -f "$BIN/toro_wrf_teste.txt" ] || falha "faltam toro_wrf.txt / toro_wrf_teste.txt em $BIN"
    ls "$AQUI"/wps_run/met_em.d01.* >/dev/null 2>&1 || falha "faltam os met_em em wps_run/" ;;
  real)
    prepara toro_real
    msg "real_A.exe (NP=16)"; NP=16 OMP_NUM_THREADS=1 BIND=core bash "$AQUI/mpi_kit.sh" "$BIN/real_A.exe" > real.out 2>&1
    grep -q "SUCCESS COMPLETE REAL_EM" rsl.error.0000 || { tail -20 rsl.error.0000; falha "real_A (ver toro_real/rsl.error.0000)"; }
    msg "real_A ok: $(ls wrfinput_d0* wrfbdy_d01 | tr '\n' ' ')" ;;
  teste_bits)
    ( prepara toro_tA; liga_ic; msg "teste A (30 min)"; curto "$BIN/wrf_A.exe"; msg "teste A ok" ) || exit 1
    ( prepara toro_tB; liga_ic; msg "teste B sem toro_wrf.txt (30 min)"; curto "$BIN/wrf_B.exe"; msg "teste B ok" ) || exit 1
    grep -c "toro_wrf" toro_tB/rsl.error.0000 | sed 's/^/  linhas toro_wrf no rsl de B (tem de ser 0): /' ;;
  teste_ativo)
    prepara toro_tBa; liga_ic; cp "$BIN/toro_wrf_teste.txt" toro_wrf.txt
    msg "teste B com o modulo ativo (30 min)"; curto "$BIN/wrf_B.exe"
    grep -m1 "toro_wrf" rsl.error.0000 | sed 's/^/  /'; msg "teste B ativo ok" ;;
  teste_bits_C)   # C (patch com o vortice) sem toro_wrf.txt tem de ser = A (toro_tA/ ja rodado)
    [ -f toro_tA/wrfout_d02_2026-08-25_00:00:00 ] || falha "falta toro_tA (rode teste_bits antes)"
    prepara toro_tC; liga_ic; msg "teste C sem toro_wrf.txt (30 min)"; curto "$BIN/wrf_C.exe"
    for f in wrfout_d01_2026-08-25_00:00:00 wrfout_d02_2026-08-25_00:00:00; do
      cmp -s "$AQUI/toro_tA/$f" "$f" && msg "  $f: C = A byte a byte" || msg "  $f: C DIFERE de A"
    done ;;
  teste_ativo_C)  # C com o vortice e a nucleacao no nucleo ligados (no d02, 30 min)
    prepara toro_tCa; liga_ic; cp "$BIN/toro_wrf_teste_v.txt" toro_wrf.txt
    msg "teste C com vortice ativo (30 min)"; curto "$BIN/wrf_C.exe"
    grep "toro_wrf" rsl.error.0000 | sort | uniq -c | sed 's/^/  /'; msg "teste C ativo ok" ;;
  rodada)
    case "${2:-}" in B) d=toro_B; e=wrf_B.exe ;; A) d=toro_A; e=wrf_A.exe ;; C) d=toro_C; e=wrf_C.exe ;; *) falha "rodada B|A|C" ;; esac
    prepara "$d"; liga_ic
    [ "$2" = B ] && cp "$BIN/toro_wrf.txt" toro_wrf.txt
    [ "$2" = C ] && cp "$BIN/toro_wrf_vortice.txt" toro_wrf.txt
    msg "rodada $2 (27 h, NP=$NP) em segundo plano em $d"
    setsid nohup bash -c "NP=$NP OMP_NUM_THREADS=1 BIND=core bash '$AQUI/mpi_kit.sh' '$BIN/$e' > wrf.out 2>&1; echo \"[\$(date -u +%FT%TZ)] rodada $2 terminou: \$(tail -1 rsl.error.0000)\" >> '$LOG'" > /dev/null 2>&1 < /dev/null & ;;
  enviar)
    export RCLONE_CONFIG=${RCLONE_CONFIG:-/home/jovyan/privado/.config/rclone/rclone.conf}
    command -v rclone >/dev/null || export PATH="/home/jovyan/privado/conda_envs/cm1pos/bin:$PATH"
    d=${2:?dir}; dst=gdrive:vlab_cache/Himalaia_2026/saida/wrf_lhende/$d
    for f in "$AQUI/$d"/wrfaux_d0* "$AQUI/$d"/rsl.error.0000 "$AQUI/$d"/namelist.input "$AQUI/$d"/toro_wrf.txt "$LOG"; do
      [ -f "$f" ] && rclone copy "$f" "$dst/" 2>&1 | grep -v client_id
    done
    msg "enviado ao Drive: $dst" ;;
  *) echo "uso: bash rodar_toro_wrf.sh verificar|real|teste_bits|teste_ativo|teste_bits_C|teste_ativo_C|rodada B|A|C|enviar <dir>" >&2; exit 1 ;;
esac
