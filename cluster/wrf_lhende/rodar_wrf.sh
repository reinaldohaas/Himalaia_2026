#!/bin/bash
# WRF do Lhende Khola no vlab, com os executaveis ja compilados em privado/WRF-Chem (WRF 4.7.1, WPS 4.6.0,
# gfortran 11.4, dmpar) rodando pelo kit_wrf (carregador ld-linux + glibc 2.39 + OpenMPI 4.1.6 + netCDF);
# nada e instalado e nada em privado/WRF-Chem e alterado (tudo roda em copias/links neste diretorio).
#
#   bash rodar_wrf.sh verificar   -> confere kit, executaveis, tabelas e dados (nao roda nada)
#   bash rodar_wrf.sh wps         -> geogrid + ungrib + metgrid  (wps_run/)
#   bash rodar_wrf.sh real        -> real.exe (wrf_run/), NP ranks
#   bash rodar_wrf.sh teste       -> wrf.exe por 30 min de modelo (wrf_teste/), para ver se sobe
#   bash rodar_wrf.sh wrf         -> wrf.exe completo (36 h; d03 a partir de 25/08 06 UTC), em segundo plano
#   bash rodar_wrf.sh estado
# Variaveis: NP (ranks, padrao 112), WRFDIR, WPSDIR, GEOG, ERA5 (dir dos .grib).
set -uo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd); cd "$AQUI"
WRFDIR=${WRFDIR:-/home/jovyan/privado/WRF-Chem/WRF}
WPSDIR=${WPSDIR:-/home/jovyan/privado/WRF-Chem/WPS}
GEOG=${GEOG:-/home/jovyan/privado/gis4wrf/datasets/geog}
ERA5=${ERA5:-$AQUI/era5}
export KIT_MPI=${KIT_MPI:-$AQUI/kit_wrf}
NP=${NP:-112}
LD="$KIT_MPI/lib/ld-linux-x86-64.so.2 --library-path $KIT_MPI/lib"
LOG="$AQUI/logs/wrf.log"; mkdir -p "$AQUI/logs"
msg() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }
falha() { msg "FALHA: $*"; exit 1; }

