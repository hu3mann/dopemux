#!/usr/bin/env python3
from utils import log_dev, log_audit
from uberslicer.rituals import slice_blocks, dump_blocks
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python uberslicer.py <input_file> <output_dir>")
        sys.exit(1)
    input_file, outdir = sys.argv[1:3]
    blocks = slice_blocks(input_file)
    dump_blocks(blocks, outdir)
    log_dev("uberslice", details=[f"Sliced {len(blocks)} blocks from {input_file} to {outdir}"])
    log_audit("info", f"Sliced file {input_file} into {len(blocks)} blocks.")
    print(f"[OK] Sliced, tagged, and dumped {len(blocks)} ritual blocks to {outdir}.")

