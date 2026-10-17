#!/bin/bash
# Reproducao, no vlab, da rodada de referencia feita no computador do pesquisador (WSL Ubuntu 24.04).
#
# O kit reproducao/ traz o MESMO executavel da referencia (gfortran 13.3, sha256 3a53a5d8...) e TODAS
# as bibliotecas de execucao da maquina de referencia: o carregador ld-linux, libc, libm, libmvec,
# libgfortran, libgomp, libgcc_s, libquadmath. O CM1 roda pelo carregador do kit, entao nem o
# compilador nem a glibc do vlab entram. Sobra so a diferenca de processador.
#
# Threads: 8, como na referencia. Saida em execucoes/<caso>_repro (nao toca nas rodadas existentes).
#
# Uso:  bash reproduzir.sh [caso]        (padrao: rad_06utc)
#       TESTE=1 bash reproduzir.sh       (120 s de modelo, para conferir que o kit funciona)
#       bash rodar_direto.sh estado      (acompanhar)
# Depois: bash relatorio.sh --enviar ; bash coletar.sh --leve <caso>_repro ; bash gdrive.sh enviar
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
CASO=${1:-rad_06utc}
K="$AQUI/reproducao"
[ -f "$K/cm1.exe" ] || { echo "ERRO: falta $K/cm1.exe (kit de reproducao nao instalado)" >&2; exit 1; }
( cd "$K" && sha256sum -c --quiet MANIFESTO_kit.sha256 ) || { echo "ERRO: kit de reproducao corrompido (sha256)" >&2; exit 1; }
chmod +x "$K/cm1.exe" "$K/lib/ld-linux-x86-64.so.2"
RUN="$K/lib/ld-linux-x86-64.so.2 --library-path $K/lib"
$RUN --version >/dev/null 2>&1 || $RUN "$K/cm1.exe" --help >/dev/null 2>&1 || true
mkdir -p "$AQUI/logs"
{
  echo "reproducao  $(date -u +%FT%TZ)  host=$(hostname)  caso=$CASO  threads=8  teste=${TESTE:-0}"
  echo "exe: $(sha256sum "$K/cm1.exe")"
  echo "glibc do kit: $($K/lib/ld-linux-x86-64.so.2 --version 2>/dev/null | head -1)"
  echo "glibc do sistema: $(ldd --version 2>/dev/null | head -1)"
  lscpu 2>/dev/null | grep -E "Model name|Socket|Thread|Core" || true
  echo "flags: $(grep -o -w -E 'avx2|fma|avx512f' /proc/cpuinfo | sort -u | tr '\n' ' ')"
} | tee "$AQUI/logs/reproducao_${CASO}.info"
export EXE_ALT="$K/cm1.exe" SUFIXO=_repro CM1_RUNNER="$RUN"
TESTE=${TESTE:-0} bash "$AQUI/rodar_direto.sh" -j 8 $( [ "${TESTE:-0}" = 1 ] && echo -t ) "$CASO"
