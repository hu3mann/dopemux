#!/usr/bin/env python3
"""Update state.yaml using an OpenAI ChatGPT prompt."""
import openai
import yaml
import json
from pathlib import Path

MANIFEST = Path('manifest.json')
STATE = Path('state.yaml')

PROMPT = (
    "Summarize the attached manifest as YAML with keys: summary and file_count."
)

def main():
    if not MANIFEST.exists():
        raise SystemExit('manifest.json missing')
    with MANIFEST.open() as f:
        manifest = json.load(f)
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": PROMPT},
                  {"role": "system", "content": json.dumps(manifest)}],
    )
    content = completion.choices[0].message.content
    data = yaml.safe_load(content)
    with STATE.open('w') as f:
        yaml.safe_dump(data, f)

if __name__ == '__main__':
    main()
