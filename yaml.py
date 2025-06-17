"""Minimal YAML stand-in using JSON for environments without PyYAML."""
import json
from typing import Any, Union, IO
from pathlib import Path

__all__ = ["safe_load", "dump", "safe_load_all"]

def safe_load(stream: Union[str, bytes, IO[str]]) -> Any:
    if hasattr(stream, "read"):
        return json.load(stream)
    return json.loads(stream)

def safe_load_all(stream: Union[str, bytes, IO[str]]):
    # For compatibility with PyYAML's safe_load_all, just yield one document
    yield safe_load(stream)

class _Encoder(json.JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, Path):
            return str(o)
        return super().default(o)


def dump(data: Any, stream: IO[str] | None = None, sort_keys: bool = False) -> str:
    text = json.dumps(data, indent=2, sort_keys=sort_keys, cls=_Encoder)
    if stream is None:
        return text
    stream.write(text)
    return text
