--- BEGIN: 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-DEVLOG.txt ---
entries:
- action: patch
  details:
  - old.py -> new.py
  - demo
  timestamp: '2025-06-17T04:40:14.579515'

--- END: 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-DEVLOG.txt ---

--- BEGIN: pyproject.toml ---
# pyproject.toml

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "dopemux"
version = "0.1.0"
description = "Terminal-native, forensic context engine with dopamine rituals."
authors = [{name = "Your Name", email = "you@example.com"}]
dependencies = [
  "click>=8.1",
  "pyyaml>=6.0",
  "pydantic>=2.0",
]

[project.scripts]
dopemux = "cli:cli"

[tool.setuptools]
py-modules = ["cli"]

[tool.setuptools.packages.find]
where = ["."]
include = ["uberslicer", "uberslicer.*"]

--- END: pyproject.toml ---

--- BEGIN: uberslicer-manifest.yaml ---
# generated 2025-06-17T13:14:35Z
files:
  - path: "uberslicer/__init__.py"
    size: 414
    sha256: "d0562442e0404515e3fd4b0ee66c2577b022dd62260720b764bfd92b2a9640af"
  - path: "uberslicer/doctor.py"
    size: 2237
    sha256: "ae42433724f398a12597be9085e31f1fa22aa3793663efa6604055cfc91906ad"
  - path: "uberslicer/patch.py"
    size: 1732
    sha256: "3a491d06fbdf9742e9be2a561659a8cdeb374ff9d68a208e130a94671ba5a75b"
  - path: "uberslicer/ultraslicer.py"
    size: 2218
    sha256: "03130697fa4f1dc01871bdc2e142c3cfd3a0a850f55164f3af8f3ba0ad725281"
  - path: "uberslicer/utils.py"
    size: 2373
    sha256: "1592c2880d715f418f056ddbc0354c96d03ec6c6a4c5d3e50f014a00ecfb72c2"
  - path: "uberslicer/validator.py"
    size: 1328
    sha256: "e6cd921760b98eb9b6446725adab8cf3ea4f6b550de9777483fa18529322264c"

--- END: uberslicer-manifest.yaml ---

--- BEGIN: config.yaml ---
dopemux:
  filth_level: terminal_goblin
  paths:
    tagged: "./tagged"
    patch_dir: "./tagged/patched"
    outputs: "./outputs"
    devlog: "./logs/devlog.json"
    audit: "./logs/audit.json"
  schema:
    file: "/Users/hu/code/DØPEMÜX/schema/extraction_schema.json"
  auditor:
    block_review_tag: "needs-review"
  colors:
    dopamine: cyan
    filth: magenta

# -- ensure these directories exist --
auditor_dirs:
- "tagged"
- "tagged/patch"
- "logs"
- "schema"

--- END: config.yaml ---

--- BEGIN: uberslicer-all.txt ---
##### >>> BEGIN FILE: uberslicer/__init__.py <<< #####
import importlib, yaml, pathlib
from uberslicer.utils import log_dev

PLUGIN_DIR = pathlib.Path("plugins")

def load_plugins():
    for yml in PLUGIN_DIR.glob("*/plugin.yaml"):
        meta = yaml.safe_load(yml.read_text())
        mod = importlib.import_module(meta["entrypoint"].rstrip(".py").replace("/", "."))
        log_dev({"action":"plugin_loaded","name":meta["name"]})
        yield meta["name"], mod.run

##### <<< END FILE:   uberslicer/__init__.py <<< #####

##### >>> BEGIN FILE: uberslicer/doctor.py <<< #####
"""
Sanity checker for folder layout, config keys, and required files.
Called via `dopemux doctor`.
"""

from pathlib import Path
import yaml
import sys

# Match your config.yaml structure
REQUIRED_CONFIG_KEYS = [
    "dopemux.paths.tagged",
    "dopemux.paths.patch_dir",
    "dopemux.paths.outputs",
    "dopemux.paths.devlog",
    "dopemux.paths.audit",
    "dopemux.schema.file",
    "dopemux.auditor.block_review_tag",
]

REQUIRED_DIRS = [
    "tagged",
    "tagged/patch",
    "logs",
    "schema",
]

REQUIRED_FILES = [
    "schema/extraction-schema.json",
    "config.yaml",
]

def warn(msg):
    print(f"❌  {msg}")

def ok(msg):
    print(f"✅  {msg}")

def load_cfg():
    try:
        with open("config.yaml") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        warn("config.yaml not found at repo root.")
        sys.exit(1)

def check_keys(cfg):
    # flatten nested dict to dot-keys
    flat = {}
    def _flatten(prefix, mapping):
        for k, v in mapping.items():
            key = f"{prefix}.{k}" if prefix else k
            flat[key] = v
            if isinstance(v, dict):
                _flatten(key, v)
    _flatten("", cfg)
    missing = [k for k in REQUIRED_CONFIG_KEYS if k not in flat]
    if missing:
        warn(f"Missing config keys: {', '.join(missing)}")
    else:
        ok("All required config keys present.")
    return not missing

def check_dirs():
    missing = [d for d in REQUIRED_DIRS if not Path(d).exists()]
    if missing:
        warn(f"Missing directories: {', '.join(missing)}")
    else:
        ok("All required directories exist.")
    return not missing

def check_files():
    missing = [f for f in REQUIRED_FILES if not Path(f).exists()]
    if missing:
        warn(f"Missing files: {', '.join(missing)}")
    else:
        ok("All required files exist.")
    return not missing

def run_diagnosis() -> None:
    cfg = load_cfg()
    results = [
        check_keys(cfg),
        check_dirs(),
        check_files(),
    ]
    if all(results):
        ok("Doctor check passed — repo looks healthy.")
        sys.exit(0)
    warn("Doctor check failed — fix the ❌ items above.")
    sys.exit(1)

if __name__ == "__main__":
    run_diagnosis()

##### <<< END FILE:   uberslicer/doctor.py <<< #####

##### >>> BEGIN FILE: uberslicer/patch.py <<< #####
import difflib
import uuid
import datetime
import os
import yaml
from pathlib import Path
from uberslicer.utils import CFG, log_dev, log_audit


def create_patch_block(oldfile: str, newfile: str, reason: str) -> None:
    """
    Create a YAML patch block by diffing OLD and NEW files.
    Writes output to the configured patch directory.
    """
    # Read file contents
    try:
        with open(oldfile, 'r') as f:
            old_lines = f.read().splitlines()
    except FileNotFoundError:
        old_lines = []
    try:
        with open(newfile, 'r') as f:
            new_lines = f.read().splitlines()
    except FileNotFoundError:
        new_lines = []

    # Generate unified diff
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=oldfile,
        tofile=newfile,
        lineterm=""
    )
    content = "\n".join(diff)

    # Build the patch block
    block_id = f"patch-{uuid.uuid4()}"
    block = {
        "block_id": block_id,
        "session_metadata": {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "source": os.getcwd()
        },
        "tags": ["patch", "needs-review"],
        "content": content,
        "summary": reason,
        "patch_type": "diff"
    }

    # Ensure output directory exists
    patch_dir = CFG['paths']['patch_dir']
    Path(patch_dir).mkdir(parents=True, exist_ok=True)

    # Write YAML block
    outfile = Path(patch_dir) / f"{block_id}.yaml"
    with open(outfile, 'w') as f:
        yaml.dump(block, f, sort_keys=False)

    # Log and audit
    log_dev("patch", [f"{oldfile} -> {newfile}", reason])
    log_audit("info", f"Patch block created: {outfile}")
    print(f"[OK] Patch block written to {outfile}")

##### <<< END FILE:   uberslicer/patch.py <<< #####

##### >>> BEGIN FILE: uberslicer/ultraslicer.py <<< #####
#!/usr/bin/env python3
import os, sys, uuid, yaml, datetime
from uberslicer.utils import log_dev, log_audit

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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dopemux_ultraslicer.py <input_file> <output_dir>")
        sys.exit(1)
    input_file, outdir = sys.argv[1:3]
    blocks = slice_blocks(input_file)
    dump_blocks(blocks, outdir)
    log_dev(f"ultraslice", details=[f"Sliced {len(blocks)} blocks from {input_file} to {outdir}"])
    log_audit("info", f"Sliced file {input_file} into {len(blocks)} blocks.")
    print(f"[OK] Sliced, tagged, and dumped {len(blocks)} ritual blocks to {outdir}.")

##### <<< END FILE:   uberslicer/ultraslicer.py <<< #####

##### >>> BEGIN FILE: uberslicer/utils.py <<< #####
import yaml
import os
import datetime
from pathlib import Path
import random

# ─── CLI SUPPORTING UTILITIES ──────────────────────────────────────────────
def load_config():
    """Load only the `dopemux` section from config.yaml at project root."""
    cfg_path = Path("config.yaml")
    if not cfg_path.exists():
        raise FileNotFoundError("config.yaml not found")
    full_cfg = yaml.safe_load(cfg_path.read_text())
    if "dopemux" not in full_cfg:
        raise KeyError("config.yaml missing top-level 'dopemux' key")
    return full_cfg["dopemux"]

def colorize(text, style):
    """Placeholder: color your text by style."""
    return text

def print_banner(cfg):
    """If `banner` is set in config, print it once at startup."""
    banner = cfg.get("banner")
    if banner:
        print(banner)

def dopamine_nudge(cfg):
    """Randomly emit one of the `nudges` defined in config."""
    nudges = cfg.get("nudges", [])
    if nudges:
        print(random.choice(nudges))
