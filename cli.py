import click
from utils import print_banner, dopamine_nudge
from uberslicer import load_plugins
from banners import on_boot

@click.group()
def cli():
    print_banner()
    dopamine_nudge()

for name, cmd in load_plugins():
    cli.add_command(cmd, name)

if __name__ == "__main__":
    cli()
