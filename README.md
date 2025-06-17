# Dopemux

Terminal-native, forensic context engine with dopamine rituals.

## CLI

Run commands from the project root:

```bash
dopemux patch OLD --new NEW --reason "why"
dopemux validate
dopemux doctor
```

## Layout

- `uberslicer/` - core library modules
- `schema/` - JSON schemas
- `tagged/` - generated YAML blocks
- `logs/` - dev/audit logs

Configure paths in `config.yaml`. Schema paths are relative so the
project works anywhere.

