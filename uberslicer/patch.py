import difflib
import uuid
import datetime
import os
import yaml
from pathlib import Path
from utils import load_config, log_dev, log_audit
from banners import on_block_success


def create_patch_block(oldfile: str, newfile: str, reason: str) -> None:
    """
    Create a YAML patch block by diffing OLD and NEW files.
    Writes output to the configured patch directory.
    """
    # Read file contents
    try:
        with open(oldfile, 'r') as f:
            old_lines = f.read().splitlines()
    except FileNotFoundError:
        old_lines = []
    try:
        with open(newfile, 'r') as f:
            new_lines = f.read().splitlines()
    except FileNotFoundError:
        new_lines = []

    # Generate unified diff
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=oldfile,
        tofile=newfile,
        lineterm=""
    )
    content = "\n".join(diff)

    # Build the patch block
    block_id = f"patch-{uuid.uuid4()}"
    block = {
        "block_id": block_id,
        "session_metadata": {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "source": os.getcwd()
        },
        "tags": ["patch", "needs-review"],
        "content": content,
        "summary": reason,
        "patch_type": "diff"
    }

    # Ensure output directory exists
    cfg = load_config()
    patch_dir = cfg['paths']['patch_dir']
    Path(patch_dir).mkdir(parents=True, exist_ok=True)

    # Write YAML block
    outfile = Path(patch_dir) / f"{block_id}.yaml"
    with open(outfile, 'w') as f:
        yaml.dump(block, f, sort_keys=False)

    # Log and audit
    log_dev("patch", [f"{oldfile} -> {newfile}", reason])
    log_audit("info", f"Patch block created: {outfile}")
    print(f"[OK] Patch block written to {outfile}")
    on_block_success()
