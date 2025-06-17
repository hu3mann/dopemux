import click
import pyyaml
import os
import random
from uberslicer.utils import load_config, colorize, print_banner, dopamine_nudge

@click.group()
def cli():
    cfg = load_config()
    print_banner(cfg)
    dopamine_nudge(cfg)

@cli.command()
@click.argument('filepath')
def chunk(filepath):
    "Chunk a raw file and estimate token cost."
    from uberslicer.chunker import chunk_file
    cfg = load_config()
    chunk_file(
        filepath,
        chunk_size=cfg['chunk_size'],
        overlap=cfg['chunk_overlap'],
        model=cfg['default_model'],
        price_per_1k_tokens=cfg['price_per_1k_tokens']
    )

@cli.command()
def prefilter():
    "Prefilter all new chunks to dopemux signal only."
    from uberslicer.prefilter import prefilter_all
    prefilter_all()

@cli.command()
def extract():
    "Extract schema-perfect memory blocks from filtered."
    from uberslicer.extractor import extract_all
    extract_all()

@cli.command()
def merge():
    "Merge, dedupe, and manifest all processed blocks."
    from uberslicer.merge import merge_all
    merge_all()

@cli.command()
def status():
    "Show pipeline progress, manifest, and cost summary."
    from uberslicer.indexer import status_report
    status_report()

@cli.command()
def demo():
    "Run demo/test pipeline on test_data."
    print(colorize("Running dopemux demo on test data...", "accent1"))
    # Optionally call chunk/prefilter/extract/merge on /test_data/

@cli.command()
def package():
    "Zip your full pipeline for dopamine-rich sharing."
    import shutil
    shutil.make_archive("dopemux_memory_dump", 'zip', "data/")
    print(colorize("dopemux memory pit zipped. Extract your dopamine.", "success"))

@cli.command()
@click.argument("oldfile", type=click.Path(exists=True))
@click.option(
    "--new",
    "newfile",
    required=True,
    type=click.Path(exists=True),
    help="Path to the NEW version of the file you are patching"
)
@click.option(
    "--reason",
    default="File diff captured",
    help="Short reason for this patch (shown in devlog)"
)
def patch(oldfile, newfile, reason):
    """
    Create a Dopemux PATCH block between OLDFILE and --new NEWFILE.
    """
    from uberslicer.patch import create_patch_block
    create_patch_block(oldfile, newfile, reason)

@cli.command()
def validate():
    """
    Validate all tagged YAML blocks against the extraction schema,
    and error if any PATCH blocks still carry 'needs-review'.
    """
    from uberslicer.validator import validate_all
    validate_all()

@cli.command()
def doctor():
    """
    Run a quick sanity check on Dopemux paths, config keys, and required folders.
    """
    from uberslicer.doctor import run_diagnosis
    run_diagnosis()

if __name__ == "__main__":
    cli()
