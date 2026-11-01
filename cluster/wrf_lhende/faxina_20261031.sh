#!/bin/bash
# Faxina do disco de 31/10/2026, decidida pelo pesquisador sobre relatorios/inventario_disco_20261031.txt.
# Quem roda e o pesquisador, no terminal do vlab; o script mostra cada grupo, o tamanho, e so apaga se a resposta for SIM.
#   G1  refugos: parciais, falhas, versoes antigas do teste_unico, duplicata, testes do ensemble, wrf_teste
#   G2  wrfout_d0* de toro_A..D e wrf_run, so se o recorte (recortes_antigos/<nome>.npz) existir e abrir
#   G3  cm1rst* das rodadas do CM1 que terminaram normalmente (os cm1out ficam)
#   bash faxina_20261031.sh          lista tudo e pergunta grupo a grupo
#   bash faxina_20261031.sh listar   so lista (nao apaga nada)
# rm -r nao segue links simbolicos: os links para WRF-Chem/WRF/run, wps_run e toro_real somem, os alvos ficam.
set -uo pipefail
H=/home/jovyan/privado/Himalaia_2026
W=$H/wrf_lhende
LISTAR=${1:-}

G1="toro_C_parcial_20261021 toro_D_parcial_20261021
toro_tUA_falha_001550 toro_tUA_falha_005901 toro_tUA_falha_010002 toro_tUA_falha_235107 toro_tUA_V42_tent1
toro_tUB_falha_001550 toro_tUB_falha_005901 toro_tUB_falha_235107 toro_tUB_falha_V41_121501 toro_tUB_falha_V41_121547
toro_tUB_falha_V41_121633 toro_tUB_falha_V41_121719 toro_tUB_falha_V41_121838 toro_tUB_falha_V42_131716
toro_tUB_falha_V42_131748 toro_tUB_falha_V42_225356 toro_tUB_parcial
toro_tUC_falha_005901 toro_tUC_falha_235107 toro_tUD_falha_005901
toro_tUA_v3 toro_tUB_v3 toro_tUC_v3 toro_tUD_v3 toro_tUA_v41 toro_tUB_v41 toro_tUC_v41 toro_tUD_v41 toro_tUC_v4b toro_tUEa
toro_tUA_V42_ok_20261030
ens_d03/teste_A1 ens_d03/teste_A2 ens_d03/teste_S1
wrf_teste d04/erro_script_BCD_131644 d04/logs"
G2="toro_A toro_B toro_C toro_D wrf_run"

ocupado() { pgrep -f "wrf.*\.exe|real.*\.exe" > /dev/null; }
confirma() {  # confirma <grupo>: so segue com SIM
  [ "$LISTAR" = listar ] && return 1
  read -r -p "  Apagar o grupo $1 acima? Digite SIM para apagar, qualquer outra coisa para pular: " r
  [ "$r" = SIM ]
}
dentro() {    # o caminho e diretorio de verdade (nao link) dentro de wrf_lhende
  [ -d "$1" ] && [ ! -L "$1" ] && case "$(realpath "$1")" in "$W"/*) return 0 ;; esac; return 1
}

echo "== disco antes"; df -h /home/jovyan/privado | tail -1

echo; echo "== G1: pastas inteiras"
alvo1=()
for p in $G1; do
  if dentro "$W/$p"; then alvo1+=("$W/$p"); printf "  %8s  %s\n" "$(du -sh "$W/$p" | cut -f1)" "$p"
  else echo "  (nao existe ou nao e pasta: $p)"; fi
done
case " ${alvo1[*]:-} " in *" $W/toro_tA "*|*" $W/toro_tBa "*|*" $W/toro_tCa "*|*" $W/toro_tDa "*) echo "ERRO: referencia na lista"; exit 1 ;; esac
if [ ${#alvo1[@]} -gt 0 ] && confirma G1; then
  for p in "${alvo1[@]}"; do rm -rf -- "$p" && echo "  apagado $p"; done
fi

echo; echo "== G2: so os wrfout_d0* (ficam wrfaux, rsl, namelists e o resto)"
alvo2=()
for n in $G2; do
  d=$W/$n; z=$W/recortes_antigos/$n.npz
  dentro "$d" || { echo "  (nao existe: $n)"; continue; }
  if ! python3 -c "import numpy as np,sys; z=np.load(sys.argv[1]); assert 'c_QCLOUD' in z.files and 's_OLR' in z.files and len(z['tempos'])>=8" "$z" 2>/dev/null; then
    echo "  PULA $n: recorte $z ausente ou incompleto"; continue
  fi
  n_arq=$(find "$d" -maxdepth 1 -type f -name 'wrfout_d0*' | wc -l)
  [ "$n_arq" -eq 0 ] && { echo "  $n: sem wrfout (ja limpo)"; continue; }
  alvo2+=("$d")
  printf "  %8s  %s (%d wrfout; recorte %s)\n" "$(find "$d" -maxdepth 1 -type f -name 'wrfout_d0*' -printf '%b\n' | awk '{s+=$1*512} END {printf "%.1fG", s/2^30}')" "$n" "$n_arq" "$(du -h "$z" | cut -f1)"
done
if [ ${#alvo2[@]} -gt 0 ]; then
  ocupado && echo "  (ha WRF rodando no host; os wrfout acima nao sao da rodada em curso, que esta em ens_d03/)"
  if confirma G2; then
    for d in "${alvo2[@]}"; do find "$d" -maxdepth 1 -type f -name 'wrfout_d0*' -print -delete | sed 's/^/  apagado /'; done
  fi
fi

echo; echo "== G3: cm1rst* das rodadas do CM1 que terminaram normalmente"
alvo3=()
for d in "$H"/toro_cm1_lhende/execucoes/*/; do
  d=${d%/}; [ -L "$d" ] && continue
  ls "$d"/cm1rst* > /dev/null 2>&1 || continue
  if grep -qi "terminated normally" "$d"/cm1.print.out 2>/dev/null; then
    alvo3+=("$d"); printf "  %8s  %s\n" "$(du -ch "$d"/cm1rst* | tail -1 | cut -f1)" "${d#$H/}"
  else
    echo "  PULA ${d#$H/}: cm1.print.out sem 'terminated normally'"
  fi
done
if [ ${#alvo3[@]} -gt 0 ] && confirma G3; then
  for d in "${alvo3[@]}"; do find "$d" -maxdepth 1 -type f -name 'cm1rst*' -delete && echo "  apagados os cm1rst de ${d#$H/}"; done
fi

echo; echo "== disco depois"; df -h /home/jovyan/privado | tail -1
