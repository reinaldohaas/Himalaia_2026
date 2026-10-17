#!/bin/bash
# Gera relatorio_vlab.txt (estado das execucoes, para verificacao independente) e, com --enviar,
# copia para gdrive:vlab_cache/Himalaia_2026/saida/toro_cm1_lhende/relatorios/  -> G:\Meu Drive\vlab_cache\Himalaia_2026\saida\... no Windows.
# Uso:  bash relatorio.sh [--enviar]
set -uo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
source "$AQUI/ambiente.sh"
cd "$AQUI"
OUT="$AQUI/relatorio_vlab.txt"
{
  echo "relatorio_vlab  $(date -u +%FT%TZ)  host=$(hostname)"
  echo "== pacote: $(sha256sum "$PERSIST/Himalaia_2026/toro_cm1_lhende_vlab.tar.gz" 2>/dev/null | cut -c1-16)  manifesto:"
  sha256sum -c --quiet MANIFESTO.sha256 2>&1 | grep -v -E "cm1/run|execucoes|logs|resultados|relatorio|MUDANCAS" | head -5 || true
  echo "   (linhas acima = arquivos do pacote alterados; vazio = entradas intactas)"
  echo "== recursos"; bash rodar_direto.sh recursos 2>&1
  echo "== cm1.exe"; sha256sum cm1/run/cm1.exe 2>&1; cat cm1/run/cm1.env 2>/dev/null; grep -m1 "compilador\|GNU Fortran" cm1/compilacao.log 2>/dev/null
  echo "== fila"; bash rodar_direto.sh estado 2>&1
  for d in execucoes/*/; do [ -d "$d" ] || continue
    echo "== $d"; cat "$d/execucao.info" 2>/dev/null; tail -n 2 "$d/cm1.print.out" 2>/dev/null
    ls -l "$d"/cm1out_s.dat "$d"/cm1out_stats.dat 2>/dev/null | awk '{print "   ",$5,$9}'
  done
  echo "== MUDANCAS.md"; cat MUDANCAS.md 2>/dev/null || echo "(nao existe)"
} > "$OUT" 2>&1
echo "gerado: $OUT ($(wc -l < "$OUT") linhas)"
if [ "${1:-}" = "--enviar" ]; then
  command -v rclone >/dev/null 2>&1 || export PATH="$ENVDIR/cm1pos/bin:$PATH"
  command -v rclone >/dev/null 2>&1 || { echo "ERRO: rclone nao encontrado; NADA foi enviado (rode: bash gdrive.sh instalar)" >&2; exit 1; }
  ALVO="gdrive:vlab_cache/Himalaia_2026/saida/toro_cm1_lhende/relatorios"
  COPIA="$AQUI/relatorio_vlab_$(date +%Y%m%d_%H%M).txt"; cp "$OUT" "$COPIA"
  if LOGR=$(rclone copy "$COPIA" "$ALVO/" 2>&1); then
    if rclone lsf "$ALVO/" 2>/dev/null | grep -qx "$(basename "$COPIA")"; then
      echo "enviado e conferido: $ALVO/$(basename "$COPIA")"
      echo "Windows: G:\Meu Drive\vlab_cache\Himalaia_2026\saida\toro_cm1_lhende\relatorios\\"
    else echo "ERRO: o rclone nao acusou erro, mas o arquivo nao aparece em $ALVO" >&2; exit 1; fi
  else
    echo "ERRO: falha no envio; NADA foi enviado:" >&2; echo "$LOGR" | grep -v client_id >&2; exit 1
  fi
fi
