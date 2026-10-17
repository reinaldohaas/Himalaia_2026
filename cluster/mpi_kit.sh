#!/bin/bash
# Lancador MPI do kit_mpi (usado como CM1_RUNNER pelo rodar_caso.sh):  bash mpi_kit.sh ./cm1.exe
# Sobe o orterun do kit pelo ld-linux do kit; cada rank tambem sobe pelo ld-linux do kit (modo "rank").
# Variaveis: NP (ranks, padrao 16), OMP_NUM_THREADS (threads por rank), BIND (core|none, padrao core).
# Ajustes para conteiner: root permitido, memoria compartilhada em /tmp (o /dev/shm do docker e pequeno),
# copia unica desligada (process_vm_readv costuma ser bloqueado), so btl self,vader e pml ob1.
set -euo pipefail
K=$(cd "$(dirname "$0")" && pwd)/kit_mpi
LD="$K/lib/ld-linux-x86-64.so.2 --library-path $K/lib"
if [ "${1:-}" = "rank" ]; then shift; exec $LD "$@"; fi
NP=${NP:-16}; T=${OMP_NUM_THREADS:-1}
export OPAL_PREFIX="$K/ompi" PMIX_INSTALL_PREFIX="$K/pmix2"
export OMPI_MCA_mca_base_component_path="$K/ompi/lib/x86_64-linux-gnu/openmpi/lib/openmpi3"
export PMIX_PREFIX="$K/pmix2" PMIX_MCA_mca_base_component_path="$K/pmix2/lib/pmix" PMIX_MCA_pmix_mca_base_component_path="$K/pmix2/lib/pmix"
export HWLOC_PLUGINS_PATH="$K/hwloc_sem_plugins"      # vazio: o hwloc usa so a deteccao interna (sem X11/OpenCL/libxml2 do sistema)
mkdir -p "$HWLOC_PLUGINS_PATH"
ln -sfn "$K/pmix2" /tmp/.kit_mpi_cm1_lhende_pmix_2     # caminho trocado na libpmix.so.2 do kit (montar_kit_mpi.sh)
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
if [ "${BIND:-core}" = "core" ]; then MAPA=(--map-by "slot:PE=$T" --bind-to core); else MAPA=(--bind-to none); fi
exec $LD "$K/ompi/bin/orterun" -np "$NP" "${MAPA[@]}" \
  --mca btl self,vader --mca pml ob1 --mca btl_vader_single_copy_mechanism none \
  --mca btl_vader_backing_directory /tmp --mca orte_tmpdir_base /tmp \
  -x OMP_NUM_THREADS -x OMP_STACKSIZE -x OMP_PLACES -x OMP_PROC_BIND \
  bash "$K/../mpi_kit.sh" rank "$@"
