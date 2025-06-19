from pathlib import Path
import random
import sys

BANNER_DIR = Path(__file__).resolve().parent / "dopemux-banners"


def _read_file(name: str) -> str:
    path = BANNER_DIR / name
    if not path.exists():
        return ""
    return path.read_text().rstrip()


def supports_unicode() -> bool:
    enc = sys.stdout.encoding or "utf-8"
    try:
        "✓".encode(enc)
        return True
    except UnicodeEncodeError:
        return False


def print_banner(filename: str) -> None:
    text = _read_file(filename)
    if text:
        print(text)


def on_boot():
    if supports_unicode():
        print_banner("system_boot_unicode.txt")
    else:
        print_banner("ascii_fallback.txt")


def on_chunking_start():
    print_banner("ultraslicer_max_context.txt")


def on_block_success():
    print_banner("dopamine_hit.txt")


def on_drift_or_error():
    print_banner("context_drift.txt")
    roast = random_roast()
    if roast:
        print(roast)


def on_pr_open():
    print_banner("atomic_pr.txt")


def random_roast() -> str:
    lines = [l.strip() for l in _read_file("roast_lines.txt").splitlines() if l.strip()]
    return random.choice(lines) if lines else ""
