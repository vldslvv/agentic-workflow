"""Read-only checks for required suite entry points and local Markdown links."""
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


SUITE = Path(__file__).resolve().parents[1]
ROLES = ("SUPERVISOR", "PLANNER", "IMPLEMENTER", "REVIEWER", "VALIDATOR")
SKILLS = ("planner", "supervisor")


def anchors(text):
    # GitHub-style ATX heading anchors, including duplicate headings.
    used, result = {}, set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = used.get(slug, 0)
        result.add(f"{slug}-{count}" if count else slug)
        used[slug] = count + 1
    return result


def check(files):
    expected = {"AGENTS.md", "MODELS.md", "templates/project.md",
                "templates/task_order.md", "templates/tasks/task.md",
                "templates/verification.md"}
    expected.update(f"{role}.md" for role in ROLES)
    expected.update(f".agents/skills/spec-{skill}/{name}"
                    for skill in SKILLS for name in ("SKILL.md", "agents/openai.yaml"))
    errors = [f"Missing package file: {p}" for p in sorted(expected - files.keys())]
    links = 0
    documents = {name: data for name, data in files.items() if name.endswith(".md")}
    root_instructions = SUITE.parent / "AGENTS.md"
    if root_instructions.is_file():
        documents["../AGENTS.md"] = root_instructions.read_bytes()
    for name, data in documents.items():
        text = data.decode()
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if re.match(r"[\w+.-]+:", target):
                continue
            links += 1
            path, _, fragment = unquote(target).partition("#")
            destination = (SUITE / name).parent / path if path else SUITE / name
            if not destination.is_file():
                errors.append(f"Broken link in {name}: {target}")
            elif fragment and fragment not in anchors(destination.read_text()):
                errors.append(f"Missing anchor in {name}: {target}")
    for skill in SKILLS:
        prefix = f".agents/skills/spec-{skill}/"
        source = files.get(prefix + "SKILL.md", b"").decode()
        policy = files.get(prefix + "agents/openai.yaml", b"").decode()
        required = (f"name: spec-{skill}", "description:",
                    "disable-model-invocation: true", "../../../AGENTS.md",
                    f"../../../{skill.upper()}.md")
        if not all(item in source for item in required):
            errors.append(f"Invalid skill entry point: spec-{skill}")
        if "allow_implicit_invocation: false" not in policy or f"$spec-{skill}" not in policy:
            errors.append(f"Invalid invocation policy: spec-{skill}")
    shared = files.get("AGENTS.md", b"").decode()
    for role in ROLES:
        if f"]({role}.md)" not in shared:
            errors.append(f"Missing shared role entry point: {role}")
        if "](AGENTS.md)" not in files.get(f"{role}.md", b"").decode():
            errors.append(f"Missing shared-rules entry point in {role}")
    return errors, links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Deprecated compatibility option; baseline comparison was removed")
    args = parser.parse_args()
    if args.base is not None:
        print("Notice: --base is ignored; baseline comparison was removed.", file=sys.stderr)
    try:
        current = {str(p.relative_to(SUITE)): p.read_bytes() for p in SUITE.rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
        errors, links = check(current)
        print(json.dumps({"status": "FAIL" if errors else "PASS",
                          "errors": errors, "local_links_checked": links}, indent=2))
        return 1 if errors else 0
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"Package check could not complete: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
