"""Static provider selection and side-effect-free active-session resolution."""

from collections.abc import Mapping
from pathlib import Path
from typing import Protocol

from . import codex, opencode
from .shared.types import CollectedEvidence, Diagnostic


class Provider(Protocol):
    def detect_current(self, environment: Mapping[str, str]) -> str | None: ...
    def detect_saved(self, implementation_dir: Path) -> bool: ...
    def capture_current(self, implementation_dir: Path, session_id: str) -> list[Diagnostic]: ...
    def collect(self, implementation_dir: Path) -> CollectedEvidence: ...


PROVIDERS: dict[str, Provider] = {"codex": codex, "opencode": opencode}


def select(provider: str) -> Provider:
    try:
        return PROVIDERS[provider]
    except KeyError:
        raise ValueError(f"unsupported tracing provider: {provider}") from None


def detect_saved(implementation_dir: Path) -> str:
    """Identify one provider from saved evidence without host access or writes."""
    root = Path(implementation_dir).resolve()
    if not root.is_dir():
        raise ValueError(
            f"cannot detect tracing provider: implementation directory does not exist: {root}"
        )
    matches = []
    for name, provider in PROVIDERS.items():
        try:
            if provider.detect_saved(root):
                matches.append(name)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise ValueError(
                f"cannot detect tracing provider: unreadable or invalid {name} evidence in {root / 'native'}: {exc}"
            ) from exc
    if not matches:
        raise ValueError(
            f"cannot detect tracing provider: no supported saved native evidence in {root / 'native'}; capture or import native traces first"
        )
    if len(matches) > 1:
        raise ValueError(
            f"ambiguous tracing provider: {', '.join(matches)} evidence found in {root / 'native'}; use an implementation directory containing one provider's evidence"
        )
    return matches[0]


def detect_current(environment: Mapping[str, str]) -> tuple[Provider, str] | None:
    matches = [
        (name, provider, session)
        for name, provider in PROVIDERS.items()
        if (session := provider.detect_current(environment)) is not None
    ]
    if len(matches) > 1:
        raise ValueError(
            "conflicting tracing providers: " + ", ".join(name for name, _, _ in matches)
        )
    return (matches[0][1], matches[0][2]) if matches else None


def capture_current(root: Path, detected: tuple[Provider, str] | None) -> list[Diagnostic]:
    if detected is None:
        return [dict(code="current_session_unavailable", coverage_effect="informational")]
    provider, session = detected
    return provider.capture_current(root, session)
