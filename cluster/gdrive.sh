#!/bin/bash
# Cache no Google Drive entre o seu computador e o vlab (via rclone).
#
#   No seu computador (Google Drive para desktop): a pasta  G:\Meu Drive\vlab_cache\
#       entrada\   o que vai PARA o vlab   (pacotes .tar.gz + .sha256)
#       saida\     o que volta DO vlab     (saida\<projeto>\<data>\...)
#   No vlab: o remoto rclone "gdrive:" aponta para o mesmo Drive.
#
# Uso (no vlab):
#   bash gdrive.sh instalar          # instala o rclone no ambiente conda "cm1pos" (se nao houver)
#   bash gdrive.sh configurar        # mostra como criar o remoto "gdrive" (o login e SEU)
#   bash gdrive.sh estado            # lista o que ha em entrada/ e saida/
#   bash gdrive.sh baixar [arquivo]  # entrada/ -> ~/mesoescala-montanhas/  (confere sha256)
#   bash gdrive.sh enviar [--completo]
#                                    # pacote leve mais recente (e, com --completo, o completo) -> saida/<projeto>/<data>/
#
# Variaveis: REMOTO (padrao gdrive), CACHE (padrao vlab_cache), PROJETO (padrao toro_cm1_lhende),
#            DESTINO (padrao ~/mesoescala-montanhas)
# Este script nunca le, grava nem imprime token; o token fica no rclone.conf do proprio rclone.
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
REMOTO=${REMOTO:-gdrive}; CACHE=${CACHE:-vlab_cache}; PROJETO=${PROJETO:-toro_cm1_lhende}
DESTINO=${DESTINO:-$HOME/mesoescala-montanhas}
CMD=${1:-ajuda}; shift || true

ativar_rclone() {
  command -v rclone >/dev/null 2>&1 && return 0
  export PATH=$HOME/miniforge3/bin:$PATH
  local MAMBA; MAMBA=$(command -v mamba || command -v conda || true)
  [ -n "$MAMBA" ] || { echo "ERRO: sem rclone e sem conda (instale o Miniforge, ver README)" >&2; exit 1; }
  source "$(dirname "$MAMBA")/../etc/profile.d/conda.sh"
  if ! $MAMBA env list | grep -q '^cm1pos '; then
    $MAMBA create -y -n cm1pos -c conda-forge python=3.11 numpy matplotlib rclone
  fi
  conda activate cm1pos
  command -v rclone >/dev/null 2>&1 || { $MAMBA install -y -n cm1pos -c conda-forge rclone; conda activate cm1pos; }
}
checar_remoto() {
  rclone listremotes | grep -qx "$REMOTO:" || { echo "Remoto '$REMOTO:' nao configurado. Rode: bash gdrive.sh configurar" >&2; exit 1; }
}

case "$CMD" in
  instalar)
    ativar_rclone; rclone version | head -1 ;;
  configurar)
    ativar_rclone
    cat <<TXT
Configuracao do remoto "$REMOTO" (uma vez). No terminal do Jupyter do vlab:

  rclone config
    n                      (novo remoto)
    name>  $REMOTO
    Storage> drive         (Google Drive)
    client_id / client_secret: <Enter> <Enter>
    scope> 1               (acesso completo: precisa ver o que o Drive para desktop sincroniza;
                            o escopo "drive.file" so enxerga arquivos criados pelo proprio rclone)
    service_account_file: <Enter>   Edit advanced config? n
    Use web browser to automatically authenticate? n      (o vlab nao tem navegador)

  O rclone mostra um comando  rclone authorize "drive" "..."  para rodar numa maquina COM navegador.
  No seu computador Windows (PowerShell):
      winget install Rclone.Rclone          (uma vez)
      rclone authorize "drive" "...cole o que o vlab mostrou..."
  Faca o login do Google no navegador; o Windows imprime um bloco "config_token".
  Cole esse bloco no prompt do vlab.  Configure as a Shared Drive? n  ->  y (Keep)  ->  q

Teste:  rclone lsd $REMOTO:   e   bash gdrive.sh estado
TXT
    ;;
  estado)
    ativar_rclone; checar_remoto
    rclone mkdir "$REMOTO:$CACHE/entrada"; rclone mkdir "$REMOTO:$CACHE/saida"
    echo "== $REMOTO:$CACHE/entrada"; rclone lsl "$REMOTO:$CACHE/entrada" || true
    echo "== $REMOTO:$CACHE/saida/$PROJETO"; rclone lsl "$REMOTO:$CACHE/saida/$PROJETO" 2>/dev/null || echo "(vazio)" ;;
  baixar)
    ativar_rclone; checar_remoto; mkdir -p "$DESTINO"
    if [ $# -ge 1 ]; then
      for a in "$@"; do rclone copy -P "$REMOTO:$CACHE/entrada/$a" "$DESTINO/"; rclone copy "$REMOTO:$CACHE/entrada/$a.sha256" "$DESTINO/" 2>/dev/null || true; done
    else
      rclone copy -P "$REMOTO:$CACHE/entrada" "$DESTINO/"
    fi
    cd "$DESTINO"
    for s in *.sha256; do [ -f "$s" ] && sha256sum -c "$s"; done ;;
  enviar)
    ativar_rclone; checar_remoto
    DATA=$(date +%Y%m%d_%H%M); ALVO="$REMOTO:$CACHE/saida/$PROJETO/$DATA"
    LEVE=$(ls -t "$AQUI"/resultados_cm1_leve_*.tar.gz 2>/dev/null | head -1 || true)
    [ -n "$LEVE" ] || { echo "Nenhum pacote leve. Rode antes: bash pos/analisar.sh && bash coletar.sh --leve" >&2; exit 1; }
    ARQS=("$LEVE" "$LEVE.sha256")
    for f in "$AQUI"/pos/*.png "$AQUI"/pos/*.json; do [ -f "$f" ] && ARQS+=("$f"); done
    if [ "${1:-}" = "--completo" ]; then
      CHEIO=$(ls -t "$AQUI"/resultados_cm1_2*.tar.gz 2>/dev/null | head -1 || true)
      [ -n "$CHEIO" ] || { echo "Nenhum pacote completo. Rode antes: bash coletar.sh" >&2; exit 1; }
      ARQS+=("$CHEIO" "$CHEIO.sha256")
    fi
    for f in "${ARQS[@]}"; do rclone copy -P "$f" "$ALVO/"; done
    rclone check --one-way --size-only "$(dirname "$LEVE")" "$ALVO" --include "$(basename "$LEVE")" >/dev/null 2>&1 && echo "conferido"
    echo "OK: $ALVO"
    echo "No seu computador: G:\\Meu Drive\\$CACHE\\saida\\$PROJETO\\$DATA" ;;
  *)
    sed -n '2,21p' "$0" ;;
esac
