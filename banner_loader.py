import os
import random
from utils import colorize, load_config

BANNER_DIR = os.path.join(os.path.dirname(__file__), "dopemux-banners")


def _load_banners():
    banners = []
    for name in [
        "system_boot_unicode.txt",
        "ultraslicer_max_context.txt",
        "dopamine_hit.txt",
        "context_drift.txt",
        "atomic_pr.txt",
        "ascii_fallback.txt",
    ]:
        path = os.path.join(BANNER_DIR, name)
        if os.path.exists(path):
            with open(path) as f:
                banners.append(f.read())
    return banners


BANNERS = _load_banners()


def print_random_banner(style="dopamine"):
    if not BANNERS:
        return
    banner = random.choice(BANNERS)
    cfg = load_config()
    color = cfg.get("colors", {}).get(style)
    if color:
        banner = colorize(banner, color)
    print(banner)


if __name__ == "__main__":
    print_random_banner()
