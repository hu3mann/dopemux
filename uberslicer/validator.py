from pydantic import BaseModel, ValidationError
import yaml, json, sys, glob
from pathlib import Path
from utils import log_audit, CFG

SCHEMA_PATH = Path(CFG["schema"]["file"])
SCHEMA = json.loads(SCHEMA_PATH.read_text())

class UltraBlock(BaseModel):
    project: str
    block_id: str
    session_metadata: dict
    content: str
    tags: list
    summary: str | None = None
    patch_type: str | None = None  # only for patch blocks

def validate_all():
    """
    Validate every YAML block under the tagged folder against the UltraBlock schema,
    and also catch any 'patch' blocks still carrying the 'needs-review' tag.
    """
    paths = glob.glob(f"{CFG['paths']['tagged']}/**/*.yaml", recursive=True)
    bad, pending = 0, 0

    for p in paths:
        try:
            data = yaml.safe_load(open(p))
            UltraBlock(**data)  # will raise on invalid schema
            if "patch" in data.get("tags", []) and CFG["auditor"]["block_review_tag"] in data.get("tags", []):
                pending += 1
        except ValidationError as e:
            log_audit("error", {"file": p, "errors": e.errors()})
            bad += 1

    if bad or pending:
        sys.exit(f"❌ validation failed: {bad} bad blocks, {pending} pending patches")
    print("✅ all blocks validated & no pending patch review")
