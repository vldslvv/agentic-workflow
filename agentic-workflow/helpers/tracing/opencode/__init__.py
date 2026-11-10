"""OpenCode tracing provider; imports perform no host I/O."""

from collections.abc import Mapping
from pathlib import Path

from tracing.shared.types import Diagnostic

from .capture import capture_current as capture
from .collection import collect as collect
from .collection import saved_exports
from .diagnostics import classify


def detect_current(environment: Mapping[str, str]) -> str | None:
    return environment.get("OPENCODE_SESSION_ID") or None


def detect_saved(implementation_dir: Path) -> bool:
    return bool(saved_exports(implementation_dir))


def capture_current(implementation_dir: Path, session_id: str) -> list[Diagnostic]:
    return classify(capture(implementation_dir, session_id))
