#!/usr/bin/env zsh
# ---------------------------------------------------------------------------
# Dump a full manifest + concatenated file contents for the local uberslicer
# project.  Run from anywhere inside the repo.
#
# Outputs:
#   ./uberslicer-manifest.yaml   # list of files, sizes, sha256
#   ./uberslicer-all.txt         # full source with file markers
#
# Usage:
#   chmod +x scripts/dump-uberslicer.zsh
#   scripts/dump-uberslicer.zsh
# ---------------------------------------------------------------------------

set -euo pipefail

# ─── Resolve repo root & target dir ────────────────────────────────────────
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
UBER_DIR="${REPO_ROOT}/uberslicer"

if [[ ! -d "${UBER_DIR}" ]]; then
  echo "❌  No uberslicer/ directory found under ${REPO_ROOT}"
  exit 1
fi

MANIFEST="${REPO_ROOT}/uberslicer-manifest.yaml"
CONTENT_FILE="${REPO_ROOT}/uberslicer-all.txt"

# ─── Collect files (skip __pycache__ + *.pyc) ──────────────────────────────
files=($(find "${UBER_DIR}" -type f \
          ! -path "*/__pycache__/*" ! -name "*.pyc" | sort))

# ─── Build manifest YAML ───────────────────────────────────────────────────
{
  echo "# generated $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo "files:"
  for f in "${files[@]}"; do
    rel="${f#$REPO_ROOT/}"
    size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f")
    hash=$(shasum -a 256 "$f" | awk '{print $1}')
    printf "  - path: \"%s\"\n    size: %s\n    sha256: \"%s\"\n" "$rel" "$size" "$hash"
  done
} >| "${MANIFEST}"

# ─── Concatenate contents with markers ─────────────────────────────────────
{
  for f in "${files[@]}"; do
    rel="${f#$REPO_ROOT/}"
    echo "##### >>> BEGIN FILE: ${rel} <<< #####"
    command cat "$f"
    echo "\n##### <<< END FILE:   ${rel} <<< #####\n"
  done
} >| "${CONTENT_FILE}"

echo "[OK] Manifest saved  →  ${MANIFEST}"
echo "[OK] Full dump saved →  ${CONTENT_FILE}"
echo "[OK] ${#files[@]} files processed from ${UBER_DIR}"