# ────────────────────────────────────────────────────────────────────────────

# Dev/audit logging helpers (unchanged)
DEVLOG_PATH = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-DEVLOG.txt"
AUDIT_PATH  = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-AUDIT-ULTRA-RITUAL.txt"

def _append_block(path, entry):
    entry['timestamp'] = datetime.datetime.utcnow().isoformat()
    if not os.path.exists(path):
        with open(path, "w") as f: yaml.dump({'entries': [entry]}, f)
    else:
        with open(path) as f: data = yaml.safe_load(f) or {}
        entries = data.get('entries', [])
        entries.append(entry)
        with open(path, "w") as f: yaml.dump({'entries': entries}, f)

def log_dev(action, details=None):
    block = {'action': action, 'details': details or []}
    _append_block(DEVLOG_PATH, block)

def log_audit(level, summary):
    block = {'level': level, 'summary': summary}
    _append_block(AUDIT_PATH, block)

# ─── GLOBAL CONFIG REFERENCE ────────────────────────────────────────────────
CFG = load_config()

##### <<< END FILE:   uberslicer/utils.py <<< #####

##### >>> BEGIN FILE: uberslicer/validator.py <<< #####
from pydantic import BaseModel, ValidationError
import yaml, json, sys, glob
from pathlib import Path
from uberslicer.utils import log_audit, CFG

SCHEMA_PATH = Path(CFG["schema"]["file"])
SCHEMA = json.loads(SCHEMA_PATH.read_text())

class UltraBlock(BaseModel):
    project: str
    block_id: str
    session_metadata: dict
    content: str
    tags: list
    summary: str | None = None
    patch_type: str | None = None  # only for patch blocks

def validate_all():
    """
    Validate every YAML block under the tagged folder against the UltraBlock schema,
    and also catch any 'patch' blocks still carrying the 'needs-review' tag.
    """
    paths = glob.glob(f"{CFG['paths']['tagged']}/**/*.yaml", recursive=True)
    bad, pending = 0, 0

    for p in paths:
        try:
            data = yaml.safe_load(open(p))
            UltraBlock(**data)  # will raise on invalid schema
            if "patch" in data.get("tags", []) and CFG["auditor"]["block_review_tag"] in data.get("tags", []):
                pending += 1
        except ValidationError as e:
            log_audit("error", {"file": p, "errors": e.errors()})
            bad += 1

    if bad or pending:
        sys.exit(f"❌ validation failed: {bad} bad blocks, {pending} pending patches")
    print("✅ all blocks validated & no pending patch review")

##### <<< END FILE:   uberslicer/validator.py <<< #####


--- END: uberslicer-all.txt ---

--- BEGIN: cli.py ---
import click
import pyyaml
import os
import random
from uberslicer.utils import load_config, colorize, print_banner, dopamine_nudge

@click.group()
def cli():
    cfg = load_config()
    print_banner(cfg)
    dopamine_nudge(cfg)

@cli.command()
@click.argument('filepath')
def chunk(filepath):
    "Chunk a raw file and estimate token cost."
    from uberslicer.chunker import chunk_file
    cfg = load_config()
    chunk_file(
        filepath,
        chunk_size=cfg['chunk_size'],
        overlap=cfg['chunk_overlap'],
        model=cfg['default_model'],
        price_per_1k_tokens=cfg['price_per_1k_tokens']
    )

@cli.command()
def prefilter():
    "Prefilter all new chunks to dopemux signal only."
    from uberslicer.prefilter import prefilter_all
    prefilter_all()

@cli.command()
def extract():
    "Extract schema-perfect memory blocks from filtered."
    from uberslicer.extractor import extract_all
    extract_all()

@cli.command()
def merge():
    "Merge, dedupe, and manifest all processed blocks."
    from uberslicer.merge import merge_all
    merge_all()

@cli.command()
def status():
    "Show pipeline progress, manifest, and cost summary."
    from uberslicer.indexer import status_report
    status_report()

@cli.command()
def demo():
    "Run demo/test pipeline on test_data."
    print(colorize("Running dopemux demo on test data...", "accent1"))
    # Optionally call chunk/prefilter/extract/merge on /test_data/

@cli.command()
def package():
    "Zip your full pipeline for dopamine-rich sharing."
    import shutil
    shutil.make_archive("dopemux_memory_dump", 'zip', "data/")
    print(colorize("dopemux memory pit zipped. Extract your dopamine.", "success"))

@cli.command()
@click.argument("oldfile", type=click.Path(exists=True))
@click.option(
    "--new",
    "newfile",
    required=True,
    type=click.Path(exists=True),
    help="Path to the NEW version of the file you are patching"
)
@click.option(
    "--reason",
    default="File diff captured",
    help="Short reason for this patch (shown in devlog)"
)
def patch(oldfile, newfile, reason):
    """
    Create a Dopemux PATCH block between OLDFILE and --new NEWFILE.
    """
    from uberslicer.patch import create_patch_block
    create_patch_block(oldfile, newfile, reason)

@cli.command()
def validate():
    """
    Validate all tagged YAML blocks against the extraction schema,
    and error if any PATCH blocks still carry 'needs-review'.
    """
    from uberslicer.validator import validate_all
    validate_all()

@cli.command()
def doctor():
    """
    Run a quick sanity check on Dopemux paths, config keys, and required folders.
    """
    from uberslicer.doctor import run_diagnosis
    run_diagnosis()

if __name__ == "__main__":
    cli()

--- END: cli.py ---

--- BEGIN: 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-AUDIT-ULTRA-RITUAL.txt ---
entries:
- level: info
  summary: 'Patch block created: tagged/patched/patch-9439c6c8-401e-4214-9c91-e774caa3e3c4.yaml'
  timestamp: '2025-06-17T04:40:14.579774'

--- END: 💊DØPEMÜX-☠️UBERSLICER☠️—TFE-AUDIT-ULTRA-RITUAL.txt ---

