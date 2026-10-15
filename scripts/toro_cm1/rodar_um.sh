#!/bin/bash
# $1 = diretorio absoluto WSL, $2 = threads
cd "$1" || exit 1
export OMP_NUM_THREADS=$2 OMP_STACKSIZE=512M; ulimit -s unlimited 2>/dev/null
s=$(date +%s); ./cm1.single.gnu.exe > cm1.print.out 2>&1; rc=$?
echo "$(basename $1)  rc=$rc  parede=$(( $(date +%s)-s ))s  $(tail -1 cm1.print.out)" >> ../fila_terreno.log
