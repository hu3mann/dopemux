import click
import os
import random
from uberslicer.utils import load_config, colorize, print_banner, dopamine_nudge

@click.group()
def cli():
    cfg = load_config()
    print_banner(cfg)
    dopamine_nudge(cfg)


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
