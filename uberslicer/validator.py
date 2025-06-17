import yaml, json, sys, glob
from pathlib import Path
from uberslicer.utils import log_audit, load_config

CFG = load_config()
SCHEMA_PATH = Path(CFG["schema"]["file"])
SCHEMA = json.loads(SCHEMA_PATH.read_text())


class ValidationError(Exception):
    def __init__(self, errors):
        self._errors = errors
    def errors(self):
        return self._errors

def validate_block(data):
    missing = [k for k in SCHEMA.get("required", []) if k not in data]
    if missing:
        raise ValidationError({"missing": missing})

def validate_all():
    """
    Validate every YAML block under the tagged folder against the UltraBlock schema,
    and also catch any 'patch' blocks still carrying the 'needs-review' tag.
    """
    cfg = load_config()
    paths = glob.glob(f"{cfg['paths']['tagged']}/**/*.yaml", recursive=True)
    bad, pending = 0, 0

    for p in paths:
        try:
            data = yaml.safe_load(open(p))
            validate_block(data)
            if "patch" in data.get("tags", []) and cfg["auditor"]["block_review_tag"] in data.get("tags", []):
                pending += 1
        except ValidationError as e:
            log_audit("error", {"file": p, "errors": e.errors()})
            bad += 1

    if bad or pending:
        sys.exit(f"❌ validation failed: {bad} bad blocks, {pending} pending patches")
    print("✅ all blocks validated & no pending patch review")
