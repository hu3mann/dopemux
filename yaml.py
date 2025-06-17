import json
from typing import Any, TextIO

__all__ = ["safe_load", "dump", "safe_load_all"]

def safe_load(stream: Any) -> Any:
    if hasattr(stream, "read"):
        data = stream.read()
    else:
        data = stream
    if data == "" or data is None:
        return None
    return json.loads(data)

def safe_load_all(stream: Any):
    yield safe_load(stream)

def dump(data: Any, stream: TextIO = None, sort_keys: bool = False) -> str:
    text = json.dumps(data, indent=2, sort_keys=sort_keys)
    if stream is not None:
        stream.write(text)
        return ""
    return text
