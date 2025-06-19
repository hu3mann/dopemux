from uberslicer.rituals import slice_blocks, dump_blocks


def test_slice_and_dump(tmp_path):
    input_file = tmp_path / "in.txt"
    input_file.write_text("one\n\ntwo")
    blocks = slice_blocks(input_file)
    assert len(blocks) == 2
    outdir = tmp_path / "out"
    dump_blocks(blocks, outdir)
    files = list(outdir.glob("*.yaml"))
    assert len(files) == 2