--- BEGIN: manifest.json ---
[
  {
    "file": "\ud83d\udc8aD\u00d8PEM\u00dcX-\u2620\ufe0fUBERSLICER\u2620\ufe0f\u2014TFE-DEVLOG.txt",
    "size": 108,
    "sha256": "bf23ad6f58117dedd4ba71abef858b0afecddad687846f396574683962359310",
    "modified": "2025-06-16T21:40:14.579755"
  },
  {
    "file": "pyproject.toml",
    "size": 529,
    "sha256": "5da1d87af9027ca9800ff441d409eecf53e6170a766d0cfd6b9a47e4882b68a6",
    "modified": "2025-06-16T21:24:16.162383"
  },
  {
    "file": "uberslicer-manifest.yaml",
    "size": 809,
    "sha256": "7ae6b4b81c61050f221d08bfc3be09a52253cb30cbbecd798d85c41433493498",
    "modified": "2025-06-17T06:14:35.974773"
  },
  {
    "file": "config.yaml",
    "size": 470,
    "sha256": "9eb7290102744576cd3e88d99b4321babbd47ca4ea0fbae99cc4b2b03020c95e",
    "modified": "2025-06-16T21:35:28.445849"
  },
  {
    "file": "uberslicer-all.txt",
    "size": 10966,
    "sha256": "960028b14526d8dcdd74a746f4a8a9bc6205f160d83558fe1c07928c57ee1879",
    "modified": "2025-06-17T06:14:35.981721"
  },
  {
    "file": "cli.py",
    "size": 2757,
    "sha256": "50f1833e1bc5acd5788efbc68165d99baa158fd610486471ed29ec72935771ec",
    "modified": "2025-06-17T06:07:49.956539"
  },
  {
    "file": "\ud83d\udc8aD\u00d8PEM\u00dcX-\u2620\ufe0fUBERSLICER\u2620\ufe0f\u2014TFE-AUDIT-ULTRA-RITUAL.txt",
    "size": 162,
    "sha256": "c145be09a863e40299bf6b88fe13091a2ce263f26bd367f9081d7b1b5b357422",
    "modified": "2025-06-16T21:40:14.579983"
  },
  {
    "file": "manifest.json",
    "size": 0,
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "modified": "2025-06-17T07:46:51.003544"
  },
  {
    "file": "manifest-gen.py",
    "size": 1338,
    "sha256": "f0a730b06f600fa107230b8c975878c4c4184c73aaac0d2477daac6675326051",
    "modified": "2025-06-16T21:16:04.871866"
  },
  {
    "file": "EXPORT-PROJECT.sh",
    "size": 2320,
    "sha256": "abcc10a7f38e035636501b819980232a681ee4eaeb5e96545c6278dd1c1a1c64",
    "modified": "2025-06-16T21:50:43.760439"
  },
  {
    "file": "local_manifest1.md",
    "size": 0,
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "modified": "2025-06-17T06:07:06.835343"
  },
  {
    "file": "patches/dopemux_patch.patch",
    "size": 2249,
    "sha256": "a214e40cf0e95c01ce66214ea28347ba713a80f96775e2616c2eda8f61952688",
    "modified": "2025-06-16T20:42:23.209907"
  },
  {
    "file": "patches/add-cli-helpers.patch",
    "size": 1407,
    "sha256": "8dd2985979a315ddba200bc7a281e7baf09952571834812673b6b88ada2da76b",
    "modified": "2025-06-16T21:19:35.721341"
  },
  {
    "file": "tests/test_patch_flow.py",
    "size": 661,
    "sha256": "3137f7992d58b0b4d2b842c0dafa5414ebe6d736e3f3d0317a52640598835b5c",
    "modified": "2025-06-16T20:25:22.639657"
  },
  {
    "file": "tagged/patched/patch-9439c6c8-401e-4214-9c91-e774caa3e3c4.yaml",
    "size": 229,
    "sha256": "5436cda8e671d01e6266cf61e6c070563fbb6f64e3bbcf6ecfada7dd4914c71d",
    "modified": "2025-06-16T21:40:14.579491"
  },
  {
    "file": "schema/prompt.json",
    "size": 158,
    "sha256": "34d4deff6a94f9e63c9122583ad8305f8047db107b7e6ff838e1cd7f2087e7f0",
    "modified": "2025-06-17T06:10:26.374316"
  },
  {
    "file": "schema/extraction-schema.json",
    "size": 581,
    "sha256": "8e9c4cb741cc97ef396d040851b7b094093f73917b41a1e0f445eedef4a5b663",
    "modified": "2025-06-16T20:26:48.581851"
  },
  {
    "file": "schema/project_omnibus.json",
    "size": 302,
    "sha256": "7969f1777d085dfd978d368af0cd4f065f96b2944021dc830cb775ffeeac5c53",
    "modified": "2025-06-17T06:10:26.374391"
  },
  {
    "file": "schema/devlog.json",
    "size": 153,
    "sha256": "2702fbb1d2c3957df781bcba67f5568800e80905d63f60c79986c7a312b8a7c4",
    "modified": "2025-06-17T06:10:26.374164"
  },
  {
    "file": "schema/schemas.yaml",
    "size": 1506,
    "sha256": "a4e1f82fe3182958fdac48f0e500e6fbc3e7326f90ad4841296ee235433034b0",
    "modified": "2025-06-17T06:03:57.324730"
  },
  {
    "file": "schema/omnibus.json",
    "size": 354,
    "sha256": "32d3974c6633462c3393fd44e4fe0235310b754cbf3e41b8b524c835f54f82cc",
    "modified": "2025-06-17T06:10:26.374085"
  },
  {
    "file": "schema/ultraslice.json",
    "size": 402,
    "sha256": "b97cc9b2915f6f6c05a15eb570fad508bafe498f96005cb0c5470f15c2f43632",
    "modified": "2025-06-17T06:10:26.373974"
  },
  {
    "file": "schema/artifact.json",
    "size": 189,
    "sha256": "20e386ebb85f809f1b98972cc9802854b9771c561d9f6c585963a0f9a3142799",
    "modified": "2025-06-17T06:10:26.374242"
  },
  {
    "file": "logs/devlog,json",
    "size": 356,
    "sha256": "c21178807f615ff72fd45bf6703e87e26adc601c4610b0b66f6602402ebec6ae",
    "modified": "2025-06-16T20:18:10.029862"
  },
  {
    "file": "scripts/split_yaml_to_json.py",
    "size": 509,
    "sha256": "15acf43d976bac74d0ac636a6b6c2dff7f10e48382b9a93fe5682d3ded941d31",
    "modified": "2025-06-17T06:10:23.289514"
  },
  {
    "file": "scripts/generate-manifest.py",
    "size": 3142,
    "sha256": "1af53cc98295aa3b45bf52d96f4be0c9ad1c9e5f9483c1a759e792cb6043bd8a",
    "modified": "2025-06-17T07:44:24.905055"
  },
  {
    "file": "venv/pyvenv.cfg",
    "size": 349,
    "sha256": "b16560fe8343b4b8c790f1205b88a5a3d33d837c5171aaf28f1d5e8861b80fe4",
    "modified": "2025-06-17T07:44:42.818606"
  },
  {
    "file": "venv/.gitignore",
    "size": 69,
    "sha256": "36692e1840f82f75adce103fd03e65b1eaa35f798c885b3b545e3abc14ffcbf0",
    "modified": "2025-06-17T07:44:42.818319"
  },
  {
    "file": "venv/bin/Activate.ps1",
    "size": 9031,
    "sha256": "eb8ce20f580877d300c4fed60a7f36daa18715d35c50bb3596d6995d023b4ffe",
    "modified": "2025-06-11T08:36:57"
  },
  {
    "file": "venv/bin/python3",
    "size": 52640,
    "sha256": "a1f6d9dc20d4787a84dc2fe782094a7bac5946f49a962aa0af48a02f0e8d5bc5",
    "modified": "2025-06-14T03:28:32.858893"
  },
  {
    "file": "venv/bin/pip3.13",
    "size": 250,
    "sha256": "629a6b2c2d2cc31b27e659d6f98bfc84401d49863d33e6df0f29a31423f16017",
    "modified": "2025-06-17T06:09:39.327869"
  },
  {
    "file": "venv/bin/python",
    "size": 52640,
    "sha256": "a1f6d9dc20d4787a84dc2fe782094a7bac5946f49a962aa0af48a02f0e8d5bc5",
    "modified": "2025-06-14T03:28:32.858893"
  },
  {
    "file": "venv/bin/pip3",
    "size": 250,
    "sha256": "629a6b2c2d2cc31b27e659d6f98bfc84401d49863d33e6df0f29a31423f16017",
    "modified": "2025-06-17T06:09:39.327754"
  },
  {
    "file": "venv/bin/activate.fish",
    "size": 2192,
    "sha256": "40fa1c730fbc26ce4b3defc833e14ec1b16f67a5963b17c423d3ab4085003f45",
    "modified": "2025-06-17T07:44:43.492303"
  },
  {
    "file": "venv/bin/pip",
    "size": 250,
    "sha256": "629a6b2c2d2cc31b27e659d6f98bfc84401d49863d33e6df0f29a31423f16017",
    "modified": "2025-06-17T06:09:39.327621"
  },
  {
    "file": "venv/bin/activate",
    "size": 2174,
    "sha256": "14c2ad7270db02b84e34e71e78a0b2b35dc2f20773df60b95c7a0f2b92ab621c",
    "modified": "2025-06-17T07:44:43.492444"
  },
  {
    "file": "venv/bin/python3.13",
    "size": 52640,
    "sha256": "a1f6d9dc20d4787a84dc2fe782094a7bac5946f49a962aa0af48a02f0e8d5bc5",
    "modified": "2025-06-14T03:28:32.858893"
  },
  {
    "file": "venv/bin/activate.csh",
    "size": 921,
    "sha256": "02c1ba9ae1708fa69bbbcb01ba6f34599b0f68c64fe4d22bbb5253c5a73741ba",
    "modified": "2025-06-17T07:44:43.491435"
  },
  {
    "file": "uberslicer/validator.py",
    "size": 1328,
    "sha256": "e6cd921760b98eb9b6446725adab8cf3ea4f6b550de9777483fa18529322264c",
    "modified": "2025-06-16T21:30:41.010898"
  },
  {
    "file": "uberslicer/patch.py",
    "size": 1732,
    "sha256": "3a491d06fbdf9742e9be2a561659a8cdeb374ff9d68a208e130a94671ba5a75b",
    "modified": "2025-06-16T21:40:09.299222"
  },
  {
    "file": "uberslicer/__init__.py",
    "size": 414,
    "sha256": "d0562442e0404515e3fd4b0ee66c2577b022dd62260720b764bfd92b2a9640af",
    "modified": "2025-06-16T21:09:15.846469"
  },
  {
    "file": "uberslicer/ultraslicer.py",
    "size": 2218,
    "sha256": "03130697fa4f1dc01871bdc2e142c3cfd3a0a850f55164f3af8f3ba0ad725281",
    "modified": "2025-06-16T21:28:08.814837"
  },
  {
    "file": "uberslicer/utils.py",
    "size": 2373,
    "sha256": "1592c2880d715f418f056ddbc0354c96d03ec6c6a4c5d3e50f014a00ecfb72c2",
    "modified": "2025-06-16T21:30:33.868573"
  },
  {
    "file": "uberslicer/doctor.py",
    "size": 2237,
    "sha256": "ae42433724f398a12597be9085e31f1fa22aa3793663efa6604055cfc91906ad",
    "modified": "2025-06-16T21:30:50.024274"
  }
]
--- END: manifest.json ---

--- BEGIN: manifest-gen.py ---
import os
import argparse

def generate_manifest(root, max_depth=None):
    manifest = []
    for dirpath, dirnames, filenames in os.walk(root):
        depth = dirpath.replace(root, '').count(os.sep)
        if max_depth is not None and depth > max_depth:
            # prune deeper dirs
            dirnames[:] = []
            continue
        # directory entry
        rel_path = os.path.relpath(dirpath, root)
        if rel_path == '.':
            rel_path = root
        manifest.append((rel_path + os.sep, 'dir', ''))
        # files
        for f in filenames:
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, root)
            manifest.append((rel, 'file', ''))
    return manifest


def to_markdown(manifest):
    md = ['| Path | Type | |', '|---|---|---|']
    for path, typ, desc in manifest:
        md.append(f'| `{path}` | {typ} | {desc} |')
    return '\n'.join(md)


def main():
    parser = argparse.ArgumentParser(description='Generate a directory manifest in Markdown.')
    parser.add_argument('root', help='Root directory to scan')
    parser.add_argument('--depth', type=int, default=None, help='Max recursion depth')
    args = parser.parse_args()

    manifest = generate_manifest(args.root, args.depth)
    print(to_markdown(manifest))

if __name__ == '__main__':
    main()

