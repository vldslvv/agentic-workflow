"""Decode explicitly supplied JSON objects without native interpretation."""

import json
from typing import cast


def object_value(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return cast(dict[str, object], value)
    if not isinstance(value, (str, bytes, bytearray)):
        return {}
    try:
        result = json.loads(value)
        return cast(dict[str, object], result) if isinstance(result, dict) else {}
    except (ValueError, TypeError):
        return {}
