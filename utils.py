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

# Dev/audit logging helpers
DEVLOG_PATH = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-DEVLOG.txt"
AUDIT_PATH = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-AUDIT-ULTRA-RITUAL.txt"


def _append_block(path, entry):
    entry["timestamp"] = datetime.datetime.utcnow().isoformat()
    if not os.path.exists(path):
        with open(path, "w") as f:
            yaml.dump({"entries": [entry]}, f)
    else:
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        entries = data.get("entries", [])
        entries.append(entry)
        with open(path, "w") as f:
            yaml.dump({"entries": entries}, f)


def log_dev(action, details=None):
    block = {"action": action, "details": details or []}
    _append_block(DEVLOG_PATH, block)


def log_audit(level, summary):
    block = {"level": level, "summary": summary}
    _append_block(AUDIT_PATH, block)

# ─── GLOBAL CONFIG REFERENCE ────────────────────────────────────────────────
CFG = load_config()
