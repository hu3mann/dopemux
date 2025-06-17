#!/usr/bin/env python3
import os, sys, uuid, yaml, datetime
from utils import log_dev, log_audit

SCHEMA_FIELDS = [
    "session_metadata", "source", "block_id", "tags", "content",
    "summary", "map_refs", "decisions", "blockers", "meta_validation",
    "dopaminehit", "ritual_notes"
]

def ritual_header(block_id, summary):
    return {
        "block_id": block_id,
        "summary": summary,
        "ritual_notes": f"Ritual block created {datetime.datetime.utcnow().isoformat()}Z"
    }

def slice_blocks(input_path):
    with open(input_path) as f: raw = f.read()
    blocks = [b.strip() for b in raw.split('\n\n') if b.strip()]
    ritual_blocks = []
    for i, content in enumerate(blocks):
        block_id = f"block-{uuid.uuid4()}"
        ritual = {
            **ritual_header(block_id, f"UltraSlice {i+1}"),
            "session_metadata": {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "source_file": os.path.basename(input_path)
            },
            "source": input_path,
            "tags": ["ultraslice", "auto", "needs-review"],
            "content": content,
            "map_refs": [],
            "decisions": [],
            "blockers": [],
            "meta_validation": [],
            "dopaminehit": ["auto"],
        }
        for k in SCHEMA_FIELDS:
            ritual.setdefault(k, None)
        ritual_blocks.append(ritual)
    return ritual_blocks

def dump_blocks(blocks, outdir):
    os.makedirs(outdir, exist_ok=True)
    for block in blocks:
        outpath = os.path.join(outdir, f"{block['block_id']}.yaml")
        with open(outpath, "w") as f:
            yaml.dump(block, f, sort_keys=False)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dopemux_ultraslicer.py <input_file> <output_dir>")
        sys.exit(1)
    input_file, outdir = sys.argv[1:3]
    blocks = slice_blocks(input_file)
    dump_blocks(blocks, outdir)
    log_dev(f"ultraslice", details=[f"Sliced {len(blocks)} blocks from {input_file} to {outdir}"])
    log_audit("info", f"Sliced file {input_file} into {len(blocks)} blocks.")
    print(f"[OK] Sliced, tagged, and dumped {len(blocks)} ritual blocks to {outdir}.")
