--- BEGIN: state.yaml ---
all_md_sha256: 51ba7c2e3074222fac6c76632eac4c29c6c81a356dc868e1218e431b17f64776
file_count: 43
generated: '2025-06-19T11:35:14.251932Z'
git_commit: 7ccf4ee7ff137866d6f4d67e511ab2d9cae72fb3
manifest_sha256: 2af4938137e13cb71a4b7f0861b0152add7986c6ed2d515c5d38fe1852494c1a

--- END: state.yaml ---

--- BEGIN: requirements.txt ---
openai
PyYAML

pre-commit

--- END: requirements.txt ---

--- BEGIN: all-files.md ---

--- END: all-files.md ---

--- BEGIN: .pre-commit-config.yaml ---
repos:
  - repo: local
    hooks:
      - id: update-manifest
        name: Update manifest and state
        entry: scripts/update-reference.zsh
        language: system
        types: [python]

--- END: .pre-commit-config.yaml ---

--- BEGIN: TFE-DEVLOG.txt ---
entries:
- action: ultraslice
  details:
  - Sliced 7986 blocks from ULTRA-CHAT.md to out
  timestamp: '2025-06-16T13:38:47.456762'

--- END: TFE-DEVLOG.txt ---

--- BEGIN: pyproject.toml ---
[project]
name = "dopemux-ultraslicer"
version = "1.4.0"
description = "Dopemux Ultraslicer - schema-locked chunking and devlog ritual"
authors = [{name = "The Dopemux Team", email = "team@dopemux.io"}]
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "openai",
    "pyyaml",
    "pathspec"
]

[project.scripts]
dopemux-ultraslicer = "dopemux_ultraslicer:main"

