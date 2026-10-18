#!/bin/bash
# Kit de execucao do WRF/WPS ja compilados no vlab (privado/WRF-Chem: WRF 4.7.1 e WPS 4.6.0, gfortran 11.4,
# OpenMPI, netCDF do sistema), que nao carregam no conteiner atual por falta de libnetcdff.so.7 e libmpi*.so.40.
# Parte de um kit_mpi do CM1 (carregador ld-linux + glibc 2.39 + OpenMPI 4.1.6 + PMIx, validado no vlab) e
# acrescenta o fecho de dependencias do netCDF-Fortran/netCDF/HDF5 do WSL (Ubuntu 24.04; mesmos sonames
# que os executaveis pedem: libnetcdff.so.7, libnetcdf.so.19). Nada e instalado: tudo fica em kit_wrf/lib.
#
# Uso: bash montar_kit_wrf.sh <kit_mpi_base> <dir_saida>
set -euo pipefail
BASE=${1:?kit_mpi de base}; OUT=${2:?saida}
K="$OUT/kit_wrf"
mkdir -p "$OUT"
cp -a "$BASE" "$K"
rm -f "$K/cm1.exe" "$K/MANIFESTO_kit.sha256" "$K/KIT.info"
lista=$(mktemp)
for l in /lib/x86_64-linux-gnu/libnetcdff.so.7 /lib/x86_64-linux-gnu/libnetcdf.so.19; do
  echo "$l" >> "$lista"
  ldd "$l" | awk '/=>/ && $3 ~ /^\// {print $3}' >> "$lista"
done
novos=0
sort -u "$lista" | while read -r l; do
  b=$(basename "$l")
  [ -e "$K/lib/$b" ] || { cp -L "$l" "$K/lib/$b"; echo "  + $b"; }
done
rm -f "$lista"
( cd "$K" && find . -type f ! -name MANIFESTO_kit.sha256 -print0 | sort -z | xargs -0 sha256sum > MANIFESTO_kit.sha256 )
{
  echo "kit_wrf montado $(date -u +%FT%TZ) em $(hostname) a partir de $(basename "$BASE")"
  echo "glibc: $(ldd --version | head -1)"
  echo "netCDF-Fortran: $(dpkg -l libnetcdff7 2>/dev/null | awk '/^ii/{print $3}')  netCDF: $(dpkg -l 'libnetcdf19*' 2>/dev/null | awk '/^ii/{print $3}' | head -1)  HDF5: $(dpkg -l 'libhdf5-103*' 2>/dev/null | awk '/^ii/{print $3}' | head -1)"
  echo "bibliotecas: $(ls "$K/lib" | wc -l)"
} | tee "$K/KIT.info"
du -sh "$K"
