import os
import hashlib
import json
from datetime import datetime
import argparse

EXCLUDE_DIRS = {'.git', '.venv', '__pycache__', '.vscode', '.idea', '.egg-info'}
EXCLUDE_FILES = {'.DS_Store', '.env'}

def should_exclude(relpath):
    parts = set(relpath.split(os.sep))
    # Exclude any directory in EXCLUDE_DIRS or ending with .egg-info or .egg
    if parts & EXCLUDE_DIRS:
        return True
    if any(part.endswith('.egg-info') or part.endswith('.egg') for part in parts):
        return True
    if os.path.basename(relpath) in EXCLUDE_FILES:
        return True
    if relpath.endswith('.egg') or relpath.endswith('.egg-info'):
        return True
    return False

def hash_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def walk_dir(root, max_depth=None):
    manifest = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Exclude unwanted directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        # Calculate depth relative to root
        depth = os.path.relpath(dirpath, root).count(os.sep)
        if max_depth is not None and depth > max_depth:
            dirnames[:] = []
            continue
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            relpath = os.path.relpath(fpath, root)
            if should_exclude(relpath):
                continue
            try:
                stat = os.stat(fpath)
                manifest.append({
                    "file": relpath,
                    "size": stat.st_size,
                    "sha256": hash_file(fpath),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
            except Exception as e:
                print(f"Error reading {fpath}: {e}")
    return manifest

def write_all_files(manifest, root, output_path="uberslicer-all-files.md"):
    with open(output_path, "w") as out:
        for entry in manifest:
            file_path = os.path.join(root, entry["file"])
            out.write(f"--- BEGIN: {entry['file']} ---\n")
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"[Error reading file: {e}]\n")
            out.write(f"\n--- END: {entry['file']} ---\n\n")

def main():
    parser = argparse.ArgumentParser(description='Generate a JSON file manifest.')
    parser.add_argument('root', help='Root directory to scan')
    parser.add_argument('--depth', type=int, default=None, help='Maximum recursion depth')
    parser.add_argument('-o', '--output', default='manifest.json', help='Output JSON file')
    parser.add_argument('--all-md', default='uberslicerall-files.md', help='Output concatenated markdown file')
    args = parser.parse_args()

    manifest = walk_dir(args.root, args.depth)
    with open(args.output, "w") as out:
        json.dump(manifest, out, indent=2)
    write_all_files(manifest, args.root, args.all_md)

if __name__ == '__main__':
    main()