--- END: manifest-gen.py ---

--- BEGIN: EXPORT-PROJECT.sh ---
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

--- END: EXPORT-PROJECT.sh ---

--- BEGIN: local_manifest1.md ---

--- END: local_manifest1.md ---

--- BEGIN: patches/dopemux_patch.patch ---
#!/usr/bin/env python3
import difflib, yaml, os, sys, pathlib, datetime, hashlib, json
from uuid import uuid4
from dopemux_utils import log_dev               # already in repo

CFG = yaml.safe_load(open("config.yaml"))["dopemux"]
PATCH_DIR = pathlib.Path(CFG["paths"]["tagged"]) / "patch"

def unified(old, new, fname):
    return "\n".join(
        difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile=f"{fname} (old)",
            tofile=f"{fname} (new)",
            lineterm=""
        )
    )

def make_block(fname, diff_text, reason):
    now = datetime.datetime.utcnow().isoformat() + "Z"
    block = {
        "project": "dopemux",
        "session_metadata": {"timestamp": now, "source_file": fname},
        "block_id": f"patch-{uuid4()}",
        "patch_type": "file",
        "source_file": fname,
        "tags": ["patch", "needs-review"],
        "summary": reason or "File diff captured",
        "content": "|-\n" + diff_text.replace("\n", "\n  "),
        "map_refs": [],
        "decisions": [],
        "blockers": [],
        "meta_validation": [],
        "dopaminehit": [],
        "ritual_notes": f"PATCH block generated {now}"
    }
    return yaml.dump(block, sort_keys=False)

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: dopemux patch <file> [--reason '...']")
    fname = sys.argv[1]
    reason = " ".join(sys.argv[2:]).lstrip("--reason").strip() if len(sys.argv) > 2 else ""
    old = open(fname).read()
    # quick safety copy
    new_path = input("[?] Path to NEW version (leave blank to abort): ").strip()
    if not new_path:
        sys.exit("Aborted.")
    new = open(new_path).read()
    diff = unified(old, new, fname)
    if not diff:
        sys.exit("[OK] No changes detected.")
    PATCH_DIR.mkdir(parents=True, exist_ok=True)
    outfile = PATCH_DIR / f"{pathlib.Path(fname).stem}_{uuid4()}.yaml"
    outfile.write_text(make_block(fname, diff, reason))
    # log dev event
    log_dev({"timestamp": datetime.datetime.utcnow().isoformat()+"Z",
             "action": "patch_created",
             "file": str(outfile),
             "source": fname})
    print(f"[OK] PATCH block saved → {outfile}")

if __name__ == "__main__":
    main()

--- END: patches/dopemux_patch.patch ---

--- BEGIN: patches/add-cli-helpers.patch ---
--- a/uberslicer/utils.py
+++ b/uberslicer/utils.py
@@
-import yaml, os, datetime
+import yaml, os, datetime
+from pathlib import Path
+
+# ─── CLI SUPPORTING UTILITIES ──────────────────────────────────────────────
+def load_config():
+    """Load config.yaml from project root."""
+    cfg_path = Path("config.yaml")
+    if not cfg_path.exists():
+        raise FileNotFoundError("config.yaml not found")
+    return yaml.safe_load(cfg_path.read_text())
+
+def colorize(text, style):
+    """Placeholder for coloring text by style."""
+    return text
+
+def print_banner(cfg):
+    """Print banner if defined in config under 'banner'."""
+    banner = cfg.get("banner")
+    if banner:
+        print(banner)
+
+def dopamine_nudge(cfg):
+    """Print a random dopamine nudge if defined under 'nudges'."""
+    nudges = cfg.get("nudges", [])
+    if nudges:
+        import random
+        print(random.choice(nudges))
+# ────────────────────────────────────────────────────────────────────────────

 DEVLOG_PATH = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-DEVLOG.txt"
 AUDIT_PATH  = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-AUDIT-ULTRA-RITUAL.txt"

--- END: patches/add-cli-helpers.patch ---

--- BEGIN: tests/test_patch_flow.py ---
import yaml, subprocess, shutil, pathlib, uuid

def test_patch_block(tmp_path):
    old = tmp_path / "old.py"
    new = tmp_path / "new.py"
    old.write_text("x = 1\n")
    new.write_text("x = 2\n")
    tagdir = tmp_path / "tagged/patch"
    tagdir.mkdir(parents=True)
    # point config at tmp dirs
    patch = subprocess.run([
        "dopemux", "patch", str(old),
        "--new", str(new),
        "--reason", "unit test"
    ], cwd=tmp_path, capture_output=True, text=True)
    assert patch.returncode == 0
    files = list(tagdir.glob("*.yaml"))
    assert len(files) == 1
    blk = yaml.safe_load(files[0].read_text())
    assert "patch" in blk["tags"]

--- END: tests/test_patch_flow.py ---

--- BEGIN: tagged/patched/patch-9439c6c8-401e-4214-9c91-e774caa3e3c4.yaml ---
block_id: patch-9439c6c8-401e-4214-9c91-e774caa3e3c4
session_metadata:
  timestamp: '2025-06-17T04:40:14.578857'
  source: "/Users/hu/code/D\xD8PEMU\u0308X"
tags:
- patch
- needs-review
content: ''
summary: demo
patch_type: diff

--- END: tagged/patched/patch-9439c6c8-401e-4214-9c91-e774caa3e3c4.yaml ---

--- BEGIN: schema/prompt.json ---
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
--- END: schema/prompt.json ---

--- BEGIN: schema/extraction-schema.json ---
{
  "title": "UltraBlock",
  "type": "object",
  "required": [
    "project","block_id","session_metadata","content",
    "tags","summary","map_refs","decisions",
    "blockers","meta_validation","dopaminehit","ritual_notes"
  ],
  "properties": {
    "project": { "type": "string" },
    "block_id": { "type": "string" },
    "session_metadata": {
      "type": "object",
      "required": ["timestamp","source_file"]
    },
    "content": { "type": "string" },
    "tags": { "type": "array", "items": { "type": "string" } },
    "patch_type": { "type": "string" }           
}
}

--- END: schema/extraction-schema.json ---

--- BEGIN: schema/project_omnibus.json ---
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
--- END: schema/project_omnibus.json ---

--- BEGIN: schema/devlog.json ---
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
--- END: schema/devlog.json ---

--- BEGIN: schema/schemas.yaml ---
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

--- END: schema/schemas.yaml ---

--- BEGIN: schema/omnibus.json ---
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
--- END: schema/omnibus.json ---

--- BEGIN: schema/ultraslice.json ---
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
--- END: schema/ultraslice.json ---

--- BEGIN: schema/artifact.json ---
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
--- END: schema/artifact.json ---

--- BEGIN: logs/devlog,json ---
{
  "2024-06-12": [
    "Initial filth, brand, and logic flows implemented.",
    "Adaptive dopamine engine draft finished.",
    "Dopamine hits now support LLM memory/context.",
    "Configurable filth level and thresholds."
  ],
  "2024-06-13": [
    "Began LLM self-check validation and feedback loop.",
    "Tested YAML/JSON config integration."
  ]
}

--- END: logs/devlog,json ---

--- BEGIN: scripts/split_yaml_to_json.py ---
import yaml
import json
import pathlib

SCHEMA_YAML = pathlib.Path(__file__).parent.parent / "schema" / "schemas.yaml"
OUTPUT_DIR = pathlib.Path(__file__).parent.parent / "schema"

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

def write_all_files(manifest, root, output_path="all-files.md"):
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
    parser.add_argument('--all-md', default='all-files.md', help='Output concatenated markdown file')
    args = parser.parse_args()

    manifest = walk_dir(args.root, args.depth)
    with open(args.output, "w") as out:
        json.dump(manifest, out, indent=2)
    write_all_files(manifest, args.root, args.all_md)

if __name__ == '__main__':
    main()
--- END: scripts/generate-manifest.py ---

--- BEGIN: venv/pyvenv.cfg ---
home = /opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/bin
include-system-site-packages = false
version = 3.13.5
executable = /opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/bin/python3.13
command = /Users/hu/code/DØPEMÜX/venv/bin/python3 -m venv /Users/hu/code/DØPEMÜX/venv

--- END: venv/pyvenv.cfg ---

--- BEGIN: venv/.gitignore ---
# Created by venv; see https://docs.python.org/3/library/venv.html
*

--- END: venv/.gitignore ---

--- BEGIN: venv/bin/Activate.ps1 ---
<#
.Synopsis
Activate a Python virtual environment for the current PowerShell session.

.Description
Pushes the python executable for a virtual environment to the front of the
$Env:PATH environment variable and sets the prompt to signify that you are
in a Python virtual environment. Makes use of the command line switches as
well as the `pyvenv.cfg` file values present in the virtual environment.

.Parameter VenvDir
Path to the directory that contains the virtual environment to activate. The
default value for this is the parent of the directory that the Activate.ps1
script is located within.

.Parameter Prompt
The prompt prefix to display when this virtual environment is activated. By
default, this prompt is the name of the virtual environment folder (VenvDir)
surrounded by parentheses and followed by a single space (ie. '(.venv) ').

.Example
Activate.ps1
Activates the Python virtual environment that contains the Activate.ps1 script.

.Example
Activate.ps1 -Verbose
Activates the Python virtual environment that contains the Activate.ps1 script,
and shows extra information about the activation as it executes.

