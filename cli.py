import click
from utils import load_config, print_banner, dopamine_nudge
from uberslicer import load_plugins

@click.group()
def cli():
    cfg = load_config()
    print_banner(cfg)
    dopamine_nudge(cfg)

for name, cmd in load_plugins():
    cli.add_command(cmd, name)

if __name__ == "__main__":
    cli()
