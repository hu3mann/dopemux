import importlib, yaml, pathlib
from uberslicer.utils import log_dev
from . import uberslicer as slicer

__all__ = ["slicer", "load_plugins"]

PLUGIN_DIR = pathlib.Path("plugins")

def load_plugins():
    for yml in PLUGIN_DIR.glob("*/plugin.yaml"):
        meta = yaml.safe_load(yml.read_text())
        mod = importlib.import_module(meta["entrypoint"].rstrip(".py").replace("/", "."))
        log_dev({"action":"plugin_loaded","name":meta["name"]})
        yield meta["name"], mod.run
