# Dopemux

Terminal-native, forensic context engine with dopamine rituals.

## CLI

Run commands from the project root:

```bash
dopemux patch OLD --new NEW --reason "why"
dopemux validate
dopemux doctor
```

## Setup

Run the locale setup script before using Dopemux. It ensures Python sees UTF-8
locales on macOS and Linux:

```bash
bash scripts/setup-env.sh
```

After running the script you can call the CLI commands normally.

Create a `logs/` directory in your workspace before running commands. The
application writes `devlog.json` and `audit.json` there but the folder is ignored
in version control.

## Layout

- `uberslicer/` - core library modules
- `schema/` - JSON schemas
- `tagged/` - generated YAML blocks
- `logs/` - dev/audit logs created at runtime (ignored in git)

Configure paths in `config.yaml`. Schema paths are relative so the
project works anywhere.

## Color output

`utils.colorize()` wraps text with ANSI escape codes. Customize styles in
`config.yaml` under `dopemux.colors`.

### Banners

Run `python banner_loader.py` to print a random dopamine banner. The `dopemux-banners` folder contains the raw banner files; create `dopemux-banners.zip` yourself if you need a zipped archive.

