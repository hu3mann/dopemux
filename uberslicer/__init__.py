from dataclasses import dataclass
from importlib import import_module, util as importlib_util
from pathlib import Path
from typing import Callable, Iterable, Tuple
import yaml

from utils import log_dev

PLUGIN_DIR = Path(__file__).resolve().parent / "plugins"


@dataclass
class PluginSpec:
    """Metadata describing a Dopemux plugin."""

    name: str
    entrypoint: str
    description: str = ""


def discover_plugins(directory: Path = PLUGIN_DIR) -> Iterable[PluginSpec]:
    """Yield ``PluginSpec`` objects for each plugin under ``directory``."""
    for yml in directory.glob("*/plugin.yaml"):
        meta = yaml.safe_load(yml.read_text())
        yield PluginSpec(
            name=meta["name"],
            entrypoint=meta["entrypoint"],
            description=meta.get("description", ""),
        )


def load_plugins(directory: Path = PLUGIN_DIR) -> Iterable[Tuple[str, Callable]]:
    """Import plugin entrypoints and yield ``(name, run_callable)`` pairs."""
    for spec in discover_plugins(directory):
        module = import_module(spec.entrypoint.rstrip(".py").replace("/", "."))
        log_dev("plugin_loaded", [spec.name])
        yield spec.name, getattr(module, "run")

# ─── Legacy helpers ---------------------------------------------------------
# Keep backward compatibility with the old `uberslicer.py` module that
# exposes ``slice_blocks`` and ``dump_blocks``.
legacy_path = Path(__file__).resolve().parent.parent / "uberslicer.py"
_legacy_spec = importlib_util.spec_from_file_location(
    "_uberslicer_legacy", legacy_path
)
_legacy_mod = importlib_util.module_from_spec(_legacy_spec)
_legacy_spec.loader.exec_module(_legacy_mod)
slice_blocks = _legacy_mod.slice_blocks
dump_blocks = _legacy_mod.dump_blocks
