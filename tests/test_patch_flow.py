import yaml, subprocess, shutil, pathlib, uuid

def test_patch_block(tmp_path):
    old = tmp_path / "old.py"
    new = tmp_path / "new.py"
    old.write_text("x = 1\n")
    new.write_text("x = 2\n")
    tagdir = tmp_path / "tagged/patch"
    tagdir.mkdir(parents=True)
    # point config at tmp dirs
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
