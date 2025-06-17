import os
import argparse

def generate_manifest(root, max_depth=None):
    manifest = []
    for dirpath, dirnames, filenames in os.walk(root):
        depth = dirpath.replace(root, '').count(os.sep)
        if max_depth is not None and depth > max_depth:
            # prune deeper dirs
            dirnames[:] = []
            continue
        # directory entry
        rel_path = os.path.relpath(dirpath, root)
        if rel_path == '.':
            rel_path = root
        manifest.append((rel_path + os.sep, 'dir', ''))
        # files
        for f in filenames:
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, root)
            manifest.append((rel, 'file', ''))
    return manifest


def to_markdown(manifest):
    md = ['| Path | Type | |', '|---|---|---|']
    for path, typ, desc in manifest:
        md.append(f'| `{path}` | {typ} | {desc} |')
    return '\n'.join(md)


def main():
    parser = argparse.ArgumentParser(description='Generate a directory manifest in Markdown.')
    parser.add_argument('root', help='Root directory to scan')
    parser.add_argument('--depth', type=int, default=None, help='Max recursion depth')
    args = parser.parse_args()

    manifest = generate_manifest(args.root, args.depth)
    print(to_markdown(manifest))

if __name__ == '__main__':
    main()
