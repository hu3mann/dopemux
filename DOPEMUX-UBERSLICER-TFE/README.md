# 💊 DØPEMÜX ULTRASLICER v1.4.0

## Ritual Summary
- Schema-locked chunking, filth escalation, dopamine hits.
- CLI: `python -m dopemux_ultraslicer <input_file> <output_dir>`
- Terminal: `zsh dopemux_terminal.zsh`

## Installation
```bash
pip install -e .
```

## File Law
- Every run is autopatched to devlog/audit.
- All outputs are YAML ritual blocks.
- See metafile/schema for compliance.

## Commands
- `extract <file> <outdir>`: Slice & tag file to ritual blocks.
- `audit <file>`: Log an audit event.
- `dopamine_hit`: Log a dopamine hit event.
- `exit`: Leave ritual terminal.

## Reference Manifest
`scripts/update-reference.zsh` regenerates `manifest.json`, `all-files.md`, and updates `state.yaml`.
The hook runs automatically via `pre-commit` and during the build process.
Run it manually with:
```bash
zsh scripts/update-reference.zsh
```
Install the git hook with:
```bash
pre-commit install
```

### Updating state via ChatGPT
`scripts/update-state-from-gpt.py` can update `state.yaml` by summarizing `manifest.json` with OpenAI's API.

## Do not break ritual law. All memory. No mercy.
