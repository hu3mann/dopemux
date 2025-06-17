import yaml, os, datetime

from pathlib import Path
import random

# ─── CLI SUPPORTING UTILITIES ──────────────────────────────────────────────
def load_config():
    """Load config.yaml from project root."""
    cfg_path = Path("config.yaml")
    if not cfg_path.exists():
        raise FileNotFoundError("config.yaml not found")
    return yaml.safe_load(cfg_path.read_text())

def colorize(text, style):
    """Placeholder for coloring text by style."""
    return text

def print_banner(cfg):
    """Print banner if defined in config under 'banner'."""
    banner = cfg.get("banner")
    if banner:
        print(banner)

def dopamine_nudge(cfg):
    """Print a random dopamine nudge if defined under 'nudges'."""
    nudges = cfg.get("nudges", [])
    if nudges:
        print(random.choice(nudges))
# ────────────────────────────────────────────────────────────────────────────

DEVLOG_PATH = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-DEVLOG.txt"
AUDIT_PATH  = "💊DØPEMÜX-☠️UBERSLICER☠️—TFE-AUDIT-ULTRA-RITUAL.txt"

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