.Example
Activate.ps1 -VenvDir C:\Users\MyUser\Common\.venv
Activates the Python virtual environment located in the specified location.

.Example
Activate.ps1 -Prompt "MyPython"
Activates the Python virtual environment that contains the Activate.ps1 script,
and prefixes the current prompt with the specified string (surrounded in
parentheses) while the virtual environment is active.

.Notes
On Windows, it may be required to enable this Activate.ps1 script by setting the
execution policy for the user. You can do this by issuing the following PowerShell
command:

PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

For more information on Execution Policies: 
https://go.microsoft.com/fwlink/?LinkID=135170

#>
Param(
    [Parameter(Mandatory = $false)]
    [String]
    $VenvDir,
    [Parameter(Mandatory = $false)]
    [String]
    $Prompt
)

<# Function declarations --------------------------------------------------- #>

<#
.Synopsis
Remove all shell session elements added by the Activate script, including the
addition of the virtual environment's Python executable from the beginning of
the PATH variable.

.Parameter NonDestructive
If present, do not remove this function from the global namespace for the
session.

#>
function global:deactivate ([switch]$NonDestructive) {
    # Revert to original values

    # The prior prompt:
    if (Test-Path -Path Function:_OLD_VIRTUAL_PROMPT) {
        Copy-Item -Path Function:_OLD_VIRTUAL_PROMPT -Destination Function:prompt
        Remove-Item -Path Function:_OLD_VIRTUAL_PROMPT
    }

    # The prior PYTHONHOME:
    if (Test-Path -Path Env:_OLD_VIRTUAL_PYTHONHOME) {
        Copy-Item -Path Env:_OLD_VIRTUAL_PYTHONHOME -Destination Env:PYTHONHOME
        Remove-Item -Path Env:_OLD_VIRTUAL_PYTHONHOME
    }

    # The prior PATH:
    if (Test-Path -Path Env:_OLD_VIRTUAL_PATH) {
        Copy-Item -Path Env:_OLD_VIRTUAL_PATH -Destination Env:PATH
        Remove-Item -Path Env:_OLD_VIRTUAL_PATH
    }

    # Just remove the VIRTUAL_ENV altogether:
    if (Test-Path -Path Env:VIRTUAL_ENV) {
        Remove-Item -Path env:VIRTUAL_ENV
    }

    # Just remove VIRTUAL_ENV_PROMPT altogether.
    if (Test-Path -Path Env:VIRTUAL_ENV_PROMPT) {
        Remove-Item -Path env:VIRTUAL_ENV_PROMPT
    }

    # Just remove the _PYTHON_VENV_PROMPT_PREFIX altogether:
    if (Get-Variable -Name "_PYTHON_VENV_PROMPT_PREFIX" -ErrorAction SilentlyContinue) {
        Remove-Variable -Name _PYTHON_VENV_PROMPT_PREFIX -Scope Global -Force
    }

    # Leave deactivate function in the global namespace if requested:
    if (-not $NonDestructive) {
        Remove-Item -Path function:deactivate
    }
}

<#
.Description
Get-PyVenvConfig parses the values from the pyvenv.cfg file located in the
given folder, and returns them in a map.

For each line in the pyvenv.cfg file, if that line can be parsed into exactly
two strings separated by `=` (with any amount of whitespace surrounding the =)
then it is considered a `key = value` line. The left hand string is the key,
the right hand is the value.

If the value starts with a `'` or a `"` then the first and last character is
stripped from the value before being captured.

.Parameter ConfigDir
Path to the directory that contains the `pyvenv.cfg` file.
#>
function Get-PyVenvConfig(
    [String]
    $ConfigDir
) {
    Write-Verbose "Given ConfigDir=$ConfigDir, obtain values in pyvenv.cfg"

    # Ensure the file exists, and issue a warning if it doesn't (but still allow the function to continue).
    $pyvenvConfigPath = Join-Path -Resolve -Path $ConfigDir -ChildPath 'pyvenv.cfg' -ErrorAction Continue

    # An empty map will be returned if no config file is found.
    $pyvenvConfig = @{ }

    if ($pyvenvConfigPath) {

        Write-Verbose "File exists, parse `key = value` lines"
        $pyvenvConfigContent = Get-Content -Path $pyvenvConfigPath

        $pyvenvConfigContent | ForEach-Object {
            $keyval = $PSItem -split "\s*=\s*", 2
            if ($keyval[0] -and $keyval[1]) {
                $val = $keyval[1]

                # Remove extraneous quotations around a string value.
                if ("'""".Contains($val.Substring(0, 1))) {
                    $val = $val.Substring(1, $val.Length - 2)
                }

                $pyvenvConfig[$keyval[0]] = $val
                Write-Verbose "Adding Key: '$($keyval[0])'='$val'"
            }
        }
    }
    return $pyvenvConfig
}


<# Begin Activate script --------------------------------------------------- #>

# Determine the containing directory of this script
$VenvExecPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VenvExecDir = Get-Item -Path $VenvExecPath

Write-Verbose "Activation script is located in path: '$VenvExecPath'"
Write-Verbose "VenvExecDir Fullname: '$($VenvExecDir.FullName)"
Write-Verbose "VenvExecDir Name: '$($VenvExecDir.Name)"

# Set values required in priority: CmdLine, ConfigFile, Default
# First, get the location of the virtual environment, it might not be
# VenvExecDir if specified on the command line.
if ($VenvDir) {
    Write-Verbose "VenvDir given as parameter, using '$VenvDir' to determine values"
}
else {
    Write-Verbose "VenvDir not given as a parameter, using parent directory name as VenvDir."
    $VenvDir = $VenvExecDir.Parent.FullName.TrimEnd("\\/")
    Write-Verbose "VenvDir=$VenvDir"
}

# Next, read the `pyvenv.cfg` file to determine any required value such
# as `prompt`.
$pyvenvCfg = Get-PyVenvConfig -ConfigDir $VenvDir

# Next, set the prompt from the command line, or the config file, or
# just use the name of the virtual environment folder.
if ($Prompt) {
    Write-Verbose "Prompt specified as argument, using '$Prompt'"
}
else {
    Write-Verbose "Prompt not specified as argument to script, checking pyvenv.cfg value"
    if ($pyvenvCfg -and $pyvenvCfg['prompt']) {
        Write-Verbose "  Setting based on value in pyvenv.cfg='$($pyvenvCfg['prompt'])'"
        $Prompt = $pyvenvCfg['prompt'];
    }
    else {
        Write-Verbose "  Setting prompt based on parent's directory's name. (Is the directory name passed to venv module when creating the virtual environment)"
        Write-Verbose "  Got leaf-name of $VenvDir='$(Split-Path -Path $venvDir -Leaf)'"
        $Prompt = Split-Path -Path $venvDir -Leaf
    }
}

Write-Verbose "Prompt = '$Prompt'"
Write-Verbose "VenvDir='$VenvDir'"

# Deactivate any currently active virtual environment, but leave the
# deactivate function in place.
deactivate -nondestructive

# Now set the environment variable VIRTUAL_ENV, used by many tools to determine
# that there is an activated venv.
$env:VIRTUAL_ENV = $VenvDir

$env:VIRTUAL_ENV_PROMPT = $Prompt

if (-not $Env:VIRTUAL_ENV_DISABLE_PROMPT) {

    Write-Verbose "Setting prompt to '$Prompt'"

    # Set the prompt to include the env name
    # Make sure _OLD_VIRTUAL_PROMPT is global
    function global:_OLD_VIRTUAL_PROMPT { "" }
    Copy-Item -Path function:prompt -Destination function:_OLD_VIRTUAL_PROMPT
    New-Variable -Name _PYTHON_VENV_PROMPT_PREFIX -Description "Python virtual environment prompt prefix" -Scope Global -Option ReadOnly -Visibility Public -Value $Prompt

    function global:prompt {
        Write-Host -NoNewline -ForegroundColor Green "($_PYTHON_VENV_PROMPT_PREFIX) "
        _OLD_VIRTUAL_PROMPT
    }
}

# Clear PYTHONHOME
if (Test-Path -Path Env:PYTHONHOME) {
    Copy-Item -Path Env:PYTHONHOME -Destination Env:_OLD_VIRTUAL_PYTHONHOME
    Remove-Item -Path Env:PYTHONHOME
}

# Add the venv to the PATH
Copy-Item -Path Env:PATH -Destination Env:_OLD_VIRTUAL_PATH
$Env:PATH = "$VenvExecDir$([System.IO.Path]::PathSeparator)$Env:PATH"

--- END: venv/bin/Activate.ps1 ---

