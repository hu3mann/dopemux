from pydantic import BaseModel, ValidationError
import yaml, json, sys, glob
from pathlib import Path
from uberslicer.utils import log_audit, CFG

SCHEMA_PATH = Path(CFG["schema"]["file"])
SCHEMA = json.loads(open(SCHEMA_PATH).read())

class UltraBlock(BaseModel):
    project: str
    block_id: str
    session_metadata: dict
    content: str
    tags: list
    summary: str | None = None
    patch_type: str | None = None       # only for patch blocks

def validate_file(path):
    data = yaml.safe_load(open(path))
    UltraBlock(**data)                  # raises on invalid
    return data

def main():
    paths = glob.glob(f"{CFG['paths']['tagged']}/**/*.yaml", recursive=True)
    bad, pending = 0, 0
    for p in paths:
        try:
            blk = validate_file(p)
            if "patch" in blk["tags"] and CFG["auditor"]["block_review_tag"] in blk["tags"]:
                pending += 1
        except ValidationError as e:
            log_audit({"file": p, "error": e.errors()})
            bad += 1
    if bad or pending:
        sys.exit(f"❌ validation failed: {bad} bad blocks, {pending} pending patches")
    print("✅ all blocks validated & no pending patch review")

if __name__ == "__main__":
    main()
