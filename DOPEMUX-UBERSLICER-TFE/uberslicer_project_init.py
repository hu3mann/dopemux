# [OK] DØPEMÜX ULTRASLICER — MANIFEST-AWARE, CHAT LOG TO CHUNKS FLOW
# Fully compliant with your chunking/manifest ecosystem (and ready for messy, from-scratch starts).

import os
import shutil
import json
import subprocess

# --- CONFIG: Update as needed ---
CHUNKER_SCRIPT = "chunkasaurus.py"         # Your chunker logic (must accept input/output args)
CHUNKS_DIR = "chunks"
MANIFEST_PATH = "chunk_manifest.json"
LOGS_DIR = "dopemux-project/logs"
PROJECT_ROOT = "dopemux-project"
GIT_AUTO = True
# ---------------------------------

def run_chunker(chatlog_path):
    """Run chunker on chat log, generate chunks and manifest."""
    print(f"[OK] Running chunker on: {chatlog_path}")
    result = subprocess.run(
        ["python3", CHUNKER_SCRIPT, "--input", chatlog_path, "--output_dir", CHUNKS_DIR, "--manifest", MANIFEST_PATH],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[ERROR] Chunker failed:\n{result.stderr}")
        exit(1)
    print(result.stdout)
    print(f"[OK] Chunker complete. Chunks and manifest written.")

def audit_manifest_and_files():
    """Ensure all manifest chunks exist and no orphans are present."""
    if not os.path.exists(MANIFEST_PATH):
        print(f"[ERROR] No manifest found at {MANIFEST_PATH}")
        return None
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    all_chunks = set(os.listdir(CHUNKS_DIR)) if os.path.exists(CHUNKS_DIR) else set()
    manifest_files = set(os.path.basename(meta['file']) for meta in manifest.values())

    missing = manifest_files - all_chunks
    orphans = all_chunks - manifest_files

    if missing:
        print(f"[WARN] Manifest references missing chunk files: {missing}")
    if orphans:
        print(f"[WARN] Found orphan chunk files not in manifest: {orphans}")

    return manifest

def copy_chunks_to_logs(manifest):
    """Copy all manifest chunks to dopemux-project/logs/, never overwriting."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    moved, skipped = [], []
    for chunk_name, meta in manifest.items():
        src = meta['file']
        tgt = os.path.join(LOGS_DIR, os.path.basename(src))
        if not os.path.exists(src):
            print(f"[WARN] Missing chunk: {src}")
            skipped.append(chunk_name)
            continue
        if not os.path.exists(tgt):
            shutil.copy2(src, tgt)
            moved.append(chunk_name)
            print(f"[OK] {chunk_name}: {src} → {tgt}")
        else:
            print(f"[SKIP] {chunk_name}: Already present.")
            skipped.append(chunk_name)
    return moved, skipped

def git_commit(msg):
    """Auto-add/commit any new files (if GIT_AUTO=True)."""
    if not GIT_AUTO:
        return
    os.chdir(PROJECT_ROOT)
    os.system("git add logs/")
    os.system(f'git commit -m "{msg}"')
    print("[OK] Git committed new/changed logs.")

def main():
    print("\n[=== DØPEMÜX ULTRASLICER: CHATLOG → CHUNKS → MANIFEST → LOGS ===]\n")
    chatlog_path = input("[?] Path to raw chat log (or leave empty to skip chunking): ").strip()
    if chatlog_path:
        run_chunker(chatlog_path)
    manifest = audit_manifest_and_files()
    if not manifest:
        print("[ERROR] No manifest, cannot proceed.")
        exit(1)
    moved, skipped = copy_chunks_to_logs(manifest)
    print(f"\n[SUMMARY] Moved: {moved}\nSkipped: {skipped}")
    git_commit("Processed and logged manifest chunks from latest chat log chunking — ritual enforced")
    print("\n[OK] Ultraslicer run complete. No chunk left behind, no mercy.")

if __name__ == "__main__":
    main()
