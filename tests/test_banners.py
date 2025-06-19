from banners import random_roast, supports_unicode


def test_random_roast_returns_line(tmp_path, monkeypatch):
    # copy roast file to temp dir and monkeypatch BANNER_DIR
    roast = tmp_path / "roast_lines.txt"
    roast.write_text("one\ntwo\n")
    monkeypatch.setattr("banners.BANNER_DIR", tmp_path)
    assert random_roast() in {"one", "two"}


def test_supports_unicode():
    assert isinstance(supports_unicode(), bool)
