import json
import hashlib
import subprocess
from datetime import datetime
import yaml
import os


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def update_state(manifest_path='manifest.json', md_path='all-files.md', state_path='state.yaml'):
    data = {
        'generated': datetime.utcnow().isoformat() + 'Z',
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
    }
    if os.path.exists(manifest_path):
        data['manifest_sha256'] = sha256(manifest_path)
        with open(manifest_path) as f:
            try:
                manifest = json.load(f)
                data['file_count'] = len(manifest)
            except Exception:
                data['file_count'] = 0
    if os.path.exists(md_path):
        data['all_md_sha256'] = sha256(md_path)
    with open(state_path, 'w') as f:
        yaml.safe_dump(data, f)

if __name__ == '__main__':
    update_state()
