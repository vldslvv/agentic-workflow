#!/usr/bin/env python3
"""Execute an explicit version-1 check manifest and retain immutable run evidence.

The manifest requires requirements, setup, checks, and cleanup arrays. Each step
requires id, argv, cwd, timeout_seconds, timeout_kind (behavioral/infrastructure),
and expected_exit_codes. Checks also require requirements and mandatory. Relative
working directories resolve from the manifest directory. No shell or environment
snapshot is used. This executes checks; it does not establish review or acceptance.
"""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone


ID = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,127}\Z")


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    # Exclusive creation protects previous evidence, including individual records.
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def identifiers(value, label, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError(f"{label} must be {'a nonempty' if nonempty else 'an'} array")
    if any(not isinstance(item, str) or not ID.fullmatch(item) for item in value):
        raise ValueError(f"{label} contains an invalid ID")
    if len(set(value)) != len(value):
        raise ValueError(f"{label} contains duplicate IDs")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def validate(manifest):
    fields = {"version", "requirements", "setup", "checks", "cleanup"}
    if not isinstance(manifest, dict) or set(manifest) != fields:
        raise ValueError("manifest requires exactly version, requirements, setup, checks, cleanup")
    if type(manifest["version"]) is not int or manifest["version"] != 1:
        raise ValueError("unsupported manifest version (expected 1)")
    identifiers(manifest["requirements"], "requirements", nonempty=True)
    declared = set(manifest["requirements"])
    covered, seen = set(), set()
    common = {"id", "argv", "cwd", "timeout_seconds", "timeout_kind", "expected_exit_codes"}
    for phase in ("setup", "checks", "cleanup"):
        if not isinstance(manifest[phase], list):
            raise ValueError(f"{phase} must be an array")
        for step in manifest[phase]:
            required = common | ({"requirements", "mandatory"} if phase == "checks" else set())
            if not isinstance(step, dict) or set(step) != required:
                raise ValueError(f"{phase} step requires exactly {', '.join(sorted(required))}")
            identifiers([step["id"]], "step ID")
            if step["id"] in seen:
                raise ValueError(f"duplicate step ID: {step['id']}")
            seen.add(step["id"])
            argv = step["argv"]
            if (not isinstance(argv, list) or not argv or not argv[0]
                    or any(not isinstance(arg, str) or "\0" in arg for arg in argv)):
                raise ValueError(f"{step['id']}: argv must be a nonempty string array without NULs")
            if not isinstance(step["cwd"], str) or not step["cwd"] or "\0" in step["cwd"]:
                raise ValueError(f"{step['id']}: cwd must be an explicit path")
            seconds = step["timeout_seconds"]
            if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds <= 0:
                raise ValueError(f"{step['id']}: timeout_seconds must be finite and positive")
            if step["timeout_kind"] not in ("behavioral", "infrastructure"):
                raise ValueError(f"{step['id']}: invalid timeout_kind")
            exits = step["expected_exit_codes"]
            if (not isinstance(exits, list) or not exits
                    or any(type(code) is not int or not 0 <= code <= 255 for code in exits)
                    or len(exits) != len(set(exits))):
                raise ValueError(f"{step['id']}: expected_exit_codes must contain unique exit codes 0..255")
            if phase == "checks":
                identifiers(step["requirements"], f"{step['id']} requirements", nonempty=True)
                if type(step["mandatory"]) is not bool:
                    raise ValueError(f"{step['id']}: mandatory must be boolean")
                if set(step["requirements"]) - declared:
                    raise ValueError(f"{step['id']}: unknown requirement mapping")
                if step["mandatory"]:
                    covered.update(step["requirements"])
    if covered != declared:
        raise ValueError("incomplete mandatory requirement mappings: " + ", ".join(sorted(declared - covered)))


class Interrupted(BaseException):
    def __init__(self, signum):
        self.signum = signum


def terminate(process):
    """Reap a process and, on POSIX, its group even if the leader has exited."""
    def send(signum):
        try:
            if os.name == "posix":
                os.killpg(process.pid, signum)
            elif process.poll() is None:
                process.terminate() if signum == signal.SIGTERM else process.kill()
        except ProcessLookupError:
            pass

    send(signal.SIGTERM)
    try:
        process.wait(timeout=0.25)
    except subprocess.TimeoutExpired:
        pass
    finally:
        send(signal.SIGKILL)
        process.wait()


def execute(step, phase, index, manifest_dir, output, cancellations):
    directory = output / "steps" / f"{phase}-{index:03d}-{step['id']}"
    directory.mkdir(parents=True)
    cwd = str((manifest_dir / step["cwd"]).resolve())
    started = timestamp()
    invocation = {**step, "phase": phase, "cwd": cwd, "started_at": started}
    save(directory / "invocation.json", invocation)
    result = {"id": step["id"], "phase": phase, "status": "BLOCKED", "started_at": started,
              "executed": False, "exit_code": None, "signal": None, "timed_out": False,
              "interrupted_by": None, "evidence": str(directory)}
    process = None
    begin = time.monotonic()
    prior_cancellations = len(cancellations) if phase == "cleanup" else 0
    with (directory / "stdout.txt").open("xb") as stdout, (directory / "stderr.txt").open("xb") as stderr:
        try:
            if len(cancellations) > prior_cancellations:
                raise Interrupted(cancellations[-1])
            process = subprocess.Popen(step["argv"], cwd=cwd, stdout=stdout, stderr=stderr,
                                       start_new_session=(os.name == "posix"))
            result["executed"] = True
            deadline = time.monotonic() + step["timeout_seconds"]
            while True:
                if len(cancellations) > prior_cancellations:
                    raise Interrupted(cancellations[-1])
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(step["argv"], step["timeout_seconds"])
                try:
                    code = process.wait(timeout=min(remaining, 0.1))
                    break
                except subprocess.TimeoutExpired:
                    continue
            result["status"] = "PASS" if code in step["expected_exit_codes"] else "FAIL"
            if result["status"] == "FAIL":
                result["reason"] = "unexpected process exit"
        except subprocess.TimeoutExpired:
            result.update(timed_out=True, timeout_seconds=step["timeout_seconds"],
                          timeout_kind=step["timeout_kind"], reason="timeout",
                          status="FAIL" if step["timeout_kind"] == "behavioral" else "BLOCKED")
        except Interrupted as error:
            result.update(interrupted_by=error.signum, reason="execution interrupted")
        except OSError as error:
            result.update(reason=f"process could not start: {error}")
        finally:
            if process is not None:
                if result["timed_out"] or result["interrupted_by"]:
                    terminate(process)
                code = process.returncode
                result["exit_code"] = code if code is not None and code >= 0 else None
                result["signal"] = -code if code is not None and code < 0 else None
            result.update(duration_seconds=time.monotonic() - begin, finished_at=timestamp())
            save(directory / "result.json", result)
    return result


def aggregate(results):
    statuses = {result["status"] for result in results}
    if "FAIL" in statuses:
        return "FAIL"
    if not statuses or statuses - {"PASS"}:
        return "BLOCKED"
    return "PASS"


def run(manifest_path, output):
    output.mkdir(parents=True, exist_ok=False)
    started = timestamp()
    save(output / "invocation.json", {"manifest": str(manifest_path), "output": str(output),
                                      "started_at": started, "version": 1})
    summary = {"version": 1, "status": "BLOCKED", "primary_status": "BLOCKED",
               "cleanup_status": "NOT_RUN", "requirements": {}, "mandatory_executed": 0,
               "steps": [], "evidence": str(output), "started_at": started}
    try:
        content = manifest_path.read_bytes()
        manifest = json.loads(content, object_pairs_hook=unique_object)
        validate(manifest)
    except (OSError, ValueError) as error:
        summary["reason"] = str(error)
    else:
        save(output / "manifest.json", manifest)
        summary["manifest_sha256"] = hashlib.sha256(content).hexdigest()
        previous = {}
        cancellations = []
        def interrupt(signum, _frame):
            # Defer handling to execution boundaries so signal delivery cannot
            # interrupt evidence writes, process creation, or cleanup bookkeeping.
            cancellations.append(signum)
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous[signum] = signal.signal(signum, interrupt)
        results, cleanup = [], []
        interrupted = False
        try:
            for phase in ("setup", "checks"):
                for index, step in enumerate(manifest[phase]):
                    if interrupted or (phase == "checks" and any(
                            row["phase"] == "setup" and row["status"] != "PASS" for row in results)):
                        result = {"id": step["id"], "phase": phase, "status": "NOT_RUN", "executed": False}
                    else:
                        result = execute(step, phase, index, manifest_path.parent, output, cancellations)
                    results.append(result)
                    interrupted = interrupted or bool(result.get("interrupted_by"))
                    if phase == "setup" and result["status"] != "PASS":
                        # Remaining setup cannot be assumed safe after failed preparation.
                        interrupted = True
            summary["primary_status"] = aggregate(results)
            if cancellations and summary["primary_status"] == "PASS":
                summary["primary_status"] = "BLOCKED"
        except Interrupted as error:
            summary["reason"] = f"execution interrupted by signal {error.signum}"
            summary["primary_status"] = "BLOCKED"
        finally:
            try:
                for index, step in enumerate(manifest["cleanup"]):
                    cleanup.append(execute(step, "cleanup", index, manifest_path.parent, output, cancellations))
            finally:
                for signum, handler in previous.items():
                    signal.signal(signum, handler)
        if cancellations:
            summary["interrupted_by"] = cancellations
        by_id = {row["id"]: row for row in results}
        for requirement in manifest["requirements"]:
            mapped = [by_id[step["id"]] for step in manifest["checks"]
                      if step["mandatory"] and requirement in step["requirements"] and step["id"] in by_id]
            summary["requirements"][requirement] = aggregate(mapped)
        summary["mandatory_executed"] = sum(bool(by_id.get(step["id"], {}).get("executed"))
                                             for step in manifest["checks"] if step["mandatory"])
        summary["cleanup_status"] = aggregate(cleanup) if cleanup else "NOT_RUN"
        summary["steps"] = results + cleanup
        summary["status"] = aggregate([{"status": summary["primary_status"]}]
                                      + cleanup + [{"status": value} for value in summary["requirements"].values()]
                                      + ([{"status": "BLOCKED"}] if cancellations else []))
        if not summary["mandatory_executed"] and summary["status"] == "PASS":
            summary["status"] = "BLOCKED"
    summary["finished_at"] = timestamp()
    save(output / "summary.json", summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", required=True, type=Path, help="new evidence directory; never overwritten")
    arguments = parser.parse_args()
    try:
        summary = run(arguments.manifest.resolve(), arguments.output.absolute())
    except OSError as error:
        print(json.dumps({"status": "BLOCKED", "reason": str(error)}))
        return 2
    print(json.dumps({key: summary[key] for key in (
        "status", "primary_status", "cleanup_status", "mandatory_executed", "requirements", "evidence")}))
    return {"PASS": 0, "FAIL": 1, "BLOCKED": 2}[summary["status"]]


if __name__ == "__main__":
    sys.exit(main())
