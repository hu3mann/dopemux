#!/usr/bin/env zsh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# Activate venv if it exists
if [[ -d "$REPO_ROOT/.venv" ]]; then
  source "$REPO_ROOT/.venv/bin/activate"
fi

# Generate manifest and concatenated markdown using the relocated scripts
python3 "$SCRIPT_DIR/generate-manifest.py" "$REPO_ROOT" -o "$REPO_ROOT/manifest.json" --all-md "$REPO_ROOT/all-files.md"

# Update state.yaml with current repo info
python3 "$SCRIPT_DIR/update-state.py"

