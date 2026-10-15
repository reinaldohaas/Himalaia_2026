# Carregado (source) pelos scripts do pacote. Define onde as coisas ficam no vlab.
#
# O vlab e um conteiner (JupyterHub) rodando como root com HOME=/root; /root pode ser
# APAGADO quando o servidor reinicia. O que precisa sobreviver vai para PERSIST:
#   PERSIST      /home/jovyan/privado (se existir e for gravavel), senao /home/jovyan, senao $HOME
#   ENVDIR       $PERSIST/conda_envs        ambientes conda criados pelo pacote (cm1, cm1pos)
#   RCLONE_CONFIG $PERSIST/.config/rclone/rclone.conf   (o token do Drive fica so ai)
#   GH_CONFIG_DIR $PERSIST/.config/gh
# Qualquer um pode ser sobrescrito exportando a variavel antes.

if [ -z "${PERSIST:-}" ]; then
  if [ -d /home/jovyan/privado ] && [ -w /home/jovyan/privado ]; then PERSIST=/home/jovyan/privado
  elif [ -d /home/jovyan ] && [ -w /home/jovyan ]; then PERSIST=/home/jovyan
  else PERSIST=$HOME; fi
fi
export PERSIST
export ENVDIR=${ENVDIR:-$PERSIST/conda_envs}
export RCLONE_CONFIG=${RCLONE_CONFIG:-$PERSIST/.config/rclone/rclone.conf}
export GH_CONFIG_DIR=${GH_CONFIG_DIR:-$PERSIST/.config/gh}          # login do gh (alternativa GitHub Release)
mkdir -p "$(dirname "$RCLONE_CONFIG")" 2>/dev/null || true

# devolve o caminho de um mamba/conda utilizavel
achar_conda() {
  local c
  for c in "$(command -v mamba 2>/dev/null)" "$(command -v conda 2>/dev/null)" "${CONDA_EXE:-}" \
           "$PERSIST/miniforge3/bin/mamba" "$HOME/miniforge3/bin/mamba" "$HOME/anaconda3/bin/conda" \
           /opt/conda/bin/conda /home/jovyan/anaconda3/bin/conda; do
    [ -n "$c" ] && [ -x "$c" ] && { echo "$c"; return 0; }
  done
  return 1
}

# usar_env <nome> <pacotes...> : cria (se preciso) o ambiente em $ENVDIR/<nome> e ativa
usar_env() {
  local nome=$1; shift
  local M base
  M=$(achar_conda) || { echo "ERRO: conda/mamba nao encontrado (instale o Miniforge em $PERSIST/miniforge3)" >&2; return 1; }
  base=$("$M" info --base 2>/dev/null | tail -1) || true
  [ -n "$base" ] && [ -f "$base/etc/profile.d/conda.sh" ] || base=$(dirname "$(dirname "$M")")
  # shellcheck disable=SC1091
  source "$base/etc/profile.d/conda.sh"
  if [ ! -d "$ENVDIR/$nome/conda-meta" ]; then
    echo "criando ambiente $ENVDIR/$nome ..." >&2
    "$M" create -y -p "$ENVDIR/$nome" -c conda-forge "$@" >&2
  fi
  conda activate "$ENVDIR/$nome"
}

# garantir <nome_env> <comando> <pacote> : instala o pacote no ambiente se o comando faltar
garantir() {
  command -v "$2" >/dev/null 2>&1 && return 0
  local M; M=$(achar_conda)
  "$M" install -y -p "$ENVDIR/$1" -c conda-forge "$3" >&2
  conda activate "$ENVDIR/$1"
}
