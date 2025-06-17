import yaml
import subprocess


def test_patch_block(tmp_path):
    old = tmp_path / "old.py"
    new = tmp_path / "new.py"
    old.write_text("x = 1\n")
    new.write_text("x = 2\n")
    tagdir = tmp_path / "tagged/patch"
    tagdir.mkdir(parents=True)
    # Write minimal config pointing to tmp dirs
    (tmp_path / "logs").mkdir()
    (tmp_path / "schema").mkdir()
    schema = tmp_path / "schema/extraction-schema.json"
    schema.write_text('{"title": "UltraBlock"}')
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
    (tmp_path / "config.yaml").write_text(yaml.dump(cfg))
    patch = subprocess.run([
        "dopemux", "patch", str(old),
        "--new", str(new),
        "--reason", "unit test"
    ], cwd=tmp_path, capture_output=True, text=True)
    assert patch.returncode == 0
    files = list(tagdir.glob("*.yaml"))
    assert len(files) == 1
    blk = yaml.safe_load(files[0].read_text())
    assert "patch" in blk["tags"]