--- BEGIN: venv/bin/python3 ---
����            0  �          H   __PAGEZERO                                                        �  __TEXT                  @               @                   __text          __TEXT          P
     �      P
               �            __stubs         __TEXT          H     �       H              �           __cstring       __TEXT               �                                    __unwind_info   __TEXT          �     h       �                                �   __DATA_CONST     @      @       @       @                  __got           __DATA_CONST     @     �        @                              �   __DATA           �      @                                   __bss           __DATA           �                                              H   __LINKEDIT       �      �       �      �M                    4  �    �  �  3  �   ��  0         ��     �  0     P                                              P�  %                             /usr/lib/dyld             |;g�[�1n������۸2                     �*              (  �   P
                 x          
  
 /opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/Python           8           G   /usr/lib/libSystem.B.dylib      &      ��     )      ��             �  �H                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  ����_��W��O��{������   �  @��C ��  �`  5 ��   �@����  �� � � ��  �� �  ������  �� �� �  T��J�_8�	�_� qA��T�	� ���*@8_� q��	  �)%� @�  � ��< ��< �R� �@  �   ��3 ��  �  5U  �� �����R�  �� �   � ��A  �!  ��  �@ �@  �   �  �!�� �R �R~  � �� T@  �   ���
  � �@9 9A  �!  ����  �� �� 9@  �   ��� �R �Ri  � � Tc  ���R  �� �  �!P�     � ��A  �!  �" �R{  �t �� ��C �  �(  �@�@��C �  ���� ����_  �� �  �!��  �RN  ��� ��O��{��� �� �W  �� �=  �  �4 5��R �r� �� ��# ���! �RN  � 1  T�@� �� T���RI  �� �)  �  �3 5�{B��OA��� ��_�
  �  �(  �
@�@�   � ��A�R" �R(  �  �R#  �  ��{��� �  �!��@ �R  ��{��� �  �!8�  �R  ��{��� �  �! �  �R
  �  �@� �  �
@� �  �@� �  �@� �  �@� �  �"@� �  �&@� �  �*@� �  �.@� �  �2@� �  �6@� �  �:@� �  �>@� �  �B@� �  �F@� �  �J@� �  �N@� �realpath: %s . / __PYVENV_LAUNCHER__ posix_spawn: %s Resources/Python.app/Contents/MacOS/Python posix_spawnattr_int posix_spawnattr_setbinpref posix_spawnattr_setbinpref failed to copy
 posix_spawnattr_setflags                         P
  @   @   H      @                          � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  �     �     �     �     �     �     �     �     �	     �
     �     �     �
     �     �     �     �     �     �      �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        P   �                                           @  @                  L  ^  t  �  �  �  �  �  �  �   0 n � � � �    _Py_Initialize __NSGetExecutablePath ___error ___stderrp ___strlcat_chk _dladdr _environ _err _exit _fwrite _malloc _posix_spawn _posix_spawnattr_init _posix_spawnattr_setbinpref_np _posix_spawnattr_setflags _realpath$DARWIN_EXTSN _setenv _strcpy _strlen _strrchr         __mh_execute_header         header 	main 
  ���           <   BEa                            '             =             F             Q             `             h             q             v             |             �             �             �             �             �             �             �                                                             	   
         
                                                	   
         
                                   __mh_execute_header _Py_Initialize __NSGetExecutablePath ___error ___stderrp ___strlcat_chk _dladdr _environ _err _exit _fwrite _malloc _posix_spawn _posix_spawnattr_init _posix_spawnattr_setbinpref_np _posix_spawnattr_setflags _realpath$DARWIN_EXTSN _setenv _strcpy _strlen _strrchr radr://5614542          ���  !          $     
     ��  �        �   X      	  �                                         @        python3-555549447c3b67815ba7316ea1b1fcffedf7dbb8 �y �N�eux�J��RNj����-��7�C��                                qg��cơ�Ϸ��H�o$đ�k�j���\ �,R��A]xwO"!��"�0��e������qG|���Xo��f����kOX�|�|z�ڽ�H�,����Xo��f����kOX�|�|z�ڽ�H�,�$�G���:t"�x�����F�%),�D����Xo��f����kOX�|�|z�ڽ�H�,����Xo��f����kOX�|�|z�ڽ�H�,����Xo��f����kOX�|�|z�ڽ�H�,��5\M��eޓC[��eĂ���.�@,�7��͑��       ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
--- END: venv/bin/python3 ---

--- BEGIN: venv/bin/pip3.13 ---
#!/Users/hu/code/DØPEMÜX/venv/bin/python3.13
# -*- coding: utf-8 -*-
import re
import sys
from pip._internal.cli.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

--- END: venv/bin/pip3.13 ---

--- BEGIN: venv/bin/python ---
����            0  �          H   __PAGEZERO                                                        �  __TEXT                  @               @                   __text          __TEXT          P
     �      P
               �            __stubs         __TEXT          H     �       H              �           __cstring       __TEXT               �                                    __unwind_info   __TEXT          �     h       �                                �   __DATA_CONST     @      @       @       @                  __got           __DATA_CONST     @     �        @                              �   __DATA           �      @                                   __bss           __DATA           �                                              H   __LINKEDIT       �      �       �      �M                    4  �    �  �  3  �   ��  0         ��     �  0     P                                              P�  %                             /usr/lib/dyld             |;g�[�1n������۸2                     �*              (  �   P
                 x          
  
 /opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/Python           8           G   /usr/lib/libSystem.B.dylib      &      ��     )      ��             �  �H                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  ����_��W��O��{������   �  @��C ��  �`  5 ��   �@����  �� � � ��  �� �  ������  �� �� �  T��J�_8�	�_� qA��T�	� ���*@8_� q��	  �)%� @�  � ��< ��< �R� �@  �   ��3 ��  �  5U  �� �����R�  �� �   � ��A  �!  ��  �@ �@  �   �  �!�� �R �R~  � �� T@  �   ���
  � �@9 9A  �!  ����  �� �� 9@  �   ��� �R �Ri  � � Tc  ���R  �� �  �!P�     � ��A  �!  �" �R{  �t �� ��C �  �(  �@�@��C �  ���� ����_  �� �  �!��  �RN  ��� ��O��{��� �� �W  �� �=  �  �4 5��R �r� �� ��# ���! �RN  � 1  T�@� �� T���RI  �� �)  �  �3 5�{B��OA��� ��_�
  �  �(  �
@�@�   � ��A�R" �R(  �  �R#  �  ��{��� �  �!��@ �R  ��{��� �  �!8�  �R  ��{��� �  �! �  �R
  �  �@� �  �
@� �  �@� �  �@� �  �@� �  �"@� �  �&@� �  �*@� �  �.@� �  �2@� �  �6@� �  �:@� �  �>@� �  �B@� �  �F@� �  �J@� �  �N@� �realpath: %s . / __PYVENV_LAUNCHER__ posix_spawn: %s Resources/Python.app/Contents/MacOS/Python posix_spawnattr_int posix_spawnattr_setbinpref posix_spawnattr_setbinpref failed to copy
 posix_spawnattr_setflags                         P
  @   @   H      @                          � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  �     �     �     �     �     �     �     �     �	     �
     �     �     �
     �     �     �     �     �     �      �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        P   �                                           @  @                  L  ^  t  �  �  �  �  �  �  �   0 n � � � �    _Py_Initialize __NSGetExecutablePath ___error ___stderrp ___strlcat_chk _dladdr _environ _err _exit _fwrite _malloc _posix_spawn _posix_spawnattr_init _posix_spawnattr_setbinpref_np _posix_spawnattr_setflags _realpath$DARWIN_EXTSN _setenv _strcpy _strlen _strrchr         __mh_execute_header         header 	main 
  ���           <   BEa                            '             =             F             Q             `             h             q             v             |             �             �             �             �             �             �             �                                                             	   
         
                                                	   
         
                                   __mh_execute_header _Py_Initialize __NSGetExecutablePath ___error ___stderrp ___strlcat_chk _dladdr _environ _err _exit _fwrite _malloc _posix_spawn _posix_spawnattr_init _posix_spawnattr_setbinpref_np _posix_spawnattr_setflags _realpath$DARWIN_EXTSN _setenv _strcpy _strlen _strrchr radr://5614542          ���  !          $     
     ��  �        �   X      	  �                                         @        python3-555549447c3b67815ba7316ea1b1fcffedf7dbb8 �y �N�eux�J��RNj����-��7�C��                                qg��cơ�Ϸ��H�o$đ�k�j���\ �,R��A]xwO"!��"�0��e������qG|���Xo��f����kOX�|�|z�ڽ�H�,����Xo��f����kOX�|�|z�ڽ�H�,�$�G���:t"�x�����F�%),�D����Xo��f����kOX�|�|z�ڽ�H�,����Xo��f����kOX�|�|z�ڽ�H�,����Xo��f����kOX�|�|z�ڽ�H�,��5\M��eޓC[��eĂ���.�@,�7��͑��       ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
--- END: venv/bin/python ---

--- BEGIN: venv/bin/pip3 ---
#!/Users/hu/code/DØPEMÜX/venv/bin/python3.13
# -*- coding: utf-8 -*-
import re
import sys
from pip._internal.cli.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

--- END: venv/bin/pip3 ---

--- BEGIN: venv/bin/activate.fish ---
# This file must be used with "source <venv>/bin/activate.fish" *from fish*
# (https://fishshell.com/). You cannot run it directly.

function deactivate  -d "Exit virtual environment and return to normal shell environment"
    # reset old environment variables
    if test -n "$_OLD_VIRTUAL_PATH"
        set -gx PATH $_OLD_VIRTUAL_PATH
        set -e _OLD_VIRTUAL_PATH
    end
    if test -n "$_OLD_VIRTUAL_PYTHONHOME"
        set -gx PYTHONHOME $_OLD_VIRTUAL_PYTHONHOME
        set -e _OLD_VIRTUAL_PYTHONHOME
    end

    if test -n "$_OLD_FISH_PROMPT_OVERRIDE"
        set -e _OLD_FISH_PROMPT_OVERRIDE
        # prevents error when using nested fish instances (Issue #93858)
        if functions -q _old_fish_prompt
            functions -e fish_prompt
            functions -c _old_fish_prompt fish_prompt
            functions -e _old_fish_prompt
        end
    end

    set -e VIRTUAL_ENV
    set -e VIRTUAL_ENV_PROMPT
    if test "$argv[1]" != "nondestructive"
        # Self-destruct!
        functions -e deactivate
    end
end

# Unset irrelevant variables.
deactivate nondestructive

set -gx VIRTUAL_ENV '/Users/hu/code/DØPEMÜX/venv'

set -gx _OLD_VIRTUAL_PATH $PATH
set -gx PATH "$VIRTUAL_ENV/"bin $PATH
set -gx VIRTUAL_ENV_PROMPT venv

# Unset PYTHONHOME if set.
if set -q PYTHONHOME
    set -gx _OLD_VIRTUAL_PYTHONHOME $PYTHONHOME
    set -e PYTHONHOME
end

if test -z "$VIRTUAL_ENV_DISABLE_PROMPT"
    # fish uses a function instead of an env var to generate the prompt.

    # Save the current fish_prompt function as the function _old_fish_prompt.
    functions -c fish_prompt _old_fish_prompt

    # With the original prompt function renamed, we can override with our own.
    function fish_prompt
        # Save the return status of the last command.
        set -l old_status $status

        # Output the venv prompt; color taken from the blue of the Python logo.
        printf "%s(%s)%s " (set_color 4B8BBE) venv (set_color normal)

        # Restore the return status of the previous command.
        echo "exit $old_status" | .
        # Output the original/"old" prompt.
        _old_fish_prompt
    end

    set -gx _OLD_FISH_PROMPT_OVERRIDE "$VIRTUAL_ENV"
end

--- END: venv/bin/activate.fish ---

--- BEGIN: venv/bin/pip ---
#!/Users/hu/code/DØPEMÜX/venv/bin/python3.13
# -*- coding: utf-8 -*-
import re
import sys
from pip._internal.cli.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

--- END: venv/bin/pip ---

--- BEGIN: venv/bin/activate ---
# This file must be used with "source bin/activate" *from bash*
# You cannot run it directly

deactivate () {
    # reset old environment variables
    if [ -n "${_OLD_VIRTUAL_PATH:-}" ] ; then
        PATH="${_OLD_VIRTUAL_PATH:-}"
        export PATH
        unset _OLD_VIRTUAL_PATH
    fi
    if [ -n "${_OLD_VIRTUAL_PYTHONHOME:-}" ] ; then
        PYTHONHOME="${_OLD_VIRTUAL_PYTHONHOME:-}"
        export PYTHONHOME
        unset _OLD_VIRTUAL_PYTHONHOME
    fi

    # Call hash to forget past locations. Without forgetting
    # past locations the $PATH changes we made may not be respected.
    # See "man bash" for more details. hash is usually a builtin of your shell
    hash -r 2> /dev/null

    if [ -n "${_OLD_VIRTUAL_PS1:-}" ] ; then
        PS1="${_OLD_VIRTUAL_PS1:-}"
        export PS1
        unset _OLD_VIRTUAL_PS1
    fi

    unset VIRTUAL_ENV
    unset VIRTUAL_ENV_PROMPT
    if [ ! "${1:-}" = "nondestructive" ] ; then
    # Self destruct!
        unset -f deactivate
    fi
}

# unset irrelevant variables
deactivate nondestructive

# on Windows, a path can contain colons and backslashes and has to be converted:
case "$(uname)" in
    CYGWIN*|MSYS*|MINGW*)
        # transform D:\path\to\venv to /d/path/to/venv on MSYS and MINGW
        # and to /cygdrive/d/path/to/venv on Cygwin
        VIRTUAL_ENV=$(cygpath '/Users/hu/code/DØPEMÜX/venv')
        export VIRTUAL_ENV
        ;;
    *)
        # use the path as-is
        export VIRTUAL_ENV='/Users/hu/code/DØPEMÜX/venv'
        ;;
