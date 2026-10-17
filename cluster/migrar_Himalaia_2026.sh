#!/bin/bash
# Migra a base do vlab de /home/jovyan/privado/mesoescala-montanhas (nome errado: e o projeto do livro)
# para /home/jovyan/privado/Himalaia_2026, como C:\Users\haas\github\Himalaia_2026.
# O cache do Drive passa de vlab_cache/{entrada,saida} para vlab_cache/Himalaia_2026/{entrada,saida}
# (a mudanca no Drive ja foi feita pelo computador do pesquisador).
#
# Uso (no vlab):  bash migrar_Himalaia_2026.sh
#
# O que faz, nesta ordem (para se algo der errado):
#   1. recusa se houver CM1 rodando
#   2. encerra as sessoes tmux "claude" e "sentinela" (elas apontam para o caminho antigo)
#   3. move a pasta (nada e apagado; execucoes/, cm1/run/cm1.exe e resultados vao junto)
#   4. move o historico do Claude Code para a chave do caminho novo (para o --continue achar a conversa)
#   5. baixa o pacote novo do Drive (caminhos corrigidos) e extrai por cima
#   6. reinicia o Claude (tmux) e a sentinela
set -uo pipefail
P=/home/jovyan/privado
A=$P/mesoescala-montanhas
N=$P/Himalaia_2026
export RCLONE_CONFIG=$P/.config/rclone/rclone.conf
export PATH="$P/conda_envs/cm1pos/bin:$P/conda_envs/ferramentas/bin:$HOME/.local/bin:$PATH"

echo "== 1. CM1 rodando?"
if pgrep -x cm1.exe >/dev/null; then echo "ERRO: ha cm1.exe rodando; espere terminar antes de migrar" >&2; exit 1; fi
echo "   nenhum"

echo "== 2. encerrando sessoes tmux"
for s in sentinela claude; do tmux kill-session -t "$s" 2>/dev/null && echo "   $s encerrada" || echo "   $s nao estava ativa"; done

echo "== 3. movendo a pasta"
if [ -d "$A" ] && [ ! -e "$N" ]; then mv "$A" "$N" && echo "   $A -> $N"
elif [ -d "$N" ] && [ ! -e "$A" ]; then echo "   ja migrado ($N existe)"
elif [ -d "$A" ] && [ -d "$N" ]; then echo "ERRO: existem as duas pastas ($A e $N); nao mexi. Decida qual manter." >&2; exit 1
else echo "ERRO: nem $A nem $N existem" >&2; exit 1; fi

echo "== 4. historico do Claude Code"
PJ=$P/.claude_persist/.claude/projects
if [ -d "$PJ" ]; then
  for d in "$PJ"/*mesoescala-montanhas*; do
    [ -e "$d" ] || continue
    novo="${d//mesoescala-montanhas/Himalaia-2026}"
    if [ ! -e "$novo" ]; then mv "$d" "$novo" && echo "   $(basename "$d") -> $(basename "$novo")"; else echo "   $(basename "$novo") ja existe (mantido)"; fi
  done
else echo "   (sem historico)"; fi

echo "== 5. pacote novo do Drive"
cd "$N"
rclone copy gdrive:vlab_cache/Himalaia_2026/entrada/toro_cm1_lhende_vlab.tar.gz . 2>&1 | grep -v client_id || true
rclone copy gdrive:vlab_cache/Himalaia_2026/entrada/toro_cm1_lhende_vlab.tar.gz.sha256 . 2>&1 | grep -v client_id || true
sha256sum -c toro_cm1_lhende_vlab.tar.gz.sha256 || { echo "ERRO: sha256 do pacote nao confere; parei antes de extrair" >&2; exit 1; }
tar xzf toro_cm1_lhende_vlab.tar.gz --overwrite
for nb in toro_cm1_vlab.ipynb claude_vlab.ipynb; do cp "$N/toro_cm1_lhende/$nb" "$P/$nb" && echo "   notebook atualizado: $P/$nb"; done
grep -c mesoescala-montanhas toro_cm1_lhende/*.sh toro_cm1_lhende/CLAUDE.md 2>/dev/null | grep -v ':0' && echo "AVISO: ainda ha nome antigo" || echo "   pacote sem o nome antigo"

echo "== 6. reiniciando Claude e sentinela"
cd "$N/toro_cm1_lhende"
bash claude_permanente.sh iniciar
bash claude_permanente.sh sentinela
echo
echo "PRONTO. Base: $N/toro_cm1_lhende"
echo "Notebooks novos em $P/ (os antigos com o caminho errado podem ser apagados)."
