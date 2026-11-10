"""Discover saved OpenCode exports and recover native assignment inheritance."""

import json
from pathlib import Path
from typing import cast

from tracing.shared.assignments import annotate_assignments, assignment_tag
from tracing.shared.events import read_source
from tracing.shared.files import local_path
from tracing.shared.types import Assignment, CollectedEvidence, Event, EvidenceKey, Source

from .capture import refresh
from .capture import turns as opencode_turns
from .diagnostics import classify, gap
from .parser import parse
from .types import OpenCode


def saved_exports(root: Path) -> list[Source]:
    exports: list[Source] = []
    for path in sorted((root / "native").rglob("*.json")):
        if not path.is_file():
            continue
        local_path(root, path)
        data = cast(OpenCode, json.loads(path.read_text()))
        info = data["info"]
        legacy = "version" in info
        if legacy:
            turns = [
                m["info"]["id"]
                for m in data["messages"]
                if m["info"]["role"] == "user" and m["info"].get("sessionID") == info["id"]
            ]
        else:
            turns = list(opencode_turns(data))
        exports.append(
            dict(
                id=str(path.relative_to(root)),
                path=str(path.relative_to(root)),
                adapter="opencode",
                session_id=info["id"],
                turn_ids=turns,
                source_version="opencode-export-" + str(info.get("version", "v2")),
            )
        )
    return exports


def collect(implementation_dir: Path) -> CollectedEvidence:
    root = Path(implementation_dir).resolve()
    exports = saved_exports(root)
    diagnostics = refresh(root, exports)
    exports = saved_exports(root)
    if not exports:
        diagnostics.append(gap("no_native_evidence"))
    assignments: dict[EvidenceKey, Assignment] = {}
    export_prompts: dict[str, dict[str, tuple[float, str]]] = {}
    for source in exports:
        data = cast(OpenCode, json.loads((root / source["path"]).read_text()))
        if "version" not in data["info"]:
            # Synthetic notifications quote child output, not this agent's assignment.
            prompts = [
                (
                    turn,
                    messages[0]["time"]["created"],
                    "\n".join(
                        [m.get("text", "") for m in messages if m["type"] == "user"]
                        + [
                            p.get("text", "")
                            for m in messages
                            if m["type"] == "assistant"
                            for p in m.get("content", [])
                            if p["type"] == "text"
                        ]
                    ),
                )
                for turn, messages in opencode_turns(data).items()
            ]
        else:
            prompts = [
                (
                    m["info"]["id"],
                    m["info"].get("time", {}).get("created", 0),
                    "\n".join(p.get("text", "") for p in m["parts"] if p.get("type") == "text"),
                )
                for m in data["messages"]
                if m["info"]["id"] in source["turn_ids"]
            ]
        for turn, time, text in prompts:
            export_prompts.setdefault(source["session_id"], {})[turn] = (time, text)
    for session, session_prompts in export_prompts.items():
        previous = None
        for turn, (_, text) in sorted(session_prompts.items(), key=lambda item: item[1][0]):
            tag, ambiguous = assignment_tag(text, root.name)
            if ambiguous:
                diagnostics.append(gap("ambiguous_assignment", session, turn))
                previous = None
            elif tag:
                previous = tag
            assignments[("opencode", session, turn)] = previous or {}
    annotate_assignments(root, exports, assignments, "opencode")
    events: list[Event] = []
    for source in exports:
        source["tracing_provider"] = "opencode"
        native, gaps = read_source(source, root / source["path"], parse)
        events.extend(native)
        diagnostics.extend(gaps)
    return CollectedEvidence(events, exports, assignments, {}, classify(diagnostics))