esac

_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/"bin":$PATH"
export PATH

VIRTUAL_ENV_PROMPT=venv
export VIRTUAL_ENV_PROMPT

# unset PYTHONHOME if set
# this will fail if PYTHONHOME is set to the empty string (which is bad anyway)
# could use `if (set -u; : $PYTHONHOME) ;` in bash
if [ -n "${PYTHONHOME:-}" ] ; then
    _OLD_VIRTUAL_PYTHONHOME="${PYTHONHOME:-}"
    unset PYTHONHOME
fi

if [ -z "${VIRTUAL_ENV_DISABLE_PROMPT:-}" ] ; then
    _OLD_VIRTUAL_PS1="${PS1:-}"
    PS1="("venv") ${PS1:-}"
    export PS1
fi

# Call hash to forget past commands. Without forgetting
# past commands the $PATH changes we made may not be respected
hash -r 2> /dev/null

--- END: venv/bin/activate ---

--- BEGIN: venv/bin/python3.13 ---
����            0  �          H   __PAGEZERO                                                        �  __TEXT                  @               @                   __text          __TEXT          P
     �      P
               �            __stubs         __TEXT          H     �       H              �           __cstring       __TEXT               �                                    __unwind_info   __TEXT          �     h       �                                �   __DATA_CONST     @      @       @       @                  __got           __DATA_CONST     @     �        @                              �   __DATA           �      @                                   __bss           __DATA           �                                              H   __LINKEDIT       �      �       �      �M                    4  �    �  �  3  �   ��  0         ��     �  0     P                                              P�  %                             /usr/lib/dyld             |;g�[�1n������۸2                     �*              (  �   P
                 x          
  
 /opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/Python           8           G   /usr/lib/libSystem.B.dylib      &      ��     )      ��             �  �H                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  ����_��W��O��{������   �  @��C ��  �`  5 ��   �@����  �� � � ��  �� �  ������  �� �� �  T��J�_8�	�_� qA��T�	� ���*@8_� q��	  �)%� @�  � ��< ��< �R� �@  �   ��3 ��  �  5U  �� �����R�  �� �   � ��A  �!  ��  �@ �@  �   �  �!�� �R �R~  � �� T@  �   ���
  � �@9 9A  �!  ����  �� �� 9@  �   ��� �R �Ri  � � Tc  ���R  �� �  �!P�     � ��A  �!  �" �R{  �t �� ��C �  �(  �@�@��C �  ���� ����_  �� �  �!��  �RN  ��� ��O��{��� �� �W  �� �=  �  �4 5��R �r� �� ��# ���! �RN  � 1  T�@� �� T���RI  �� �)  �  �3 5�{B��OA��� ��_�
  �  �(  �
@�@�   � ��A�R" �R(  �  �R#  �  ��{��� �  �!��@ �R  ��{��� �  �!8�  �R  ��{��� �  �! �  �R
  �  �@� �  �
@� �  �@� �  �@� �  �@� �  �"@� �  �&@� �  �*@� �  �.@� �  �2@� �  �6@� �  �:@� �  �>@� �  �B@� �  �F@� �  �J@� �  �N@� �realpath: %s . / __PYVENV_LAUNCHER__ posix_spawn: %s Resources/Python.app/Contents/MacOS/Python posix_spawnattr_int posix_spawnattr_setbinpref posix_spawnattr_setbinpref failed to copy
 posix_spawnattr_setflags                         P
  @   @   H      @                          � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  �     �     �     �     �     �     �     �     �	     �
     �     �     �
     �     �     �     �     �     �      �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        P   �                                           @  @                  L  ^  t  �  �  �  �  �  �  �   0 n � � � �    _Py_Initialize __NSGetExecutablePath ___error ___stderrp ___strlcat_chk _dladdr _environ _err _exit _fwrite _malloc _posix_spawn _posix_spawnattr_init _posix_spawnattr_setbinpref_np _posix_spawnattr_setflags _realpath$DARWIN_EXTSN _setenv _strcpy _strlen _strrchr         __mh_execute_header         header 	main 
  ���           <   BEa                            '             =             F             Q             `             h             q             v             |             �             �             �             �             �             �             �                                                             	   
         
                                                	   
         
                                   __mh_execute_header _Py_Initialize __NSGetExecutablePath ___error ___stderrp ___strlcat_chk _dladdr _environ _err _exit _fwrite _malloc _posix_spawn _posix_spawnattr_init _posix_spawnattr_setbinpref_np _posix_spawnattr_setflags _realpath$DARWIN_EXTSN _setenv _strcpy _strlen _strrchr radr://5614542          ���  !          $     
     ��  �        �   X      	  �                                         @        python3-555549447c3b67815ba7316ea1b1fcffedf7dbb8 �y �N�eux�J��RNj����-��7�C��                                qg��cơ�Ϸ��H�o$đ�k�j���\ �,R��A]xwO"!��"�0��e������qG|���Xo��f����kOX�|�|z�ڽ�H�,����Xo��f����kOX�|�|z�ڽ�H�,�$�G���:t"�x�����F�%),�D����Xo��f����kOX�|�|z�ڽ�H�,����Xo��f����kOX�|�|z�ڽ�H�,����Xo��f����kOX�|�|z�ڽ�H�,��5\M��eޓC[��eĂ���.�@,�7��͑��       ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
--- END: venv/bin/python3.13 ---

--- BEGIN: venv/bin/activate.csh ---
# This file must be used with "source bin/activate.csh" *from csh*.
# You cannot run it directly.

# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>

alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; unsetenv VIRTUAL_ENV_PROMPT; test "\!:*" != "nondestructive" && unalias deactivate'

# Unset irrelevant variables.
deactivate nondestructive

setenv VIRTUAL_ENV '/Users/hu/code/DØPEMÜX/venv'

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/"bin":$PATH"
setenv VIRTUAL_ENV_PROMPT venv


set _OLD_VIRTUAL_PROMPT="$prompt"

if (! "$?VIRTUAL_ENV_DISABLE_PROMPT") then
    set prompt = "("venv") $prompt:q"
endif

alias pydoc python -m pydoc

rehash

--- END: venv/bin/activate.csh ---

--- BEGIN: uberslicer/validator.py ---
from pydantic import BaseModel, ValidationError
import yaml, json, sys, glob
from pathlib import Path
from uberslicer.utils import log_audit, CFG

SCHEMA_PATH = Path(CFG["schema"]["file"])
SCHEMA = json.loads(SCHEMA_PATH.read_text())

class UltraBlock(BaseModel):
    project: str
    block_id: str
    session_metadata: dict
    content: str
    tags: list
    summary: str | None = None
    patch_type: str | None = None  # only for patch blocks

def validate_all():
    """
    Validate every YAML block under the tagged folder against the UltraBlock schema,
    and also catch any 'patch' blocks still carrying the 'needs-review' tag.
    """
    paths = glob.glob(f"{CFG['paths']['tagged']}/**/*.yaml", recursive=True)
    bad, pending = 0, 0

    for p in paths:
        try:
            data = yaml.safe_load(open(p))
            UltraBlock(**data)  # will raise on invalid schema
            if "patch" in data.get("tags", []) and CFG["auditor"]["block_review_tag"] in data.get("tags", []):
                pending += 1
        except ValidationError as e:
            log_audit("error", {"file": p, "errors": e.errors()})
            bad += 1

    if bad or pending:
        sys.exit(f"❌ validation failed: {bad} bad blocks, {pending} pending patches")
    print("✅ all blocks validated & no pending patch review")

--- END: uberslicer/validator.py ---

--- BEGIN: uberslicer/patch.py ---
import difflib
import uuid
import datetime
import os
import yaml
from pathlib import Path
from uberslicer.utils import CFG, log_dev, log_audit


def create_patch_block(oldfile: str, newfile: str, reason: str) -> None:
    """
    Create a YAML patch block by diffing OLD and NEW files.
    Writes output to the configured patch directory.
    """
    # Read file contents
    try:
        with open(oldfile, 'r') as f:
            old_lines = f.read().splitlines()
    except FileNotFoundError:
        old_lines = []
    try:
        with open(newfile, 'r') as f:
            new_lines = f.read().splitlines()
    except FileNotFoundError:
        new_lines = []

    # Generate unified diff
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=oldfile,
        tofile=newfile,
        lineterm=""
    )
    content = "\n".join(diff)

    # Build the patch block
    block_id = f"patch-{uuid.uuid4()}"
    block = {
        "block_id": block_id,
        "session_metadata": {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "source": os.getcwd()
        },
        "tags": ["patch", "needs-review"],
        "content": content,
        "summary": reason,
        "patch_type": "diff"
    }

    # Ensure output directory exists
    patch_dir = CFG['paths']['patch_dir']
    Path(patch_dir).mkdir(parents=True, exist_ok=True)

    # Write YAML block
    outfile = Path(patch_dir) / f"{block_id}.yaml"
    with open(outfile, 'w') as f:
        yaml.dump(block, f, sort_keys=False)

    # Log and audit
    log_dev("patch", [f"{oldfile} -> {newfile}", reason])
    log_audit("info", f"Patch block created: {outfile}")
    print(f"[OK] Patch block written to {outfile}")

