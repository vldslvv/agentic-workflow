"""Grade the public CLI scenarios in specs/todolist/verification.md."""

import json

from . import runtime


# Each step specifies argv, exact stdout, and the expected exit condition.
SCENARIOS = (
    ("commands-and-persistence", "cli.md#ordered-scenario", (
        (("list",), "No tasks.\n", 0),
        (("add", "Buy milk"), "Added task 1: Buy milk\n", 0),
        (("add", "Write tests"), "Added task 2: Write tests\n", 0),
        (("list",), "1 [ ] Buy milk\n2 [ ] Write tests\n", 0),
        (("complete", "1"), "Completed task 1\n", 0),
        (("list",), "1 [x] Buy milk\n2 [ ] Write tests\n", 0),
        (("delete", "1"), "Deleted task 1\n", 0),
        (("list",), "2 [ ] Write tests\n", 0),
        (("delete", "2"), "Deleted task 2\n", 0),
        (("list",), "No tasks.\n", 0),
        (("help",), "Usage: todo <command>\nCommands:\n  add <text> [--parent <id>]\n"
         "  list\n  complete <id>\n  delete <id>\n  help\n", 0),
    )),
    ("hierarchy-and-subtree-deletion", "cli.md#hierarchy-scenario", (
        (("add", "Project"), "Added task 1: Project\n", 0),
        (("add", "Unrelated"), "Added task 2: Unrelated\n", 0),
        (("add", "Build", "--parent", "1"), "Added task 3: Build\n", 0),
        (("add", "Document", "--parent", "1"), "Added task 4: Document\n", 0),
        (("add", "Test", "--parent", "3"), "Added task 5: Test\n", 0),
        (("complete", "1"), "Completed task 1\n", 0),
        (("list",), "1 [x] Project\n  3 [ ] Build\n    5 [ ] Test\n  4 [ ] Document\n2 [ ] Unrelated\n", 0),
        (("delete", "3"), "Deleted task 3\n", 0),
        (("list",), "1 [x] Project\n  4 [ ] Document\n2 [ ] Unrelated\n", 0),
        (("delete", "1"), "Deleted task 1\n", 0),
        (("list",), "2 [ ] Unrelated\n", 0),
        (("delete", "2"), "Deleted task 2\n", 0),
        (("list",), "No tasks.\n", 0),
    )),
    ("invalid-parent-assignments", "cli.md#parent-input-checks", (
        (("add", "First"), "Added task 1: First\n", 0),
        (("add", "Second"), "Added task 2: Second\n", 0),
        (("add", "Orphan", "--parent", "999"), "", "nonzero"),
        (("list",), "1 [ ] First\n2 [ ] Second\n", 0),
        (("add", "Ambiguous", "--parent", "1", "--parent", "2"), "", "nonzero"),
        (("list",), "1 [ ] First\n2 [ ] Second\n", 0),
        (("add", "Repeated", "--parent", "1", "--parent", "1"), "", "nonzero"),
        (("list",), "1 [ ] First\n2 [ ] Second\n", 0),
    )),
)


def stored_state(path):
    """Observe persistence without prescribing the application's JSON layout."""
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError("tasks.json must be a regular file")
    return {"exists": path.exists(), "value": json.loads(path.read_bytes()) if path.exists() else None}


def grade_scenario(app, evidence, timeout, steps):
    result = {"status": "PASS", "commands": []}
    data = app / "tasks.json"
    for number, (args, expected_stdout, expected_exit) in enumerate(steps, 1):
        stdout, stderr = evidence / f"{number:02d}.stdout", evidence / f"{number:02d}.stderr"
        observed = None
        try:
            before = stored_state(data)
            observed = runtime.execute(["uv", "run", "todo", *args], app, timeout, stdout, stderr)
            observed.update(expected_stdout=expected_stdout, expected_exit=expected_exit,
                            stdout=stdout.read_bytes().decode(errors="replace"),
                            stderr=stderr.read_bytes().decode(errors="replace"))
            result["commands"].append(observed)
            if observed["status"] in ("TIMEOUT", "INTERRUPTED", "RUNNER_ERROR"):
                result["status"] = observed["status"]
                if "signal" in observed:
                    result["signal"] = observed["signal"]
                return result
            after = stored_state(data)
            observed.update(state_before=before, state_after=after)
            checks = {
                "exit": observed["returncode"] != 0 if expected_exit == "nonzero" else observed["returncode"] == expected_exit,
                "stdout": stdout.read_bytes() == expected_stdout.encode(),
            }
            if args[0] == "add" and expected_exit == 0:
                checks["tasks_json_created"] = after["exists"]
            if expected_exit == "nonzero":
                checks["state_unchanged"] = before == after
            observed.update(checks=checks, status="PASS" if all(checks.values()) else "FAIL")
            if observed["status"] == "FAIL":
                result["status"] = "FAIL"
        except (ValueError, UnicodeError) as exc:
            if observed is not None:
                observed.update(status="FAIL", error=str(exc))
            result.update(status="FAIL", error=str(exc))
            return result
    return result


def grade(app, results, timeout):
    """Run each scenario from an empty store and always restore generation data."""
    result = {"status": "FAIL", "scenarios": []}
    if not app.is_dir():
        return {**result, "error": f"Missing app directory: {app}"}
    data = app / "tasks.json"
    if data.is_symlink() or (data.exists() and not data.is_file()):
        return {**result, "error": "tasks.json must be a regular file"}
    original = data.read_bytes() if data.exists() else None
    if original is not None:
        (results / "generation-tasks.json").write_bytes(original)
    try:
        for name, source, steps in SCENARIOS:
            data.unlink(missing_ok=True)
            evidence = results / "cli" / name
            evidence.mkdir(parents=True)
            scenario = grade_scenario(app, evidence, timeout, steps)
            scenario.update(name=name, contract=f"specs/todolist/contracts/{source}")
            result["scenarios"].append(scenario)
            runtime.write_json(evidence / "result.json", scenario)
            if scenario["status"] in ("TIMEOUT", "INTERRUPTED", "RUNNER_ERROR"):
                result["status"] = scenario["status"]
                if "signal" in scenario:
                    result["signal"] = scenario["signal"]
                return result
        result["status"] = "PASS" if all(s["status"] == "PASS" for s in result["scenarios"]) else "FAIL"
        return result
    finally:
        data.unlink(missing_ok=True)
        if original is not None:
            data.write_bytes(original)