verificar() {
  ( cd "$KIT_MPI" && sha256sum -c --quiet MANIFESTO_kit.sha256 ) || falha "kit_wrf corrompido"
  for e in "$WRFDIR/wrf.exe" "$WRFDIR/real.exe" "$WPSDIR/geogrid.exe" "$WPSDIR/ungrib.exe" "$WPSDIR/metgrid.exe"; do
    [ -x "$e" ] || falha "falta $e"
    echo "  $(basename "$e"): $( $LD --list "$e" 2>&1 | grep -c 'not found') bibliotecas faltando pelo kit"
  done
  for t in "$WPSDIR/geogrid/GEOGRID.TBL.ARW" "$WPSDIR/metgrid/METGRID.TBL.ARW" "$WPSDIR/ungrib/Variable_Tables/Vtable.ECMWF" "$WPSDIR/link_grib.csh" \
           "$WRFDIR/run/RRTMG_LW_DATA" "$WRFDIR/run/RRTMG_SW_DATA" "$WRFDIR/run/LANDUSE.TBL" "$WRFDIR/run/VEGPARM.TBL" "$WRFDIR/run/SOILPARM.TBL" "$WRFDIR/run/GENPARM.TBL"; do
    [ -e "$t" ] && echo "  ok $t" || echo "  FALTA $t"
  done
  ls "$GEOG"/topo_gmted2010_30s/index >/dev/null 2>&1 && echo "  ok geog ($GEOG)" || echo "  FALTA geog em $GEOG"
  ls "$ERA5"/*.grib 2>/dev/null | wc -l | sed 's/^/  arquivos ERA5: /'
  command -v csh >/dev/null && echo "  csh: ok" || echo "  csh: ausente (link_grib.csh sera substituido por ln)"
}

wps() {
  mkdir -p wps_run && cd wps_run || falha "wps_run"
  sed -e "s|GEOG_DATA_PATH|$GEOG|" -e "s|WPS_DIR|$WPSDIR|" "$AQUI/namelist.wps" > namelist.wps
  msg "geogrid"; $LD "$WPSDIR/geogrid.exe" > geogrid.out 2>&1; grep -q "Successful completion of geogrid" geogrid.out || { tail -20 geogrid.out; falha "geogrid (ver wps_run/geogrid.out)"; }
  ln -sf "$WPSDIR/ungrib/Variable_Tables/Vtable.ECMWF" Vtable
  rm -f GRIBFILE.* ; i=0
  L=(A B C D E F G H I J K L M N O P Q R S T U V W X Y Z)
  for f in $(ls "$ERA5"/*.grib | sort); do
    ln -sf "$f" "GRIBFILE.${L[i / 676]}${L[(i / 26) % 26]}${L[i % 26]}"; i=$((i + 1))   # como o link_grib.csh
  done
  msg "ungrib ($i arquivos GRIB)"; "$WPSDIR/ungrib.exe" > ungrib.out 2>&1 || $LD "$WPSDIR/ungrib.exe" > ungrib.out 2>&1
  grep -q "Successful completion of ungrib" ungrib.out || { tail -20 ungrib.out; falha "ungrib (ver wps_run/ungrib.out)"; }
  msg "metgrid"; $LD "$WPSDIR/metgrid.exe" > metgrid.out 2>&1; grep -q "Successful completion of metgrid" metgrid.out || { tail -20 metgrid.out; falha "metgrid (ver wps_run/metgrid.out)"; }
  msg "WPS ok: $(ls met_em.d01.* | wc -l) met_em d01, $(ls met_em.d02.* 2>/dev/null | wc -l) d02, $(ls met_em.d03.* 2>/dev/null | wc -l) d03"
}

prepara_run() {   # prepara_run <dir>
  mkdir -p "$1" && cd "$1" || falha "$1"
  for f in "$WRFDIR"/run/*; do b=$(basename "$f"); case "$b" in *.exe|namelist*|wrfout*|rsl.*) ;; *) ln -sf "$f" "$b";; esac; done
  ln -sf "$AQUI"/wps_run/met_em.d0* .
  cp "$AQUI/namelist.input" namelist.input
  cp "$AQUI/iofields_toro.txt" iofields_toro.txt          # saida leve (wrfaux_*): OLR, chuva, superficie
}

enviar() {        # manda os wrfaux_* (leves) e os logs ao Drive, para o diagnostico fora do vlab
  export RCLONE_CONFIG=${RCLONE_CONFIG:-/home/jovyan/privado/.config/rclone/rclone.conf}
  command -v rclone >/dev/null || export PATH="/home/jovyan/privado/conda_envs/cm1pos/bin:$PATH"
  local dst=gdrive:vlab_cache/Himalaia_2026/saida/wrf_lhende/${1:-wrf_run}
  for f in "$AQUI/${1:-wrf_run}"/wrfaux_d0* "$AQUI/${1:-wrf_run}"/rsl.error.0000 "$AQUI/${1:-wrf_run}"/namelist.input "$LOG"; do
    [ -f "$f" ] && rclone copy "$f" "$dst/" 2>&1 | grep -v client_id
  done
  msg "enviado ao Drive: $dst ($(ls "$AQUI/${1:-wrf_run}"/wrfaux_d0* 2>/dev/null | wc -l) wrfaux)"
}

real() {
  prepara_run wrf_run
  msg "real.exe (NP=16)"; NP=16 OMP_NUM_THREADS=1 BIND=core bash "$AQUI/mpi_kit.sh" "$WRFDIR/real.exe" > real.out 2>&1
  grep -q "SUCCESS COMPLETE REAL_EM" rsl.error.0000 || { tail -25 rsl.error.0000; falha "real.exe (ver wrf_run/rsl.error.0000)"; }
  msg "real ok: $(ls wrfinput_d0* wrfbdy_d01 2>/dev/null | tr '\n' ' ')"
}

teste() {
  prepara_run wrf_teste
  ln -sf "$AQUI"/wrf_run/wrfinput_d0* "$AQUI"/wrf_run/wrfbdy_d01 .
  sed -i -E 's/^( run_hours +=).*/\1 0,/; s/^( run_minutes +=).*/\1 30,/; s/^( max_dom +=).*/\1 2,/' namelist.input
  msg "wrf teste (30 min, d01+d02, NP=$NP)"; NP=$NP OMP_NUM_THREADS=1 BIND=core bash "$AQUI/mpi_kit.sh" "$WRFDIR/wrf.exe" > wrf.out 2>&1
  grep -q "SUCCESS COMPLETE WRF" rsl.error.0000 || { tail -25 rsl.error.0000; falha "wrf teste (ver wrf_teste/rsl.error.0000)"; }
  msg "wrf teste ok: $(grep -c 'Timing for main' rsl.error.0000) passos; $(grep 'Timing for main' rsl.error.0000 | tail -1)"
}

wrf_bg() {
  prepara_run wrf_run
  msg "wrf completo (NP=$NP) em segundo plano"
  setsid nohup bash -c "NP=$NP OMP_NUM_THREADS=1 BIND=core bash '$AQUI/mpi_kit.sh' '$WRFDIR/wrf.exe' > wrf.out 2>&1; echo \"[\$(date -u +%FT%TZ)] wrf terminou: \$(tail -1 rsl.error.0000)\" >> '$LOG'" > /dev/null 2>&1 < /dev/null &
}

estado() {
  tail -8 "$LOG" 2>/dev/null
  [ -f wrf_run/rsl.error.0000 ] && grep 'Timing for main' wrf_run/rsl.error.0000 | tail -2
  ls -la wrf_run/wrfout_* 2>/dev/null | tail -3
}

case "${1:-}" in
  verificar) verificar ;; wps) wps ;; real) real ;; teste) teste ;; wrf) wrf_bg ;; estado) estado ;;
  enviar) enviar "${2:-wrf_run}" ;;
  *) echo "uso: bash rodar_wrf.sh verificar|wps|real|teste|wrf|estado|enviar [wrf_run|wrf_teste]" >&2; exit 1 ;;
esac
