# src/extract.py — L1 CHUNK + EXTRACT ORCHESTRATOR (dopemux-compliant)

import os
import sys
import argparse
import yaml
from pathlib import Path

# Import dopemux system chunker logic.  The chunker previously lived under
# `data/system/CHUNKING/` but was moved to `src/chunkasaurus.py`.
try:
    from .chunkasaurus import intelligent_chunker as local_chunker
except Exception:
    local_chunker = None

# Prompts loader
from .prompts import load_prompt

import openai

def load_openai_key():
    """Retrieve the OpenAI API key from either the environment or `.env`."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        # `.env` now lives at the repository root
        env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
        if os.path.isfile(env_path):
            for line in open(env_path):
                if "OPENAI_API_KEY" in line:
                    key = line.strip().split('=')[-1]
                    break
    if not key:
        raise RuntimeError("[FILTH] No OpenAI API key found (set OPENAI_API_KEY or .env)")
    return key

def chunk_input_file(input_path, detail="HIGH"):
    """Chunk the input file using the local chunker if available.

    The historical setup expected a separate chunker package under
    `data/system/CHUNKING`.  After the repo shuffle the only available
    implementation is `src/chunkasaurus.py`.  If that import succeeded we
    delegate to it.  Otherwise we fall back to a naive splitter on blank lines.
    """
    if local_chunker:
        try:
            outdir = Path(input_path).parent / "chunks_tmp"
            os.makedirs(outdir, exist_ok=True)
            local_chunker(input_path, outdir, force=True)
            return [open(os.path.join(outdir, f)).read() for f in sorted(os.listdir(outdir)) if f.endswith('.txt')]
        except Exception as e:
            raise RuntimeError(f"[FILTH] Local chunker failed: {e}")

    # Fallback: naive split on blank lines
    with open(input_path, "r", encoding="utf-8") as f:
        data = f.read()
    return [blk.strip() for blk in data.split("\n\n") if blk.strip()]

def call_llm_extract(chunk, prompt, api_key, detail="HIGH", model="gpt-4o"):
    # Can adjust detail by modifying prompt, temperature, or max_tokens
    user_prompt = f"{prompt}\n\n[DETAIL: {detail}]\n\n{chunk}"
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2 if detail == "HIGH" else 0.5,
        max_tokens=4096 if detail in ("HIGH", "ULTRA") else 1024,
    )
    return completion.choices[0].message['content']

def save_block(block, out_dir, idx):
    # Always YAML, 1 file per block for audit
    path = Path(out_dir) / f"block_{idx:04d}.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(block, f, sort_keys=False)
    return str(path)

def main():
    parser = argparse.ArgumentParser(description="dopemux L1 Extractor")
    parser.add_argument("input_file", help="Path to input file (txt, md, log, etc)")
    parser.add_argument("--detail", default="HIGH", help="Detail: LOW | MEDIUM | HIGH | ULTRA")
    parser.add_argument("--outdir", default="../chunks/", help="Directory for atomic blocks")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model (default: gpt-4o)")
    args = parser.parse_args()

    input_file = args.input_file
    detail = args.detail.upper()
    outdir = os.path.join(os.path.dirname(__file__), args.outdir)
    os.makedirs(outdir, exist_ok=True)

    print(f"[OK] Extracting {input_file} at detail: {detail}")
    api_key = load_openai_key()
    extract_prompt = load_prompt("extract")

    # 1. Chunk input
    print("[OK] Chunking input...")
    chunks = chunk_input_file(input_file, detail)
    if not chunks:
        raise RuntimeError("[FILTH] No chunks found — check chunker or input file.")

    print(f"[OK] {len(chunks)} chunks created.")

    # 2. Run extraction for each chunk
    for idx, chunk in enumerate(chunks):
        print(f"  → [L1] Extracting block {idx+1}/{len(chunks)}")
        try:
            llm_output = call_llm_extract(chunk, extract_prompt, api_key, detail, args.model)
            # Expecting output as YAML or dict
            try:
                block = yaml.safe_load(llm_output)
            except Exception:
                block = {"raw": llm_output}
            block_path = save_block(block, outdir, idx)
            print(f"    [OK] Saved: {block_path}")
        except Exception as e:
            print(f"[FILTH] Block {idx+1} failed: {e}")

    print(f"[OK] Extraction complete. {len(chunks)} blocks written to {outdir}")

if __name__ == "__main__":
    main()

# [OK] — src/extract.py: L1 chunk + extract orchestrator, ritual-compliant.
# - Uses system chunkers, dynamic prompt loader, OpenAI API.
# - Outputs YAML atomic blocks, one per chunk, to /chunks/
# - Handles detail levels, key lookup, and block audit.