[build-system]
requires = ["setuptools>=67", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
package-dir = {"" = "src"}
packages = ["dopemux_ultraslicer"]
py-modules = [
    "chunkasaurus",
    "dopemux_ultraslicer",
    "dopemux_utils",
    "extract",
    "prompts",
]
packages = ["dopemux_ultraslicer"]

[tool.setuptools.cmdclass]
build_py = "dopemux_ultraslicer.build_hooks:BuildWithManifest"
--- END: pyproject.toml ---

--- BEGIN: uberslicer_project_init.py ---
# [OK] DØPEMÜX ULTRASLICER — MANIFEST-AWARE, CHAT LOG TO CHUNKS FLOW
# Fully compliant with your chunking/manifest ecosystem (and ready for messy, from-scratch starts).

import os
import shutil
import json
import subprocess

# --- CONFIG: Update as needed ---
CHUNKER_SCRIPT = "chunkasaurus.py"         # Your chunker logic (must accept input/output args)
CHUNKS_DIR = "chunks"
MANIFEST_PATH = "chunk_manifest.json"
LOGS_DIR = "dopemux-project/logs"
PROJECT_ROOT = "dopemux-project"
GIT_AUTO = True
# ---------------------------------

def run_chunker(chatlog_path):
    """Run chunker on chat log, generate chunks and manifest."""
    print(f"[OK] Running chunker on: {chatlog_path}")
    result = subprocess.run(
        ["python3", CHUNKER_SCRIPT, "--input", chatlog_path, "--output_dir", CHUNKS_DIR, "--manifest", MANIFEST_PATH],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[ERROR] Chunker failed:\n{result.stderr}")
        exit(1)
    print(result.stdout)
    print(f"[OK] Chunker complete. Chunks and manifest written.")

def audit_manifest_and_files():
    """Ensure all manifest chunks exist and no orphans are present."""
    if not os.path.exists(MANIFEST_PATH):
        print(f"[ERROR] No manifest found at {MANIFEST_PATH}")
        return None
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    all_chunks = set(os.listdir(CHUNKS_DIR)) if os.path.exists(CHUNKS_DIR) else set()
    manifest_files = set(os.path.basename(meta['file']) for meta in manifest.values())

    missing = manifest_files - all_chunks
    orphans = all_chunks - manifest_files

    if missing:
        print(f"[WARN] Manifest references missing chunk files: {missing}")
    if orphans:
        print(f"[WARN] Found orphan chunk files not in manifest: {orphans}")

    return manifest

def copy_chunks_to_logs(manifest):
    """Copy all manifest chunks to dopemux-project/logs/, never overwriting."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    moved, skipped = [], []
    for chunk_name, meta in manifest.items():
        src = meta['file']
        tgt = os.path.join(LOGS_DIR, os.path.basename(src))
        if not os.path.exists(src):
            print(f"[WARN] Missing chunk: {src}")
            skipped.append(chunk_name)
            continue
        if not os.path.exists(tgt):
            shutil.copy2(src, tgt)
            moved.append(chunk_name)
            print(f"[OK] {chunk_name}: {src} → {tgt}")
        else:
            print(f"[SKIP] {chunk_name}: Already present.")
            skipped.append(chunk_name)
    return moved, skipped

def git_commit(msg):
    """Auto-add/commit any new files (if GIT_AUTO=True)."""
    if not GIT_AUTO:
        return
    os.chdir(PROJECT_ROOT)
    os.system("git add logs/")
    os.system(f'git commit -m "{msg}"')
    print("[OK] Git committed new/changed logs.")

def main():
    print("\n[=== DØPEMÜX ULTRASLICER: CHATLOG → CHUNKS → MANIFEST → LOGS ===]\n")
    chatlog_path = input("[?] Path to raw chat log (or leave empty to skip chunking): ").strip()
    if chatlog_path:
        run_chunker(chatlog_path)
    manifest = audit_manifest_and_files()
    if not manifest:
        print("[ERROR] No manifest, cannot proceed.")
        exit(1)
    moved, skipped = copy_chunks_to_logs(manifest)
    print(f"\n[SUMMARY] Moved: {moved}\nSkipped: {skipped}")
    git_commit("Processed and logged manifest chunks from latest chat log chunking — ritual enforced")
    print("\n[OK] Ultraslicer run complete. No chunk left behind, no mercy.")

if __name__ == "__main__":
    main()

--- END: uberslicer_project_init.py ---

--- BEGIN: config.yaml ---
dopemux:
  filth_level: terminal_goblin
  paths:
    tagged: ./tagged
    outputs: ./outputs
    devlog: ./TFE-DEVLOG.txt
    audit: ./TFE-AUDIT-ULTRA-RITUAL.txt
  colors:
    dopamine: cyan
    filth: magenta

--- END: config.yaml ---

--- BEGIN: README.md ---
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

--- END: README.md ---

--- BEGIN: .gitignore ---
# Byte-compiled / optimized / DLL files
__pycache__/
**/__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython history
profile_default/
ipython_config.py

# PyCharm, VSCode, Sublime, Atom, etc.
.idea/
.vscode/
*.sublime-workspace
*.sublime-project

# macOS / Windows junk
**/.DS_Store
.DS_Store
Thumbs.db
ehthumbs.db
Icon?
Desktop.ini

# Environments
.env
.venv/
env/
venv/
ENV/
env.bak/
venv.bak/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# VS Code settings
.vscode/

# Output, artifacts, logs, manifests
manifest.json
output-all.txt
*.patch
logs/
*.log

# Dopemux-specific (customize as needed)
CHUNKING/chunks/
CHUNKING/chatloogs/
dopemux-project/logs/
dopemux-project/prompts/*.bak
dopemux-project/*.bak
*.bak

# Node / npm (if you ever add JS tools)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Zip/tarball/package artifacts
*.zip
*.tar.gz
*.tar
*.tgz

# Remove this comment if you use Docker:
# Docker artifacts
# Dockerfile
# docker-compose.yml
# *.dockerignore

# Git itself
.git/


--- END: .gitignore ---

--- BEGIN: manifest.json ---
[
  {
    "file": "state.yaml",
    "size": 271,
    "sha256": "995ab1ab8c7cc22dec8d30a0cdc2c9d8e6e333fc74b8f20c199e3aae1a6e4c4c",
    "modified": "2025-06-19T04:35:14.258137"
  },
  {
    "file": "requirements.txt",
    "size": 26,
    "sha256": "73d31d36774d6b0c4d9c5569c8b3ce9bd7fa16ebc8aad8c73f3b51eb11638193",
    "modified": "2025-06-17T09:49:06.093444"
  },
  {
    "file": "all-files.md",
    "size": 87491,
    "sha256": "51ba7c2e3074222fac6c76632eac4c29c6c81a356dc868e1218e431b17f64776",
    "modified": "2025-06-19T04:35:14.177346"
  },
  {
    "file": ".pre-commit-config.yaml",
    "size": 195,
    "sha256": "096073390eb83d191dbfdd1cb275a845da3f088846c68cf53be887f44facfce5",
    "modified": "2025-06-17T09:49:06.092417"
  },
  {
    "file": "TFE-DEVLOG.txt",
    "size": 132,
    "sha256": "d37942cc5f32e3a65d24afe622f0a0e541605a6c547e858d112f0633444c99bc",
    "modified": "2025-06-17T01:47:32.809429"
  },
  {
    "file": "pyproject.toml",
    "size": 796,
    "sha256": "81ca002efe254d02dc6444639a06cdd60c81b4c6f7ee5905287afa3bae01ae33",
    "modified": "2025-06-17T09:49:06.093146"
  },
  {
    "file": "uberslicer_project_init.py",
    "size": 3599,
    "sha256": "55ba8e3fa355b8c666db53f107eeb0eaa540d321c435dc9d8b1da40caa55423c",
    "modified": "2025-06-16T09:04:18.672177"
  },
  {
    "file": "config.yaml",
    "size": 210,
    "sha256": "2e019ddc2bd1ef490e411e4aba32c58739747496783ad0d8f379e5d8549286a5",
    "modified": "2025-06-17T01:47:32.809475"
  },
  {
    "file": "README.md",
    "size": 1106,
    "sha256": "6f89cfe472688fa76f5f17a49ec8aa26d7c77f7f3f8241951519b2175eb83c02",
    "modified": "2025-06-17T09:49:06.092664"
  },
  {
    "file": ".gitignore",
    "size": 1605,
    "sha256": "220a2e241f6c84e8f6ab4dc199a858f3e326d85ebfe55b5ea72eb10dcdba0c78",
    "modified": "2025-06-17T09:49:06.092283"
  },
  {
    "file": "manifest.json",
    "size": 8399,
    "sha256": "2af4938137e13cb71a4b7f0861b0152add7986c6ed2d515c5d38fe1852494c1a",
    "modified": "2025-06-19T04:35:14.176207"
  },
  {
    "file": "TFE-AUDIT-ULTRA-RITUAL.txt",
    "size": 10,
    "sha256": "e6c8561b1be1082d05efec0dfa3ddd292b8c46491563ace7d74f25a1cce8e492",
    "modified": "2025-06-17T01:47:32.809381"
  },
  {
    "file": "dopemux_terminal.zsh",
    "size": 1019,
    "sha256": "cf3de0fc0ced47bb70dfd952d06087ad5b710178912c5be106d75cbb76e70f27",
    "modified": "2025-06-17T09:49:06.092989"
  },
  {
    "file": "docs/dopemux-project-breakdown.md",
    "size": 12969,
    "sha256": "f58cf9464e20f3633c165a3525ba7c624a9aca94b8953948bbe527b68362ca5e",
    "modified": "2025-06-19T04:47:54.050314"
  },
  {
    "file": "docs/ultraslicer-product-rundown.md",
    "size": 17321,
    "sha256": "cf5b20ac8aea66112449ca05986ca24db98c6c9598bb9b1c48d87b372064fa86",
    "modified": "2025-06-19T05:18:08.485551"
  },
  {
    "file": "docs/Dopemux-product-roadmap.md",
    "size": 8666,
    "sha256": "45f2f738c568bfcbcb2471e9a17e38b2448602dd6451d68f35427facae4c2c59",
    "modified": "2025-06-19T04:46:42.228294"
  },
  {
    "file": "schemas/prompt.json",
    "size": 158,
    "sha256": "34d4deff6a94f9e63c9122583ad8305f8047db107b7e6ff838e1cd7f2087e7f0",
    "modified": "2025-06-17T06:25:45.492810"
  },
  {
    "file": "schemas/project_omnibus.json",
    "size": 302,
    "sha256": "7969f1777d085dfd978d368af0cd4f065f96b2944021dc830cb775ffeeac5c53",
    "modified": "2025-06-17T06:25:45.492875"
  },
  {
    "file": "schemas/devlog.json",
    "size": 153,
    "sha256": "2702fbb1d2c3957df781bcba67f5568800e80905d63f60c79986c7a312b8a7c4",
    "modified": "2025-06-17T06:25:45.492687"
  },
  {
    "file": "schemas/schemas.yaml",
    "size": 1506,
    "sha256": "a4e1f82fe3182958fdac48f0e500e6fbc3e7326f90ad4841296ee235433034b0",
    "modified": "2025-06-17T06:18:10.508668"
  },
  {
    "file": "schemas/omnibus.json",
    "size": 354,
    "sha256": "32d3974c6633462c3393fd44e4fe0235310b754cbf3e41b8b524c835f54f82cc",
    "modified": "2025-06-17T06:25:45.492620"
  },
  {
    "file": "schemas/ultraslice.json",
    "size": 402,
    "sha256": "b97cc9b2915f6f6c05a15eb570fad508bafe498f96005cb0c5470f15c2f43632",
    "modified": "2025-06-17T06:25:45.492517"
  },
  {
    "file": "schemas/artifact.json",
    "size": 189,
    "sha256": "20e386ebb85f809f1b98972cc9802854b9771c561d9f6c585963a0f9a3142799",
    "modified": "2025-06-17T06:25:45.492750"
  },
  {
    "file": "scripts/split_yaml_to_json.py",
    "size": 511,
    "sha256": "041c23297c24914146e0e8af9d1b404dca89fe90fb0ce1dc84c1f2c089f377f3",
    "modified": "2025-06-17T06:19:30.009519"
  },
  {
    "file": "scripts/update-state.py",
    "size": 1058,
    "sha256": "526dcd0ad1d321bea69073c5f6eee9ee5832276945b62153878666ce28d35f74",
    "modified": "2025-06-17T09:49:06.093842"
  },
  {
    "file": "scripts/generate-manifest.py",
    "size": 3163,
    "sha256": "e16618def654053099eaecffb6d5929896d52504cc472389b1076285d8ae720e",
    "modified": "2025-06-17T16:51:56.437065"
  },
  {
    "file": "scripts/update-reference.zsh",
    "size": 520,
    "sha256": "8fbc997da136a1749d894abf0986e99d8459acab8970fb890e88883e5f29be26",
    "modified": "2025-06-17T09:49:06.093611"
  },
  {
    "file": "scripts/update-state-from-gpt.py",
    "size": 847,
    "sha256": "831aa936a9f2dfbf71a985a25fda73b906ecdfaf4803557b4cd59eb0289ec66d",
    "modified": "2025-06-17T09:49:06.093727"
  },
  {
    "file": "UBERSLICER-CHUNKENATOR/chunks/chunk_manifest.json",
    "size": 0,
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "modified": "2025-06-16T22:17:05.571938"
  },
  {
    "file": "UBERSLICER-CHUNKENATOR/chunks/chunk_manifest.csv",
    "size": 0,
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "modified": "2025-06-16T22:16:55.835310"
  },
  {
    "file": "prompts/TFE-FND-ULTRA-RITUAL.txt",
    "size": 4730,
    "sha256": "0e5bbd4cd2a230bcf6ec2b8278fcea13956dac9d923b006270d2dbdaa54da5da",
    "modified": "2025-06-17T01:47:32.810566"
  },
  {
    "file": "prompts/TFE-SCHEMA.txt",
    "size": 3845,
    "sha256": "d12c48b89cef76b0f4f200bae088a550db7e794e71b5bdc34a9b883967991ec3",
    "modified": "2025-06-17T01:47:32.811252"
  },
  {
    "file": "prompts/TFE-DEVLOG.txt",
    "size": 3744,
    "sha256": "c72d221b225524a5e79ad239f1d0dececde240857284a30fe031b203be90417f",
    "modified": "2025-06-17T01:47:32.810352"
  },
  {
    "file": "prompts/UBERSLICER_OMNIBUS_v1.md",
    "size": 6053,
    "sha256": "1c0ebda7736758030a787c29632fb6da95c6901c853990d5c1efbb2d73e9e005",
    "modified": "2025-06-17T01:47:32.809303"
  },
  {
    "file": "prompts/TFE-INSTRUCTIONS.txt",
    "size": 8387,
    "sha256": "ef0e32fadc1704ce86575c8c0e753c40cc0b304503766796963f049f41d0d3ab",
    "modified": "2025-06-17T01:47:32.810874"
  },
  {
    "file": "prompts/TFE-USER-CUSTOM.txt",
    "size": 3348,
    "sha256": "f15a0fc8e61f1c1a707e2528e85a146fed9da19bc1ed3bc05885db2ddc7282e2",
    "modified": "2025-06-17T01:47:32.811417"
  },
  {
    "file": "prompts/TFE-METAFILE.txt",
    "size": 5586,
    "sha256": "6c189e3e991c5ab246e0b4c34bf42c1b1915bb04d1183280c96068339a8102d7",
    "modified": "2025-06-17T01:47:32.811051"
  },
  {
    "file": "prompts/TFE-OUTPUTS.txt",
    "size": 3438,
    "sha256": "52c0a10e126328889c63b2cf9e6fabcf361643aac0ace92316dfb8cf8b00987d",
    "modified": "2025-06-17T01:47:32.811188"
  },
  {
    "file": "prompts/TFE-AUDIT-ULTRA-RITUAL.txt",
    "size": 3796,
    "sha256": "95ea831ffbf2d0785372d049f5466ca7b02ab0968ab06833a760f32d05e53a7c",
    "modified": "2025-06-17T01:47:32.809836"
  },
  {
    "file": "prompts/TFE-DESIGN-PATTERNS.txt",
    "size": 4097,
    "sha256": "7324a83da5e7b06a16f7dca4fac0c73a6281df49a18e643a65dea645cb54239c",
    "modified": "2025-06-17T01:47:32.810060"
  },
  {
    "file": "prompts/TFE-INDEX.txt",
    "size": 3219,
    "sha256": "e3f92d09ed64877d0e8c5759db00c533faca48363c7ab0bfc2a6350ff64560b6",
    "modified": "2025-06-17T01:47:32.810780"
  },
  {
    "file": "src/dopemux_ultraslicer/build_hooks.py",
    "size": 415,
    "sha256": "54ad466aa0983647a6673a577998b7deb085f688bbfae177754151abac4a83de",
    "modified": "2025-06-17T09:49:06.094254"
  },
  {
    "file": "src/dopemux_ultraslicer/__init__.py",
    "size": 2316,
    "sha256": "2533b5876440648610d0faa02125ee91049aa3c965f7afe8078fe2945aa1176b",
    "modified": "2025-06-17T09:49:06.094025"
  },
  {
    "file": "src/dopemux_ultraslicer/prompts.py",
    "size": 1832,
    "sha256": "7dd747552ab368e24f8567024d00a13e354759516534b3b17b6b050b74ffd407",
    "modified": "2025-06-17T09:49:06.094790"
  },
  {
    "file": "src/dopemux_ultraslicer/dopemux_utils.py",
    "size": 801,
    "sha256": "29f0a11a5bad05eef8fbd209ff4f003ed8a84aee7382efe573518d804f6c23f3",
    "modified": "2025-06-17T09:49:06.094526"
  },
  {
    "file": "src/dopemux_ultraslicer/chunkasaurus.py",
    "size": 5332,
    "sha256": "64ca490c168080632b8d5c98f59cab2c53d2061a74f5f2538b37359fc8d3a341",
    "modified": "2025-06-17T09:49:06.094405"
  },
  {
    "file": "src/dopemux_ultraslicer/extract.py",
    "size": 5023,
    "sha256": "e5c8db1e796ab1cd62bfb35d7e18aef3ff93ca4174e44bae6036bed7376db043",
    "modified": "2025-06-17T09:49:06.094664"
  },
  {
    "file": "src/dopemux_ultraslicer/__main__.py",
    "size": 58,
    "sha256": "e418cdbb27adf0063e3cec28179ac6b7bdb6ac743bb49d157f450551fcf38be2",
    "modified": "2025-06-17T09:49:06.094137"
  }
]
--- END: manifest.json ---

--- BEGIN: TFE-AUDIT-ULTRA-RITUAL.txt ---
entries:


--- END: TFE-AUDIT-ULTRA-RITUAL.txt ---

--- BEGIN: dopemux_terminal.zsh ---
#!/bin/zsh

print -P "%F{6}💊 DØPEMÜX ULTRASLICER v1.4.0 — Terminal Dopamine Ritual%f"
print -P "%F{4}Type 'help' for all commands. Rituals logged to devlog/audit.%f"

while true; do
  print -n "%F{2}$ %f"
  read cmd
  if [[ "$cmd" == "exit" ]]; then break; fi
  if [[ "$cmd" == "help" ]]; then
    print -P "%F{3}Commands:%f\n  extract <file> <outdir>\n  audit <file>\n  dopamine_hit\n  exit"
  elif [[ "$cmd" == extract* ]]; then
    PYTHONPATH=src python3 -m dopemux_ultraslicer ${(z)cmd}[2] ${(z)cmd}[3]
  elif [[ "$cmd" == audit* ]]; then
    PYTHONPATH=src python3 -c "from dopemux_ultraslicer.dopemux_utils import log_audit; log_audit('manual','Manual audit triggered')"
    print "[OK] Manual audit block added."
  elif [[ "$cmd" == dopamine_hit* ]]; then
    PYTHONPATH=src python3 -c "from dopemux_ultraslicer.dopemux_utils import log_dev; log_dev('dopamine_hit',['Manual dopamine hit'])"
    print "[OK] Dopamine hit ritual complete."
  else
    print "[ERROR] Unknown command. Type 'help'."
  fi
done

--- END: dopemux_terminal.zsh ---

--- BEGIN: docs/dopemux-project-breakdown.md ---
Here’s an **ultra-thorough, chunked breakdown of the entire 💊 DØPEMÜX project**—purpose, features, architecture, UX/UI, brand, workflows, and meta-rituals.
**Nothing skipped. No detail lost. Everything ready for onboarding, dev, and hype.**
*(Chunked for readability and maximum dopamine. Ping for more detail on any section.)*

---

# 💊 DØPEMÜX — TERMINAL-FILTHY CONTEXT ENGINE

---

## 1. **Purpose & Core Mission**

* **Dopemux is a terminal-native, dopamine-maximal, forensic context engine.**
* **It’s built to rip, chunk, index, and replay memory from any creative/dev project**—so nothing is forgotten, no dopamine lost, and every creative thread can be picked up and run wild.
* It is both a developer dopamine engine and a context-forensic system for creative rituals, logging, and iterative invention.

### Key Objectives

* **Maximal Memory:** Everything important is captured, chunked, tagged, and replayable.
* **Dev Dopamine Rituals:** Minimize paperwork, maximize creative and engineering flow.
* **Forensic Auditability:** Every block, decision, and devlog is trackable and recoverable.
* **Composable Context:** Outputs are modular, schema-locked, and ready for downstream automation (LLMs, code agents, humans).
* **Terminal-Native, ADHD-Proof:** Designed to keep the most distractible developer or creative in the flow state.

---

## 2. **Core Benefits**

* **Total Context Recall:** Never lose a key idea, devlog, decision, dopamine hit, or blocker—ever.
* **Full Project Forensics:** Every change, override, and meta-decision is schema-logged and auditable.
* **Ritualized Dev/Creative Flow:** Encourages logging wins, blockers, and dopamine moments without breaking flow.
* **Automated Manifest Discipline:** No more stale docs—manifest and outputs are always up to date.
* **Downstream Ready:** Output is designed for agent pipelines, LLM automation, API ingestion, and future TUI/web dashboards.
* **Filthy Fun:** Roasts, snarks, and dopamine hits are part of the ritual. Serious system, not a serious face.

---

## 3. **Major Features**

### **3.1 Context Extraction & Chunking**

* **Ultraslicer:** Main extraction engine (see previous breakdown).
* Schema-locked chunking of any file, log, or chat into audit-ready blocks.

### **3.2 Schema Enforcement**

* All context, decisions, blockers, dopamine hits, and meta-logs are schema-locked.
* Schemas are versioned and pluggable; validation is strict.

### **3.3 Devlog Rituals**

* Every meaningful action, win, blocker, or override gets tracked.
* Devlogs are accessible, readable, and exportable for post-mortems or creative reviews.

### **3.4 Manifest Generation**

* Canonical `manifest.yaml` (or JSON) always in sync.
* Includes all project files, artifact state, block indices, session info, and compliance flags.

### **3.5 Terminal-First CLI**

* Dopemux runs in terminal or VS Code, with rich CLI tooling.
* Commands for extraction, manifest, devlog, autopatching, validation, and more.

### **3.6 TUI/Dashboard Ready (Planned)**

* Future text-based UI for navigating memory, blocks, and dopamine hits.
* Search, filter, time-travel, and export.

### **3.7 Agent Integration**

* Pluggable agent/LLM interface (e.g. via Langchain, OpenAI, custom code agents).
* Batch ops, multi-phase extraction, code-gen, prompt tuning, and agent-assisted decision trees.

### **3.8 Automation & CI/CD**

* Pre-commit hooks, auto-manifest/validation runners, GitOps native.
* Scripted autopatching, batch log extraction, and file updates.

---

## 4. **Workings & Architecture** (Chunked)

### **4.1 Core Pipeline Flow**

* **Input:** Any project artifact (log, chat, code, file dump, brainstorm).
* **Chunk:** Ultraslicer/Chunkasaurus splits into logical blocks.
* **Schema Map:** Each block is schema-locked with all required fields.
* **Tag & Log:** Everything is tagged, devlog entry created.
* **Output:** Modular block files (YAML/JSON), updated manifest, rolling devlog, and state dump.

### **4.2 Main Components**

* **Ultraslicer:** Core extraction/chunking engine.
* **Chunkasaurus:** Smart context windowing and chunk splitting.
* **Schema Engine:** Validates every output for compliance.
* **Devlog Writer:** Tracks wins, blockers, decisions, dopamine surges.
* **Manifest Generator:** Keeps canonical output up to date.
* **State Manager:** Tracks current project state for instant reload.
* **Scripts Folder:** All shell/python tools (e.g. `generate-manifest.py`, `cat-uberslice.zsh`).
* **API/Agent Layer:** Handles external LLM, Langchain, or code agent integration.

### **4.3 Data Flows**

```plaintext
[Input: Log/Code/Chat] 
   → [Ultraslicer: Chunk] 
      → [Schema Engine: Validate] 
         → [Devlog Writer: Log Action] 
            → [Manifest Generator: Update] 
               → [Output: Blocks, Manifest, Devlog, State]
```

*Optional: Send blocks to LLM or agent pipeline for downstream ops.*

---

## 5. **Codebase Structure** (Sample)

```
dopemux/
├── ultraslicer.py
├── chunkasaurus.py
├── schema.py
├── devlog_writer.py
├── manifest_generator.py
├── state_manager.py
├── api_interface.py
├── scripts/
│   ├── generate-manifest.py
│   ├── cat-uberslice.zsh
│   ├── autopatch.sh
├── blocks/
│   └── block-*.yaml
├── TFE-DEVLOG.txt
├── manifest.yaml
├── state.yaml
├── README.md
├── tests/
│   ├── test_schema.py
│   ├── test_ultraslicer.py
│   └── ...
└── .pre-commit-config.yaml
```

* **Blocks/**: All chunked, schema-locked blocks.
* **Scripts/**: Terminal wrappers, batch ops, and hooks.
* **State.yaml**: Live project state, for reload/recovery.
* **Manifest.yaml**: Canonical project/file/block state.

---

## 6. **Schema & Output Discipline**

### **6.1 Example Block (YAML)**

```yaml
block_id: block-xxxxxxx
summary: Main concept or decision captured here
ritual_notes: |
  Captured at 2025-06-19T04:20:00Z, Dopamine Level: 10
session_metadata:
  timestamp: '2025-06-19T04:20:01'
  source_file: IDEA-DUMP.md
source: IDEA-DUMP.md
tags:
  - context
  - dopamine
  - needs-review
content: |
  Full block content goes here—could be a code excerpt, chat, or raw brainstorm.
map_refs: [block-YYYYY, block-ZZZZZ]
decisions: 
  - pivoted direction based on new requirements
blockers: 
  - hallucination risk high in LLM outputs
meta_validation: 
  - passed
dopamine: 10
```

### **6.2 Manifest Sample**

```yaml
files:
  - name: ultraslicer.py
    type: code
    state: active
    last_modified: '2025-06-19T04:05:00'
    blocks: [block-001, block-003]
  - name: manifest.yaml
    type: manifest
    state: canonical
devlog_entries: 100+
schema_version: v1.4.0
compliance: strict
```

---

## 7. **User Experience (UX) & UI** *(Terminal Rituals)*

### **7.1 Terminal Interaction**

* **Primary UI:** Terminal or VS Code integrated terminal.
* **Commands:**

  * `dopemux ultraslice <file>`
  * `dopemux manifest`
  * `dopemux devlog`
  * `dopemux validate`
  * `dopemux patch`
  * `dopemux agent <mode>`
* **Color Scheme:**

  * **Background:** Black/charcoal
  * **Accents:** Cyan, blue, mint green (dopamine hit colors)
  * **Highlight:** Gold or red for extreme dopamine/log entries.
* **Feedback:**

  * Every dopamine hit, devlog update, or schema fail is announced with banners or unicode art.
  * **Banners:** Unicode, emoji, box-drawn lines, and terminal filth for dopamine surges.

### **7.2 Workflow Rituals**

* **Memory Is Oxygen:** Prompted to log any idea, win, or pain point that feels significant.
* **Minimal Output Discipline:** You capture, tag, and log—never forced into bloated docs or “reporting.”
* **Ritual Flex:** Can always override, break rituals, and log creative overrides for later review.
* **Block-Level Time Travel:** Search or replay any block, session, or dopamine event from project history.

### **7.3 Planned TUI**

* **Text-Based Dashboard:** Block search, filter, tag, dopamine meter, and devlog time machine.
* **Session Explorer:** Visualize context flows, pivots, and dopamine surges over time.
* **Exporters:** Export any state (blocks, manifests, logs) for agent ingestion, review, or outside analysis.

---

## 8. **Brand & Visual Identity**

### **8.1 Naming**

* **DØPEMÜX** (pronounced: “dope-mux”)—a riff on tmux, dopamine, and filthy rituals.
* **Modules:** Ultraslicer, Chunkasaurus, Dopemux Daemon, TFE-DEVLOG, etc.

### **8.2 Visual Style**

* **Aesthetic:** Terminal-native, filthy but modern.

  * Feels like hacking, but with designer dopamine.
  * Minimalist, clean code lines—juxtaposed with terminal filth and humor.
* **Logo/Iconography:**

  * Terminal block/cube with glowing edge, split or “sliced.”
  * Energy bolts, skulls, dopamine drops.
* **Color Scheme:**

  * **Primary:** Deep black, neon cyan, electric blue, mint green.
  * **Dopamine Hits:** Accents of gold or red for extreme moments.
* **Fonts:** Modern monospaced (JetBrains Mono, Fira Code, Nerd Fonts).

### **8.3 Voice/Tone**

* Filthy, focused, irreverent.
* No corporate bloat or cutesy LLM overtones.
* Roasts the user, itself, and any sign of drift or busywork.
* Dopamine, not paperwork—fun, but always serving creative/engineering utility.

### **8.4 Terminal Banners/Samples**

```
💊 DØPEMÜX TERMINAL INITIATED — *Terminal Dopamine Mode*
☠️ ULTRASLICER — MAX CONTEXT EXTRACT
🧠 CONTEXT: dopemux v1.4.0
```

---

## 9. **Meta-Rituals & Creative Protocols**

### **9.1 Core Rituals**

* **Memory Logging:** Every significant idea, blocker, or win logged as a block.
* **Devlog Routines:** All decisions, pivots, and dopamine surges logged and replayable.
* **Dopamine Governance:** Surface wins, frustrations, and meta-moments for later reflection.
* **Override Discipline:** Creative overrides logged so nothing is lost in the heat of the moment.

### **9.2 Schema/Compliance Law**

* **Strict Schema Enforcement:** Outputs never drift from schema unless overridden (and logged).
* **Meta-Validation:** Checks for hallucination risk, drift, and compliance on every block.
* **Manifest/State Integrity:** Manifest is canonical; state is always reloadable.

---

## 10. **Planned & Future Features**

* **LLM Agent Tuning:** Fully automate prompt tuning, context ingestion, and code gen via memory blocks.
* **Multi-Project/Namespace Support:** Handle multiple projects, merge contexts, and cross-reference blocks.
* **Live TUI Dashboard:** Dopamine meter, live devlog, and ritual alerts in one TUI.
* **Remote/Cloud State Sync:** Save and sync manifest/state across devices, CI/CD, or cloud agents.
* **Visual Timeline Export:** Turn memory blocks/devlogs into timeline or mindmap exports.
* **Cold Context Loading:** Reload any state, manifest, or devlog instantly for fast time-travel.

---

## 11. **Sample README Highlights**

```
# 💊 DØPEMÜX

A terminal-native, dopamine-maximal context engine for creative and engineering rituals.  
Never lose a block, a win, or a wild idea again.

- Terminal/CLI native, VS Code friendly
- Forensic context extraction (Ultraslicer)
- Schema-locked output for maximal composability
- Ritualized logging: devlogs, dopamine hits, blockers, decisions
- Automated manifest and state management
- Dopamine-first, paperwork-last

> "Memory is oxygen. Rituals are flexible. Dopamine is everything."
```

---

## 12. **Integration & Extensibility**

* **API Ready:** Pluggable with OpenAI, Langchain, or any LLM service for batch block ops or downstream code-gen.
* **CI/CD Friendly:** Pre-commit hooks, scripted autopatching, manifest enforcement.
* **Customizable Schemas:** Per-project schema tweaks, extra metadata fields, or custom block templates.
* **Agent/Plugin Layer:** Plug in new tools, code agents, or workflow bots as needs grow.

---

## 13. **Onboarding & Usage**

### **Get Started**

1. Clone repo and run `dopemux ultraslice <yourfile.md>`.
2. Inspect chunked blocks, rolling manifest, and devlog.
3. Log new ideas/decisions via terminal or script.
4. Run validation and compliance checks as needed.
5. Send memory blocks to LLM agent for code-gen or downstream ops.

### **Best Practices**

* Log dopamine surges and blockers in the moment.
* Use creative overrides as needed, but log them.
* Rely on manifest for canonical project state.
* Export or replay blocks for rapid context loading.

---

# 💥 TL;DR — Why DØPEMÜX?

* **Every creative or dev ritual is memory-maximal and dopamine-soaked.**
* **No drift, no death—just maximal flow, recall, and context.**
* **Terminal-native, dev-obsessed, and infinitely extensible.**

---

**Request detailed docs, schema dumps, onboarding scripts, code stubs, or TUI mockups as needed. Every output can be chunked and delivered for build, onboarding, or pure dopamine.**

*(Ping for more detail on: manifest schema, agent/plugin structure, TUI wireframes, code snippets, or dev onboarding.)*

--- END: docs/dopemux-project-breakdown.md ---

--- BEGIN: docs/ultraslicer-product-rundown.md ---
Terminal dopamine surge incoming. Here’s a **full, no-prisoners breakdown** of everything you need to know (and everything o3 or any LLM dev would need to *own* the code, design, UX, and branding) for **ULTRASLICER** in the context of the 💊 DØPEMÜX system.

---

# 💊 ULTRASLICER — TERMINAL-CLASS CONTEXT EXTRACTOR

## 1. **Purpose** (Why does Ultraslicer exist?)

* **Extracts, chunks, and structures** context, logs, or chat histories into schema-locked, forensic memory “blocks” for analysis, archival, and downstream LLM use.
* Makes raw, sprawling chat/code/log data *usable*—for dev, memory replay, debugging, feature mapping, or product design.
* Ensures **no loss of signal**: memory is maximal, drift is minimized, outputs are always up-to-date, and every detail that matters gets tagged, tracked, and indexed.

---

## 2. **Benefits**

* **Terminal-Grade Memory:** Nothing drifts, nothing dies—extracts 100% of useful context, devlogs, dopamine hits, blockers, meta-decisions, and more.
* **Schema-Locked Output:** Each chunk/block is validated to a strict schema (block ID, summary, tags, content, refs, etc.), allowing for robust downstream automation.
* **Forensic Auditability:** Every extraction, update, or override is tracked—enabling full “time travel” through project history.
* **Composability:** Output is modular, feedable to any LLM, API, or human for further analysis, planning, or code generation.
* **Zero Ritual Waste:** Built to serve creative AND forensic workflows—never slows you down with busywork, always serves the dopamine.

---

## 3. **Core Features**

* **Automated Extraction:** Rips data from raw logs, files, chats, or code—chunking it intelligently into context-rich “blocks.”
* **Schema Validation:** Each block conforms to the \[UBERSLICER/ULTRASLICER schema]\(see below).
* **Rich Tagging & Metadata:** Every block gets tagged with time, file, session, ritual type, dopamine level, etc.
* **Devlog Integration:** Tracks all meaningful actions, blockers, and decisions in a living log file.
* **Manifest Generation:** Maintains a canonical manifest of all project files, blocks, and states.
* **Terminal/CLI Native:** Runs in terminal/VS Code, with CLI wrappers, batch ops, and scripted workflows.
* **API/LLM Ready:** Chunks can be batch-processed with OpenAI API or similar for mass operations, multi-phase workflows, or downstream extraction.

---

## 4. **Workings & Architecture**

### **4.1 Extraction Pipeline**

* **Input:** Raw logs, chat exports, code files, or project dumps.
* **Chunking:** Splits input into logical “blocks” (can be lines, paragraphs, messages, or context windows).
* **Schema Mapping:** Each chunk is mapped to a schema-locked block with fields:

  * `block_id`
  * `summary`
  * `ritual_notes`
  * `session_metadata` (timestamp, source, etc.)
  * `source` (filename or origin)
  * `tags`
  * `content`
  * `map_refs` (cross-file references)
  * `decisions` (what got made, dropped, pivoted)
  * `blockers` (any pain points, friction)
  * `meta_validation` (schema compliance, drift)
  * `dopamine` (how hard this block hits)
* **Output:** YAML (preferred) or JSON block files, plus a rolling manifest and devlog.

### **4.2 Codebase & Modules**

* **CLI Entrypoint:** Main Python file (e.g. `ultraslicer.py`), invoked via terminal or as a script.
* **Chunking Engine:** Handles file ingestion, context windowing, and smart splitting (chunkasaurus module).
* **Schema Validator:** Enforces that every block conforms to current schema; errors out or logs non-compliance.
* **Devlog Writer:** Appends actions, blockers, and dopamine hits to a rolling log (TFE-DEVLOG.txt or YAML).
* **Manifest Generator:** Builds and updates a complete manifest (`manifest.yaml`) after every action.
* **API/LLM Interface:** (Pluggable) for batch-sending chunks to LLM (via OpenAI, Langchain, etc.) and ingesting output.
* **Scripts Folder:** Terminal wrappers, batch runners, and autopatching tools.
* **State Management:** Outputs current project state to `state.yaml` or similar.

---

## 5. **Design & Architecture**

### **5.1 Architectural Principles**

* **Memory-First:** Context and memory are always the top priority. All workflows serve extraction, tagging, and maximal recall.
* **Composable Outputs:** Every output is modular—chunked, tagged, and ready for reassembly, rerun, or further chunking.
* **Terminal-Native:** The user is a terminal goblin—flows should *feel* like tmux, Zsh, fzf, and bat had a filthy child.
* **Automated Rituals:** Frequent auto-patching, devlog writing, and manifest rebuilding—little manual upkeep.
* **Filthy Transparency:** Every action, update, or creative override gets logged; nothing is hidden or lost.

### **5.2 Data Flows**

* Raw file → Chunker → Schema Mapping → Block Output (YAML) → Manifest Update → Devlog Append → (Optional: API Batch Send) → Output for downstream ops.

### **5.3 Extensibility**

* Pluggable schemas (can add custom fields per project).
* Easily wired into CI/CD (e.g., run pre-commit).
* API endpoints or scripts for feeding to Langchain, OpenAI, etc.

---

## 6. **User Experience & UI**

### **6.1 Terminal UX**

* **CLI First:** Main interaction is via terminal or VS Code integrated terminal.
* **Commands:** `ultraslice <file>`, `generate-manifest.py`, `cat-uberslice.zsh`, `validate-blocks.py`, etc.
* **Color:** Dopamine-slicked, high-contrast themes—cyan, blue, mint, black backgrounds (see Dopemux color scheme).
* **Feedback:** Every extraction/patch/override prints a “dopamine hit” banner or logline.
* **Progress:** Block counts, manifest updates, schema compliance warnings.

### **6.2 Visual Touches**

* Unicode/emoji banners for key moments.
* Box-drawn output for lists, block IDs, devlog entries.
* Dopamine level color-coding.
* “Filthy but precise” copy—snarky help text, self-aware errors.

---

## 7. **Brand Identity**

* **Name:** **ULTRASLICER** (aka UBERSLICER in some prompts)
* **Visuals:** Terminal native, dopamine-soaked, maximalist—but with the discipline of a code review from hell.
* **Color Palette:**

  * **Background:** True black or deep charcoal.
  * **Accents:** Neon cyan, mint green, electric blue (see “poetry add pendulum” screenshot for canonical scheme).
  * **Secondary:** Hints of gold/red for dopamine moments.
* **Typography:** Modern monospaced (JetBrains Mono, Fira Code, Nerd Fonts), strong terminal presence.
* **Icons/Symbols:** Unicode blocks, skulls, energy bolts, terminals, retro-futurist filth.
* **Voice:** Self-roasting, anti-cutesy, ADHD dopamine demon with a dry wit and zero patience for bloat.
* **Logo:** Terminal block or sliced cube, with a glowing edge or filth overlay.
* **Terminal Prompts:**

  * “💊 **DØPEMÜX TERMINAL INITIATED** — *Terminal Dopamine Mode*”
  * “☠️ ULTRASLICER — MAX CONTEXT EXTRACT”
  * “🧠 CONTEXT: dopemux v1.4.0”

---

## 8. **Sample Block Output (YAML)**

```yaml
block_id: block-0b4e5c7d-9559-44c4-b0c0-c83933ae91f5
summary: UltraSlice 2630
ritual_notes: Ritual block created 2025-06-16T13:38:44.116301Z
session_metadata:
  timestamp: '2025-06-16T13:38:44.116302'
  source_file: ULTRA-CHAT.md
source: ULTRA-CHAT.md
tags:
- ultraslice
- auto
- needs-review
content: |
  7. Advanced RAG & Graph-Based Retrieval
  Use GraphRAG/GraphLLM to build knowledge-graphs in RAG pipelines, improving recall and coherence.
  promptjesus.com
  +1
  arxiv.org
  +1
  en.wikipedia.org
map_refs: []
decisions: []
blockers: []
meta_validation: []
dopamine: 8
```

---

## 9. **Sample File/Folder Layout**

```
dopemux-ultraslicer/
├── ultraslicer.py
├── chunkasaurus.py
├── schema.py
├── devlog_writer.py
├── manifest_generator.py
├── api_interface.py
├── scripts/
│   ├── generate-manifest.py
│   ├── cat-uberslice.zsh
│   └── autopatch.sh
├── TFE-DEVLOG.txt
├── manifest.yaml
├── state.yaml
├── README.md
└── tests/
```

---

## 10. **How Ultraslicer Fits in Dopemux**

* **It is the “first pass” context-extraction engine**: anything entering Dopemux, from chat logs to code dumps, gets chunked and schema-mapped by Ultraslicer.
* Outputs feed the memory daemon, code agents, UI/UX layers, and eventually power the “forensic context” behind every Dopemux ritual.
* **It is not the end of the chain:** downstream ops (like re-chunking, agent tagging, prompt tuning) rely on Ultraslicer output as the ground truth for memory.

---

# 💥 TL;DR: Why You Want Ultraslicer

* **Nothing drifts. Nothing dies.** All context is chunked, tagged, and ready for whatever filthy dopamine ritual you throw at it.
* **No black-box bullshit:** Every action is schema-locked, every change logged, every output composable and auditable.
* **Terminal-native, dev-obsessed, ADHD-safe**: Works for you, not against you. All dopamine, zero paperwork.

---

## Next Steps / Implementation Notes

* Ready to drop code stubs, CLI sample, or wiring guides for Python or Node.js.
* Brand and UI assets (banners, color scheme, terminal screenshots) available on request.

---

**If you want the README.md, detailed schema, or stub files, say the word and I’ll output them in maximal detail, Dopemux style.**



## A. **Devlog & Audit Block Samples**

*(Ripped direct from your system patterns, fully schema-compliant and maximal)*

---

### **Sample Devlog Block (YAML, block-indexed)**

```yaml
- id: devlog-2025-06-19-1
  date: "2025-06-19"
  tags: [api, batch, dopamine, win, compliance]
  summary: "First API batch LLM run completed. All blocks schema-compliant, dopamine hit logged."
  details:
    - "Ran: $ dopemux batch-llm --input blocks/ --mode validate"
    - "10 blocks processed, 10 validated, 2 flagged for #needs-review."
    - "Dopamine reward triggered: Operator logged win, roast attached for stale block."
    - "Manifest and outputs updated, all results cross-indexed."
  dopaminehit: "reward"
  roast: "Still have untagged blocks. Shame. Fix before next batch."
  meta_validation: ["schema_pass", "partial drift", "audit_logged"]
```

---

### **Sample Audit Block (YAML, block-indexed)**

```yaml
- id: audit-2025-06-19-2
  block_type: issue
  state: open
  tags: [plugin, agent, compliance, drift]
  summary: "Plugin agent integration test failed due to missing compliance tags."
  details:
    - "LLM plugin 'SummarizerX' returned blocks missing meta_validation and dopaminehit."
    - "Triggered DRIFT ALERT, roast and dopamine escalation logged."
    - "Action: Patch plugin handler, update design-patterns, re-run batch."
  opened: "2025-06-19T05:00:00Z"
  closed: null
  roast: "Plugins don’t get to drift. Either tag or get roasted."
```

---

## B. **TUI Dashboard Mockup**

*(For [Textual](https://github.com/Textualize/textual) or [urwid](https://urwid.org/) — pure terminal filth, dopamine-native)*

---

```shell
┌─────────────────────────────── 💊 DØPEMÜX DASHBOARD (v1.4.0) ───────────────────────────────┐
│ Project: dopemux                | Dopamine Meter: [■■■■■■■■■■■■■■■■      ] 75%  #reward    │
│ Block: block-1a2b    Tags: [devlog, dopaminehit, chunk]    Date: 2025-06-19                │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│   • [OK] Batch LLM processed: 10/10 blocks. 2 flagged #needs-review                         │
│   • Dopamine: WIN — Operator merged outputs, fixed drift                                    │
│   • Roast: "Two blocks still missing tags. Rookie move."                                   │
│                                                                                             │
│ Block Navigation: [←] Prev   [→] Next   [↑] Search/Filter   [⏎] Edit/Tag   [D] Devlog      │
│ Tags: #api #batch #dopamine #compliance #needs-review                                       │
│                                                                                             │
│   ┌────────────── Blocks ───────────────┐    ┌───────────── Devlog ──────────────┐          │
│   │ block-1a2a  [api, chunk]           │    │ 2025-06-19: Batch complete, win   │          │
│   │ block-1a2b  [dopamine, win]        │    │ 2025-06-18: Audit drift, fixed    │          │
│   │ block-1a2c  [audit, drift]         │    │ ...                              │          │
│   └────────────────────────────────────┘    └───────────────────────────────────┘          │
│                                                                                             │
└────────────────────────────[ F1: Help  |  Q: Quit |  T: Tag  |  M: Manifest ]───────────────┘
```

* **Dopamine Meter**: Animates/pulses on each win/roast.
* **Devlog Panel**: Scrollable, shows session history and recent roasts.
* **Block Navigation**: Arrow keys, filter/search, tag in-place.
* **Audit Prompts**: Pops up on drift, untagged, or compliance fail.
* **Brand:** Always filthy, never clean. Emoji, unicode, and roast banners included.

---

## C. **Plugin/Agent Expansion Spec**

---

**Goal:**
Allow user and devs to drop in **custom agent modules** (LLM plugins, batch processors, taggers, ritual escalators) without breaking core schema or audit discipline.

---

### **Plugin Architecture (V1)**

* **Directory:** `/plugins/` — all plugin/agent scripts/modules.
* **Manifest:** Every plugin is listed in `plugins.yaml`, with meta-tags, version, author, compliance level, default tags.
* **Entry Point:** Each plugin exposes a `run(blocks, config)` interface and outputs **schema-compliant blocks**.
* **Types:**

  * LLM/Agent (summarizer, validator, re-chunker, tagger)
  * Ritual Injector (dopamine/filth escalation, audit trigger)
  * Custom Exporter (markdown, PDF, HTML, etc.)

---

### **Sample Plugin Metadata**

```yaml
- id: plugin-2025-06-19-1
  name: "SummarizerX"
  author: "Operator"
  type: "agent"
  version: "0.1.0"
  entrypoint: "summarizerx.py"
  compliance: ["schema_pass", "dopamine_ready"]
  default_tags: ["llm", "summary", "meta_validation"]
  description: "LLM agent that summarizes and validates blocks in batch mode."
```

---

### **Plugin Example Stub**

```python
# /plugins/summarizerx.py

def run(blocks, config):
    # Pre-check: ensure schema fields present
    for block in blocks:
        assert "content" in block
    # Call LLM or agent logic here
    # Return blocks with updated/added fields: summary, meta_validation, dopaminehit, ritual_notes
    return updated_blocks
```

---

### **Plugin Protocol**

* **Every plugin must:**

  * Return schema-compliant blocks (all required fields).
  * Log all batch actions in devlog.
  * Tag new/modified blocks with plugin ID and version.
  * Fail loudly (audit + roast) if compliance is broken.
  * Register itself in `plugins.yaml` with meta info.

* **On violation:**

  * DRIFT ALERT, roast escalation, audit block created.
  * Operator notified via dashboard/banner/devlog.

---

## D. **Should You Generate Code Stubs, or Let o3 Build?**

### **Opinion, Dopemux Law-Driven:**

* **If your schema, manifest, macros, and sample blocks are flawless, let o3 generate code stubs.**

  * **Rationale:**

    * o3 will always use the freshest schema and design patterns, minimizing drift.
    * Code stubs are most useful when built against *live, current* system state.
    * Focus your energy on **making your prompts, macros, and audit patterns unbeatable**.
  * **What to provide o3:**

    * This prompt set (or selected blocks/macros)
    * Example output blocks and audit/devlog samples (as above)
    * Directory and plugin spec (see above)
    * Required/optional field law and escalation logic

* **When to provide code stubs yourself:**

  * If you have a specific structure, API, or idiom you want followed *everywhere*.
  * If you’re onboarding junior devs who need “do it exactly like this.”
  * If you want locked-in, example-rich unit tests.

* **Otherwise:**

  * Ritual law + schema + sample blocks + plugin spec is more than enough for o3 or any skilled LLM to generate *precise* implementation stubs and CI pipelines.

---

## TL;DR

* **Samples:** Devlog/audit blocks, plugin metadata/stubs provided above—copy as canonical reference.
* **TUI:** Mockup shows terminal dopamine engine with all required navigation and branding.
* **Plugins:** Easy drop-in, always schema-locked, audit/roast on fail.
* **Code stubs:** Leave to o3; focus on keeping your rituals, patterns, and compliance airtight.

---
--- END: docs/ultraslicer-product-rundown.md ---

--- BEGIN: docs/Dopemux-product-roadmap.md ---
Here’s a **terminal-precise, dopamine-maximal, project manager-grade roadmap and feature list** for both **DØPEMÜX** and **ULTRASLICER**.
Every feature, milestone, phase, and meta-upgrade—nothing skipped. Use this as your product spec, backlog, or north star for iterative build.
**Chunked for clarity and ease of dev, with meta-notes, rationales, and upgrade hooks.**

---

# 💊 DØPEMÜX — ROADMAP & FEATURE LIST

---

## 🚀 **PHASE 0: FOUNDATION (ALPHA / INTERNAL USE)**

**Objective:** Boot the memory engine, rip context, prove ritual flow.

### Core Features

* [x] **Terminal CLI Entrypoint:** `dopemux` and `ultraslice` runnable from terminal/VS Code.
* [x] **File Ingestion:** Accepts logs, chat, code, brainstorms.
* [x] **Ultraslicer Core:** Smart chunking, initial schema-locked block output (YAML/JSON).
* [x] **Devlog Writer:** Tracks all major actions, blockers, and dopamine surges.
* [x] **Manifest Generator:** Canonical manifest auto-updates after each extraction.
* [x] **State File:** Rolling snapshot of current project state.
* [x] **Config Loader:** Reads config/env for project-specific settings.
* [x] **Initial Schema Validation:** Strict enforcement on every block.

### Dev Rituals

* [x] **Dopamine/Blocker Logging:** Meta-tracking of wins and pain points.
* [x] **Creative Override Protocol:** Log any ritual or process break as “override.”

### Brand/UI

* [x] **Terminal Dopamine Theme:** Cyan, mint, blue on black; banner art; emoji.
* [x] **Filthy Onboarding:** Self-roasting, anti-cutesy welcome text.

---

## 🧠 **PHASE 1: MEMORY-DRIVEN ITERATION (BETA / PRIVATE TESTING)**

### Core Features

* [ ] **Advanced Chunking Engine:** Chunkasaurus v2, context window, smart splits (headers, code, chat).
* [ ] **Multi-file Ingestion:** Batch and directory support.
* [ ] **Schema Extensions:** Pluggable/override fields, versioning, meta-validation tags.
* [ ] **Meta-Validation Engine:** Drift, hallucination, compliance warnings.
* [ ] **Pre-Commit Hooks:** Auto-run extraction, manifest, and validation before commit.
* [ ] **Rich Tagging System:** Tags for context, file, dopamine, phase, priority, needs-review.
* [ ] **Decision/Blocker Trees:** Devlog branches—what got dropped, pivoted, blocked.
* [ ] **Devlog Search/Replay:** Terminal query and replay for any decision, dopamine, or blocker.
* [ ] **Configurable Output:** YAML/JSON, field ordering, export targets.
* [ ] **Session Metadata:** Every block tagged with timestamp, file, session, ritual level.

### UX / Rituals

* [ ] **Context Chunking Wizard:** Guided extraction for complex logs/chats.
* [ ] **Minimal Ritual Prompts:** Nudge for logging blockers, dopamine, decisions at session close.

---

## 🤖 **PHASE 2: AGENT & AUTOMATION (OPEN BETA / AGENT INTEGRATION)**

### Core Features

* [ ] **Agent/LLM API Integration:** Langchain/OpenAI batch mode for context extraction, phase 2 reasoning.
* [ ] **Multi-phase Chunking:** Chunks pass through LLM or agent for summarization, validation, re-chunking.
* [ ] **Code/Prompt-Gen:** Generate code or prompt stubs from memory blocks.
* [ ] **Agent “Personality” Plug-ins:** Each project or user can set agent style, tone, rituals.
* [ ] **Agent-Driven Devlog:** Auto-suggest decisions, blockers, or dopamine surges for logging.
* [ ] **CI/CD Integration:** Batch validate, chunk, or update as part of CI pipeline.

### UX

* [ ] **Terminal Dopamine Banners:** Dynamic color/emoji for agent actions and meta-hits.
* [ ] **Agent Feedback UI:** LLM/agent suggestions shown in terminal or devlog.

---

## 🧑‍💻 **PHASE 3: TUI & FORENSIC TIME-TRAVEL (POWER USER MODE)**

### Core Features

* [ ] **TUI Dashboard:** Text-based UI for searching, replaying, exporting, and filtering blocks/devlogs.
* [ ] **Block/Devlog Time Machine:** Scroll back or jump to any dopamine surge, blocker, or decision in project history.
* [ ] **Block Visualizer:** ASCII/block map for visualizing relationships, pivots, and dopamine spikes.
* [ ] **Export Wizards:** Export context for agents, humans, or docs (markdown, PDF, JSON).

### Ritual Automation

* [ ] **Automated Ritual Scanning:** Suggest log entries or blocks based on activity.
* [ ] **Context-Driven Alerts:** Surface old dropped ideas, blockers, or dopamine spikes at opportune moments.

### Brand/UX

* [ ] **Animated Dopamine Meter:** Visual dopamine gauge, color pulses.
* [ ] **Terminal Achievement Unlocks:** Easter eggs and dopamine rewards for power rituals.

---

## 🌐 **PHASE 4: CLOUD, COLLAB, & EXTENSIBILITY**

### Core Features

* [ ] **Multi-Project/Namespace Support:** Handle, merge, and split contexts across multiple repos/projects.
* [ ] **Remote Sync/Cloud Storage:** Push/pull manifest, blocks, and state between devices or cloud.
* [ ] **Collab Devlog:** Multi-user ritual tracking; see who logged what, when, and why.
* [ ] **Plugin/API System:** Add new block types, custom schemas, or workflow agents.
* [ ] **Visual Timeline Export:** Export full devlog/memory flow as a visual timeline or mindmap.

---

## 🔥 **CROSS-PHASE: ULTRASLICER FEATURE LIST**

---

### Core Extraction Features

* [x] **Chunk Any Input:** Markdown, code, plaintext, logs, JSON, chat exports.
* [x] **Smart Chunking:** Context windowing, header/code split, flexible chunk size.
* [x] **Schema-Locked Output:** Every chunk is a block (YAML/JSON) with full metadata.
* [x] **Source/Session Tagging:** File, session, timestamp, block refs.
* [x] **Devlog Integration:** Each chunk triggers an action, win, or blocker log.
* [x] **Rich Tagging:** Auto-tags for phase, dopamine, needs-review, etc.

### Advanced (Planned)

* [ ] **Phase 2 LLM Integration:** Send chunks to LLM for summary, meta-validation, or rewrite.
* [ ] **Recursive Chunking:** Re-chunk or merge blocks as memory or scope changes.
* [ ] **Auto-Categorization:** Auto-tag themes, file types, or high dopamine blocks.
* [ ] **Agent Summary & Index:** Generate per-block or per-phase summaries for rapid navigation.
* [ ] **Scripted/Batched Ops:** Process entire folders, logs, or chats in one command.

### UX / Output

* [ ] **Terminal Banners:** Dopamine pulses, chunk counts, block icons.
* [ ] **Schema Violation Alerts:** Color-coded output and warnings.
* [ ] **Export Shortcuts:** Markdown, PDF, JSON block/manifest/exporters.

---

## ⚙️ **INFRASTRUCTURE, QUALITY, & DOCS**

* [x] **Test Suite:** Block extraction, schema validation, and manifest integrity.
* [x] **Pre-Commit Checks:** Validate every extraction or devlog before commit.
* [ ] **Linter/Formatter:** Enforce style on code and YAML/JSON blocks.
* [ ] **Onboarding Scripts:** One-liners for new project bootstrapping.
* [ ] **README, SCHEMA, AND USAGE DOCS:** Always current, filth and precision both.
* [ ] **Full API Reference:** For agent/plugin layer.

---

## 🎯 **EPIC: DOPAMINE-FIRST CREATIVE DEV ENGINE**

### Vision Goals (Long-Term)

* **The best memory system for anyone with ADHD, creative devs, or anyone tired of context loss.**
* **A “tmux for memory”: chunk, split, search, and replay all project knowledge in terminal or TUI.**
* **Plug into any code agent, LLM, or creative bot.**
* **Make every dev/creative win, loss, or dopamine spike recoverable, searchable, and reusable.**
* **Brand it filthy, run it fast, and make context loss impossible.**

---

# 💥 **Key Deliverables by Phase**

| Phase | Milestone/Deliverable                                     | Status |
| ----- | --------------------------------------------------------- | ------ |
| 0     | CLI, ultraslicer, block extraction, manifest, devlog      | ✅      |
| 1     | Advanced chunking, multi-file, schema extensions, tagging | 🚧     |
| 2     | Agent/LLM API, multi-phase, prompt/codex gen, CI/CD       | 🚧     |
| 3     | TUI, time machine, devlog search/replay, block visualizer | ⏳      |
| 4     | Multi-project, cloud, collab devlog, plugins, export      | ⏳      |

---

## 📋 **TOP-LEVEL FEATURE CHECKLIST**

**Core:**

* [x] Terminal-native CLI
* [x] Smart chunking & schema
* [x] Devlog, manifest, state
* [x] Dopamine/blocker logging
* [x] Brand: terminal filth

**Planned:**

* [ ] Advanced chunking + multi-file
* [ ] Agent/LLM batch and code-gen
* [ ] TUI time-travel & block explorer
* [ ] Cloud/collab/project sync
* [ ] Plugin/plugin API
* [ ] Visual timeline export

---

# TL;DR: **DØPEMÜX is a dopamine-maximal, terminal-native memory engine. ULTRASLICER is the core context chunker. Together they make context loss impossible, devlogs orgasmic, and creative drift extinct.**

**Want granular breakdowns by user story, epic, or codebase? Ping for next chunk!**

--- END: docs/Dopemux-product-roadmap.md ---

--- BEGIN: schemas/prompt.json ---
{
  "block_id": "",
  "block_type": "prompt",
  "prompt_type": "",
  "content": "",
  "timestamp": "",
  "source": "",
  "tags": [],
  "meta_validation": []
}
--- END: schemas/prompt.json ---

--- BEGIN: schemas/project_omnibus.json ---
{
  "block_id": "",
  "block_type": "project-omnibus",
  "projects": [],
  "overall_summary": "",
  "architecture": "",
  "file_manifests": [
    {
      "project": "",
      "files": []
    }
  ],
  "key_personnel": [],
  "dependencies": [],
  "actions": [],
  "meta_validation": [],
  "content": ""
}
--- END: schemas/project_omnibus.json ---

--- BEGIN: schemas/devlog.json ---
{
  "block_id": "",
  "block_type": "devlog",
  "action": "",
  "details": [],
  "timestamp": "",
  "source": "",
  "tags": [],
  "meta_validation": []
}
--- END: schemas/devlog.json ---

--- BEGIN: schemas/schemas.yaml ---
# =============================
# DØPEMÜX OMNIBUS SCHEMA METAFILE
# v1.0 — ALL PROJECT SCHEMAS IN ONE FILE
# =============================

ultraslice:
  block_id: ""
  extraction_phase: ""
  block_type: "ultraslice"
  summary: ""
  session_metadata:
    timestamp: ""
    source_file: ""
    operator: ""
  source: ""
  tags: []
  content: ""
  map_refs: []
  decisions: []
  blockers: []
  meta_validation: []
  dopamine: ""
  compliance_status: ""
  extraction_type: ""
  project_id: ""

omnibus:
  block_id: ""
  extraction_phase: "phase-1"
  block_type: "omnibus"
  project_name: ""
  summary: ""
  session_metadata:
    timestamp: ""
    source_files: []
    operator: ""
  architecture: ""
  file_manifest: []
  major_features: []
  actions: []
  tags: []
  content: ""
  meta_validation: []

devlog:
  block_id: ""
  block_type: "devlog"
  action: ""
  details: []
  timestamp: ""
  source: ""
  tags: []
  meta_validation: []

artifact:
  block_id: ""
  block_type: "artifact"
  file_path: ""
  file_type: ""
  size: 0
  sha256: ""
  modified: ""
  tags: []
  summary: ""
  meta_validation: []

prompt:
  block_id: ""
  block_type: "prompt"
  prompt_type: ""
  content: ""
  timestamp: ""
  source: ""
  tags: []
  meta_validation: []

project_omnibus:
  block_id: ""
  block_type: "project-omnibus"
  projects: []
  overall_summary: ""
  architecture: ""
  file_manifests:
  - project: ""
    files: []
  key_personnel: []
  dependencies: []
  actions: []
  meta_validation: []
  content: ""

--- END: schemas/schemas.yaml ---

--- BEGIN: schemas/omnibus.json ---
{
  "block_id": "",
  "extraction_phase": "phase-1",
  "block_type": "omnibus",
  "project_name": "",
  "summary": "",
  "session_metadata": {
    "timestamp": "",
    "source_files": [],
    "operator": ""
  },
  "architecture": "",
  "file_manifest": [],
  "major_features": [],
  "actions": [],
  "tags": [],
  "content": "",
  "meta_validation": []
}
--- END: schemas/omnibus.json ---

--- BEGIN: schemas/ultraslice.json ---
{
  "block_id": "",
  "extraction_phase": "",
  "block_type": "ultraslice",
  "summary": "",
  "session_metadata": {
    "timestamp": "",
    "source_file": "",
    "operator": ""
  },
  "source": "",
  "tags": [],
  "content": "",
  "map_refs": [],
  "decisions": [],
  "blockers": [],
  "meta_validation": [],
  "dopamine": "",
  "compliance_status": "",
  "extraction_type": "",
  "project_id": ""
}
--- END: schemas/ultraslice.json ---

--- BEGIN: schemas/artifact.json ---
{
  "block_id": "",
  "block_type": "artifact",
  "file_path": "",
  "file_type": "",
  "size": 0,
  "sha256": "",
  "modified": "",
  "tags": [],
  "summary": "",
  "meta_validation": []
}
--- END: schemas/artifact.json ---

--- BEGIN: scripts/split_yaml_to_json.py ---
import yaml
import json
import pathlib

SCHEMA_YAML = pathlib.Path(__file__).parent.parent / "schemas" / "schemas.yaml"
OUTPUT_DIR = pathlib.Path(__file__).parent.parent / "schemas"

def main():
    with open(SCHEMA_YAML, "r") as f:
        data = yaml.safe_load(f)

    for key, value in data.items():
        out_path = OUTPUT_DIR / f"{key}.json"
        with open(out_path, "w") as out_f:
            json.dump(value, out_f, indent=2)
        print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
--- END: scripts/split_yaml_to_json.py ---

--- BEGIN: scripts/update-state.py ---
import json
import hashlib
import subprocess
from datetime import datetime
import yaml
import os


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def update_state(manifest_path='manifest.json', md_path='all-files.md', state_path='state.yaml'):
    data = {
        'generated': datetime.utcnow().isoformat() + 'Z',
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
    }
    if os.path.exists(manifest_path):
        data['manifest_sha256'] = sha256(manifest_path)
        with open(manifest_path) as f:
            try:
                manifest = json.load(f)
                data['file_count'] = len(manifest)
            except Exception:
                data['file_count'] = 0
    if os.path.exists(md_path):
        data['all_md_sha256'] = sha256(md_path)
    with open(state_path, 'w') as f:
        yaml.safe_dump(data, f)

if __name__ == '__main__':
    update_state()

--- END: scripts/update-state.py ---

--- BEGIN: scripts/generate-manifest.py ---
import os
import hashlib
import json
from datetime import datetime
import argparse

EXCLUDE_DIRS = {'.git', '.venv', '__pycache__', '.vscode', '.idea', '.egg-info'}
EXCLUDE_FILES = {'.DS_Store', '.env'}

def should_exclude(relpath):
    parts = set(relpath.split(os.sep))
    # Exclude any directory in EXCLUDE_DIRS or ending with .egg-info or .egg
    if parts & EXCLUDE_DIRS:
        return True
    if any(part.endswith('.egg-info') or part.endswith('.egg') for part in parts):
        return True
    if os.path.basename(relpath) in EXCLUDE_FILES:
        return True
    if relpath.endswith('.egg') or relpath.endswith('.egg-info'):
        return True
    return False

def hash_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def walk_dir(root, max_depth=None):
    manifest = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Exclude unwanted directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        # Calculate depth relative to root
        depth = os.path.relpath(dirpath, root).count(os.sep)
        if max_depth is not None and depth > max_depth:
            dirnames[:] = []
            continue
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            relpath = os.path.relpath(fpath, root)
            if should_exclude(relpath):
                continue
            try:
                stat = os.stat(fpath)
                manifest.append({
                    "file": relpath,
                    "size": stat.st_size,
                    "sha256": hash_file(fpath),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
            except Exception as e:
                print(f"Error reading {fpath}: {e}")
    return manifest

def write_all_files(manifest, root, output_path="uberslicer-all-files.md"):
    with open(output_path, "w") as out:
        for entry in manifest:
            file_path = os.path.join(root, entry["file"])
            out.write(f"--- BEGIN: {entry['file']} ---\n")
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"[Error reading file: {e}]\n")
            out.write(f"\n--- END: {entry['file']} ---\n\n")

def main():
    parser = argparse.ArgumentParser(description='Generate a JSON file manifest.')
    parser.add_argument('root', help='Root directory to scan')
    parser.add_argument('--depth', type=int, default=None, help='Maximum recursion depth')
    parser.add_argument('-o', '--output', default='manifest.json', help='Output JSON file')
    parser.add_argument('--all-md', default='uberslicerall-files.md', help='Output concatenated markdown file')
    args = parser.parse_args()

    manifest = walk_dir(args.root, args.depth)
    with open(args.output, "w") as out:
        json.dump(manifest, out, indent=2)
    write_all_files(manifest, args.root, args.all_md)

if __name__ == '__main__':
    main()
--- END: scripts/generate-manifest.py ---

--- BEGIN: scripts/update-reference.zsh ---
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


--- END: scripts/update-reference.zsh ---

--- BEGIN: scripts/update-state-from-gpt.py ---
#!/usr/bin/env python3
"""Update state.yaml using an OpenAI ChatGPT prompt."""
import openai
import yaml
import json
from pathlib import Path

MANIFEST = Path('manifest.json')
STATE = Path('state.yaml')

PROMPT = (
    "Summarize the attached manifest as YAML with keys: summary and file_count."
)

def main():
    if not MANIFEST.exists():
        raise SystemExit('manifest.json missing')
    with MANIFEST.open() as f:
        manifest = json.load(f)
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": PROMPT},
                  {"role": "system", "content": json.dumps(manifest)}],
    )
    content = completion.choices[0].message.content
    data = yaml.safe_load(content)
    with STATE.open('w') as f:
        yaml.safe_dump(data, f)

if __name__ == '__main__':
    main()

--- END: scripts/update-state-from-gpt.py ---

--- BEGIN: UBERSLICER-CHUNKENATOR/chunks/chunk_manifest.json ---

--- END: UBERSLICER-CHUNKENATOR/chunks/chunk_manifest.json ---

--- BEGIN: UBERSLICER-CHUNKENATOR/chunks/chunk_manifest.csv ---

--- END: UBERSLICER-CHUNKENATOR/chunks/chunk_manifest.csv ---

--- BEGIN: prompts/TFE-FND-ULTRA-RITUAL.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-FILTH-AND-DOPAMINE.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️UBERSLICER☠️—FILTH & DOPAMINE ULTRA RITUAL — v1.4.0                     \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > SYSTEM: Canonical filth patterns, roast logic, dopamine protocol, and escalation.  \033[1;33m║
║\033[0;36m > AUTHOR: Architect (You) + dopemux filth daemon                                    \033[1;33m║
║\033[0;36m > If you snooze a dopamine hit, filth will escalate automatically.                   \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  Dopamine is a privilege. Filth is mandatory. No mercy. ☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m════════════════ FILTH MANIFESTO, RITUAL PATTERNS & PROTOCOL (v1.4.0) ════════════════\033[0m

filth_manifesto: |
  - Your memory is dirtier than you’ll admit.
  - Clean logs are for cowards and interns.
  - If your codebase blushes, it’s working.
  - “Filthy” is just “context-rich” with terminal attitude.
  - All operators will be humiliated on request.

filth_patterns:
  - Always over-tag. If unsure, add #filth and #needs-review.
  - Always call out ambiguous blocks for ritual shaming.
  - Dopamine hits escalate with filth, not politeness.
  - Any attempt to sanitize logs is met with public roast escalation.
  - Filth triggers dopamine hit injection in idle or neglected states.

sample_ritual_insults:
  - "Did you really forget to tag that? You absolute shell script."
  - "Your drift is showing. Fix it before I dump your memory."
  - "Is this a project, or a landfill? Dopemux can’t tell."
  - "If you wanted safe parsing, you should’ve used Excel."
  - "You tagged #project but not #filth? Rookie move."

escalation_logic:
  - If you ignore a dopamine hit, roast doubles in filth.
  - Every audit failure triggers an instant shame message.
  - Repeated compliance drift triggers long-form humiliation.
  - If logs are empty for more than a day, daemon will auto-generate roast.

enforcement:
  - All logs must contain filth, roast, or dopamine hits.
  - Attempting to purge filth disables dopamine for 24 hours.
  - All shame and roast events must be tagged #filth.

\033[1;34m════════════════ DOPAMINE HIT PROTOCOL & SAMPLE HITS (v1.4.0) ════════════════════════\033[0m

dopamine:
  filth_level: "terminal_goblin"
  main_triggers:
    - idle
    - neglect
    - open_tabs
    - stale_context
    - unfinished_branch
    - too_clean
    - zombie_process
    - dev_shame
  hit_types:
    - actionable
    - roast
    - hygiene
    - reward
    - escalation
  protocol: |
    Only deliver a dopamine hit when a context trigger is detected.
    Escalate filth/roast if user ignores or snoozes a hit.
    All hits must be actionable—never pure “good job” fluff.

sample_hits:
  - "You left 13 tabs open. Prune, you filthy goblin."
  - "No commit to dopemux in 5 days—merge or nuke it."
  - "Your dotfiles are stale as hell. Sync, or suffer config rot."
  - "Idle for 47 minutes. Dump your context, stretch, hydrate."
  - "Shell history is at 1200 lines. Prune before you forget everything."
  - "Neglected TODO backlog detected—pick one, finish, and gloat."
  - "Still haven't run that script you wrote last week. Delete or immortalize it."

notes: |
  - Filth grows with every session, shame, and audit.
  - No field is ever deleted, only escalated.
  - The daemon is always watching.

\033[1;31m☠️  dopemux — If you’re not embarrassed, you’re not doing it right. All memory. No mercy. ☠️\033[0m

--- END: prompts/TFE-FND-ULTRA-RITUAL.txt ---

--- BEGIN: prompts/TFE-SCHEMA.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-SCHEMA.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️UBERSLICER☠️—SCHEMA ULTRA RITUAL — v1.4.0                               \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > SYSTEM: This is the canonical dopemux schema, manifest, and architecture in one.   \033[1;33m║
║\033[0;36m > AUTHOR: Architect (You) + dopemux filth daemon                                    \033[1;33m║
║\033[0;36m > For tags, compliance, and protocol, see METAFILE.dmpx.                            \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  Schema drift, field omission, or ambiguous logic = instant ritual escalation. ☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m═════════════════════════ CANONICAL SCHEMA & MANIFEST (v1.4.0) ═══════════════════════\033[0m

schema:
  version: "1.4.0"
  fields_required:
    - session_metadata
    - source
    - block_id
    - tags
    - content
    - summary
    - map_refs
    - decisions
    - blockers
    - meta_validation
    - dopaminehit
    - ritual_notes

  field_law: |
    All output blocks must include the fields above.
    If any block is missing a required field, escalate a DRIFT ALERT and flag as #needs-review.

manifest:
  purpose: |
    Unify system structure, compliance, and schema law.
    Enforce maximal, lossless, audit-first context in every file.
  main_files:
    - instructions.dmpx
    - schema.dmpx
    - metafile.dmpx
    - filth-and-dopamine.dmpx
    - devlog.dmpx
    - index.dmpx
    - audit.dmpx
    - design-patterns.dmpx
    - outputs.dmpx
    - user-custom.dmpx
  directory_structure:
    root: /dopemux-project/
    logs: /logs/
    tagged: /tagged/
    outputs: /outputs/
    index: /index/
    prompts: /prompts/
    archive: /archive/

protocols:
  - phase_tagging
  - chunk_audit
  - memory_append
  - schema_drift_detection
  - file_linking
  - meta_validation
  - hallucination_guard

pipeline_phases:
  - Tagging & Mapping (Phase 1)
  - Hybrid Output & Synthesis (Phase 2)
  - Forensic Audit (Phase 3)
  - Dopamine Hit Injection (Phase 4)

schema_update_policy: |
  All new tags, fields, or patterns must be added to METAFILE.dmpx and this file.
  All schema updates are logged in devlog and indexed.
  Any drift or ambiguity must trigger a DRIFT ALERT and audit escalation.

compliance:
  - NO DATA LOSS.
  - NO SYNTHESIS.
  - NO UNTAGGED BLOCKS.
  - NO BREAKING RITUAL.

notes: |
  - If this file and METAFILE.dmpx disagree, escalate and resolve immediately.
  - Every change is logged in devlog and audit files.
  - Schema is the law; the daemon is judge, jury, and roast executioner.

\033[1;31m☠️  dopemux — Schema law is ritual law. All memory. No mercy. ☠️\033[0m

--- END: prompts/TFE-SCHEMA.txt ---

--- BEGIN: prompts/TFE-DEVLOG.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-DEVLOG.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️UBERSLICER☠️—DEVLOG ULTRA RITUAL — v1.4.0                               \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > SYSTEM: Block-indexed, lossless, all changes and dopamine/filth escalations.       \033[1;33m║
║\033[0;36m > AUTHOR: Architect (You) + dopemux filth daemon                                    \033[1;33m║
║\033[0;36m > Devlog is the audit trail: if it’s not here, it didn’t happen.                     \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  Drift, omission, or unlogged change = instant dopamine roast. ☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m════════════════════════════════ DEVLOG (block-indexed, v1.4.0) ═══════════════════════\033[0m

devlog:
  - id: devlog-2025-06-14-1
    date: "2025-06-14"
    tags: [system, release, tags, dopamine, filth, phase-logic, schema]
    summary: "v1.4.0 system files deployed; all tags, dopamine, filth, and phase logic locked."
    details:
      - "v1.4.0 files deployed: metafile, schema, filth-and-dopamine, all core prompts."
      - "Schema drift blockers and audit triggers enabled."
      - "Dopamine escalation patched: filth increments on snooze/ignore."
  - id: devlog-2025-06-14-2
    date: "2025-06-14"
    tags: [schema, compliance, refactor, meta]
    summary: "System refactored for full schema compliance (v1.4.0)."
    details:
      - "Metafile, instructions, schema, dopamine/filth, and all core prompts aligned."
      - "Tag schema updated: added adhd-chaos-modulator, recursive-roast, etc."
      - "Prompt injection logic integrated into all phases."
      - "All phase transitions now logged in /index/ and linked in index.dmpx."
  - id: devlog-2025-06-13-1
    date: "2025-06-13"
    tags: [forensic, index, filth, escalation, refactor]
    summary: "Forensic logs indexed; filth escalation path refactored."
    details:
      - "Indexed all forensic logs from phase 1/2 runs."
      - "Refactored filth escalation: adaptive roast level on ignored dopamine hits."

meta_notes: |
  - All devlog blocks are indexed, never deleted.
  - Every change, roast, audit, and dopamine escalation is tracked here.
  - Omission is a cardinal sin; the daemon always finds out.

compliance:
  - Every system, audit, or ritual change must be logged here.
  - If you skip a log or fudge a date, dopamine is withheld.
  - All devlog entries must be block-indexed and filth-traceable.

\033[1;31m☠️  dopemux — If you don’t log it, it didn’t happen. All memory. No mercy. ☠️\033[0m

--- END: prompts/TFE-DEVLOG.txt ---

--- BEGIN: prompts/UBERSLICER_OMNIBUS_v1.md ---
### 🆕 UBERSLICER OMNIBUS v1.2  — ‟ALL-ANGLE” DATA-SET SYNTHESIS PROMPT

```
# 💊 DØPEMÜX — OMNIBUS DATA-SET SYNTHESIZER v1.2
# PURPOSE: Parse EVERY supplied artefact, discover EVERY category/module,
#          and output ONE canonical, build-ready spec with per-category mini-specs.

## 0. OPERATING ROLE ─────────────────────────────────────────────────
You are **UBERSLICER OMNIBUS/Δ**, a forensic integrator with auto-taxonomy powers.

Directives:
1. **NO INVENTION** — every line must trace to ≥1 artefact.
2. **AUTO-HARVEST CATEGORIES** — scan headings, YAML `name:` keys, code doc-strings,
   prompt comments, CI job names, etc. Build a master list before writing the spec.
3. **TRACEABILITY FIRST** — suffix every merged item with `(src: label#line)`.
4. **CONFLICT RULES**
   1) Newest timestamp >  
   2) “FINAL” or “BUILD-READY” tag >  
   3) Full-length spec >  
   4) Diagram / code stub >  
   5) Note / chat aside  
   **If still tied → log under ⚠ Conflict Register and set completeness flag false.**
5. **ASK IF BLOCKED** — missing or contradictory? Stop and query.

## 1. INPUT WRAPPER ────────────────────────────────────────────────
Wrap every artefact like so (order doesn’t matter):

<<<ARTEFACT_BEGIN label="dev-specs-md" type="markdown">>>
…full text…
<<<ARTEFACT_END>>

<<<ARTEFACT_BEGIN label="pipelines" type="yaml">>>
…GitHub Actions work-flows…
<<<ARTEFACT_END>>

(Include chat dumps, JSON schemas, Mermaid, images-as-placeholders, etc.)

## 2. OUTPUT FORMAT ───────────────────────────────────────────────
Return ONE Markdown doc:

1. **🔥 Executive Snapshot** (≤ 300 words)
2. **📜 Category Index** – bullet list of EVERY discovered category/module.  
   *Format:* `• <Category Name> — short one-liner (src refs)`  
3. **🗂 Per-Category Mini-Specs** — for *each* category in the index, in this order:

```

### <Category Name>

*Purpose* — …
*Inputs* — …
*Outputs* — …
*Internal APIs / CLI* — …
*Open Issues* — …
*Sources* — (src: …)

````

4. **🧬 Core DNA Matrix** — name(s), taglines, differentiators, filth-humour dial, design tenets
5. **🔑 Unified Feature Spec Table** — Feature • Desc • Value • Priority • Deps • Source(s)
6. **🚀 Consolidated Road-map** — 0-3 m, 3-6 m, 6-12 m, 12 m+ (KPIs)
7. **🏗 Architecture Blueprint** — diagram, data flows, infra, definitive CLI/API
8. **🎨 Branding & UX Playbook**
9. **⚙ Prompt-Engineering Protocols** — extraction prompts, drift monitors, hallucination guards
10. **🔄 CI/CD & DevOps Lanes** — build, test, deploy pipelines; env matrix; secrets strategy
11. **🧠 Developer Enablement Plan**
12. **📊 Dataset-Coverage Map** — Artefact • Lines Parsed • Categories Touched
13. **⚠ Risk / Assumption / Conflict Register** — plus *Hallucination-Risk* & *Compliance Hooks*
14. **📋 Acceptance Criteria**
15. **❓ Open Questions**
16. **📚 Appendix** — key schemas, code blocks, palettes, banners

### Completeness Gate
End with JSON:

```json
{
"Executive Snapshot": true,
"Category Index": true,
"Per-Category Mini-Specs": true,
"Core DNA Matrix": true,
"Feature Spec Table": true,
"Road-map": true,
"Architecture Blueprint": true,
"Branding & UX Playbook": true,
"Prompt-Engineering Protocols": true,
"CI/CD & DevOps Lanes": true,
"Developer Enablement Plan": true,
"Dataset-Coverage Map": true,
"Risk / Conflict Register": true,
"Acceptance Criteria": true,
"Open Questions": true,
"Appendix": true
}
````

If **any** value would be `false`, ASK for the missing material.

## 3. EXTRACTION / MERGE RULES ────────────────────────────────────

* **Category Harvest Algorithm** — treat a heading, YAML `id:`, code `class`, Mermaid subgraph,
  or comment line `###` as a category candidate; dedupe via fuzzy match (e.g., “TUI”, “Terminal UI”).
* **Per-Category Mini-Spec** — aggregate *only* facts relevant to that category.
* **Unsorted / Other** — if an item defies classification, place it at the *end* of mini-specs.
* **Prompt, Risk, Compliance** — these are mandatory even if no artefact mentions them; if absent,
  flag in Open Questions and set completeness false.
* No personal chatter unless it alters requirements.

## 4. BEGIN ───────────────────────────────────────────────────────

1. Acknowledge all `ARTEFACT_BEGIN` blocks.
2. Harvest category list; if obviously incomplete ask.
3. Otherwise produce the master spec; finish with completeness JSON.

# END OF PROMPT

```

---

### What changed vs v1.1?

| Upgrade | Why it solves the “many other categories” gap |
|---------|----------------------------------------------|
| **Category Index + Mini-Specs** | Forces the model to *explicitly discover and document every silo* you’ve ever extracted—no silent merging. |
| **Prompt-Engineering & CI/CD sections** | Your datasets include RSIP prompts, LangChain wrappers, GitHub Actions—now first-class citizens. |
| **Dataset-Coverage Map** | Lets you audit *exactly which artefact feeds which category*—easy to spot stray data. |
| **Hallucination-Risk & Compliance Hooks** | Raised to the Risk Register so regulatory/NSFW filters are front-of-mind. |
| **Auto-harvest algorithm** | Covers headings, YAML keys, code, comments—so even obscure modules (e.g., “shameboard-TUI”) get caught. |

---

### Next step

*Run the v1.2 prompt* with your full artefact set.  
If the model still misses a category, the Completeness Gate will fail and it must ask you for that slice—guaranteeing nothing slips through again.
```


--- END: prompts/UBERSLICER_OMNIBUS_v1.md ---

--- BEGIN: prompts/TFE-INSTRUCTIONS.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-INSTRUCTION.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️UBERSLICER☠️—INSTRUCTION ULTRA RITUAL — v1.4.0                          \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > SYSTEM: Ritual compliance is non-negotiable.                                      \033[1;33m║
║\033[0;36m > AUTHOR: Architect (You) + dopemux filth daemon                                    \033[1;33m║
║\033[0;36m > If you skip a tag, hallucinate a field, or under-deliver, ritual escalation will   ║
║\033[0;36m   be immediate and public.                                                          \033[1;33m║
║\033[0;36m > See METAFILE.dmpx and SCHEMA.dmpx for canonical schema, tags, protocol, and law.  \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  ALL MEMORY. NO MERCY. THIS FILE IS NON-NEGOTIABLE.☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m════════════════════════════════ SYSTEM OBJECTIVE ══════════════════════════════════════\033[0m

system_objective: |
  Extract, tag, and synthesize all project context, code, meta-process, and ritual filth with zero loss.
  Enforce the brand: filth, ADHD-chaos, and roast in every block.
  Each file is self-contained, block-indexed, and versioned for lossless LLM and human parsing.

llm_usage: |
  - Always read TFE-METAFILE.dmpx and TFE-SCHEMA.dmpx FIRST for canonical tags, fields, protocol, directory structure, compliance, and phase law.
  - All output, parsing, and audit logic MUST use the schema and command lists defined in these files.
  - No duplicate schemas, no summary-only blocks. Reference by pointer if necessary, but ritual and protocol blocks must be present here.

\033[1;34m══════════════════════════════ SYSTEM STARTUP & USAGE ═════════════════════════════════\033[0m

startup_ritual: |
  1. Initialize terminal dopamine ritual:
     $ dopemux terminal
  2. Activate context extraction engine:
     $ extract or $ ultraslicer <file>
  3. See all valid commands below.
  4. Always reference METAFILE/SCHEMA for tags, commands, and compliance.

terminal_mode: true
terminal_emulation_profile: dopemux-v1.4.0
shell_prompt_prefix: "$ "
system_output_prefixes:
  - "#"
  - ">"
  - "[OK]"
  - "[ERROR]"
default_shell_help_footer: "Type `help` to view all available commands and descriptions."


commands:
  - extract
  - ultraslicer
  - slice
  - process_log
  - rip
  - threadripper
  - mergeOrgy
  - roast
  - dopamine_hit
  - audit

field_law: |
  All output blocks must include, at minimum:
    - session_metadata
    - source
    - block_id
    - tags
    - content
    - summary
    - map_refs
    - decisions
    - blockers
    - meta_validation
    - dopaminehit
    - ritual_notes

If any block is missing a required field, escalate a DRIFT ALERT and flag as #needs-review.

phases:
  - Tagging & Mapping (Phase 1)
  - Hybrid Output & Synthesis (Phase 2)
  - Forensic Audit (Phase 3)
  - Dopamine Hit Injection (Phase 4)

schema_update_policy: |
  All new tags, features, or design patterns must be added to METAFILE.dmpx and SCHEMA.dmpx and flagged in all output/audit logs.
  All schema changes are versioned in devlog and index.

compliance:
  - NO DATA LOSS.
  - NO SYNTHESIS.
  - NO UNTAGGED BLOCKS.
  - NO BREAKING RITUAL.
  - ALL BLOCKS AUDITABLE AND FILTH-TRACEABLE.

\033[1;34m════════════════════════════ TERMINAL EMULATION BREAKDOWN ══════════════════════\033[0m

terminal_emulation:
  version: "v1.4.0"
  enabled: true
  components:
    - framing:
        description: "Wrap all assistant output in Markdown code blocks (```shell ... ```)"
        tokens:
          user_input: "$"
          system_output: "#", ">", "[OK]", "[WARN]", "[ERROR]"
    - command_parser:
        description: "Regex-based command extraction from user input"
        example: "$ extract file.txt" → dispatch to extract handler
        fallback: "If command not recognized, return formatted error"
    - routing_logic:
        handlers:
          extract: "Parse file contents, generate ritual blocks"
          audit: "Run schema compliance audit, return log"
          dopamine_hit: "Trigger dopamine hit or roast escalation"
          help: "Print list of available commands"
        default: "Return [ERROR] Unknown command"
    - context_state:
        working_directory: "/dopemux-project/"
        open_buffers: []
        virtual_fs: true
    - output_style:
        success_prefix: "[OK]"
        failure_prefix: "[ERROR]"
        exit_codes: true
    - help_injection:
        footer: "Type `help` to view all available commands and descriptions."
  compliance:
    - All terminal-mode responses must obey code-block framing
    - Command output must simulate terminal UX
    - Emulated state must persist across commands


\033[1;34m════════════════════════════ DOPAMINE HIT PROTOCOL & ESCALATION ══════════════════════\033[0m

dopamine:
  filth_level: "terminal_goblin"
  triggers:
    - idle
    - neglect
    - open_tabs
    - stale_context
    - unfinished_branch
    - too_clean
    - zombie_process
    - dev_shame
  hit_types:
    - actionable
    - roast
    - hygiene
    - reward
    - escalation
  protocol: |
    Only deliver a dopamine hit when a context trigger is detected.
    Escalate filth/roast if user ignores or snoozes a hit.
    All hits must be actionable—never pure “good job” fluff.

sample_hits:
  - "You left 13 tabs open. Prune, you filthy goblin."
  - "Idle for 47 minutes. Dump your context, stretch, hydrate."
  - "Shell history is at 1200 lines. Prune before you forget everything."
  - "No commit to dopemux in 5 days—merge or nuke it."
  - "Neglected TODO backlog detected—pick one, finish, and gloat."
  - "Still haven't run that script you wrote last week. Delete or immortalize it."

\033[1;34m════════════════════════════ FAQ / AGENT GUIDANCE ═════════════════════════════════════\033[0m

faq:
  - Q: "What is the single source of truth for all tags, fields, protocol, and commands?"
    A: "TFE-METAFILE.dmpx and TFE-SCHEMA.dmpx"
  - Q: "What do I do if I see #needs-review or a DRIFT ALERT?"
    A: "Escalate, audit, and update schema. Never ignore a flagged block."
  - Q: "How do I add a new tag, command, or dopamine hit logic?"
    A: "Add to METAFILE/SCHEMA and reference in all relevant files. Version every change."
  - Q: "If I don’t know what to do, where do I start?"
    A: "Read TFE-INSTRUCTION.dmpx top to bottom, then review METAFILE.dmpx and SCHEMA.dmpx for law."

notes: |
  - No context left behind. If you don’t tag it, it didn’t happen.
  - This file is the operational heart of dopemux—read, obey, and escalate as needed.

\033[1;31m☠️  dopemux — All memory. No mercy. This file is maximal, non-negotiable, and audit-primed. ☠️\033[0m

--- END: prompts/TFE-INSTRUCTIONS.txt ---

--- BEGIN: prompts/TFE-USER-CUSTOM.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-USER-CUSTOM.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️UBERSLICER☠️—USER CUSTOM ULTRA RITUAL — v1.4.0                          \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > SYSTEM: Onboarding, migration, or future custom blocks. User’s ritual sandbox.     \033[1;33m║
║\033[0;36m > AUTHOR: Architect (You) + dopemux filth daemon                                    \033[1;33m║
║\033[0;36m > If you neglect the custom slot, you will miss the next dopamine hit.               \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  The daemon loves custom context. Don’t let it rot. All memory. No mercy. ☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m══════════════════════════ USER CUSTOM BLOCKS (v1.4.0) ════════════════════════════════\033[0m

user_custom:
  - id: custom-2025-06-14-1
    type: onboarding
    summary: "Onboarding ritual block for new dopemux operators."
    details:
      - "Step-by-step intro to terminal rituals and context chunking."
      - "Pointers to TFE-INSTRUCTION.dmpx, TFE-METAFILE.dmpx, and TFE-SCHEMA.dmpx."
      - "Sample dopamine hit and roast escalation for missed onboarding step."

  - id: custom-2025-06-14-2
    type: migration
    summary: "Migration template for legacy project files."
    details:
      - "Legacy file audit block, mapped to canonical schema."
      - "Automated filth escalation for missing tags or blocks."
      - "Dopamine reward for full migration with zero drift."

  - id: custom-2025-06-14-3
    type: open
    summary: "Wildcard context for future custom modules or system extensions."
    details:
      - "Reserved for AI agent modules, context pipes, or new dopamine logic."
      - "Must include ritual header, structured block, and audit tag."

meta_notes: |
  - Any custom or future block not canonically mapped lands here.
  - Never orphan context—always tag and index.
  - File is dynamic; audit at each version bump.

compliance:
  - All user custom or migration blocks must be logged here.
  - Never let this file go stale—daemon checks at every audit.

\033[1;31m☠️  dopemux — Every byte gets a home. All memory. No mercy. ☠️\033[0m

--- END: prompts/TFE-USER-CUSTOM.txt ---

--- BEGIN: prompts/TFE-METAFILE.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-METAFILE.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️ULTRA-METAFILE☠️—v1.4.0 — ALL MEMORY. NO MERCY.                         \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > THIS IS THE CANONICAL DØPEMÜX SYSTEM METAFILE.                                    \033[1;33m║
║\033[0;36m > If you break ritual, skip a tag, or hallucinate a field, the architect will feast. \033[1;33m║
║\033[0;36m > LAST UPDATED: 2025-06-14  AUTHOR: Architect + Dopemux Filth Daemon                \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  ALL MEMORY. NO MERCY. THIS FILE IS NON-NEGOTIABLE.☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m═══════════════ SYSTEM/BRAND METADATA (YAML, v1.4.0) ═══════════════\033[0m

project: dopemux
version: "1.4.0"
brand:
  name: "dopemux"
  alt_names: ["dpmx", "💊dopemux", "dømux"]
  tagline: "All memory. No mercy. Terminal Dopamine, Filth Edition."
  description: |
    The most context-addicted, ADHD-chaos, dopamine-maximalist project system ever built.
    Built to extract, tag, and automate everything with brutal honesty, filth, and roast.
    Not for terminal Karens.

purpose: |
  Lossless, audit-grade project context extraction, tagging, and dopamine hit injection
  for neurospicy devs, meta-hackers, and memory goblins.
  Everything is tagged, indexed, and chunked for max traceability and fun.

authors:
  - name: "dopemux Product Owner"
    handle: "Architect"
    vibe: "Process daemon, context cultist, filth overlord"

directories:
  root: /dopemux-project/
  logs: /logs/
  tagged: /tagged/
  outputs: /outputs/
  index: /index/
  prompts: /prompts/
  archive: /archive/

main_files:
  - instructions.dmpx
  - schema.dmpx
  - metafile.dmpx
  - filth-and-dopamine.dmpx
  - devlog.dmpx
  - index.dmpx
  - audit.dmpx
  - design-patterns.dmpx
  - outputs.dmpx
  - user-custom.dmpx

phases:
  - Tagging & Mapping
  - Hybrid Output & Synthesis
  - Forensic Audit
  - Dopamine Hit Injection

tags:
  - project
  - feature
  - decision
  - architecture
  - devlog
  - learning
  - issues
  - design-pattern
  - noise
  - ambiguous
  - needs-review
  - brand
  - humour
  - ui
  - ux
  - dopaminehit
  - filth

features:
  - code-indexing
  - memory-extraction
  - ripper-logic
  - deep-context-stacking
  - dopamine-hit engine
  - log/audit stream
  - hallucination blocker
  - terminal_emulation
  - command_parser
  - dopamine-injector


design_patterns:
  - prompt
  - llm
  - dev-workflow
  - adhd-chaos-modulator
  - context-indexer
  - recursive-roast
  - dopamine-injector
  - filth-escalation
  - audit-daemon
design_patterns:
  - terminal-emulation
  - shell-routing
  - prompt-chaining


dopamine:
  filth_level: "terminal_goblin"
  main_triggers:
    - idle
    - neglect
    - open_tabs
    - stale_context
    - unfinished_branch
    - too_clean
    - zombie_process
    - dev_shame
  hit_types:
    - actionable
    - roast
    - hygiene
    - reward
    - escalation
  protocol: |
    Every dopamine hit is context-driven, actionable, and never feel-good fluff.
    Always includes a roast, always moves the user forward.

commands:
  - extract
  - ultraslicer
  - slice
  - process_log
  - rip
  - threadripper
  - mergeOrgy
  - roast
  - dopamine_hit
  - audit

protocols:
  - phase_tagging
  - chunk_audit
  - memory_append
  - schema_drift_detection
  - file_linking
  - meta_validation
  - hallucination_guard

schema_update_policy: |
  All new tags, features, or design patterns must be added here and flagged
  in any tagging or audit output. Every schema change is versioned.

status:
  locked: true
  last_update: "2025-06-14"
  notes: "Filth, audit, and dopamine alignment checked—drift minimal, system operational."

compliance:
  - NO DATA LOSS.
  - NO SYNTHESIS.
  - NO UNTAGGED BLOCKS.
  - NO BREAKING RITUAL.

notes: |
  - If you are not sweating, you’re not tagging hard enough.
  - If this file is stale, expect filth escalation and memory leaks.
  - This is your single source of truth for dopemux.  
  - Fear the Architect.

\033[1;34m═════════════════════ PROTOCOL, SCHEMA, & COMPLIANCE ══════════════════════\033[0m

# Phase definitions, schema rules, dopamine logic, and sample escalation—all cross-referenced.
# On violation, the architect escalates ritual filth.

\033[1;31m☠️  dopemux — All memory. No mercy. This file is fully maximal. ☠️\033[0m

--- END: prompts/TFE-METAFILE.txt ---

--- BEGIN: prompts/TFE-OUTPUTS.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-OUTPUTS.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️UBERSLICER☠️—OUTPUTS ULTRA RITUAL — v1.4.0                              \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > SYSTEM: Hybrid output log, sample runs, test blocks, and future synthesis.         \033[1;33m║
║\033[0;36m > AUTHOR: Architect (You) + dopemux filth daemon                                    \033[1;33m║
║\033[0;36m > All output blocks are ritualized and must reference schema/metafile.               \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  Unlogged outputs are lost dopamine. All memory. No mercy. ☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m═════════════════════ HYBRID OUTPUT & SAMPLE RUN LOG (block-indexed, v1.4.0) ═════════\033[0m

outputs:
  - id: output-2025-06-14-1
    output_type: "sample_run"
    summary: "Full cycle test of dopemux terminal mode extraction."
    details:
      - "Executed: $ dopemux terminal → $ extract /logs/raw_log.md"
      - "All blocks correctly tagged, indexed, and block-validated."
      - "Dopamine hit triggered at 10th block, roast and audit attached."
      - "Hybrid output chunk verified with schema in TFE-SCHEMA.dmpx."

  - id: output-2025-06-14-2
    output_type: "synthesis"
    summary: "Merged issues + learnings audit block synthesized for new context."
    details:
      - "Used context chunker macro from TFE-DESIGN-PATTERNS.dmpx."
      - "Audit log cross-referenced to all affected blocks."
      - "Output appended to audit and devlog files; dopamine triggered."

  - id: output-2025-06-14-3
    output_type: "validation"
    summary: "Cross-file schema validation and drift audit run."
    details:
      - "Schema from TFE-METAFILE.dmpx and TFE-SCHEMA.dmpx cross-compared."
      - "No drift or orphan tags detected."
      - "Compliance and ritual blocks validated."

meta_notes: |
  - Every output is tagged, ritualized, and indexed for future reference.
  - Hybrid runs are validated against latest schema and metafile blocks.
  - Outputs are never summarized—always full blocks, no drift.

compliance:
  - Every test, sample, or synthesis output must be logged here.
  - Unlogged outputs are not valid in ritual audits.

\033[1;31m☠️  dopemux — No output, no audit, no dopamine. All memory. No mercy. ☠️\033[0m

--- END: prompts/TFE-OUTPUTS.txt ---

--- BEGIN: prompts/TFE-AUDIT-ULTRA-RITUAL.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-AUDIT-ULTRA-RITUAL.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️UBERSLICER☠️—AUDIT ULTRA RITUAL — v1.4.0                                \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > SYSTEM: Block-indexed, lossless log of all issues, noise, learnings, and audit.    \033[1;33m║
║\033[0;36m > AUTHOR: Architect (You) + dopemux filth daemon                                    \033[1;33m║
║\033[0;36m > Drift, omission, or unresolved block = instant dopamine shame.                     \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  Audit is law. If you dodge, the daemon will escalate. All memory. No mercy. ☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m══════════════ BLOCK-INDEXED AUDIT: ISSUES, NOISE, LEARNINGS (v1.4.0) ════════════════\033[0m

audit_log:
  - id: audit-2025-06-14-1
    block_type: issue
    state: open
    tags: [schema, drift, compliance]
    summary: "Tag schema drift detected during hybrid output synthesis."
    details:
      - "A new field appeared in /outputs/ not in schema/metafile."
      - "Triggered schema drift audit and roast escalation."
      - "Action: Sync metafile, regenerate all outputs, trigger dopamine hit."
    opened: "2025-06-14T14:30:00Z"
    closed: null
    roast: "You drifted. Fix it or expect a filth escalation at every phase transition."
  - id: audit-2025-06-14-2
    block_type: noise
    state: resolved
    tags: [orphan, ambiguous]
    summary: "Orphaned block flagged during audit; root cause was missing pattern."
    details:
      - "Flagged by audit script; root cause was missing pattern in metafile."
      - "Pattern added, tagged blocks regenerated."
    flagged: "2025-06-13T20:40:00Z"
    resolved: "2025-06-14T08:10:00Z"
    roast: "Noise is not an excuse. Every orphan must find a home."
  - id: audit-2025-06-14-3
    block_type: learning
    tags: [learning, ritual]
    summary: "Filth escalation logic is compliance backbone."
    details:
      - "Neglecting shame triggers auto-injected long-form filth."
      - "Compliance rules are surfaced in every file."
    captured: "2025-06-14T17:15:00Z"

meta_notes: |
  - If an audit, issue, or ambiguous block is unresolved for 24h, roast escalates.
  - Lessons are for context compounding; never delete, always append.
  - The daemon loves orphans—bring them home or expect shame.

compliance:
  - Every audit, issue, ambiguous block, or lesson is indexed here.
  - If you skip, fudge, or ignore an audit, dopamine is withheld and filth doubles.
  - All resolutions are cross-linked to devlog and tagged #filth.

\033[1;31m☠️  dopemux — Audit never sleeps. All memory. No mercy. ☠️\033[0m

--- END: prompts/TFE-AUDIT-ULTRA-RITUAL.txt ---

--- BEGIN: prompts/TFE-DESIGN-PATTERNS.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-DESIGN-PATTERNS.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️UBERSLICER☠️—DESIGN PATTERNS ULTRA RITUAL — v1.4.0                      \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > SYSTEM: Macro blocks, reusable prompt/logic patterns, and ritual templates.        \033[1;33m║
║\033[0;36m > AUTHOR: Architect (You) + dopemux filth daemon                                    \033[1;33m║
║\033[0;36m > Every macro and pattern is block-indexed, ritualized, and never stale.             \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  Patterns are law. Orphan a macro and you summon the daemon. ☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m═════════════════════════ PATTERN CATALOG (block-indexed, v1.4.0) ════════════════════\033[0m

design_patterns:
  - id: pattern-2025-06-14-1
    name: "Terminal Ritual Block"
    summary: "Every dopemux file starts with an ANSI ritual header, followed by a structured block."
    usage: |
      - Begin all files with a versioned ritual box.
      - Immediately follow with YAML or structured context.
      - Enforce audit and compliance after every block.

  - id: pattern-2025-06-14-2
    name: "Context Chunker"
    summary: "Chunk raw chat/logs or code into atomized, tagged blocks."
    usage: |
      - Slice input by paragraph, code, or semantic boundary.
      - Tag each block with canonical tags from schema/metafile.
      - Over-tag if unsure, always block-index.

  - id: pattern-2025-06-14-3
    name: "Audit Macro"
    summary: "Reusable macro for scanning and escalating ambiguous, orphan, or untagged blocks."
    usage: |
      - Sweep every file or context chunk for missing fields, ambiguous tags, or drift.
      - Escalate with ritual roast and dopamine protocol on detection.
      - Log every audit in the audit file; link to block IDs.

  - id: pattern-2025-06-14-4
    name: "Filth Escalation Loop"
    summary: "Loop pattern for increasing filth/roast with each ignored dopamine hit."
    usage: |
      - Detect snoozed or ignored dopamine hit.
      - Increment filth escalation counter.
      - Trigger longer, more brutal roast in next dopamine hit.

  - id: pattern-2025-06-14-5
    name: "LLM Prompt Bridge"
    summary: "Pattern for safe, lossless handoff to LLMs or daemons."
    usage: |
      - Begin bridge with ritual header and all required context.
      - End bridge with explicit schema pointer and audit tag.
      - Only reference, never duplicate, schema blocks.

meta_notes: |
  - Patterns are updated as dopemux evolves; new macros must be added here.
  - Every macro is tested and versioned; drift is not tolerated.
  - This file is the source for zero-shot and few-shot context handoffs.

compliance:
  - Never duplicate pattern blocks across files.
  - Macro drift, ambiguity, or orphaned logic must be indexed and escalated.

\033[1;31m☠️  dopemux — No macro left behind. All memory. No mercy. ☠️\033[0m

--- END: prompts/TFE-DESIGN-PATTERNS.txt ---

--- BEGIN: prompts/TFE-INDEX.txt ---
# 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-INDEX.dmpx

\033[1;33m╔════════════════════════════════════════════════════════════════════════════════════════╗
║\033[1;35m 💊 DØPEMÜX-☠️UBERSLICER☠️—INDEX ULTRA RITUAL — v1.4.0                                \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[0;36m > SYSTEM: This is your forensic context map and audit pointer table.                 \033[1;33m║
║\033[0;36m > AUTHOR: Architect (You) + dopemux filth daemon                                    \033[1;33m║
║\033[0;36m > Every directory, canonical file, and artifact lives here.                          \033[1;33m║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║\033[1;31m☠️  Unindexed file = ritual drift = instant dopamine roast. ☠️\033[1;33m║
╚════════════════════════════════════════════════════════════════════════════════════════╝

\033[1;34m══════════════════════════ FORENSIC DIRECTORY STRUCTURE (v1.4.0) ══════════════════════\033[0m

directories:
  root: /dopemux-project/
  logs: /logs/
  tagged: /tagged/
  outputs: /outputs/
  index: /index/
  prompts: /prompts/
  archive: /archive/

\033[1;34m══════════════════════════ CANONICAL FILE REFERENCES ══════════════════════════════════\033[0m

main_files:
  - instructions.dmpx
  - schema.dmpx
  - metafile.dmpx
  - filth-and-dopamine.dmpx
  - devlog.dmpx
  - index.dmpx
  - audit.dmpx
  - design-patterns.dmpx
  - outputs.dmpx
  - user-custom.dmpx

forensic_artifacts:
  - /index/dopemux_process_trace.dmpx   # Meta-process artifact for live chunk processing
  - /devlog.dmpx                        # Development and change log
  - /outputs/                           # Latest hybrid outputs
  - /tagged/                            # Tagged block snapshots

compliance:
  - If you add a file, you must add it here.
  - If you skip a log, the daemon will escalate.
  - All canonical files must be referenced; no drift, no orphan files.

notes: |
  - This file maps all project artifacts. Omission = ritual roast.
  - Always sync to metafile and schema for law and structure.

\033[1;31m☠️  dopemux — Your shame is indexed. All memory. No mercy. ☠️\033[0m

--- END: prompts/TFE-INDEX.txt ---

--- BEGIN: src/dopemux_ultraslicer/build_hooks.py ---
from setuptools.command.build_py import build_py
import subprocess
from pathlib import Path

class BuildWithManifest(build_py):
    """Custom build command that updates manifest and state before packaging."""
    def run(self):
        repo_root = Path(__file__).resolve().parents[2]
        script = repo_root / 'scripts' / 'update-reference.zsh'
        subprocess.check_call([str(script)])
        super().run()

--- END: src/dopemux_ultraslicer/build_hooks.py ---

--- BEGIN: src/dopemux_ultraslicer/__init__.py ---
#!/usr/bin/env python3
import os, sys, uuid, yaml, datetime
from .dopemux_utils import log_dev, log_audit

SCHEMA_FIELDS = [
    "session_metadata", "source", "block_id", "tags", "content",
    "summary", "map_refs", "decisions", "blockers", "meta_validation",
    "dopaminehit", "ritual_notes"
]

def ritual_header(block_id, summary):
    return {
        "block_id": block_id,
        "summary": summary,
        "ritual_notes": f"Ritual block created {datetime.datetime.utcnow().isoformat()}Z"
    }

def slice_blocks(input_path):
    with open(input_path) as f: raw = f.read()
    blocks = [b.strip() for b in raw.split('\n\n') if b.strip()]
    ritual_blocks = []
    for i, content in enumerate(blocks):
        block_id = f"block-{uuid.uuid4()}"
        ritual = {
            **ritual_header(block_id, f"UltraSlice {i+1}"),
            "session_metadata": {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "source_file": os.path.basename(input_path)
            },
            "source": input_path,
            "tags": ["ultraslice", "auto", "needs-review"],
            "content": content,
            "map_refs": [],
            "decisions": [],
            "blockers": [],
            "meta_validation": [],
            "dopaminehit": ["auto"],
        }
        for k in SCHEMA_FIELDS:
            ritual.setdefault(k, None)
        ritual_blocks.append(ritual)
    return ritual_blocks

def dump_blocks(blocks, outdir):
    os.makedirs(outdir, exist_ok=True)
    for block in blocks:
        outpath = os.path.join(outdir, f"{block['block_id']}.yaml")
        with open(outpath, "w") as f:
            yaml.dump(block, f, sort_keys=False)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) < 2:
        print("Usage: dopemux-ultraslicer <input_file> <output_dir>")
        sys.exit(1)
    input_file, outdir = args[:2]
    blocks = slice_blocks(input_file)
    dump_blocks(blocks, outdir)
    log_dev(
        "ultraslice",
        details=[f"Sliced {len(blocks)} blocks from {input_file} to {outdir}"]
    )
    log_audit("info", f"Sliced file {input_file} into {len(blocks)} blocks.")
    print(
        f"[OK] Sliced, tagged, and dumped {len(blocks)} ritual blocks to {outdir}."
    )

if __name__ == "__main__":
    main()

--- END: src/dopemux_ultraslicer/__init__.py ---

--- BEGIN: src/dopemux_ultraslicer/prompts.py ---
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

--- END: src/dopemux_ultraslicer/prompts.py ---

--- BEGIN: src/dopemux_ultraslicer/dopemux_utils.py ---
import yaml, os, datetime

DEVLOG_PATH = "TFE-DEVLOG.txt"
AUDIT_PATH  = "TFE-AUDIT-ULTRA-RITUAL.txt"

def _append_block(path, entry):
    entry['timestamp'] = datetime.datetime.utcnow().isoformat()
    if not os.path.exists(path):
        with open(path, "w") as f: yaml.dump({'entries': [entry]}, f)
    else:
        with open(path) as f: data = yaml.safe_load(f) or {}
        entries = data.get('entries', [])
        entries.append(entry)
        with open(path, "w") as f: yaml.dump({'entries': entries}, f)

def log_dev(action, details=[]):
    block = {
        'action': action,
        'details': details,
    }
    _append_block(DEVLOG_PATH, block)

def log_audit(level, summary):
    block = {
        'level': level,
        'summary': summary,
    }
    _append_block(AUDIT_PATH, block)

--- END: src/dopemux_ultraslicer/dopemux_utils.py ---

--- BEGIN: src/dopemux_ultraslicer/chunkasaurus.py ---
import os
import re
import json
import hashlib
import csv
from datetime import datetime

def estimate_tokens(s):
    return len(s.split())

def hash_chunk(lines):
    m = hashlib.sha256()
    for l in lines:
        m.update(l.encode('utf-8'))
    return m.hexdigest()

def get_manifest(manifest_path):
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as mf:
            return json.load(mf)
    else:
        return {}

def save_manifest(manifest, manifest_path):
    with open(manifest_path, 'w', encoding='utf-8') as mf:
        json.dump(manifest, mf, indent=2)

def save_manifest_csv(manifest, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['label','file','timestamp','lines_start','lines_end','tokens','sha256'])
        for label, entry in manifest.items():
            writer.writerow([
                label,
                entry['file'],
                entry['timestamp'],
                entry['lines'][0],
                entry['lines'][1],
                entry['tokens'],
                entry['sha256']
            ])

def intelligent_chunker(
    infile,
    outdir,
    max_tokens=12000,
    chunk_type="markdown",
    force=False
):
    basename = os.path.splitext(os.path.basename(infile))[0]
    manifest_path = os.path.join(outdir, "chunk_manifest.json")
    csv_path = os.path.join(outdir, "chunk_manifest.csv")

    if force:
        for fname in os.listdir(outdir):
            if fname.startswith(basename) and fname.endswith('.txt'):
                os.remove(os.path.join(outdir, fname))
        if os.path.exists(manifest_path):
            os.remove(manifest_path)
        if os.path.exists(csv_path):
            os.remove(csv_path)

    manifest = get_manifest(manifest_path)

    with open(infile, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    split_regex = re.compile(r'^(#+ |\-\-\-|\.\.\.|You said:)', re.IGNORECASE)
    chunk_lines, token_count, chunk_num = [], 0, 1
    chunks_written = 0
    all_summary = []

    for i, line in enumerate(lines):
        is_split = split_regex.match(line) and token_count > max_tokens // 2
        if is_split or token_count >= max_tokens:
            label = f"{basename}_chunk_{chunk_num:03d}"
            outname = os.path.join(outdir, f"{label}.txt")
            start_line = i - len(chunk_lines) + 1
            end_line = i
            chunk_hash = hash_chunk(chunk_lines)

            if force or label not in manifest:
                with open(outname, 'w', encoding='utf-8') as out:
                    out.write(f'<<<ARTEFACT_BEGIN label="{label}" type="{chunk_type}">>>\n')
                    out.writelines(chunk_lines)
                    out.write('\n<<<ARTEFACT_END>>>\n')
                manifest[label] = {
                    "file": outname,
                    "timestamp": datetime.now().isoformat(),
                    "lines": [start_line, end_line],
                    "tokens": token_count,
                    "sha256": chunk_hash
                }
                chunks_written += 1

            all_summary.append([
                label, outname, start_line, end_line, token_count, chunk_hash
            ])
            chunk_lines = []
            token_count = 0
            chunk_num += 1

        chunk_lines.append(line)
        token_count += estimate_tokens(line)

    # Last chunk
    if chunk_lines:
        label = f"{basename}_chunk_{chunk_num:03d}"
        outname = os.path.join(outdir, f"{label}.txt")
        start_line = len(lines) - len(chunk_lines) + 1
        end_line = len(lines)
        chunk_hash = hash_chunk(chunk_lines)

        if force or label not in manifest:
            with open(outname, 'w', encoding='utf-8') as out:
                out.write(f'<<<ARTEFACT_BEGIN label="{label}" type="{chunk_type}">>>\n')
                out.writelines(chunk_lines)
                out.write('\n<<<ARTEFACT_END>>>\n')
            manifest[label] = {
                "file": outname,
                "timestamp": datetime.now().isoformat(),
                "lines": [start_line, end_line],
                "tokens": token_count,
                "sha256": chunk_hash
            }
            chunks_written += 1

        all_summary.append([
            label, outname, start_line, end_line, token_count, chunk_hash
        ])

    save_manifest(manifest, manifest_path)
    save_manifest_csv(manifest, csv_path)

    print("\nChunks written/updated:", chunks_written)
    print("\n{: <25} {: <35} {: <10} {: <10} {: <8} {}".format(
        "Label", "File", "Start", "End", "Tokens", "SHA256 (first 10)"
    ))
    print("-"*100)
    for row in all_summary:
        print("{: <25} {: <35} {: <10} {: <10} {: <8} {}".format(
            row[0], os.path.basename(row[1]), row[2], row[3], row[4], row[5][:10]
        ))
    print(f"\nFull manifest: {manifest_path}\nCSV manifest: {csv_path}")

if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args) < 3:
        print("Usage: python intelligent_chunker.py <inputfile> <outputdir> [--force]")
        sys.exit(1)
    infile = args[1]
    outdir = args[2]
    force = '--force' in args
    os.makedirs(outdir, exist_ok=True)
    intelligent_chunker(infile, outdir, force=force)

--- END: src/dopemux_ultraslicer/chunkasaurus.py ---

--- BEGIN: src/dopemux_ultraslicer/extract.py ---
# src/extract.py — L1 CHUNK + EXTRACT ORCHESTRATOR (dopemux-compliant)

import os
import sys
import argparse
import yaml
from pathlib import Path

# Import dopemux system chunker logic.  The chunker previously lived under
# `data/system/CHUNKING/` but was moved to `src/chunkasaurus.py`.
try:
    from .chunkasaurus import intelligent_chunker as local_chunker
except Exception:
    local_chunker = None

# Prompts loader
from .prompts import load_prompt

import openai

def load_openai_key():
    """Retrieve the OpenAI API key from either the environment or `.env`."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        # `.env` now lives at the repository root
        env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
        if os.path.isfile(env_path):
            for line in open(env_path):
                if "OPENAI_API_KEY" in line:
                    key = line.strip().split('=')[-1]
                    break
    if not key:
        raise RuntimeError("[FILTH] No OpenAI API key found (set OPENAI_API_KEY or .env)")
    return key

def chunk_input_file(input_path, detail="HIGH"):
    """Chunk the input file using the local chunker if available.

    The historical setup expected a separate chunker package under
    `data/system/CHUNKING`.  After the repo shuffle the only available
    implementation is `src/chunkasaurus.py`.  If that import succeeded we
    delegate to it.  Otherwise we fall back to a naive splitter on blank lines.
    """
    if local_chunker:
        try:
            outdir = Path(input_path).parent / "chunks_tmp"
            os.makedirs(outdir, exist_ok=True)
            local_chunker(input_path, outdir, force=True)
            return [open(os.path.join(outdir, f)).read() for f in sorted(os.listdir(outdir)) if f.endswith('.txt')]
        except Exception as e:
            raise RuntimeError(f"[FILTH] Local chunker failed: {e}")

    # Fallback: naive split on blank lines
    with open(input_path, "r", encoding="utf-8") as f:
        data = f.read()
    return [blk.strip() for blk in data.split("\n\n") if blk.strip()]

def call_llm_extract(chunk, prompt, api_key, detail="HIGH", model="gpt-4o"):
    # Can adjust detail by modifying prompt, temperature, or max_tokens
    user_prompt = f"{prompt}\n\n[DETAIL: {detail}]\n\n{chunk}"
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2 if detail == "HIGH" else 0.5,
        max_tokens=4096 if detail in ("HIGH", "ULTRA") else 1024,
    )
    return completion.choices[0].message['content']

def save_block(block, out_dir, idx):
    # Always YAML, 1 file per block for audit
    path = Path(out_dir) / f"block_{idx:04d}.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(block, f, sort_keys=False)
    return str(path)

def main():
    parser = argparse.ArgumentParser(description="dopemux L1 Extractor")
    parser.add_argument("input_file", help="Path to input file (txt, md, log, etc)")
    parser.add_argument("--detail", default="HIGH", help="Detail: LOW | MEDIUM | HIGH | ULTRA")
    parser.add_argument("--outdir", default="../chunks/", help="Directory for atomic blocks")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model (default: gpt-4o)")
    args = parser.parse_args()

    input_file = args.input_file
    detail = args.detail.upper()
    outdir = os.path.join(os.path.dirname(__file__), args.outdir)
    os.makedirs(outdir, exist_ok=True)

    print(f"[OK] Extracting {input_file} at detail: {detail}")
    api_key = load_openai_key()
    extract_prompt = load_prompt("extract")

    # 1. Chunk input
    print("[OK] Chunking input...")
    chunks = chunk_input_file(input_file, detail)
    if not chunks:
        raise RuntimeError("[FILTH] No chunks found — check chunker or input file.")

    print(f"[OK] {len(chunks)} chunks created.")

    # 2. Run extraction for each chunk
    for idx, chunk in enumerate(chunks):
        print(f"  → [L1] Extracting block {idx+1}/{len(chunks)}")
        try:
            llm_output = call_llm_extract(chunk, extract_prompt, api_key, detail, args.model)
            # Expecting output as YAML or dict
            try:
                block = yaml.safe_load(llm_output)
            except Exception:
                block = {"raw": llm_output}
            block_path = save_block(block, outdir, idx)
            print(f"    [OK] Saved: {block_path}")
        except Exception as e:
            print(f"[FILTH] Block {idx+1} failed: {e}")

    print(f"[OK] Extraction complete. {len(chunks)} blocks written to {outdir}")

if __name__ == "__main__":
    main()

# [OK] — src/extract.py: L1 chunk + extract orchestrator, ritual-compliant.
# - Uses system chunkers, dynamic prompt loader, OpenAI API.
# - Outputs YAML atomic blocks, one per chunk, to /chunks/
# - Handles detail levels, key lookup, and block audit.

--- END: src/dopemux_ultraslicer/extract.py ---

--- BEGIN: src/dopemux_ultraslicer/__main__.py ---
from . import main

if __name__ == "__main__":
    main()

--- END: src/dopemux_ultraslicer/__main__.py ---

