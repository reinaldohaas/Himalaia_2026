# Restaura o ambiente depois de um reinicio do servidor do Jupyter (o que estava em /root se perde).
#
# No TERMINAL, para a sessao ficar configurada:   source restaurar.sh
# Numa celula do notebook, so para verificar:      bash restaurar.sh
#
# Faz (idempotente, nao instala nada sozinho):
#   - exporta PERSIST, ENVDIR, RCLONE_CONFIG, GH_CONFIG_DIR (ambiente.sh) e poe ~/.local/bin no PATH
#   - refaz os links /root/.claude e /root/.claude.json para $PERSIST/.claude_persist (login do Claude Code)
#   - avisa se ha um rclone.conf antigo em /root (o que pedia "configuration password")
#   - verifica o remoto gdrive:, o cm1.exe (bibliotecas) e a fila do rodar_direto.sh
# Sem "set -e": pode ser carregado com source sem derrubar o terminal.

_R_AQUI=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)
source "$_R_AQUI/ambiente.sh"
case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) export PATH="$HOME/.local/bin:$PATH" ;; esac

echo "== base persistente: $PERSIST"
echo "   RCLONE_CONFIG=$RCLONE_CONFIG"

# Claude Code: login e configuracao persistentes
_R_P="$PERSIST/.claude_persist"
mkdir -p "$_R_P/.claude"; [ -e "$_R_P/.claude.json" ] || echo '{}' > "$_R_P/.claude.json"
for _r_n in .claude .claude.json; do
  if [ -L "$HOME/$_r_n" ]; then :;
  elif [ -e "$HOME/$_r_n" ]; then echo "   AVISO: $HOME/$_r_n existe e nao e link (nao mexi); mova para $_R_P/ se quiser persistir"
  else ln -s "$_R_P/$_r_n" "$HOME/$_r_n" && echo "   link refeito: $HOME/$_r_n -> $_R_P/$_r_n"; fi
done
if command -v claude >/dev/null 2>&1; then echo "== Claude Code: $(command -v claude)"
else echo "== Claude Code: NAO instalado neste conteiner (reinstale no Terminal: curl -fsSL https://claude.ai/install.sh | bash)"; fi

# rclone / Drive
if [ -f /root/.config/rclone/rclone.conf ] && [ "$RCLONE_CONFIG" != /root/.config/rclone/rclone.conf ]; then
  echo "   AVISO: ha um rclone.conf antigo em /root/.config/rclone/ (ignorado; pode apagar: rm /root/.config/rclone/rclone.conf)"
fi
if [ -f "$RCLONE_CONFIG" ]; then
  if ! command -v rclone >/dev/null 2>&1 && [ -d "$ENVDIR/cm1pos/bin" ]; then export PATH="$ENVDIR/cm1pos/bin:$PATH"; fi
  if command -v rclone >/dev/null 2>&1; then
    if rclone listremotes 2>/dev/null | grep -qx "gdrive:"; then
      if rclone lsd gdrive:vlab_cache >/dev/null 2>&1; then echo "== Drive: gdrive:vlab_cache acessivel"
      else echo "== Drive: remoto existe, mas gdrive:vlab_cache nao respondeu (token vencido ou client_id retirado?)"; fi
    else echo "== Drive: $RCLONE_CONFIG nao tem o remoto gdrive (ver: bash gdrive.sh configurar)"; fi
  else echo "== Drive: rclone nao encontrado (bash gdrive.sh instalar)"; fi
else echo "== Drive: sem $RCLONE_CONFIG (primeira vez: bash gdrive.sh configurar, depois importar)"; fi

# CM1
_R_EXE="$_R_AQUI/cm1/run/cm1.exe"
if [ -x "$_R_EXE" ]; then
  [ -f "$_R_AQUI/cm1/run/cm1.env" ] && { source "$_R_AQUI/cm1/run/cm1.env"; export LD_LIBRARY_PATH="$ENV_PREFIX/lib:${LD_LIBRARY_PATH:-}"; }
  if ldd "$_R_EXE" 2>/dev/null | grep -q "not found"; then echo "== cm1.exe: faltam bibliotecas -> bash compilar.sh"
  else echo "== cm1.exe: ok"; fi
else echo "== cm1.exe: nao compilado -> bash compilar.sh"; fi

# fila
bash "$_R_AQUI/rodar_direto.sh" estado 2>/dev/null | sed 's/^/   /' | head -20
unset _R_AQUI _R_P _r_n _R_EXE
