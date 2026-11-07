"""Read-only suite structure checks and instruction-load comparison against a commit."""
import argparse
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote


SUITE = Path(__file__).resolve().parents[1]
ROLES = ("SUPERVISOR", "PLANNER", "IMPLEMENTER", "REVIEWER", "VALIDATOR")
SKILLS = ("planner", "supervisor")


def metrics(files):
    words = {name: len(data.decode().split())
             for name, data in files.items() if name.endswith(".md")}
    directories = {str(parent) for name in files for parent in Path(name).parents
                   if str(parent) != "."}
    return {"files": len(files), "directories": len(directories),
            "instruction_words": sum(words.values()),
            "shared_plus_role_words": {
                role: words.get("AGENTS.md", 0) + words.get(f"{role}.md", 0)
                for role in ROLES}}


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
    expected = {"AGENTS.md", "RUNNER.md", "PACKAGE_CHECKS.json", "SHA256SUMS",
                "helpers/usage_report.py", "helpers/check_package.py",
                "helpers/records.py", "helpers/trace_adapters.py", "helpers/trace_view.py", "helpers/trace_dashboard.py", "helpers/TRACING.md",
                "tests/fixtures/codex-0.167.0.jsonl", "tests/fixtures/opencode-1.2.27.json",
                "tests/test_usage_report.py", "tests/test_trace_view.py", "templates/project.md",
                "templates/task_order.md", "templates/tasks/task.md",
                "templates/verification.md"}
    expected.update(f"{role}.md" for role in ROLES)
    expected.update(f".agents/skills/spec-{skill}/{name}"
                    for skill in SKILLS for name in ("SKILL.md", "agents/openai.yaml"))
    errors = [f"Unexpected package file: {p}" for p in sorted(files.keys() - expected)]
    errors += [f"Missing package file: {p}" for p in sorted(expected - files.keys())]
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
    parser.add_argument("--base", required=True, help="Starting Git commit or ref; resolved in the report")
    args = parser.parse_args()
    try:
        def git(*arguments):
            return subprocess.check_output(["git", "-C", str(SUITE), *arguments], stderr=subprocess.PIPE)

        commit = git("rev-parse", "--verify", "--end-of-options", args.base + "^{commit}").decode().strip()
        prefix = git("rev-parse", "--show-prefix").decode().strip()
        names = git("ls-tree", "-rz", "--name-only", commit, "--", ".").decode().split("\0")
        before = {name: git("show", f"{commit}:{prefix}{name}") for name in names if name}
        if not before:
            raise ValueError("Baseline contains no suite files")
        current = {str(p.relative_to(SUITE)): p.read_bytes() for p in SUITE.rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
        errors, links = check(current)
        old, new = metrics(before), metrics(current)
        delta = {key: new[key] - old[key] for key in ("files", "directories", "instruction_words")}
        delta["shared_plus_role_words"] = {
            role: new["shared_plus_role_words"][role] - old["shared_plus_role_words"][role]
            for role in ROLES}
        growth = any(value > 0 for value in delta["shared_plus_role_words"].values()) or any(
            delta[key] > 0 for key in ("files", "directories", "instruction_words"))
        print(json.dumps({"status": "FAIL" if errors else "PASS", "base_commit": commit,
                          "errors": errors, "local_links_checked": links,
                          "method": "All package files excluding Python caches; directories exclude root; whitespace words in all Markdown, including skills/templates/runner.",
                          "before": old, "after": new, "delta": delta,
                          "added_files": sorted(current.keys() - before.keys()),
                          "removed_files": sorted(before.keys() - current.keys()),
                          "review_signals": ["Explain file or instruction growth in the maintenance review."] if growth else [],
                          "manual_review_required": "Assess behavior added, duplication, role placement and shared-plus-role sufficiency; structural PASS does not establish these."}, indent=2))
        return 1 if errors else 0
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"Package check could not complete: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
