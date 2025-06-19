#!/usr/bin/env python3
import os
import uuid
import yaml
import datetime
from banners import on_chunking_start, on_block_success

SCHEMA_FIELDS = [
    "session_metadata", "source", "block_id", "tags", "content",
    "summary", "map_refs", "decisions", "blockers", "meta_validation",
    "dopaminehit", "ritual_notes"
]

def ritual_header(block_id, summary):
    return {
        "block_id": block_id,
        "summary": summary,
        "ritual_notes": f"Ritual block created {datetime.datetime.utcnow().isoformat()}Z",
    }


def slice_blocks(input_path):
    on_chunking_start()
    with open(input_path) as f:
        raw = f.read()
    blocks = [b.strip() for b in raw.split('\n\n') if b.strip()]
    ritual_blocks = []
    for i, content in enumerate(blocks):
        block_id = f"block-{uuid.uuid4()}"
        ritual = {
            **ritual_header(block_id, f"UberSlice {i+1}"),
            "session_metadata": {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "source_file": os.path.basename(input_path),
            },
            "source": str(input_path),
            "tags": ["uberslice", "auto", "needs-review"],
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
        on_block_success()
