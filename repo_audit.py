import os
import json
import hashlib
import subprocess
from datetime import datetime
from collections import defaultdict

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))

CODE_EXTS = {'.py', '.c', '.cpp', '.h', '.hpp', '.js', '.ts', '.go', '.rs'}
CONFIG_EXTS = {'.json', '.yml', '.yaml', '.toml', '.ini', '.cfg'}
DOC_EXTS = {'.md', '.rst', '.txt'}
BUILD_DIRS = {'build', 'dist', '__pycache__', '.pytest_cache', '.mypy_cache', 'dopemux.egg-info'}
BUILD_EXTS = {'.o', '.pyc', '.so', '.dll', '.a'}


def get_git_files():
    """Return a list of git tracked files using null separation to handle
    special characters."""
    try:
        out = subprocess.check_output(['git', 'ls-files', '-z'], cwd=REPO_ROOT)
        return out.decode().strip('\0').split('\0') if out else []
    except subprocess.CalledProcessError:
        return []


def get_all_files():
    git_files = set(get_git_files())
    all_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), REPO_ROOT)
            if rel not in git_files:
                all_files.append(rel)
    return sorted(git_files) + sorted(all_files)


def file_type(path):
    # Determine base type from extension or directory
    ext = os.path.splitext(path)[1].lower()
    parts = path.split(os.sep)
    if any(part in BUILD_DIRS for part in parts) or ext in BUILD_EXTS:
        return 'build-artifact'
    if ext in CODE_EXTS:
        return 'code'
    if ext in CONFIG_EXTS:
        return 'config'
    if ext in DOC_EXTS:
        return 'doc'
    if ext:
        return 'asset'
    return 'other'


def detect_language(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.py':
        return 'Python'
    if ext in {'.c', '.h'}:
        return 'C'
    if ext in {'.cpp', '.hpp'}:
        return 'C++'
    if ext in {'.js'}:
        return 'JavaScript'
    if ext in {'.ts'}:
        return 'TypeScript'
    if ext in {'.go'}:
        return 'Go'
    if ext in {'.rs'}:
        return 'Rust'
    if ext in {'.json'}:
        return 'JSON'
    if ext in {'.yml', '.yaml'}:
        return 'YAML'
    if ext in {'.toml'}:
        return 'TOML'
    if ext in {'.md'}:
        return 'Markdown'
    if ext in {'.txt'}:
        return 'Text'
    return 'unknown'


def check_python(path):
    try:
        subprocess.check_output(['python', '-m', 'py_compile', path], stderr=subprocess.STDOUT)
        return True, 'compiled successfully'
    except subprocess.CalledProcessError as e:
        return False, e.output.decode(errors='ignore').strip().splitlines()[-1]


def check_javascript(path):
    try:
        subprocess.check_output(['node', '--check', path], stderr=subprocess.STDOUT)
        return True, 'syntax ok'
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        msg = 'node check failed'
        if isinstance(e, subprocess.CalledProcessError):
            msg = e.output.decode(errors='ignore').strip().splitlines()[-1]
        return False, msg


def check_c(path, lang='c'):
    compiler = 'gcc' if lang == 'c' else 'g++'
    try:
        subprocess.check_output([compiler, '-fsyntax-only', path], stderr=subprocess.STDOUT)
        return True, 'compiled'
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        msg = 'compile failed'
        if isinstance(e, subprocess.CalledProcessError):
            msg = e.output.decode(errors='ignore').strip().splitlines()[-1]
        return False, msg


def analyze_file(path):
    full = os.path.join(REPO_ROOT, path)
    info = os.stat(full)
    size = info.st_size
    mtime = datetime.fromtimestamp(info.st_mtime).isoformat()
    ftype = file_type(path)
    lang = detect_language(path)
    status = 'good'
    reason = ''

    if ftype == 'build-artifact':
        status = 'junk'
        reason = 'build artifact'
    else:
        if lang == 'Python':
            ok, reason = check_python(full)
            status = 'good' if ok else 'broken'
        elif lang == 'JavaScript':
            ok, reason = check_javascript(full)
            status = 'good' if ok else 'broken'
        elif lang in {'C', 'C++'}:
            ok, reason = check_c(full, 'c++' if lang == 'C++' else 'c')
            status = 'good' if ok else 'broken'
        else:
            status = 'good'
            reason = 'n/a'

    return {
        'path': path,
        'type': ftype,
        'language': lang,
        'size_bytes': size,
        'last_modified': mtime,
        'status': status,
        'reason': reason
    }


def compute_hash(path):
    sha1 = hashlib.sha1()
    with open(os.path.join(REPO_ROOT, path), 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha1.update(chunk)
    return sha1.hexdigest()


def main():
    files = get_all_files()
    audit_entries = []
    hash_map = defaultdict(list)
    for path in files:
        h = compute_hash(path)
        hash_map[h].append(path)
    duplicates = {h: ps for h, ps in hash_map.items() if len(ps) > 1}

    for path in files:
        entry = analyze_file(path)
        h = compute_hash(path)
        if h in duplicates and duplicates[h][0] != path:
            entry['status'] = 'junk'
            entry['reason'] = f"duplicate of {duplicates[h][0]}"
        audit_entries.append(entry)

    with open(os.path.join(REPO_ROOT, 'audit.json'), 'w') as f:
        json.dump(audit_entries, f, indent=2)

    # generate AUDIT.md
    generate_report(audit_entries)


def generate_report(entries):
    from collections import Counter
    status_counts = Counter(e['status'] for e in entries)
    lang_counts = Counter(e['language'] for e in entries)

    lines = []
    lines.append('# Repository Audit')
    lines.append('')
    lines.append('## Status Overview')
    for k, v in status_counts.items():
        lines.append(f'- **{k}**: {v}')
    lines.append('')
    lines.append('## Language Breakdown')
    for k, v in lang_counts.items():
        lines.append(f'- **{k}**: {v}')
    lines.append('')
    lines.append('| Path | Type | Lang | Size | Status | Reason |')
    lines.append('|------|------|------|------|--------|--------|')
    for e in entries:
        lines.append(f"| {e['path']} | {e['type']} | {e['language']} | {e['size_bytes']} | {e['status']} | {e['reason']} |")

    with open(os.path.join(REPO_ROOT, 'AUDIT.md'), 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    main()
