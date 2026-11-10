"""Select specification bundles and capture their local review references."""

import os
import re
import shutil
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote, urlsplit

from . import runtime
from .models import Check, Inputs

REFERENCES = (
    "agentic-workflow/templates/project.md",
    "agentic-workflow/templates/task_order.md",
    "agentic-workflow/templates/tasks/task.md",
    "agentic-workflow/templates/contracts/contract.md",
    "agentic-workflow/templates/verification.md",
    "agentic-workflow/policies/BUNDLE.md",
    "agentic-workflow/policies/DOCUMENT_STYLE.md",
    "agentic-workflow/policies/CHECKS.md",
    "agentic-workflow/policies/GUIDELINES.md",
)


def select_bundles(root: Path, bundle: str | None) -> list[Path]:
    directory = root / "specs"
    if bundle is not None:
        selected = root / bundle
        if (
            not selected.resolve().is_relative_to(directory.resolve())
            or selected.resolve().parent != directory.resolve()
            or selected.is_symlink()
            or not selected.is_dir()
        ):
            raise runtime.RunnerError(f"Select a bundle directory directly under specs/: {bundle}")
        bundles = [selected]
    else:
        bundles = (
            sorted(path for path in directory.iterdir() if path.is_dir())
            if directory.is_dir()
            else []
        )
    if not bundles:
        raise runtime.RunnerError("No bundle directories under specs/")
    for path in bundles:
        if path.is_symlink() or not any(item.is_file() for item in path.rglob("*")):
            raise runtime.RunnerError(f"Empty or symlink bundle: {path}")
    return bundles


def document_links(text: str) -> Iterator[str]:
    """Read inline and reference-style Markdown destinations outside code fences."""
    text = re.sub(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$", "", text)
    pattern = r"\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)|^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)"
    for match in re.finditer(pattern, text, re.MULTILINE):
        yield (match[1] or match[2]).strip("<>")


def excluded_path(relative: Path) -> bool:
    return (
        bool(relative.parts)
        and relative.parts[0] in ("apps", ".agentic-workflow", ".git")
        or any(part in ("__pycache__", ".venv", "node_modules") for part in relative.parts)
    )


def capture(root: Path, destination: Path, bundle: str | None) -> Inputs:
    """Copy current bundle files and the transitive closure of local source links."""
    bundles = select_bundles(root, bundle)
    destination.mkdir(parents=True)
    excluded = [
        "Application outputs (apps/), project memory and execution history (.agentic-workflow/) are excluded."
    ]
    checks: list[Check] = []
    visited = set()
    pending = [(Path(relative), "required review reference") for relative in REFERENCES]
    for selected_bundle in bundles:
        pending.extend(
            (path.relative_to(root), "selected bundle")
            for path in sorted(selected_bundle.rglob("*"))
            if path.is_file() or path.is_symlink()
        )

    def unavailable(location: str, reason: str) -> None:
        message = f"{location}: {reason}"
        excluded.append(message)
        checks.append(
            {
                "contract": "agentic-workflow/policies/BUNDLE.md — resolve requirement links and required source documents",
                "status": "UNCLEAR",
                "evidence": message,
            }
        )

    while pending:
        relative, origin = pending.pop(0)
        # Normalize .. without following symlinks; reject symlink ancestors below.
        path = Path(os.path.abspath(root / relative))
        if not path.is_relative_to(root):
            unavailable(origin, f"outside repository: {relative}")
            continue
        relative = path.relative_to(root)
        if relative in visited:
            continue
        visited.add(relative)
        if excluded_path(relative):
            unavailable(origin, f"excluded reference: {relative}")
            continue
        if any(
            parent.is_symlink()
            for parent in (path, *path.parents)
            if parent != root and parent.is_relative_to(root)
        ):
            unavailable(origin, f"symlink reference: {relative}")
            continue
        if not path.exists():
            unavailable(origin, f"unavailable reference: {relative}")
            continue
        if path == root:
            unavailable(origin, "repository directory is not a source document")
            continue
        if path.is_dir():
            pending.extend((item.relative_to(root), origin) for item in sorted(path.iterdir()))
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        if path.suffix.lower() != ".md":
            continue
        for link in document_links(path.read_text()):
            url = urlsplit(link)
            if url.scheme or url.netloc:
                excluded.append(f"{relative}: external reference not captured: {link}")
                continue
            if url.path:
                pending.append((relative.parent / unquote(url.path), f"{relative} -> {link}"))
    evidence: Inputs = {
        "bundles": [str(path.relative_to(root)) for path in bundles],
        "excluded_inputs": excluded,
        "checks": checks,
    }
    runtime.write_json(destination / "snapshot-references.json", evidence)
    return evidence
