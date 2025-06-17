import click
from doctor import run_diagnosis

@click.command()
def run():
    """Run Dopemux sanity checks."""
    run_diagnosis()
