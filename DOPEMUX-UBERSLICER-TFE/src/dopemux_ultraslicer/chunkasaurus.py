import os
import re
import json
import hashlib
import csv
from datetime import datetime

def estimate_tokens(s):
    return len(s.split())

def hash_chunk(lines):
    m = hashlib.sha256()
    for l in lines:
        m.update(l.encode('utf-8'))
    return m.hexdigest()

def get_manifest(manifest_path):
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as mf:
            return json.load(mf)
    else:
        return {}

def save_manifest(manifest, manifest_path):
    with open(manifest_path, 'w', encoding='utf-8') as mf:
        json.dump(manifest, mf, indent=2)

def save_manifest_csv(manifest, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['label','file','timestamp','lines_start','lines_end','tokens','sha256'])
        for label, entry in manifest.items():
            writer.writerow([
                label,
                entry['file'],
                entry['timestamp'],
                entry['lines'][0],
                entry['lines'][1],
                entry['tokens'],
                entry['sha256']
            ])

def intelligent_chunker(
    infile,
    outdir,
    max_tokens=12000,
    chunk_type="markdown",
    force=False
):
    basename = os.path.splitext(os.path.basename(infile))[0]
    manifest_path = os.path.join(outdir, "chunk_manifest.json")
    csv_path = os.path.join(outdir, "chunk_manifest.csv")

    if force:
        for fname in os.listdir(outdir):
            if fname.startswith(basename) and fname.endswith('.txt'):
                os.remove(os.path.join(outdir, fname))
        if os.path.exists(manifest_path):
            os.remove(manifest_path)
        if os.path.exists(csv_path):
            os.remove(csv_path)

    manifest = get_manifest(manifest_path)

    with open(infile, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    split_regex = re.compile(r'^(#+ |\-\-\-|\.\.\.|You said:)', re.IGNORECASE)
    chunk_lines, token_count, chunk_num = [], 0, 1
    chunks_written = 0
    all_summary = []

    for i, line in enumerate(lines):
        is_split = split_regex.match(line) and token_count > max_tokens // 2
        if is_split or token_count >= max_tokens:
            label = f"{basename}_chunk_{chunk_num:03d}"
            outname = os.path.join(outdir, f"{label}.txt")
            start_line = i - len(chunk_lines) + 1
            end_line = i
            chunk_hash = hash_chunk(chunk_lines)

            if force or label not in manifest:
                with open(outname, 'w', encoding='utf-8') as out:
                    out.write(f'<<<ARTEFACT_BEGIN label="{label}" type="{chunk_type}">>>\n')
                    out.writelines(chunk_lines)
                    out.write('\n<<<ARTEFACT_END>>>\n')
                manifest[label] = {
                    "file": outname,
                    "timestamp": datetime.now().isoformat(),
                    "lines": [start_line, end_line],
                    "tokens": token_count,
                    "sha256": chunk_hash
                }
                chunks_written += 1

            all_summary.append([
                label, outname, start_line, end_line, token_count, chunk_hash
            ])
            chunk_lines = []
            token_count = 0
            chunk_num += 1

        chunk_lines.append(line)
        token_count += estimate_tokens(line)

    # Last chunk
    if chunk_lines:
        label = f"{basename}_chunk_{chunk_num:03d}"
        outname = os.path.join(outdir, f"{label}.txt")
        start_line = len(lines) - len(chunk_lines) + 1
        end_line = len(lines)
        chunk_hash = hash_chunk(chunk_lines)

        if force or label not in manifest:
            with open(outname, 'w', encoding='utf-8') as out:
                out.write(f'<<<ARTEFACT_BEGIN label="{label}" type="{chunk_type}">>>\n')
                out.writelines(chunk_lines)
                out.write('\n<<<ARTEFACT_END>>>\n')
            manifest[label] = {
                "file": outname,
                "timestamp": datetime.now().isoformat(),
                "lines": [start_line, end_line],
                "tokens": token_count,
                "sha256": chunk_hash
            }
            chunks_written += 1

        all_summary.append([
            label, outname, start_line, end_line, token_count, chunk_hash
        ])

    save_manifest(manifest, manifest_path)
    save_manifest_csv(manifest, csv_path)

    print("\nChunks written/updated:", chunks_written)
    print("\n{: <25} {: <35} {: <10} {: <10} {: <8} {}".format(
        "Label", "File", "Start", "End", "Tokens", "SHA256 (first 10)"
    ))
    print("-"*100)
    for row in all_summary:
        print("{: <25} {: <35} {: <10} {: <10} {: <8} {}".format(
            row[0], os.path.basename(row[1]), row[2], row[3], row[4], row[5][:10]
        ))
    print(f"\nFull manifest: {manifest_path}\nCSV manifest: {csv_path}")

if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args) < 3:
        print("Usage: python intelligent_chunker.py <inputfile> <outputdir> [--force]")
        sys.exit(1)
    infile = args[1]
    outdir = args[2]
    force = '--force' in args
    os.makedirs(outdir, exist_ok=True)
    intelligent_chunker(infile, outdir, force=force)
