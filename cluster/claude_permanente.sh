#!/bin/bash
# Claude Code "permanente" no vlab: roda dentro do tmux (sobrevive a fechar o Terminal/notebook)
# e e reiniciado sozinho se cair, retomando a conversa desta pasta (claude --continue).
#
#   bash claude_permanente.sh instalar     # tmux (conda, persistente) + Claude Code com binario em $PERSIST
#   bash claude_permanente.sh iniciar      # cria a sessao tmux "claude" (se ja existe, nao duplica)
#   bash claude_permanente.sh estado       # a sessao existe? mostra as ultimas linhas da tela do Claude
#   bash claude_permanente.sh mandar "texto"   # digita o texto no Claude e aperta Enter
#   bash claude_permanente.sh tela [N]     # ultimas N linhas da tela (padrao 60)
#   bash claude_permanente.sh reparar      # conserta ~/.claude.json invalido e tira o Claude da tela de erro
#   bash claude_permanente.sh parar        # encerra a sessao tmux (e o laco de reinicio)
#
# Para usar o Claude interativamente: Terminal do Jupyter ->  tmux attach -t claude
#   (sair sem encerrar: Ctrl+B e depois D)
#
# Limite: nada sobrevive ao DESLIGAMENTO do servidor do Jupyter (Stop My Server / desligamento por
# ociosidade). Depois disso: rode "instalar" (rapido, so refaz links) e "iniciar" de novo.
set -uo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
source "$AQUI/ambiente.sh"
SESSAO=${SESSAO:-claude}
PP="$PERSIST/.claude_persist"
CMD_CLAUDE=${CMD_CLAUDE:-claude}     # para testes: CMD_CLAUDE="bash"

ativar_tmux() {
  command -v tmux >/dev/null 2>&1 && return 0
  [ -x "$ENVDIR/ferramentas/bin/tmux" ] && { export PATH="$ENVDIR/ferramentas/bin:$PATH"; return 0; }
  return 1
}

json_ok() { [ -s "$1" ] && python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" >/dev/null 2>&1; }

# garante que $PP/.claude.json e JSON valido: recupera a copia valida mais recente (.antigo.*) ou usa {}
reparar_json() {
  local alvo="$PP/.claude.json" c
  if json_ok "$alvo" && [ "$(tr -d '[:space:]' < "$alvo")" != "{}" ]; then return 0; fi   # valido e nao vazio
  [ -e "$alvo" ] && cp "$alvo" "$alvo.invalido.$(date +%s)" 2>/dev/null
  for c in $(ls -t "$HOME"/.claude.json.antigo.* "$PP"/.claude.json.backup* "$HOME"/.claude/backups/.claude.json* 2>/dev/null); do
    if json_ok "$c"; then cp "$c" "$alvo"; echo "config recuperada de $c"; return 0; fi
  done
  json_ok "$alvo" && return 0                       # ja era {} e nao ha copia melhor
  echo '{}' > "$alvo"; echo "nenhuma copia valida encontrada: .claude.json recriado como {} (o Claude refaz o assistente inicial; o login em .claude/ e mantido)"
}

links_claude() {
  mkdir -p "$PP/.claude" "$PP/local_share_claude" "$HOME/.local/share" "$HOME/.local/bin"
  [ -s "$PP/.claude.json" ] || echo '{}' > "$PP/.claude.json"
  # login/config: se ja houver um ~/.claude real (ex.: login feito antes dos links), junta na area persistente
  if [ -d "$HOME/.claude" ] && [ ! -L "$HOME/.claude" ]; then
    cp -an "$HOME/.claude/." "$PP/.claude/" 2>/dev/null; mv "$HOME/.claude" "$HOME/.claude.antigo.$(date +%s)"
  fi
  if [ -f "$HOME/.claude.json" ] && [ ! -L "$HOME/.claude.json" ]; then
    if json_ok "$HOME/.claude.json" && ! json_ok "$PP/.claude.json" || [ "$(cat "$PP/.claude.json" 2>/dev/null)" = "{}" ]; then
      json_ok "$HOME/.claude.json" && cp "$HOME/.claude.json" "$PP/.claude.json"
    fi
    mv "$HOME/.claude.json" "$HOME/.claude.json.antigo.$(date +%s)"
  fi
  [ -L "$HOME/.claude" ] || ln -s "$PP/.claude" "$HOME/.claude"
  [ -L "$HOME/.claude.json" ] || ln -s "$PP/.claude.json" "$HOME/.claude.json"
  # instalacao do Claude Code (binarios) persistente
  if [ ! -L "$HOME/.local/share/claude" ]; then
    [ -d "$HOME/.local/share/claude" ] && cp -a "$HOME/.local/share/claude/." "$PP/local_share_claude/" && rm -rf "$HOME/.local/share/claude"
    ln -s "$PP/local_share_claude" "$HOME/.local/share/claude"
  fi
  # o executavel ~/.local/bin/claude aponta para dentro de ~/.local/share/claude: refaz o link
  if [ -f "$PP/claude_bin_path" ] && [ -x "$(cat "$PP/claude_bin_path")" ] && [ ! -e "$HOME/.local/bin/claude" ]; then
    ln -s "$(cat "$PP/claude_bin_path")" "$HOME/.local/bin/claude"
  fi
  case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) export PATH="$HOME/.local/bin:$PATH" ;; esac
  reparar_json
}

