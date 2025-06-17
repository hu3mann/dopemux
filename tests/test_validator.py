import yaml
import subprocess
from pathlib import Path


def setup_env(root: Path):
    (root / "tagged").mkdir()
    (root / "logs").mkdir()
    (root / "schema").mkdir()
    schema = root / "schema/extraction-schema.json"
    schema.write_text('{"title":"UltraBlock"}')
    cfg = {
        "dopemux": {
            "paths": {
                "tagged": "./tagged",
                "patch_dir": "./tagged/patch",
                "outputs": "./outputs",
                "devlog": "./logs/devlog.json",
                "audit": "./logs/audit.json"
            },
            "schema": {"file": "./schema/extraction-schema.json"},
            "auditor": {"block_review_tag": "needs-review"}
        }
    }
    (root / "config.yaml").write_text(yaml.dump(cfg))


def test_validate_ok(tmp_path: Path):
    setup_env(tmp_path)
    block = {
        "project": "demo",
        "block_id": "b1",
        "session_metadata": {"timestamp": "2023", "source_file": "x"},
        "content": "hi",
        "tags": ["note"],
        "summary": "test"
    }
    with open(tmp_path / "tagged" / "one.yaml", "w") as f:
        yaml.dump(block, f)
    proc = subprocess.run(["dopemux", "validate"], cwd=tmp_path, capture_output=True)
    assert proc.returncode == 0
