"""Validate assignment text and annotations supplied for a normalized selection."""

import json
from pathlib import Path
from typing import cast

from .files import identifier, local_path
from .types import Assignment, EvidenceKey, Source
from .values import object_value


def annotate_assignments(
    root: Path, sources: list[Source], assignments: dict[EvidenceKey, Assignment], provider: str
) -> None:
    """Fill only missing selected assignments; never select evidence or override tags."""
    path = local_path(root, root / "assignment-annotations.json")
    if not path.exists():
        return
    data = json.loads(path.read_text())
    if (
        not isinstance(data, dict)
        or data.get("version") != 1
        or not isinstance(data.get("assignments"), list)
    ):
        raise ValueError("invalid assignment annotations: expected version 1 and assignments list")
    selected = {(s["adapter"], s["session_id"], t) for s in sources for t in s["turn_ids"]}
    seen = set()
    for entry in data["assignments"]:
        if not isinstance(entry, dict):
            raise ValueError("invalid assignment annotation")
        # Annotations for another provider do not participate in this selection.
        identifier(entry.get("adapter"))
        if entry["adapter"] != provider:
            continue
        key = tuple(entry.get(k) for k in ("adapter", "session_id", "turn_id"))
        for value in key:
            identifier(value)
        if key not in selected or key in seen:
            raise ValueError("assignment annotation needs a unique selected native turn")
        seen.add(key)
        tag = {k: identifier(entry.get(k)) for k in ("task", "role")}
        tag["implementation"] = root.name
        if "purpose" in entry:
            if not isinstance(entry["purpose"], str) or len(entry["purpose"]) > 500:
                raise ValueError("invalid annotation purpose")
            tag["purpose"] = entry["purpose"]
        evidence = entry.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise ValueError("assignment annotation needs evidence paths")
        for reference in evidence:
            if (
                not isinstance(reference, str)
                or not reference
                or Path(reference).is_absolute()
                or not local_path(root, root / reference).is_file()
            ):
                raise ValueError("assignment annotation needs implementation-local evidence files")
        native_key = cast(EvidenceKey, key)
        if assignments.get(native_key):
            raise ValueError("assignment annotation conflicts with a native assignment")
        assignments[native_key] = cast(
            Assignment, dict(tag, source="annotation", evidence=evidence)
        )


def assignment_tag(text: str, implementation: str) -> tuple[Assignment | None, bool]:
    tags = []
    invalid = False
    for line in text.splitlines():
        if not line.startswith("AGENTIC_WORKFLOW "):
            continue
        value = object_value(line.partition(" ")[2])
        try:
            for field in ("implementation", "task", "role"):
                identifier(value.get(field))
            if "purpose" in value and (
                not isinstance(value["purpose"], str) or len(value["purpose"]) > 500
            ):
                raise ValueError("invalid purpose")
        except ValueError:
            invalid = True
            continue
        if value["implementation"] == implementation:
            tags.append(cast(Assignment, value))
    unique = {json.dumps(t, sort_keys=True): t for t in tags}
    return (next(iter(unique.values())) if len(unique) == 1 else None, invalid or len(unique) > 1)
