"""Validate the copied package, document references and local Markdown links.

No arguments checks only the package containing this helper. --integration-root
PATH also checks PATH/AGENTS.md's marked workflow block and installed optional
workflow skills; ignores other host instructions/skills.

Read-only; creates no files and starts no capture or services.

Prints JSON with status (PASS/FAIL), errors and local_links_checked. Exit 0:
checks pass; 1: validation errors; 2: invalid arguments or check could not
complete (error on stderr).

Example: python3 agentic-workflow/helpers/check_package.py --integration-root .
"""

import argparse
import ast
import importlib.util
import json
import os.path
import re
import sys
from pathlib import Path
from urllib.parse import unquote

PACKAGE = Path(__file__).resolve().parents[1]
ROLES = ("SUPERVISOR", "PLANNER", "IMPLEMENTER", "REVIEWER", "VALIDATOR")
SKILLS = ("planner", "supervisor", "acceptance")


def anchors(text: str) -> set[str]:
    # GitHub-style ATX heading anchors, including duplicate headings.
    used: dict[str, int] = {}
    result: set[str] = set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = used.get(slug, 0)
        result.add(f"{slug}-{count}" if count else slug)
        used[slug] = count + 1
    return result


def without_fences(text: str) -> str:
    # Preserve line numbers while excluding fenced examples from document checks.
    return re.sub(
        r"^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$",
        lambda match: "\n" * match[0].count("\n"),
        text,
        flags=re.M | re.S,
    )


def check_references(text: str, source: Path) -> list[str]:
    """Check package catalogs; host instructions keep their own document style."""
    errors: list[str] = []
    labels: set[str] = set()
    uses: list[tuple[int, str]] = []
    headings = 0
    catalogs = 0
    in_references = False
    for number, line in enumerate(without_fences(text).splitlines(), 1):
        location = f"{source.relative_to(PACKAGE)}:{number}"
        heading = re.fullmatch(r"#{1,6}\s+(.+?)\s*#*\s*", line)
        if heading:
            title = heading[1]
            in_references = title == "References:"
            if title.rstrip(":").lower() == "references" and not in_references:
                errors.append(f"{location}: Reference heading must be References:")
            if in_references:
                catalogs += 1
                if catalogs > 1:
                    errors.append(f"{location}: Duplicate References: section")
                if headings != 1:
                    errors.append(
                        f"{location}: References: must be the first section after the title"
                    )
            headings += 1
            continue
        if not line.strip():
            continue
        if in_references:
            entry = re.fullmatch(r"- \[([A-Z][A-Z0-9_]*)\]: (\S.*) (\S+)", line)
            if not entry:
                errors.append(f"{location}: Invalid reference entry; use - [DOC]: description path")
                continue
            label, _, target = entry.groups()
            if label in labels:
                errors.append(f"{location}: Duplicate reference [{label}]")
            labels.add(label)
            if not target.startswith(("https://", "http://")):
                path = unquote(target).partition("#")[0]
                if not path or path.startswith("/") or re.match(r"[\w+.-]+:", path) or "\\" in path:
                    errors.append(
                        f"{location}: Reference path must be project-root-relative: {target}"
                    )
        else:
            prose = re.sub(r"(`+).*?\1", "", line)
            if re.match(r"\s*(?:- )?\[[^\]]+\]:", prose):
                errors.append(f"{location}: Reference entry outside References: section")
            uses.extend(
                (number, label) for label in re.findall(r"\[([A-Z][A-Z0-9_]*)\](?![(:])", prose)
            )
    if uses and not catalogs:
        errors.append(f"{source.relative_to(PACKAGE)}: Missing References: section")
    if catalogs and not labels:
        errors.append(f"{source.relative_to(PACKAGE)}: Empty References: section")
    for number, label in uses:
        if label not in labels:
            errors.append(f"{source.relative_to(PACKAGE)}:{number}: Undefined reference [{label}]")
    return errors


def local_targets(text: str, source: Path, root: Path) -> list[str]:
    text = without_fences(text)
    targets = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
    # Reference links share a destination declared once as [NAME]: path.
    targets.extend(
        angled or bare
        for angled, bare in re.findall(
            r"^ {0,3}\[[^\]\n]+\]:[ \t]*(?:<([^>\n]+)>|(\S+))", text, re.M
        )
    )
    # Catalog entries use project-root-relative paths, unlike Markdown links.
    targets.extend(
        os.path.relpath(root / target, source.parent)
        for target in re.findall(r"^- \[[A-Z][A-Z0-9_]*\]: .+ (\S+)$", text, re.M)
        if not re.match(r"[\w+.-]+:", target)
    )
    return [target for target in targets if not re.match(r"[\w+.-]+:", target)]


