"""Trial preparation, artifact grading and explicit cleanup."""

import json
import shutil
import stat
import subprocess
from pathlib import Path

from . import runtime
from .models import ArtifactGrade, RoleSettings

APP = Path("apps/todolist")
RESULTS = Path(".agentic-workflow/evals/todolist")
OUTPUTS = (APP, RESULTS)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=60,
    )
    if result.returncode:
        raise runtime.RunnerError(result.stderr.decode(errors="replace").strip())
    return result.stdout.decode(errors="surrogateescape")


def real_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except FileNotFoundError:
        return False


def safe_path(root: Path, relative: Path) -> Path:
    """Never read, grade, or remove an owned path through a symlink."""
    path = root
    for part in relative.parts:
        path /= part
        if path.is_symlink():
            raise runtime.RunnerError(f"Refusing symlink path: {path}")
    return path


def role_settings(path: Path, role: str) -> RoleSettings:
    tables: dict[str, dict[str, list[str]]] = {}
    section = None
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if line.startswith("|") and section in ("Profiles", "Role routes"):
            row = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
            if len(row) != 3 or not all(row):
                raise runtime.RunnerError(f"Malformed model configuration row: {line}")
            table = tables.setdefault(section, {})
            if row[0] in table:
                raise runtime.RunnerError(f"Duplicate model configuration row: {row[0]}")
            table[row[0]] = row[1:]
    try:
        profile = tables["Role routes"][role][0]
        model, reasoning = tables["Profiles"][profile]
    except KeyError as exc:
        raise runtime.RunnerError(f"Missing {role} default route or profile in MODELS.md") from exc
    return RoleSettings(profile, model, reasoning)


def preflight(root: Path, allow_dirty: bool) -> tuple[str, RoleSettings, str]:
    dirty = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if dirty and not allow_dirty:
        raise runtime.RunnerError(
            f"Clean checkout required; preserve or resolve these changes manually:\n{dirty}"
        )
    for relative in OUTPUTS:
        if safe_path(root, relative).exists():
            raise runtime.RunnerError(f"Required absent path already exists: {relative}")
    if git(root, "ls-files", "--", *(str(p) for p in OUTPUTS)):
        raise runtime.RunnerError("Eval output paths contain tracked files")
    if (
        subprocess.run(
            ["git", "-C", str(root), "check-ignore", "-q", str(RESULTS / "run.json")],
            stdin=subprocess.DEVNULL,
            timeout=60,
        ).returncode
        != 0
    ):
        raise runtime.RunnerError(".agentic-workflow/evals/todolist/ must be ignored by Git")
    for name in ("uv", "codex"):
        if not shutil.which(name):
            raise runtime.RunnerError(f"Required executable unavailable: {name}")
    auth = subprocess.run(
        ["codex", "login", "status"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=60,
    )
    if auth.returncode:
        raise runtime.RunnerError("Codex is not authenticated; run codex login first")
    override = root / ".agentic-workflow/config/MODELS.md"
    routing = override if override.exists() else root / "agentic-workflow/policies/MODELS.md"
    return git(root, "rev-parse", "HEAD").strip(), role_settings(routing, "Supervisor"), dirty


def records_entries(root: Path) -> dict[str, Path]:
    records = safe_path(root, Path(".agentic-workflow/records"))
    return {p.name: p for p in records.iterdir()} if records.exists() else {}


def new_implementations(root: Path, before: list[str]) -> list[str]:
    return sorted(
        name
        for name, path in records_entries(root).items()
        if name not in before and path.is_dir() and not path.is_symlink()
    )


def artifact_grade(root: Path, created: list[str]) -> ArtifactGrade:
    implementations = [root / ".agentic-workflow/records" / name for name in created]
    grade: ArtifactGrade = {
        "status": "FAIL",
        "implementations": [p.name for p in implementations],
        "missing": [],
    }
    if len(implementations) != 1:
        grade["error"] = "Expected one new implementation directory under .agentic-workflow/records"
        return grade
    implementation = implementations[0]
    for name in ("usage.json", "usage.md", "timeline.json"):
        relative = (implementation / "reports" / name).relative_to(root)
        if not real_file(safe_path(root, relative)):
            grade["missing"].append(str(relative))
    traces = [
        p
        for p in implementation.glob("native/*/*.jsonl")
        if real_file(safe_path(root, p.relative_to(root)))
    ]
    grade["native_files"] = [str(p.relative_to(root)) for p in sorted(traces)]
    if not traces:
        grade["missing"].append(str(implementation.relative_to(root) / "native/*/*.jsonl"))
    grade["status"] = "FAIL" if grade["missing"] else "PASS"
    return grade


def clean(root: Path) -> int:
    marker = safe_path(root, RESULTS / "run.json")
    if not real_file(marker):
        raise runtime.RunnerError("No eval run exists; refusing cleanup")
    metadata = json.loads(marker.read_text())
    if (
        not isinstance(metadata, dict)
        or metadata.get("eval") != "todolist"
        or metadata.get("root") != str(root)
    ):
        raise runtime.RunnerError("Eval run marker does not identify this checkout")
    result_path = safe_path(root, RESULTS / "result.json")
    if not real_file(result_path):
        raise runtime.RunnerError(
            "No completed eval inventory; preserve execution records and handle cleanup manually"
        )
    report = json.loads(result_path.read_text())
    before = metadata.get("records_entries_before")
    created = report.get("records_created") if isinstance(report, dict) else None
    if (
        not isinstance(before, list)
        or not isinstance(created, list)
        or any(
            not isinstance(name, str)
            or not name
            or name in (".", "..")
            or Path(name).name != name
            or name in before
            for name in created
        )
    ):
        raise runtime.RunnerError("Invalid eval records inventory; refusing cleanup")
    owned = (APP, *(Path(".agentic-workflow/records") / name for name in created), RESULTS)
    paths = [safe_path(root, p) for p in owned]
    # Include HEAD so staging a deletion cannot make tracked data eligible for removal.
    pathspecs = [f":(literal){p}" for p in owned]
    tracked = git(root, "ls-files", "--", *pathspecs)
    tracked += git(root, "ls-tree", "-r", "--name-only", "HEAD", "--", *(str(p) for p in owned))
    if tracked:
        raise runtime.RunnerError(f"Refusing cleanup: eval paths contain tracked files:\n{tracked}")
    for path in paths:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    print(
        "Removed apps/todolist, this eval's records directories, and .agentic-workflow/evals/todolist."
    )
    remaining = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if remaining:
        print(f"Unexpected changes retained for manual handling:\n{remaining}")
    return 0
