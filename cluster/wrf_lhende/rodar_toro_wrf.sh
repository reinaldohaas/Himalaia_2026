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
#   bash rodar_toro_wrf.sh teste_bits_D     -> D (nucleacao no nucleo so onde w > w_crit) sem toro_wrf.txt contra A
#   bash rodar_toro_wrf.sh teste_ativo_D    -> D com toro_wrf_teste_vD.txt (limiar baixo, d02): o disparo tem de aparecer
#   bash rodar_toro_wrf.sh rodada D         -> 27 h: como C, mas o nucleo so nucleia onde a ascendente chega (toro_D/)
#   (os passos de D recusam rodar enquanto a rodada C estiver em andamento)
#   bash rodar_toro_wrf.sh teste_unico      -> executavel UNICO (wrf_toro.exe): A, B, C e D escolhidos pelo grupo
#                                              &toro_wrf no namelist.input; 4 testes de 30 min comparados byte a byte
#                                              com toro_tA, toro_tBa, toro_tCa e toro_tDa
#   bash rodar_toro_wrf.sh rodada_u A|B|C|D -> 27 h com o executavel unico (toro_uX/)
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

espera_C() {  # D so depois que a rodada C terminar (o host e o mesmo)
  pgrep -f "wrf_C.exe" > /dev/null && falha "a rodada C ainda esta em andamento; D so depois que ela terminar"
  grep -q "SUCCESS COMPLETE WRF" "$AQUI/toro_C/rsl.error.0000" 2>/dev/null || msg "aviso: toro_C/rsl.error.0000 nao tem SUCCESS COMPLETE WRF"
}

grupo() {     # grupo <arquivo de configuracao>: acrescenta o grupo &toro_wrf ao namelist.input da rodada
  [ -f "$BIN/$1" ] || falha "falta $BIN/$1"
  { echo; cat "$BIN/$1"; } >> namelist.input
  grep -q "^&toro_wrf" namelist.input || falha "o grupo &toro_wrf nao entrou no namelist.input"
}

cfg_u() {     # configuracao de cada experimento no executavel unico
  case "$1" in B) echo toro_wrf.txt ;; C) echo toro_wrf_vortice_C.txt ;; D) echo toro_wrf_vortice_D.txt ;;
               E) echo toro_wrf_vortice_E.txt ;; E2) echo toro_wrf_vortice_E2.txt ;; esac
}

liga_ic() { ln -sf "$AQUI"/toro_real/wrfinput_d0* "$AQUI"/toro_real/wrfbdy_d01 . ; }

curto() {     # curto <exe>: 30 min, d01 + d02
  sed -i -E 's/^( run_hours +=).*/\1 0,/; s/^( run_minutes +=).*/\1 30,/; s/^( max_dom +=).*/\1 2,/' namelist.input
  NP=$NP OMP_NUM_THREADS=1 BIND=core bash "$AQUI/mpi_kit.sh" "$1" > wrf.out 2>&1
  grep -q "SUCCESS COMPLETE WRF" rsl.error.0000 || { tail -20 rsl.error.0000; falha "$(basename "$PWD") (ver rsl.error.0000)"; }
}

