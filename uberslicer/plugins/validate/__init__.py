import click
from ...validator import validate_all

@click.command()
def run():
    """Validate all tagged blocks."""
    validate_all()
