import os, random, datetime
from pathlib import Path
from typing import Any, Optional
import yaml

# ─── CONFIG LOADER ─────────────────────────────────────────────────────────
_CONFIG_CACHE: Optional[dict] = None

def load_config() -> dict:
    """Memoised loader for the top-level `dopemux` section."""
    global _CONFIG_CACHE
    if _CONFIG_CACHE:
        return _CONFIG_CACHE
    cfg_path = Path("config.yaml")
    if not cfg_path.exists():
        raise FileNotFoundError("config.yaml missing at project root")
    root_cfg = yaml.safe_load(cfg_path.read_text()) or {}
    try:
        _CONFIG_CACHE = root_cfg["dopemux"]
    except KeyError:
        raise KeyError("config.yaml missing top-level ‘dopemux’ key")
    return _CONFIG_CACHE

# ─── TERMINAL NICETIES ─────────────────────────────────────────────────────
def colorize(text: str, style: str) -> str:
    colors = {"dopamine": "\033[96m", "filth": "\033[95m", "reset": "\033[0m"}
    return f"{colors.get(style,'')}{text}{colors['reset']}"

def print_banner() -> None:
    cfg = load_config()
    print(colorize(cfg.get("banner", "💊 DØPEMÜX — Terminal Dopamine"), "dopamine"))

def dopamine_nudge() -> None:
    nudges = load_config().get("nudges", [])
    if nudges:
        print(random.choice(nudges))

# ─── DEV / AUDIT LOGGING ───────────────────────────────────────────────────
DEVLOG_PATH = Path(load_config()["paths"]["devlog"])
AUDIT_PATH  = Path(load_config()["paths"]["audit"])

def _append(path: Path, entry: dict[str, Any]) -> None:
    entry["timestamp"] = datetime.datetime.utcnow().isoformat()
    if path.exists():
        data = yaml.safe_load(path.read_text()) or {"entries": []}
    else:
        data = {"entries": []}
    data["entries"].append(entry)
    path.write_text(yaml.dump(data, sort_keys=False))

def log_dev(action: str, details: list[str] | None = None) -> None:
    _append(DEVLOG_PATH, {"action": action, "details": details or []})

def log_audit(level: str, summary: str) -> None:
    _append(AUDIT_PATH, {"level": level, "summary": summary})
