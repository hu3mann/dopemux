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

ANSI_CODES = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
    "bold": "\033[1m",
}


def colorize(text: str, style: str) -> str:
    """Return ``text`` wrapped in ANSI codes for ``style`` if known."""
    code = ANSI_CODES.get(style)
    if not code:
        return text
    return f"{code}{text}{ANSI_CODES['reset']}"

def print_banner(cfg):
    """If `banner` is set in config, print it once at startup."""
    banner = cfg.get("banner")
    if banner:
        color = cfg.get("colors", {}).get("dopamine")
        if color:
            banner = colorize(banner, color)
        print(banner)


def dopamine_nudge(cfg):
    """Randomly emit one of the `nudges` defined in config."""
    nudges = cfg.get("nudges", [])
    if nudges:

        msg = random.choice(nudges)
        color = cfg.get("colors", {}).get("filth")
        if color:
            msg = colorize(msg, color)
        print(msg)

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
