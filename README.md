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

## Layout

- `uberslicer/` - core library modules
- `schema/` - JSON schemas
- `tagged/` - generated YAML blocks
- `logs/` - dev/audit logs

Configure paths in `config.yaml`. Schema paths are relative so the
project works anywhere.

