#!/bin/bash
# Experimento definitivo no d03 (1 km), em ensemble (scripts/toro_wrf/LEIA-ME_toro_wrf.md, secao "Ensemble no d03"):
# 4 bracos x 5 membros com o executavel unico v4.2 (bin_toro/wrf_toro.exe, max_dom = 3). Os membros diferem pelo SKEBS
# no d01 e no d02 (nens = membro); a mesma semente nos quatro bracos, para comparar por pares.
#   A  = sem grupo &toro_wrf (controle)          S  = Estado A de 17 UTC ao fim, sem liberacao (toro_wrf_ens_S.txt)
#   E2 = Estado A + vortice na frente de gelo e disparo com -8 < T < -3 C (toro_wrf_vortice_E2.txt)
#   R  = Estado A ate 23:30 e liberacao por aerossol na frente ate 00:30 (toro_wrf_ens_R.txt)
#   E3 = vortice do E2 + injecao de nucleos de glaciacao no reservatorio as 00:00-00:30 e fisica do NSSL no nucleo
#        (toro_wrf_ens_E3.txt; modulo toro_wrf 4.3 em BIN_E3, padrao ./bin_toro_v43)
#
#   bash rodar_ensemble_d03.sh verificar   -> executavel, configuracoes, nomes do &stoch no Registry, disco (nao roda nada)
#   bash rodar_ensemble_d03.sh teste       -> 30 min (d01+d02): A1, S1 e A2; A1 = S1 byte a byte, A1 /= A2, A1 /= toro_tA
#   bash rodar_ensemble_d03.sh fila        -> em segundo plano, em sequencia, o que falta: membro 1 dos 4 bracos, depois o 2...
#   BRACOS="A S R" ESPERAR=1 bash rodar_ensemble_d03.sh fila -> so esses bracos; espera o host ficar livre em vez de recusar
#   bash rodar_ensemble_d03.sh estado      -> tabela braco x membro
# Variaveis: NP (padrao 112), WRFDIR (tabelas), BIN (padrao ./bin_toro), MEMBROS (padrao "1 2 3 4 5"), BRACOS (padrao "A S E2 R"),
#   ESPERAR (1 = a fila espera o WRF/real em curso terminar).
# O E2 saiu dos membros 2-5 em 01/11/2026: com os padroes do NSSL (icenucopt = 1, imeyers5 = .false., nsplinter = 0) o fnuc_v e o
#   fhm_v multiplicam termos nulos entre -3 e -5 C (relatorios/toro_wrf/ens_d03/leitura_disparo_nssl_20261101.txt).
set -uo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd); cd "$AQUI"
WRFDIR=${WRFDIR:-/home/jovyan/privado/WRF-Chem/WRF}
BIN=${BIN:-$AQUI/bin_toro}
BIN_E3=${BIN_E3:-$AQUI/bin_toro_v43}   # modulo toro_wrf 4.3 (injecao de nucleos)
export KIT_MPI=${KIT_MPI:-$AQUI/kit_wrf}
NP=${NP:-112}
MEMBROS=${MEMBROS:-"1 2 3 4 5"}
BRACOS=${BRACOS:-"A S E2 R"}
ENS="$AQUI/ens_d03"
EXE="$BIN/wrf_toro.exe"
LOG="$AQUI/logs/ensemble_d03.log"; mkdir -p "$AQUI/logs" "$ENS"
msg() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }
falha() { msg "FALHA: $*"; exit 1; }

cfg() { case "$1" in A) echo "" ;; S) echo toro_wrf_ens_S.txt ;; E2) echo toro_wrf_vortice_E2.txt ;; R) echo toro_wrf_ens_R.txt ;;
                     E3) echo toro_wrf_ens_E3.txt ;; esac; }
bin_de() { [ "$1" = E3 ] && echo "$BIN_E3" || echo "$BIN"; }   # pasta do executavel e da configuracao do braco

