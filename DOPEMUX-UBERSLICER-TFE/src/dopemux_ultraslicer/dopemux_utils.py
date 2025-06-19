import yaml, os, datetime

DEVLOG_PATH = "TFE-DEVLOG.txt"
AUDIT_PATH  = "TFE-AUDIT-ULTRA-RITUAL.txt"

def _append_block(path, entry):
    entry['timestamp'] = datetime.datetime.utcnow().isoformat()
    if not os.path.exists(path):
        with open(path, "w") as f: yaml.dump({'entries': [entry]}, f)
    else:
        with open(path) as f: data = yaml.safe_load(f) or {}
        entries = data.get('entries', [])
        entries.append(entry)
        with open(path, "w") as f: yaml.dump({'entries': entries}, f)

def log_dev(action, details=[]):
    block = {
        'action': action,
        'details': details,
    }
    _append_block(DEVLOG_PATH, block)

def log_audit(level, summary):
    block = {
        'level': level,
        'summary': summary,
    }
    _append_block(AUDIT_PATH, block)