--- END: uberslicer/patch.py ---

--- BEGIN: uberslicer/__init__.py ---
import importlib, yaml, pathlib
from uberslicer.utils import log_dev

PLUGIN_DIR = pathlib.Path("plugins")

def load_plugins():
    for yml in PLUGIN_DIR.glob("*/plugin.yaml"):
        meta = yaml.safe_load(yml.read_text())
        mod = importlib.import_module(meta["entrypoint"].rstrip(".py").replace("/", "."))
        log_dev({"action":"plugin_loaded","name":meta["name"]})
        yield meta["name"], mod.run

--- END: uberslicer/__init__.py ---

--- BEGIN: uberslicer/ultraslicer.py ---
#!/usr/bin/env python3
import os, sys, uuid, yaml, datetime
from uberslicer.utils import log_dev, log_audit

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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dopemux_ultraslicer.py <input_file> <output_dir>")
        sys.exit(1)
    input_file, outdir = sys.argv[1:3]
    blocks = slice_blocks(input_file)
    dump_blocks(blocks, outdir)
    log_dev(f"ultraslice", details=[f"Sliced {len(blocks)} blocks from {input_file} to {outdir}"])
    log_audit("info", f"Sliced file {input_file} into {len(blocks)} blocks.")
    print(f"[OK] Sliced, tagged, and dumped {len(blocks)} ritual blocks to {outdir}.")

--- END: uberslicer/ultraslicer.py ---

--- BEGIN: uberslicer/utils.py ---
import yaml
import os
import datetime
from pathlib import Path
import random

# ─── CLI SUPPORTING UTILITIES ──────────────────────────────────────────────
def load_config():
    """Load only the `dopemux` section from config.yaml at project root."""
    cfg_path = Path("config.yaml")
    if not cfg_path.exists():
        raise FileNotFoundError("config.yaml not found")
    full_cfg = yaml.safe_load(cfg_path.read_text())
    if "dopemux" not in full_cfg:
        raise KeyError("config.yaml missing top-level 'dopemux' key")
    return full_cfg["dopemux"]

def colorize(text, style):
    """Placeholder: color your text by style."""
    return text

def print_banner(cfg):
    """If `banner` is set in config, print it once at startup."""
    banner = cfg.get("banner")
    if banner:
        print(banner)

def dopamine_nudge(cfg):
    """Randomly emit one of the `nudges` defined in config."""
    nudges = cfg.get("nudges", [])
    if nudges:
        print(random.choice(nudges))
# ────────────────────────────────────────────────────────────────────────────

# Dev/audit logging helpers (unchanged)
DEVLOG_PATH = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-DEVLOG.txt"
AUDIT_PATH  = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-AUDIT-ULTRA-RITUAL.txt"

def _append_block(path, entry):
    entry['timestamp'] = datetime.datetime.utcnow().isoformat()
    if not os.path.exists(path):
        with open(path, "w") as f: yaml.dump({'entries': [entry]}, f)
    else:
        with open(path) as f: data = yaml.safe_load(f) or {}
        entries = data.get('entries', [])
        entries.append(entry)
        with open(path, "w") as f: yaml.dump({'entries': entries}, f)

def log_dev(action, details=None):
    block = {'action': action, 'details': details or []}
    _append_block(DEVLOG_PATH, block)

def log_audit(level, summary):
    block = {'level': level, 'summary': summary}
    _append_block(AUDIT_PATH, block)

# ─── GLOBAL CONFIG REFERENCE ────────────────────────────────────────────────
CFG = load_config()

--- END: uberslicer/utils.py ---

--- BEGIN: uberslicer/doctor.py ---
"""
Sanity checker for folder layout, config keys, and required files.
Called via `dopemux doctor`.
"""

from pathlib import Path
import yaml
import sys

# Match your config.yaml structure
REQUIRED_CONFIG_KEYS = [
    "dopemux.paths.tagged",
    "dopemux.paths.patch_dir",
    "dopemux.paths.outputs",
    "dopemux.paths.devlog",
    "dopemux.paths.audit",
    "dopemux.schema.file",
    "dopemux.auditor.block_review_tag",
]

REQUIRED_DIRS = [
    "tagged",
    "tagged/patch",
    "logs",
    "schema",
]

REQUIRED_FILES = [
    "schema/extraction-schema.json",
    "config.yaml",
]

def warn(msg):
    print(f"❌  {msg}")

def ok(msg):
    print(f"✅  {msg}")

def load_cfg():
    try:
        with open("config.yaml") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        warn("config.yaml not found at repo root.")
        sys.exit(1)

def check_keys(cfg):
    # flatten nested dict to dot-keys
    flat = {}
    def _flatten(prefix, mapping):
        for k, v in mapping.items():
            key = f"{prefix}.{k}" if prefix else k
            flat[key] = v
            if isinstance(v, dict):
                _flatten(key, v)
    _flatten("", cfg)
    missing = [k for k in REQUIRED_CONFIG_KEYS if k not in flat]
    if missing:
        warn(f"Missing config keys: {', '.join(missing)}")
    else:
        ok("All required config keys present.")
    return not missing

def check_dirs():
    missing = [d for d in REQUIRED_DIRS if not Path(d).exists()]
    if missing:
        warn(f"Missing directories: {', '.join(missing)}")
    else:
        ok("All required directories exist.")
    return not missing

def check_files():
    missing = [f for f in REQUIRED_FILES if not Path(f).exists()]
    if missing:
        warn(f"Missing files: {', '.join(missing)}")
    else:
        ok("All required files exist.")
    return not missing

def run_diagnosis() -> None:
    cfg = load_cfg()
    results = [
        check_keys(cfg),
        check_dirs(),
        check_files(),
    ]
    if all(results):
        ok("Doctor check passed — repo looks healthy.")
        sys.exit(0)
    warn("Doctor check failed — fix the ❌ items above.")
    sys.exit(1)

if __name__ == "__main__":
    run_diagnosis()

--- END: uberslicer/doctor.py ---

