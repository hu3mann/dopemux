#!/usr/bin/env bash
# Dopemux locale/bootstrap script
# Ensures a UTF-8 locale and installs Python deps.

set -euo pipefail

# Default locale values
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"

# Create virtualenv if not present
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Upgrade pip and install project with dev extras
pip install --upgrade pip
pip install -e .

cat <<MSG
[OK] Environment ready.
Activate with 'source $VENV_DIR/bin/activate'.
MSG