case "${1:-}" in
  verificar)
    for e in "$BIN/real_A.exe" "$BIN/wrf_A.exe" "$BIN/wrf_B.exe" "$BIN/wrf_C.exe" "$BIN/wrf_D.exe"; do
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
  teste_bits_C|teste_bits_D)   # C ou D sem toro_wrf.txt tem de ser = A (toro_tA/ ja rodado)
    x=${1#teste_bits_}; [ "$x" = D ] && espera_C
    [ -f toro_tA/wrfout_d02_2026-08-25_00:00:00 ] || falha "falta toro_tA (rode teste_bits antes)"
    prepara toro_t$x; liga_ic; msg "teste $x sem toro_wrf.txt (30 min)"; curto "$BIN/wrf_$x.exe"
    for f in wrfout_d01_2026-08-25_00:00:00 wrfout_d02_2026-08-25_00:00:00; do
      cmp -s "$AQUI/toro_tA/$f" "$f" && msg "  $f: $x = A byte a byte" || msg "  $f: $x DIFERE de A"
    done ;;
  teste_ativo_C|teste_ativo_D)  # C ou D com o vortice e a nucleacao no nucleo ligados (no d02, 30 min)
    x=${1#teste_ativo_}; [ "$x" = D ] && espera_C
    t=toro_wrf_teste_v.txt; [ "$x" = D ] && t=toro_wrf_teste_vD.txt
    prepara toro_t${x}a; liga_ic; cp "$BIN/$t" toro_wrf.txt
    msg "teste $x com vortice ativo (30 min)"; curto "$BIN/wrf_$x.exe"
    grep "toro_wrf" rsl.error.0000 | sort | uniq -c | sed 's/^/  /'
    if [ "$x" = D ]; then   # o aviso sai no rsl.error do processo que tem o nucleo
      n=$(grep -l "nucleacao no nucleo disparada" rsl.error.* 2>/dev/null | wc -l)
      [ "$n" -gt 0 ] && msg "  D: disparo registrado em $n processo(s)" || msg "  D: nenhum disparo registrado em 30 min"
    fi
    msg "teste $x ativo ok" ;;
  teste_unico)  # o executavel unico tem de reproduzir os quatro testes ja feitos com os executaveis A, B, C e D
    e="$BIN/wrf_toro.exe"; [ -x "$e" ] || falha "falta $e"
    for par in "A:toro_tA:" "B:toro_tBa:toro_wrf_teste.txt" "C:toro_tCa:toro_wrf_teste_vC.txt" "D:toro_tDa:toro_wrf_teste_vD.txt"; do
      x=${par%%:*}; r=${par#*:}; ref=${r%%:*}; cfg=${r#*:}
      [ -f "$AQUI/$ref/wrfout_d02_2026-08-25_00:00:00" ] || { msg "  $x: falta $ref (referencia), pulado"; continue; }
      ( prepara toro_tU$x; liga_ic; [ -n "$cfg" ] && grupo "$cfg"
        msg "teste unico $x (30 min)"; curto "$e" ) || exit 1
      for f in wrfout_d01_2026-08-25_00:00:00 wrfout_d02_2026-08-25_00:00:00; do
        cmp -s "$AQUI/$ref/$f" "$AQUI/toro_tU$x/$f" && msg "  $x $f: unico = $ref byte a byte" || msg "  $x $f: unico DIFERE de $ref"
      done
      grep -h "toro_wrf" "$AQUI"/toro_tU$x/rsl.error.* 2>/dev/null | sort | uniq -c | sed 's/^/    /'
    done ;;
  teste_ativo_u)  # teste ativo de 30 min com o executavel unico: teste_ativo_u E (vortice em niveis medios, faixa de T)
    x=${2:-E}; e="$BIN/wrf_toro.exe"; [ -x "$e" ] || falha "falta $e"
    ( prepara toro_tU${x}a; liga_ic; grupo toro_wrf_teste_v$x.txt
      msg "teste ativo $x com o executavel unico (30 min)"; curto "$e" ) || exit 1
    grep -h "toro_wrf" "$AQUI"/toro_tU${x}a/rsl.error.* 2>/dev/null | sort | uniq -c | sed 's/^/    /'
    for f in wrfout_d02_2026-08-25_00:00:00; do
      cmp -s "$AQUI/toro_tDa/$f" "$AQUI/toro_tU${x}a/$f" && msg "  $x $f: IGUAL a toro_tDa (o perfil/faixa novos nao atuaram?)" \
        || msg "  $x $f: difere de toro_tDa (esperado)"
    done ;;
  rodada_u)
    x=${2:-}; case "$x" in A|B|C|D|E|E2) ;; *) falha "rodada_u A|B|C|D|E|E2" ;; esac
    e="$BIN/wrf_toro.exe"; [ -x "$e" ] || falha "falta $e"
    d=toro_u$x; prepara "$d"; liga_ic; c=$(cfg_u "$x"); [ -n "$c" ] && grupo "$c"
    msg "rodada_u $x (27 h, NP=$NP, executavel unico) em segundo plano em $d"
    setsid nohup bash -c "NP=$NP OMP_NUM_THREADS=1 BIND=core bash '$AQUI/mpi_kit.sh' '$e' > wrf.out 2>&1; echo \"[\$(date -u +%FT%TZ)] rodada_u $x terminou: \$(tail -1 rsl.error.0000)\" >> '$LOG'" > /dev/null 2>&1 < /dev/null & ;;
  rodada)
    case "${2:-}" in B) d=toro_B; e=wrf_B.exe ;; A) d=toro_A; e=wrf_A.exe ;; C) d=toro_C; e=wrf_C.exe ;; D) d=toro_D; e=wrf_D.exe ;; *) falha "rodada B|A|C|D" ;; esac
    [ "$2" = D ] && espera_C
    prepara "$d"; liga_ic
    [ "$2" = B ] && cp "$BIN/toro_wrf.txt" toro_wrf.txt
    [ "$2" = C ] && cp "$BIN/toro_wrf_vortice.txt" toro_wrf.txt
    [ "$2" = D ] && cp "$BIN/toro_wrf_vortice_D.txt" toro_wrf.txt
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
  *) echo "uso: bash rodar_toro_wrf.sh verificar|real|teste_bits|teste_ativo|teste_bits_C|teste_ativo_C|teste_bits_D|teste_ativo_D|teste_unico|teste_ativo_u E|rodada B|A|C|D|rodada_u A|B|C|D|E|enviar <dir>" >&2; exit 1 ;;
esac
