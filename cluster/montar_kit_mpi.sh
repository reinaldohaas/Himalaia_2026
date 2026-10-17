#!/bin/bash
# Monta, no computador do pesquisador (WSL Ubuntu 24.04), o kit MPI+OpenMP para o vlab:
#   kit_mpi/cm1.exe                 executavel hibrido (mpif90 + OpenMP, gfortran 13.3)
#   kit_mpi/lib/                    carregador ld-linux + TODAS as bibliotecas (glibc, gfortran, OpenMPI 4.1.6,
#                                   PMIx 5.0.1, hwloc, libevent...) do fecho do ldd do exe, do orterun e dos plugins
#   kit_mpi/ompi/                   arvore relocavel do OpenMPI (OPAL_PREFIX): bin/orterun, plugins MCA, ajuda
#   kit_mpi/pmix2/                  arvore relocavel do PMIx (PMIX_INSTALL_PREFIX): plugins e ajuda
#   kit_mpi/MANIFESTO_kit.sha256
# Nada do sistema do vlab entra na execucao: o orterun e cada rank sobem pelo ld-linux do kit.
#
# Uso:  bash montar_kit_mpi.sh <cm1_hibrido.exe> <dir_saida>
set -euo pipefail
EXE=${1:?executavel hibrido}; OUT=${2:?diretorio de saida}
MA=/usr/lib/x86_64-linux-gnu
K="$OUT/kit_mpi"
rm -rf "$K"; mkdir -p "$K/lib" "$K/ompi/bin" "$K/ompi/lib/x86_64-linux-gnu/openmpi/lib" "$K/ompi/share" "$K/pmix2/lib" "$K/pmix2/share"
cp "$EXE" "$K/cm1.exe"
cp /usr/bin/orterun "$K/ompi/bin/orterun"
cp /usr/bin/orted "$K/ompi/bin/orted" 2>/dev/null || true
cp -r "$MA/openmpi/lib/openmpi3" "$K/ompi/lib/x86_64-linux-gnu/openmpi/lib/"
cp -r /usr/share/openmpi "$K/ompi/share/"
cp -r "$MA/pmix2/lib/pmix" "$K/pmix2/lib/"
cp -r "$MA/pmix2/share/pmix" "$K/pmix2/share/"
mkdir -p "$K/ompi/etc"; cp /etc/openmpi/openmpi-mca-params.conf "$K/ompi/etc/" 2>/dev/null || true

# fecho das dependencias de tudo que sera carregado
lista=$(mktemp)
for f in "$K/cm1.exe" "$K"/ompi/bin/* "$K"/ompi/lib/x86_64-linux-gnu/openmpi/lib/openmpi3/*.so "$K"/pmix2/lib/pmix/*.so; do
  ldd "$f" 2>/dev/null | awk '/=>/ && $3 ~ /^\// {print $3} /^\t\/lib64\// {print $1}' >> "$lista"
done
faltam=$(for f in "$K"/ompi/lib/x86_64-linux-gnu/openmpi/lib/openmpi3/*.so; do ldd "$f" | grep "not found" | sed "s|^|$(basename "$f"): |" || true; done)
[ -n "$faltam" ] && { echo "AVISO: plugins com dependencias ausentes no WSL (nao serao usaveis no vlab):"; echo "$faltam"; }
sort -u "$lista" | while read -r l; do cp -L "$l" "$K/lib/$(basename "$l")"; done
rm -f "$lista"
cp -L /lib64/ld-linux-x86-64.so.2 "$K/lib/ld-linux-x86-64.so.2"
# o PMIx 5 do Ubuntu tem o caminho dos plugins compilado (nenhuma variavel de ambiente o muda): na copia do
# kit, troca-se a cadeia por outra de MESMO tamanho em /tmp, que o mpi_kit.sh liga a kit_mpi/pmix2
python3 - "$K/lib/libpmix.so.2" <<'PY'
import sys
a, b = b"/usr/lib/x86_64-linux-gnu/pmix2", b"/tmp/.kit_mpi_cm1_lhende_pmix_2"
assert len(a) == len(b)
d = open(sys.argv[1], "rb").read(); n = d.count(a)
assert n >= 1, "cadeia do PMIx nao encontrada"
open(sys.argv[1], "wb").write(d.replace(a, b)); print("libpmix.so.2: %d ocorrencias do caminho trocadas" % n)
PY
chmod +x "$K/lib/ld-linux-x86-64.so.2" "$K/cm1.exe" "$K/ompi/bin/"*
( cd "$K" && find . -type f ! -name MANIFESTO_kit.sha256 -print0 | sort -z | xargs -0 sha256sum > MANIFESTO_kit.sha256 )
{
  echo "kit_mpi montado $(date -u +%FT%TZ) em $(hostname)"
  echo "exe: $(sha256sum "$K/cm1.exe" | cut -d' ' -f1)"
  echo "glibc: $(ldd --version | head -1)"
  echo "OpenMPI: $(dpkg -l libopenmpi3t64 | awk '/^ii/{print $3}')  PMIx: $(dpkg -l libpmix2t64 | awk '/^ii/{print $3}')"
  echo "bibliotecas: $(ls "$K/lib" | wc -l)  plugins MCA: $(ls "$K"/ompi/lib/x86_64-linux-gnu/openmpi/lib/openmpi3/*.so | wc -l)"
} | tee "$K/KIT.info"
du -sh "$K"