def check_links(documents: dict[Path, str], boundary: Path, root: Path) -> tuple[list[str], int]:
    errors, links = [], 0
    for source, text in documents.items():
        for target in local_targets(text, source, root):
            links += 1
            path, _, fragment = unquote(target).partition("#")
            destination = (source.parent / path if path else source).resolve()
            if not destination.is_relative_to(boundary.resolve()):
                errors.append(f"Link outside copy boundary in {source.name}: {target}")
            elif not destination.is_file():
                errors.append(f"Broken link in {source.name}: {target}")
            elif fragment and fragment not in anchors(destination.read_text()):
                errors.append(f"Missing anchor in {source.name}: {target}")
    return errors, links


def check_imports(files: dict[str, bytes]) -> list[str]:
    """Check every import, including imports in inactive branches and nested functions."""
    errors: list[str] = []
    modules = {
        str(Path(name).with_suffix("")).replace("/", ".") for name in files if name.endswith(".py")
    }
    modules |= {name.removesuffix(".__init__") for name in modules if name.endswith(".__init__")}
    modules |= {name.rpartition(".")[0] for name in modules if "." in name}

    for filename, data in files.items():
        if not filename.endswith(".py"):
            continue
        try:
            tree = ast.parse(data, filename=filename)
        except SyntaxError as exc:
            errors.append(f"{filename}:{exc.lineno}: invalid Python: {exc.msg}")
            continue
        parent = str(Path(filename).parent).replace("/", ".")
        aliases: dict[str, str] = {"__import__": "__import__"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for item in node.names:
                    aliases[item.asname or item.name] = item.name
            elif isinstance(node, ast.ImportFrom) and node.module in ("importlib", "builtins"):
                for item in node.names:
                    aliases[item.asname or item.name] = f"{node.module}.{item.name}"

        def allowed(module: str, level: int = 0) -> bool:
            if level:
                parts = list(Path(filename).parent.parts)
                if level > len(parts) + 1:
                    return False
                target = ".".join(parts[: len(parts) - level + 1] + ([module] if module else []))
                return target in modules
            return (
                module.split(".")[0] in sys.stdlib_module_names
                or module in modules
                or any(local.endswith("." + module) for local in modules)
                or f"{parent}.{module}" in modules
            )

        def check_target(module: str, line: int, level: int = 0) -> None:
            if not allowed(module, level):
                errors.append(f"{filename}:{line}: prohibited import: {'.' * level}{module}")

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for item in node.names:
                    check_target(item.name, node.lineno)
            elif isinstance(node, ast.ImportFrom):
                if node.module is None:
                    for item in node.names:
                        check_target(item.name, node.lineno, node.level)
                else:
                    check_target(node.module, node.lineno, node.level)
            elif isinstance(node, ast.Call):
                function = node.func
                name = (
                    aliases.get(function.id, function.id) if isinstance(function, ast.Name) else ""
                )
                if isinstance(function, ast.Attribute) and isinstance(function.value, ast.Name):
                    name = aliases.get(function.value.id, function.value.id) + "." + function.attr
                if name not in ("__import__", "builtins.__import__", "importlib.import_module"):
                    continue
                target = (
                    node.args[0]
                    if node.args
                    else next((kw.value for kw in node.keywords if kw.arg == "name"), None)
                )
                if not isinstance(target, ast.Constant) or not isinstance(target.value, str):
                    errors.append(
                        f"{filename}:{node.lineno}: computed import target: {ast.unparse(node)}"
                    )
                    continue
                module = target.value
                if module.startswith(".") and name == "importlib.import_module":
                    package = (
                        node.args[1]
                        if len(node.args) > 1
                        else next((kw.value for kw in node.keywords if kw.arg == "package"), None)
                    )
                    if not isinstance(package, ast.Constant) or not isinstance(package.value, str):
                        errors.append(
                            f"{filename}:{node.lineno}: computed import package: {module}"
                        )
                        continue
                    try:
                        module = importlib.util.resolve_name(module, package.value)
                    except (ImportError, ValueError):
                        errors.append(
                            f"{filename}:{node.lineno}: invalid relative import: {module}"
                        )
                        continue
                level = 0
                if name in ("__import__", "builtins.__import__"):
                    level_node = (
                        node.args[4]
                        if len(node.args) > 4
                        else next((kw.value for kw in node.keywords if kw.arg == "level"), None)
                    )
                    if level_node is not None:
                        if not isinstance(level_node, ast.Constant) or not isinstance(
                            level_node.value, int
                        ):
                            errors.append(
                                f"{filename}:{node.lineno}: computed import level: {module}"
                            )
                            continue
                        level = level_node.value
                check_target(module, node.lineno, level)
    return errors


def check(files: dict[str, bytes]) -> tuple[list[str], int]:
    expected = {"README.md", "AGENTS.md", "WORKFLOW.md"}
    expected.update(f"roles/{role}.md" for role in ROLES)
    expected.update(
        f"policies/{name}.md"
        for name in (
            "BUNDLE",
            "CHECKS",
            "DOCUMENT_STYLE",
            "GUIDELINES",
            "MEMORY",
            "MODELS",
            "RECORDS",
            "RECONSTRUCTION",
        )
    )
    expected.update(f"guides/{name}.md" for name in ("WORKFLOW_REVIEW", "TRACING"))
    expected.update(
        f"templates/{name}.md"
        for name in (
            "project",
            "task_order",
            "tasks/task",
            "verification",
            "plan",
            "acceptance",
            "result",
        )
    )
    expected.update(
        f"helpers/{name}.py"
        for name in (
            "check_package",
            "records",
            "native_traces",
            "opencode_capture",
            "opencode_v2",
            "trace_adapters",
            "usage_report",
            "trace_dashboard",
            "trace_view",
        )
    )
    errors = [f"Missing package file: {p}" for p in sorted(expected - files.keys())]
    documents = {
        PACKAGE / name: data.decode() for name, data in files.items() if name.endswith(".md")
    }
    for source, text in documents.items():
        errors.extend(check_references(text, source))
    link_errors, links = check_links(documents, PACKAGE, PACKAGE.parent)
    errors.extend(link_errors)
    errors.extend(check_imports(files))
    shared = files.get("AGENTS.md", b"").decode()
    for role in ROLES:
        if f"roles/{role}.md" not in local_targets(shared, PACKAGE / "AGENTS.md", PACKAGE.parent):
            errors.append(f"Missing shared role entry point: {role}")
        if "../AGENTS.md" not in local_targets(
            files.get(f"roles/{role}.md", b"").decode(),
            PACKAGE / f"roles/{role}.md",
            PACKAGE.parent,
        ):
            errors.append(f"Missing shared-rules entry point in {role}")
    return errors, links


def check_integration(root: Path) -> tuple[list[str], int]:
    root = root.resolve()
    errors, documents = [], {}
    instructions = root / "AGENTS.md"
    text = instructions.read_text() if instructions.is_file() else ""
    start, end = "<!-- agentic-workflow:start -->", "<!-- agentic-workflow:end -->"
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) > text.index(end):
        errors.append("Missing or invalid Agentic Workflow block in root AGENTS.md")
    else:
        block = text.split(start, 1)[1].split(end, 1)[0]
        documents[instructions] = block
        for path in (
            "AGENTS.md",
            "policies/DOCUMENT_STYLE.md",
            "policies/GUIDELINES.md",
            "policies/MEMORY.md",
        ):
            if f"agentic-workflow/{path}" not in local_targets(block, instructions, root):
                errors.append(f"Missing root entry point: {Path(path).stem}")
    for skill in SKILLS:
        name = f"agentic-workflow-{skill}"
        directory = root / ".agents/skills" / name
        if not directory.exists():
            continue
        source = directory / "SKILL.md"
        policy = directory / "agents/openai.yaml"
        content = source.read_text() if source.is_file() else ""
        invocation = policy.read_text() if policy.is_file() else ""
        required = (f"name: {name}", "description:", "disable-model-invocation: true")
        targets = local_targets(content, source, root)
        references = (
            ["AGENTS.md", "roles/PLANNER.md", "roles/SUPERVISOR.md"]
            if skill == "acceptance"
            else ["AGENTS.md", f"roles/{skill.upper()}.md"]
        )
        if not all(item in content for item in required) or not all(
            f"../../../agentic-workflow/{ref}" in targets for ref in references
        ):
            errors.append(f"Invalid skill entry point: {name}")
        if "allow_implicit_invocation: false" not in invocation or f"${name}" not in invocation:
            errors.append(f"Invalid invocation policy: {name}")
        documents[source] = content
    link_errors, links = check_links(documents, root, root)
    return errors + link_errors, links


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--integration-root",
        type=Path,
        help="Also check the marked root AGENTS.md block and installed optional skills",
    )
    args = parser.parse_args()
    try:
        current = {
            str(p.relative_to(PACKAGE)): p.read_bytes()
            for p in PACKAGE.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
        }
        errors, links = check(current)
        if args.integration_root is not None:
            integration_errors, integration_links = check_integration(args.integration_root)
            errors.extend(integration_errors)
            links += integration_links
        print(
            json.dumps(
                {
                    "status": "FAIL" if errors else "PASS",
                    "errors": errors,
                    "local_links_checked": links,
                },
                indent=2,
            )
        )
        return 1 if errors else 0
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"Package check could not complete: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
