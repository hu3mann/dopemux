"""
dopemux_doctor — Sanity checker for folder layout, config keys, and required files.

Usage:
    dopemux doctor
"""

from pathlib import Path
import yaml
import sys

REQUIRED_CONFIG_KEYS = [
    "dopemux.paths.tagged",
    "dopemux.paths.patch_dir",
    "dopemux.paths.logs",
    "dopemux.schema.file",
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
    flat = {}
    def _flatten(prefix, mapping):
        for k, v in mapping.items():
            new_key = f"{prefix}.{k}" if prefix else k
            flat[new_key] = v
            if isinstance(v, dict):
                _flatten(new_key, v)
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

# When called by `python -m uberslicer.doctor`
if __name__ == "__main__":
    run_diagnosis()