case "${1:-ajuda}" in
  instalar)
    links_claude
    if ! ativar_tmux; then
      echo "instalando tmux em $ENVDIR/ferramentas (conda-forge)..."
      usar_env ferramentas tmux >/dev/null && conda deactivate >/dev/null 2>&1 || true
      ativar_tmux || { echo "ERRO: nao consegui instalar o tmux" >&2; exit 1; }
    fi
    echo "tmux: $(command -v tmux) ($(tmux -V))"
    if command -v claude >/dev/null 2>&1 && claude --version >/dev/null 2>&1; then
      echo "Claude Code ja instalado: $(command -v claude) -> $(readlink -f "$(command -v claude)")"
    else
      echo "instalando o Claude Code (instalador oficial)..."
      curl -fsSL https://claude.ai/install.sh | bash || { echo "ERRO no instalador" >&2; exit 1; }
    fi
    B=$(readlink -f "$HOME/.local/bin/claude" 2>/dev/null || true)
    if [ -n "$B" ] && [ -x "$B" ]; then
      echo "$B" > "$PP/claude_bin_path"
      case "$B" in "$PP"/*|"$HOME/.local/share/claude"/*) echo "binario persistente: $B";;
        *) echo "AVISO: o binario ficou fora da area persistente ($B); apos reinicio rode 'instalar' de novo";; esac
      claude --version 2>/dev/null | head -1
    else echo "AVISO: ~/.local/bin/claude nao encontrado apos a instalacao" >&2; fi
    echo "login e configuracao em: $PP (links em $HOME/.claude e $HOME/.claude.json)"
    ;;
  iniciar)
    links_claude
    ativar_tmux || { echo "ERRO: sem tmux. Rode: bash claude_permanente.sh instalar" >&2; exit 1; }
    command -v "${CMD_CLAUDE%% *}" >/dev/null 2>&1 || { echo "ERRO: '$CMD_CLAUDE' nao encontrado. Rode: bash claude_permanente.sh instalar" >&2; exit 1; }
    if tmux has-session -t "$SESSAO" 2>/dev/null; then echo "sessao '$SESSAO' ja existe (nao dupliquei)"; exit 0; fi
    mkdir -p "$AQUI/logs"
    L="$AQUI/logs/claude_laco.sh"
    cat > "$L" <<LACO
#!/bin/bash
cd "$AQUI"
source restaurar.sh >/dev/null 2>&1
export PATH="$HOME/.local/bin:\$PATH"
while true; do
  echo "[\$(date -u +%FT%TZ)] iniciando $CMD_CLAUDE" >> "$AQUI/logs/claude_permanente.log"
  $CMD_CLAUDE --continue 2>/dev/null || $CMD_CLAUDE
  echo "[\$(date -u +%FT%TZ)] saiu (codigo \$?); reinicia em 10 s -- para parar: bash claude_permanente.sh parar" | tee -a "$AQUI/logs/claude_permanente.log"
  sleep 10
done
LACO
    tmux new-session -d -s "$SESSAO" -x 200 -y 50 -c "$AQUI" "bash $L"
    sleep 2
    tmux has-session -t "$SESSAO" 2>/dev/null && echo "sessao '$SESSAO' iniciada. Para usar: Terminal -> tmux attach -t $SESSAO (sair: Ctrl+B, D)" \
      || { echo "ERRO: a sessao nao subiu" >&2; exit 1; }
    ;;
  estado)
    ativar_tmux || { echo "sem tmux (rode instalar)"; exit 0; }
    if tmux has-session -t "$SESSAO" 2>/dev/null; then
      echo "sessao '$SESSAO': ATIVA"; tmux list-panes -t "$SESSAO" -F '  processo: #{pane_current_command}  pid #{pane_pid}'
      tail -n 3 "$AQUI/logs/claude_permanente.log" 2>/dev/null | sed 's/^/  /' || true
      echo "---- tela (ultimas 25 linhas) ----"
      TELA=$(tmux capture-pane -p -t "$SESSAO" 2>/dev/null | grep -v '^[[:space:]]*$' | tail -n 25 || true)
      [ -n "$TELA" ] && echo "$TELA" || echo "(tela vazia: o Claude pode estar abrindo; ou use: tmux attach -t $SESSAO)"
    else echo "sessao '$SESSAO': NAO existe (rode: bash claude_permanente.sh iniciar)"; fi
    exit 0 ;;
  tela)
    ativar_tmux || { echo "sem tmux"; exit 0; }
    tmux has-session -t "$SESSAO" 2>/dev/null || { echo "sessao '$SESSAO' nao existe"; exit 0; }
    tmux capture-pane -p -S -500 -t "$SESSAO" 2>/dev/null | grep -v '^[[:space:]]*$' | tail -n "${2:-60}" || true
    exit 0 ;;
  mandar)
    shift; MSG="$*"; [ -n "$MSG" ] || { echo "uso: bash claude_permanente.sh mandar \"texto\"" >&2; exit 1; }
    ativar_tmux && tmux has-session -t "$SESSAO" 2>/dev/null || { echo "sessao '$SESSAO' nao existe" >&2; exit 1; }
    tmux send-keys -t "$SESSAO" -l "$MSG"; sleep 0.5; tmux send-keys -t "$SESSAO" Enter
    echo "enviado. Veja a resposta em alguns segundos: bash claude_permanente.sh tela"
    ;;
  reparar)
    links_claude
    if ativar_tmux && tmux has-session -t "$SESSAO" 2>/dev/null; then
      if tmux capture-pane -p -t "$SESSAO" 2>/dev/null | grep -q "Configuration error"; then
        tmux send-keys -t "$SESSAO" Enter     # opcao 1 "Exit and fix manually" (ja selecionada): o laco reinicia em 10 s
        echo "tela de erro fechada; o Claude reinicia em ~10 s com a config corrigida (veja: bash claude_permanente.sh estado)"
      fi
    fi
    exit 0 ;;
  parar)
    ativar_tmux && tmux kill-session -t "$SESSAO" 2>/dev/null && echo "sessao '$SESSAO' encerrada" || echo "nao havia sessao '$SESSAO'" ;;
  *) sed -n '2,17p' "$0" ;;
esac
