"""POSIX process lifecycle and shared eval serialization."""

import argparse
import json
import math
import os
import signal
import subprocess
import time
from pathlib import Path
from types import FrameType
from typing import NoReturn

from .models import Execution


class RunnerError(Exception):
    pass


class Interrupted(Exception):
    def __init__(self, signum: int) -> None:
        self.signum = signum


def interrupt(signum: int, frame: FrameType | None) -> NoReturn:
    raise Interrupted(signum)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def terminate_group(process: subprocess.Popen[bytes]) -> None:
    # Ignore repeated interrupts while reaping the leader and killing descendants,
    # including a child that ignores SIGTERM after its parent exits.
    previous = {s: signal.signal(s, signal.SIG_IGN) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(process.pid, sig)
            except ProcessLookupError:
                break
            if sig == signal.SIGTERM:
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass
        process.wait()
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def execute(
    command: list[str],
    cwd: Path,
    timeout: float,
    stdout: Path,
    stderr: Path,
) -> Execution:
    started = time.monotonic()
    outcome: Execution = {"command": command, "status": "RUNNER_ERROR", "returncode": None}
    process = None
    try:
        with stdout.open("wb") as out, stderr.open("wb") as err:
            process = subprocess.Popen(
                command,
                cwd=cwd,
                stdin=subprocess.DEVNULL,
                stdout=out,
                stderr=err,
                start_new_session=True,
            )
            outcome["returncode"] = process.wait(timeout=timeout)
            outcome["status"] = "PASS" if process.returncode == 0 else "FAIL"
    except subprocess.TimeoutExpired:
        outcome["status"] = "TIMEOUT"
    except Interrupted as exc:
        outcome.update({"status": "INTERRUPTED", "signal": exc.signum})
    except OSError as exc:
        outcome["error"] = str(exc)
    finally:
        if process is not None and outcome["status"] in ("TIMEOUT", "INTERRUPTED", "RUNNER_ERROR"):
            terminate_group(process)
            outcome["returncode"] = process.returncode
        outcome["elapsed_seconds"] = time.monotonic() - started
    return outcome


def positive_seconds(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("timeout must be a positive finite number")
    return number
