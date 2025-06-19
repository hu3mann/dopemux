import click
from ...patch import create_patch_block

@click.command()
@click.argument("oldfile", type=click.Path(exists=True))
@click.option("--new", "newfile", required=True, type=click.Path(exists=True),
              help="Path to the NEW version of the file you are patching")
@click.option("--reason", default="File diff captured",
              help="Short reason for this patch (shown in devlog)")
def run(oldfile, newfile, reason):
    """Create a Dopemux PATCH block."""
    create_patch_block(oldfile, newfile, reason)
