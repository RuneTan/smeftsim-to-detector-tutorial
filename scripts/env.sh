# Load the complete tutorial environment into this Bash terminal.
export TUTORIAL_HOME="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export TUTORIAL_ROOT="$TUTORIAL_HOME/.venv-unified/lib/python3.12/site-packages/ROOT"
export PATH="$TUTORIAL_HOME/bin:$TUTORIAL_HOME/.venv-unified/bin:$TUTORIAL_ROOT/bin:$PATH"
export LD_LIBRARY_PATH="$TUTORIAL_HOME/tools/delphes:$TUTORIAL_ROOT/lib:$TUTORIAL_ROOT/../root.libs:$TUTORIAL_HOME/tools/system-libs/usr/lib/x86_64-linux-gnu"
export ROOT_INCLUDE_PATH="$TUTORIAL_HOME/tools/delphes:$TUTORIAL_HOME/tools/delphes/external"
export UV_CACHE_DIR="$TUTORIAL_HOME/tools/cache"
export UV_PYTHON_INSTALL_DIR="$TUTORIAL_HOME/tools/python"
export UV_PYTHON_BIN_DIR="$TUTORIAL_HOME/tools/bin"
export PYTHONNOUSERSITE=1
