import yaml
import json
import pathlib

SCHEMA_YAML = pathlib.Path(__file__).parent.parent / "schemas" / "schemas.yaml"
OUTPUT_DIR = pathlib.Path(__file__).parent.parent / "schemas"

def main():
    with open(SCHEMA_YAML, "r") as f:
        data = yaml.safe_load(f)

    for key, value in data.items():
        out_path = OUTPUT_DIR / f"{key}.json"
        with open(out_path, "w") as out_f:
            json.dump(value, out_f, indent=2)
        print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()