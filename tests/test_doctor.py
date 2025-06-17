import subprocess
import yaml
import sys
from pathlib import Path

def write_config(root):
    (root / "tagged/patch").mkdir(parents=True)
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


def test_doctor_ok(tmp_path):
    write_config(tmp_path)
    cli = Path(__file__).resolve().parents[1] / "cli.py"
    proc = subprocess.run([
        sys.executable,
        str(cli),
        "doctor",
    ], cwd=tmp_path, capture_output=True)
    assert proc.returncode == 0
