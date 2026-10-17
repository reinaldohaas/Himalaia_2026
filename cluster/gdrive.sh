#!/bin/bash
# Cache no Google Drive entre o seu computador e o vlab (via rclone).
#
#   No seu computador (Google Drive para desktop): a pasta  G:\Meu Drive\vlab_cache\Himalaia_2026\
#       entrada\   o que vai PARA o vlab   (pacotes .tar.gz + .sha256)
#       saida\     o que volta DO vlab     (saida\<projeto>\<data>\...)
#   No vlab: o remoto rclone "gdrive:" aponta para o mesmo Drive.
#
# Uso (no vlab):
#   bash gdrive.sh instalar          # instala o rclone no ambiente conda "cm1pos" (se nao houver)
#   bash gdrive.sh configurar        # mostra como criar o remoto "gdrive" no Windows (o login e SEU)
#   bash gdrive.sh importar [arq]    # instala o rclone.conf que voce subiu para privado/ e testa
#   bash gdrive.sh estado            # lista o que ha em entrada/ e saida/
#   bash gdrive.sh baixar [arquivo]  # entrada/ -> ~/Himalaia_2026/  (confere sha256)
#   bash gdrive.sh enviar [--completo]
#                                    # pacote leve mais recente (e, com --completo, o completo) -> saida/<projeto>/<data>/
#
# Variaveis: REMOTO (padrao gdrive), CACHE (padrao vlab_cache/Himalaia_2026), PROJETO (padrao toro_cm1_lhende),
#            DESTINO (padrao $PERSIST/Himalaia_2026); RCLONE_CONFIG em $PERSIST (ver ambiente.sh)
# Este script nunca le, grava nem imprime token; o token fica no rclone.conf ($RCLONE_CONFIG).
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
source "$AQUI/ambiente.sh"          # PERSIST, ENVDIR, RCLONE_CONFIG (persistentes)
REMOTO=${REMOTO:-gdrive}; CACHE=${CACHE:-vlab_cache/Himalaia_2026}; PROJETO=${PROJETO:-toro_cm1_lhende}
DESTINO=${DESTINO:-$PERSIST/Himalaia_2026}
CMD=${1:-ajuda}; shift || true

ativar_rclone() {
  command -v rclone >/dev/null 2>&1 && return 0
  usar_env cm1pos python=3.11 numpy matplotlib rclone
  garantir cm1pos rclone rclone
}
checar_remoto() {
  rclone listremotes | grep -qx "$REMOTO:" || { echo "Remoto '$REMOTO:' nao configurado. Rode: bash gdrive.sh configurar" >&2; exit 1; }
}

case "$CMD" in
  instalar)
    ativar_rclone; rclone version | head -1 ;;
  configurar)
    cat <<TXT
Configuracao do remoto "$REMOTO" (uma vez). O login do Google precisa de navegador, entao e feito
NO SEU WINDOWS; para o vlab vai so o arquivo pronto.

  1) No Windows (PowerShell):
       winget install Rclone.Rclone                 (uma vez; feche e reabra o PowerShell)
       rclone config create $REMOTO drive scope=drive   (abre o navegador: entre na conta Google e autorize)
       rclone lsd $REMOTO:$CACHE                        (deve listar entrada e saida)
       rclone config file                           (mostra onde esta o rclone.conf)

  2) No Jupyter do vlab: painel de arquivos > pasta  privado/  > botao Upload > escolha o rclone.conf

  3) No vlab:
       bash gdrive.sh importar                      (move privado/rclone.conf para $RCLONE_CONFIG e testa)

O rclone.conf contem o token do seu Drive: nao cole o conteudo em lugar nenhum, so mova o arquivo.
Revogar: myaccount.google.com > Seguranca > Apps de terceiros > rclone.
TXT
    ;;
  importar)
    ativar_rclone
    ORIG=${1:-$PERSIST/rclone.conf}
    [ -f "$ORIG" ] || { echo "ERRO: nao achei $ORIG. Suba o rclone.conf pelo Jupyter para $PERSIST/ (ver: bash gdrive.sh configurar)" >&2; exit 1; }
    mkdir -p "$(dirname "$RCLONE_CONFIG")"
    if [ -f "$RCLONE_CONFIG" ]; then mv "$RCLONE_CONFIG" "$RCLONE_CONFIG.anterior"; echo "(config anterior guardada em $RCLONE_CONFIG.anterior)"; fi
    mv "$ORIG" "$RCLONE_CONFIG"; chmod 600 "$RCLONE_CONFIG"
    echo "config instalada em $RCLONE_CONFIG (permissao 600)"
    checar_remoto
    rclone lsd "$REMOTO:$CACHE" && echo "OK: o vlab enxerga $REMOTO:$CACHE" ;;
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
