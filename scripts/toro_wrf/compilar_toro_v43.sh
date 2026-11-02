#!/bin/bash
# Compila o modulo toro_wrf 4.3 (E3: injecao de nucleos de glaciacao) no WSL, do mesmo jeito que o 4.2:
# copia a arvore ja compilada do 4.2 (wrf471_toroV, wrf.exe sha 478962a3...), volta os 4 arquivos ao WRF 4.7.1 original
# (*.antes_toro), aplica aplicar_patch_toro_wrf.py com o module_toro_wrf.F deste repositorio e recompila (incremental).
# So compila e empacota; os testes (teste_unico A-D e o teste da injecao) rodam no vlab.
#   bash compilar_toro_v43.sh <pasta scripts/toro_wrf do repositorio>
set -euo pipefail
REPO=$(cd "${1:?pasta scripts/toro_wrf}" && pwd)
B=/home/haas/toro_build; SRC=$B/wrf471_toroV; DST=$B/wrf471_toroV43; LOG=$B/build_toroV43.log
[ -e "$DST" ] && { echo "ja existe $DST; apague-a a mao para recompilar do zero"; exit 1; }
[ "$(sha256sum "$SRC/main/wrf.exe" | cut -c1-16)" = 478962a3c4965b95 ] || { echo "$SRC/main/wrf.exe nao e o 4.2"; exit 1; }
cp -a "$SRC" "$DST"
cd "$DST"
for f in phys/module_mp_nssl_2mom.F phys/module_microphysics_driver.F phys/module_pbl_driver.F main/depend.common; do
  cp -p "$f.antes_toro" "$f"
done
python3 "$REPO/aplicar_patch_toro_wrf.py" "$DST" "$REPO/module_toro_wrf.F"
export NETCDF=$B/netcdf_link WRFIO_NCD_LARGE_FILE_SUPPORT=1
./compile -j 16 em_real > "$LOG" 2>&1 || true
[ -x main/wrf.exe ] && [ main/wrf.exe -nt phys/module_mp_nssl_2mom.F ] || { echo "a compilacao falhou (ver $LOG)"; grep -n -i " error" "$LOG" | head; exit 1; }
echo "wrf.exe 4.3: $(sha256sum main/wrf.exe | cut -c1-16)"
# o toro_vortice nao mudou: as chamadas de coshf (1 vetorial, 6 escalares no 4.1/4.2) tem de ser as mesmas
for e in "$SRC/main/wrf.exe" main/wrf.exe; do
  echo "  $(basename "$(dirname "$(dirname "$e")")"): $(objdump -d "$e" | grep -c 'call.*<_ZGV.*coshf') vetoriais, $(objdump -d "$e" | grep -c 'call.*<coshf') escalares de coshf"
done
