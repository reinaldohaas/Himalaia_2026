#!/bin/bash
# roda no WSL: $1 = diretorio scratchpad (caminho /mnt/c/...)
SP="$1"; shift
export OMP_NUM_THREADS=3 OMP_STACKSIZE=512M; ulimit -s unlimited 2>/dev/null
for R in "$@"; do
  cd "$SP/$R" || continue
  s=$(date +%s); ./cm1.single.gnu.exe > cm1.print.out 2>&1; rc=$?; e=$(date +%s)
  echo "$R  rc=$rc  parede=$((e-s))s  $(tail -1 cm1.print.out)"
done
