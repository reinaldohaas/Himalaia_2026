#!/bin/bash
# Experimentos do "toro" no vlab: CM1 com toro_mod (anti-coalescencia de Tinsley + vortice), MPI 16 x 7,
# kit kit_mpi_toro (mesmas bibliotecas do kit_mpi validado; so o executavel muda: 35f045c9...).
#
#   bash rodar_toro.sh tudo     -> em segundo plano, na ordem, parando na primeira falha:
#        1. VALIDACAO: rad_06utc_2h com o executavel novo e SEM toro_params.txt; tem de ser bit a bit
#           identica a execucoes/rad_06utc_repro (exceto z0t/z0q). Se nao for, nada mais roda.
#        2. TESTE CURTO (120 s) com tudo ligado (anti-coalescencia modo 2 + vortice desde t=0): o modelo
#           tem de terminar normalmente e imprimir "TORO: ... LIGADO".
#        3. os experimentos de experimentos_toro/ (ordem de EXPS abaixo), cada um a partir de casos/rad_06utc
#           com tapfrq = 900 s; cada um tem de imprimir "TORO: ... LIGADO".
#        4. diagnostico (diag_toro.py) de cada experimento e do controle; tudo para o Drive.
#   bash rodar_toro.sh estado   -> onde esta
#   bash rodar_toro.sh diag     -> so o diagnostico e o envio
# Log: logs/toro_tudo.log ; resultados: gdrive:vlab_cache/Himalaia_2026/saida/toro_cm1_lhende/toro/
set -uo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
cd "$AQUI"
export KIT_MPI=${KIT_MPI:-$AQUI/kit_mpi_toro}          # outro kit: KIT_MPI=.../kit_mpi_toro2
EXPS=${EXPS:-"toro_A_rev_vort toro_Ag_vort toro_vort toro_A toro_A_rev toro_Ag"}
VALIDA_EXP=${VALIDA_EXP:-}     # ex.: toro_Ag -> 2 h com o executavel novo tem de ser bit a bit execucoes/toro_Ag
DIAG_EXTRA=${DIAG_EXTRA:-}     # rodadas ja existentes que entram no resumo (ex.: toro_Ag)
PY=python3; [ -x /home/jovyan/privado/conda_envs/cm1pos/bin/python3 ] && PY=/home/jovyan/privado/conda_envs/cm1pos/bin/python3
export RCLONE_CONFIG=${RCLONE_CONFIG:-/home/jovyan/privado/.config/rclone/rclone.conf}
DRIVE=gdrive:vlab_cache/Himalaia_2026/saida/toro_cm1_lhende/toro
LOG="$AQUI/logs/toro_tudo.log"
mkdir -p "$AQUI/logs"
msg() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }
envia() { command -v rclone >/dev/null && rclone copy "$1" "$DRIVE/" 2>&1 | grep -v client_id >> "$LOG"; }

espera_fila() {   # espera a fila do rodar_direto.sh terminar
  sleep 20
  # grep sem -q: le a saida toda (com pipefail, o -q fecharia o pipe e o laco nunca terminaria)
  while ! bash rodar_direto.sh estado 2>/dev/null | grep "nenhuma fila rodando" >/dev/null; do sleep 30; done
}

prepara_caso() {  # prepara_caso <nome> <base> <toro_params ou vazio> <tapfrq ou vazio>
  local nome=$1 base=$2 par=$3 tap=$4
  rm -rf "casos/$nome"; cp -r "casos/$base" "casos/$nome"
  [ -n "$tap" ] && sed -i -E "s/^( tapfrq +=).*/\1 $tap,/" "casos/$nome/namelist.input"
  [ -n "$par" ] && cp "$par" "casos/$nome/toro_params.txt"
  grep -q "^$nome " casos.txt || printf '%-27s %-8s %4s  %-11s  %-4s %s\n' "$nome" toro 16 04:00:00 8G "experimento do toro (rodar_toro.sh)" >> casos.txt
}

roda() {          # roda <caso> [TESTE]  (16 x 7, kit_mpi_toro)
  local caso=$1 teste=${2:-0}
  export NP=16 EXE_ALT="$KIT_MPI/cm1.exe" SUFIXO="" CM1_RUNNER="bash $AQUI/mpi_kit.sh" BIND=core FORCAR=1
  TESTE=$teste bash rodar_direto.sh -j 7 $( [ "$teste" = 1 ] && echo -t ) "$caso" >> "$LOG" 2>&1
  espera_fila
}

ok_rodada() {     # ok_rodada <dir> [exigir_toro]
  grep -q "Program terminated normally" "$1/cm1.print.out" || { msg "FALHA: $1 nao terminou normalmente"; return 1; }
  if [ "${2:-0}" = 1 ]; then grep -q "TORO: toro_params.txt lido -- experimento LIGADO" "$1/cm1.print.out" \
      || { msg "FALHA: $1 nao leu toro_params.txt (o experimento teria virado controle)"; return 1; }; fi
  return 0
}

