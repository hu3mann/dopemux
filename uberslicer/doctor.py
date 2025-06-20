"""
Sanity checker for folder layout, config keys, and required files.
Called via `dopemux doctor`.
"""

from pathlib import Path
import sys
from banners import on_block_success, on_drift_or_error
from utils import load_config

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

def warn(msg):
    print(f"❌  {msg}")

def ok(msg):
    print(f"✅  {msg}")

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

def check_dirs(cfg):
    required = [
        cfg["paths"]["tagged"],
        cfg["paths"]["patch_dir"],
        Path(cfg["paths"]["devlog"]).parent,
        Path(cfg["schema"]["file"]).parent,
    ]
    missing = [str(d) for d in required if not Path(d).exists()]
    if missing:
        warn(f"Missing directories: {', '.join(missing)}")
    else:
        ok("All required directories exist.")
    return not missing

def check_files(cfg):
    required = [
        cfg["schema"]["file"],
        "config.yaml",
    ]
    missing = [str(f) for f in required if not Path(f).exists()]
    if missing:
        warn(f"Missing files: {', '.join(missing)}")
    else:
        ok("All required files exist.")
    return not missing

def run_diagnosis() -> None:
    dopemux_cfg = load_config()
    wrapper = {"dopemux": dopemux_cfg}
    results = [
        check_keys(wrapper),
        check_dirs(dopemux_cfg),
        check_files(dopemux_cfg),
    ]
    if all(results):
        ok("Doctor check passed — repo looks healthy.")
        on_block_success()
        sys.exit(0)
    on_drift_or_error()
    warn("Doctor check failed — fix the ❌ items above.")
    sys.exit(1)

if __name__ == "__main__":
    run_diagnosis()