prepara() {   # prepara <dir> <braco> <membro>: tabelas, met_em, condicoes iniciais, namelist com &stoch e o grupo do braco
  mkdir -p "$1" && cd "$1" || falha "$1"
  local f b c   # sem o local, o b do laco das tabelas sobrescrevia o braco do chamador (so nas mensagens do log)
  for f in "$WRFDIR"/run/*; do b=$(basename "$f"); case "$b" in *.exe|namelist*|wrfout*|rsl.*) ;; *) ln -sf "$f" "$b";; esac; done
  ln -sf "$AQUI"/wps_run/met_em.d0* .
  ln -sf "$AQUI"/toro_real/wrfinput_d0* "$AQUI"/toro_real/wrfbdy_d01 .
  sed -E 's/^( mp_physics +=.*)$/\1\n do_radar_ref             = 1,/' "$AQUI/namelist.input" > namelist.input
  grep -q "do_radar_ref" namelist.input || falha "do_radar_ref nao entrou no namelist"
  # SKEBS no d01 e no d02 (o d03 recebe a perturbacao pela fronteira); o grupo entra antes de &bdy_control
  sed -i -E "s/^ &bdy_control/ \&stoch\n skebs                    = 1,    1,    0,\n nens                     = $3,\n skebs_vertstruc          = 1,\n \/\n\n \&bdy_control/" namelist.input
  grep -q "^ nens *= *$3," namelist.input || falha "o grupo &stoch nao entrou no namelist"
  cp "$AQUI/iofields_toro.txt" iofields_toro.txt
  rm -f toro_wrf.txt
  c=$(cfg "$2")
  if [ -n "$c" ]; then
    [ -f "$(bin_de "$2")/$c" ] || falha "falta $(bin_de "$2")/$c"
    { echo; cat "$(bin_de "$2")/$c"; } >> namelist.input
    grep -q "^&toro_wrf" namelist.input || falha "o grupo &toro_wrf nao entrou no namelist"
  fi
}

ocupado() { pgrep -f "wrf.*\.exe|real.*\.exe" > /dev/null; }

lanca() {     # lanca [exe]: roda o exe no diretorio atual, com ate 5 partidas (o orterun as vezes cai antes do 1o passo)
  local e=${1:-$EXE}
  for p in 1 2 3 4 5; do
    NP=$NP OMP_NUM_THREADS=1 BIND=core bash "$AQUI/mpi_kit.sh" "$e" > wrf.out 2>&1
    grep -q "Timing for main" rsl.error.0000 2>/dev/null && return 0
    msg "  $(basename "$PWD"): partida $p falhou antes do 1o passo ($(grep -c tcache wrf.out 2>/dev/null) linhas tcache)"
    mkdir -p falhas_partida/p$p; mv -f rsl.* wrf.out falhas_partida/p$p/ 2>/dev/null; sleep 20
  done
  return 1
}

case "${1:-}" in
  verificar)
    [ -x "$EXE" ] || falha "falta $EXE"; echo "  wrf_toro.exe sha256 $(sha256sum "$EXE" | cut -c1-16) (esperado 478962a3c4965b95)"
    for b in S E2 R; do [ -f "$BIN/$(cfg $b)" ] && echo "  $b: $(cfg $b) ok" || falha "falta $BIN/$(cfg $b)"; done
    if [ -x "$BIN_E3/wrf_toro.exe" ]; then
      echo "  E3: $BIN_E3/wrf_toro.exe sha256 $(sha256sum "$BIN_E3/wrf_toro.exe" | cut -c1-16); $(cfg E3) $([ -f "$BIN_E3/$(cfg E3)" ] && echo ok || echo FALTA)"
    else echo "  E3: sem $BIN_E3/wrf_toro.exe (modulo 4.3 ainda nao instalado)"; fi
    ls "$AQUI"/toro_real/wrfinput_d01 "$AQUI"/toro_real/wrfbdy_d01 > /dev/null || falha "faltam as condicoes iniciais em toro_real/"
    R="$WRFDIR/Registry"
    echo "  nomes do &stoch no Registry (skebs, nens, skebs_vertstruc tem de aparecer):"
    grep -h -i -E "^rconfig .*(skebs|nens|skebs_vertstruc) " "$R"/registry.stoch 2>/dev/null | awk '{print "    " $3, $4, $5, $6}'
    echo "  disco:"; df -h "$AQUI" | tail -1 | sed 's/^/    /'
    for d in toro_uE2 toro_D toro_A; do [ -d "$AQUI/$d" ] && echo "    uma rodada de 27 h ($d): $(du -sh "$AQUI/$d" | cut -f1)" && break; done ;;
  teste)
    ocupado && falha "ha WRF/real rodando; o teste espera o host livre"
    [ -f "$AQUI/toro_tA/wrfout_d02_2026-08-25_00:00:00" ] || falha "falta toro_tA (referencia sem SKEBS)"
    for par in A:1 S:1 A:2; do
      b=${par%%:*}; m=${par#*:}; d="$ENS/teste_${b}${m}"
      ( prepara "$d" "$b" "$m"
        sed -i -E 's/^( run_hours +=).*/\1 0,/; s/^( run_minutes +=).*/\1 30,/; s/^( max_dom +=).*/\1 2,/' namelist.input
        msg "teste $b membro $m (30 min, d01+d02)"; lanca || falha "teste $b$m nao partiu"
        grep -q "SUCCESS COMPLETE WRF" rsl.error.0000 || { tail -20 rsl.error.0000; falha "teste $b$m (ver rsl.error.0000)"; } ) || exit 1
    done
    for f in wrfout_d01_2026-08-25_00:00:00 wrfout_d02_2026-08-25_00:00:00; do
      cmp -s "$ENS/teste_A1/$f" "$ENS/teste_S1/$f" && msg "  $f: A1 = S1 byte a byte (esperado)" || msg "  $f: A1 DIFERE de S1 (NAO esperado)"
      cmp -s "$ENS/teste_A1/$f" "$ENS/teste_A2/$f" && msg "  $f: A1 = A2 (NAO esperado: o nens nao mudou nada)" || msg "  $f: A1 difere de A2 (esperado)"
      cmp -s "$ENS/teste_A1/$f" "$AQUI/toro_tA/$f" && msg "  $f: A1 = toro_tA (NAO esperado: o SKEBS nao atuou)" || msg "  $f: A1 difere de toro_tA (esperado)"
    done
    grep -h -i -E "skebs|stoch" "$ENS"/teste_A1/rsl.error.0000 | sort | uniq -c | head -5 | sed 's/^/    /' ;;
  fila)
    espera=""
    if ocupado; then
      [ "${ESPERAR:-0}" = 1 ] || falha "ha WRF/real rodando; a fila espera o host livre (ou ESPERAR=1)"
      espera="until bash '$AQUI/rodar_ensemble_d03.sh' livre; do sleep 60; done"   # o pgrep roda fora deste bash -c
      msg "fila: ha WRF/real rodando; a fila parte quando o host ficar livre"
    fi
    msg "fila do ensemble (membros: $MEMBROS; bracos: $BRACOS; NP=$NP) em segundo plano"
    setsid nohup bash -c "
      $espera
      for m in $MEMBROS; do for b in $BRACOS; do
        d='$ENS'/\${b}_m\${m}
        grep -q 'SUCCESS COMPLETE WRF' \"\$d/rsl.error.0000\" 2>/dev/null && continue
        [ -d \"\$d\" ] && mv \"\$d\" \"\${d}_parcial_\$(date -u +%Y%m%d%H%M)\"
        bash '$AQUI/rodar_ensemble_d03.sh' um \$b \$m || exit 1
      done; done
      echo \"[\$(date -u +%FT%TZ)] fila do ensemble terminou\" >> '$LOG'" > /dev/null 2>&1 < /dev/null & ;;
  livre)        # livre: sai com 0 se nao ha WRF/real rodando (usado pela fila com ESPERAR=1)
    ! ocupado ;;
  um)           # um <braco> <membro>: uma rodada de 27 h, em primeiro plano (chamada pela fila)
    b=${2:?braco}; m=${3:?membro}; d="$ENS/${b}_m${m}"
    exe="$(bin_de "$b")/wrf_toro.exe"; [ -x "$exe" ] || falha "falta $exe"
    prepara "$d" "$b" "$m"; msg "rodada $b membro $m (27 h) em $d com $exe"
    lanca "$exe" || falha "$b m$m nao partiu"
    msg "rodada $b membro $m terminou: $(tail -1 rsl.error.0000)"
    grep -q "SUCCESS COMPLETE WRF" rsl.error.0000 || falha "$b m$m sem SUCCESS (ver $d/rsl.error.0000)" ;;
  estado)
    printf "%-4s" ""; for m in $MEMBROS; do printf " %-8s" "m$m"; done; echo
    for b in $BRACOS; do printf "%-4s" "$b"
      for m in $MEMBROS; do d="$ENS/${b}_m${m}"
        if grep -q "SUCCESS COMPLETE WRF" "$d/rsl.error.0000" 2>/dev/null; then s=ok
        elif [ -f "$d/rsl.error.0000" ]; then s=$(grep -o "time 2026-08-2[56]_[0-9:]*" "$d/rsl.error.0000" | tail -1 | cut -c17-21); s=${s:-partida}
        else s=-; fi; printf " %-8s" "$s"
      done; echo
    done ;;
  *) echo "uso: bash rodar_ensemble_d03.sh verificar|teste|fila|estado|livre" >&2; exit 1 ;;
esac