diag_tudo() {
  for e in rad_06utc_hib16x7 $DIAG_EXTRA $EXPS; do
    d=execucoes/$e; [ -f "$d/cm1out_s.dat" ] || continue
    "$PY" diag_toro.py "$d" 6 "logs/diag_$e" "$e" >> "$LOG" 2>&1 && { envia "logs/diag_$e.json"; envia "logs/diag_$e.txt"; msg "diagnostico $e enviado"; } \
      || msg "AVISO: diagnostico de $e falhou (ver $LOG)"
  done
  "$PY" diag_toro.py --tabela logs/diag_ > logs/toro_resumo.txt 2>>"$LOG" && envia logs/toro_resumo.txt && msg "resumo enviado: toro/toro_resumo.txt"
}

tudo_fg() {
  msg "=== inicio (kit $KIT_MPI) ==="
  ( cd "$KIT_MPI" && sha256sum -c --quiet MANIFESTO_kit.sha256 ) || { msg "FALHA: kit_mpi_toro corrompido"; exit 1; }
  ln -sfn "$KIT_MPI/pmix2" /tmp/.kit_mpi_cm1_lhende_pmix_2
  # 1. validacao
  [ -d casos/rad_06utc_2h ] || { msg "FALHA: falta casos/rad_06utc_2h"; exit 1; }
  prepara_caso toro_validar rad_06utc_2h "" ""
  rm -rf execucoes/toro_validar; roda toro_validar
  ok_rodada execucoes/toro_validar || exit 1
  if grep -q "TORO: toro_params.txt lido" execucoes/toro_validar/cm1.print.out; then msg "FALHA: validacao leu toro_params.txt"; exit 1; fi
  "$PY" comparar_bits.py execucoes/toro_validar execucoes/rad_06utc_repro > logs/toro_validacao.txt 2>&1
  rcv=$?; envia logs/toro_validacao.txt
  [ $rcv -eq 0 ] || { msg "FALHA: o executavel novo SEM toro_params.txt NAO reproduz a rad_06utc_repro (ver logs/toro_validacao.txt). Parei."; exit 1; }
  msg "validacao OK: executavel do toro desligado = bit a bit a rad_06utc_repro (2 h)"
  if [ -n "$VALIDA_EXP" ]; then   # 1b. o executavel novo reproduz um experimento anterior (o codigo novo e inerte)
    prepara_caso toro_valida_exp rad_06utc_2h "experimentos_toro/$VALIDA_EXP.txt" 900.0
    rm -rf execucoes/toro_valida_exp; roda toro_valida_exp
    ok_rodada execucoes/toro_valida_exp 1 || exit 1
    "$PY" comparar_bits.py execucoes/toro_valida_exp "execucoes/$VALIDA_EXP" > logs/toro_validacao_exp.txt 2>&1
    rcv=$?; envia logs/toro_validacao_exp.txt
    [ $rcv -eq 0 ] || { msg "FALHA: o executavel novo NAO reproduz $VALIDA_EXP nas 2 h (ver logs/toro_validacao_exp.txt). Parei."; exit 1; }
    msg "validacao 1b OK: executavel novo = bit a bit $VALIDA_EXP (2 h)"
  fi
  # 2. teste curto com tudo ligado
  prepara_caso toro_teste rad_06utc experimentos_toro/toro_teste_curto.txt ""
  rm -rf execucoes/toro_teste_teste; roda toro_teste 1
  ok_rodada execucoes/toro_teste_teste 1 || exit 1
  msg "teste curto OK (toro ligado, vortice e anti-coalescencia, 120 s)"
  # 3. experimentos
  for e in $EXPS; do
    prepara_caso "$e" rad_06utc "experimentos_toro/$e.txt" 900.0
    rm -rf "execucoes/$e"; msg "rodando $e"; roda "$e"
    ok_rodada "execucoes/$e" 1 || { msg "pulando o diagnostico de $e"; continue; }
    msg "$e concluido"
    "$PY" diag_toro.py "execucoes/$e" 6 "logs/diag_$e" "$e" >> "$LOG" 2>&1 && { envia "logs/diag_$e.json"; envia "logs/diag_$e.txt"; }
  done
  # 4. diagnostico final (inclui o controle) e resumo
  diag_tudo
  envia "$LOG"
  msg "=== fim ==="
}

case "${1:-}" in
  tudo)
    pgrep -f "rodar_toro.sh tudo_fg" >/dev/null && { echo "ja esta rodando (bash rodar_toro.sh estado)"; exit 0; }
    setsid nohup bash "$AQUI/rodar_toro.sh" tudo_fg > /dev/null 2>&1 < /dev/null &
    echo "rodar_toro iniciado em segundo plano; acompanhe: bash rodar_toro.sh estado  (log: logs/toro_tudo.log)" ;;
  tudo_fg) tudo_fg ;;
  diag) diag_tudo ;;
  estado) tail -15 "$LOG" 2>/dev/null; bash rodar_direto.sh estado 2>/dev/null | grep -E "RODANDO|toro|nenhuma" | head -12 ;;
  *) echo "uso: bash rodar_toro.sh tudo|estado|diag" >&2; exit 1 ;;
esac
