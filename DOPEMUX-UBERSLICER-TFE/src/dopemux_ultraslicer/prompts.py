# [OK] File 1/8 — src/prompts.py
# This file dynamically loads all ritual prompts (schema, extract, merge, audit, filth, etc) directly from the canonical `/data/system/prompts/` directory.
# No hardcoding: always loads the latest on disk. 
# If a prompt is missing, escalate with a #filth warning.

import os

# Prompts now live in the repository level `prompts/` directory rather than
# `data/system/prompts`.  Resolve the path relative to this file so that the
# loader works regardless of where the repo is cloned.
PROMPT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'prompts')

PROMPT_FILES = {
    "extract": "TFE-FND-ULTRA-RITUAL.txt",
    "schema": "TFE-SCHEMA.txt",
    "devlog": "TFE-DEVLOG.txt",
    "outputs": "TFE-OUTPUTS.txt",
    "metafile": "TFE-METAFILE.txt",
    "audit": "TFE-AUDIT-ULTRA-RITUAL.txt",
    "index": "TFE-INDEX.txt",
    "design_patterns": "TFE-DESIGN-PATTERNS.txt",
    "user_custom": "TFE-USER-CUSTOM.txt",
    "instructions": "TFE-INSTRUCTIONS.dmpx",
}

def load_prompt(name):
    filename = PROMPT_FILES.get(name)
    if not filename:
        raise ValueError(f"[FILTH] Unknown prompt requested: {name}")
    filepath = os.path.join(PROMPT_DIR, filename)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"[FILTH] Prompt file missing: {filepath} (did you unzip the system files?)")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# Example: extract_prompt = load_prompt("extract")
# Use load_prompt() to fetch prompts as needed in other modules.

if __name__ == "__main__":
    # Demo: Print out the schema prompt (ritual check)
    print("========== [SCHEMA PROMPT] ==========")
    print(load_prompt("schema"))

# [OK] — src/prompts.py is ready for dopemux ritual block integration.
# Next: `src/extract.py` (L1 orchestrator).
