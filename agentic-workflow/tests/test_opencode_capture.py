"""Capture through public commands with a local export CLI fixture.

The fixture replaces only OpenCode's export process; selection, persistence,
refresh and reporting are real. A live CLI smoke check is separate.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "helpers"))
from tracing.opencode.types import OpenCode
from usage_report import refresh

FIXTURE = Path(__file__).parent / "fixtures/opencode-2.2.6.json"

HELPERS = Path(__file__).resolve().parents[1] / "helpers"


class OpenCodeCaptureTests(unittest.TestCase):
    def test_capture_refresh_resume_and_export_failure_preserve_selected_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            host = base / "host.json"
            data = json.loads(FIXTURE.read_text())
            tag = 'AGENTIC_WORKFLOW {"implementation":"001_demo","task":"orchestration","role":"supervisor"}'
            data["messages"][2]["text"] = "Implement demo"
            data["messages"][3]["content"][0]["text"] = tag
            # Assignment examples inside tool output are not self-identification.
            data["messages"][3]["content"][1]["state"]["content"][0]["text"] = (
                'AGENTIC_WORKFLOW {"implementation":"001_demo","task":"wrong","role":"reviewer"}'
            )
            steering = dict(
                id="msg_steer", type="user", text="Also check errors", time=dict(created=3200)
            )
            data["messages"].insert(3, steering)
            active = dict(data, messages=data["messages"][:4])
            host.write_text(json.dumps(active))
            binary = base / "opencode"
            binary.write_text(
                "#!" + sys.executable + "\nimport pathlib, sys\n"
                'assert sys.argv[1:] == ["session", "export", "ses_fixture"]\n'
                "print(pathlib.Path(" + repr(str(host)) + ").read_text())\n"
            )
            binary.chmod(0o755)
            with patch.dict(
                os.environ,
                PATH=str(base) + os.pathsep + os.environ["PATH"],
                OPENCODE_SESSION_ID="ses_fixture",
                CODEX_THREAD_ID="",
            ):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(HELPERS / "records.py"),
                        "allocate",
                        "demo",
                        "--records-root",
                        str(base / "records"),
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                root = Path(result.stdout.strip())
                snapshot = root / "native/ses_fixture/msg_current.json"
                self.assertTrue(snapshot.is_file(), result.stderr)
                pending = refresh(root, "opencode").usage
                self.assertIsNone(pending["summary"]["tokens"]["total_tokens"]["total"])
                self.assertIn("unfinished_turn", pending["summary"]["coverage"])
                host.write_text(json.dumps(data))
                report = refresh(root, "opencode").usage
                self.assertEqual(report["summary"]["tokens"]["total_tokens"]["total"], 75)
                self.assertEqual(report["summary"]["tokens"]["reasoning_output_tokens"]["total"], 5)
                self.assertEqual(report["assignments"][0]["role"], "supervisor")
                self.assertEqual(report["assignments"][0]["task_id"], "orchestration")
                self.assertEqual(report["summary"]["observed_tool_calls"], 1)
                self.assertEqual(report["summary"]["outcomes"], {"completed": 1})
                self.assertEqual(
                    {s["session_id"] for s in report["native_sources"]}, {"ses_fixture"}
                )
                # Refresh includes new observations in the selected turn, but no new user turn.
                new_turn = [
                    dict(id="msg_next", type="user", text="Unrelated", time=dict(created=7000))
                ]
                data["messages"] += new_turn
                host.write_text(json.dumps(data))
                self.assertEqual(
                    refresh(root, "opencode").usage["summary"]["tokens"]["total_tokens"]["total"],
                    75,
                )
                saved = json.loads(snapshot.read_text())
                self.assertEqual(
                    [m["id"] for m in saved["messages"]],
                    ["msg_current", "msg_steer", "msg_step", "msg_idle"],
                )
                before = snapshot.read_bytes()
                host.write_text("invalid JSON")
                failed = refresh(root, "opencode").usage
                self.assertEqual(snapshot.read_bytes(), before)
                self.assertIn("opencode_export_unavailable", failed["summary"]["coverage"])
                self.assertIsNone(failed["summary"]["tokens"]["total_tokens"]["total"])
                self.assertEqual(failed["summary"]["tokens"]["total_tokens"]["known_subtotal"], 75)
                host.write_text(json.dumps(data))
                (root / "tasks/work").mkdir()
                result = subprocess.run(
                    [sys.executable, str(HELPERS / "records.py"), "resolve", str(root), "work"],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((root / "native/ses_fixture/msg_next.json").is_file())
                resumed = refresh(root, "opencode").usage
                self.assertNotIn("missing_assignment", resumed["summary"]["coverage"])
                self.assertEqual(len(resumed["assignments"]), 1)
                self.assertEqual(
                    set(resumed["assignments"][0]["turns"]), {"msg_current", "msg_next"}
                )

    def test_dispatch_selects_only_child_turn_with_matching_parent_and_call_time(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "001_demo"
            data = json.loads(FIXTURE.read_text())
            task = data["messages"][3]["content"][1]
            task.update(name="subagent")
            task["state"]["metadata"] = dict(sessionID="ses_child")
            task["state"]["input"] = dict(prompt=data["messages"][2]["text"])
            child = json.loads(FIXTURE.read_text())
            child["info"].update(id="ses_child", parentID="ses_fixture")
            child["messages"][2]["time"]["created"] = 4200
            child["messages"][3]["time"]["created"] = 4300
            (base / "ses_fixture.json").write_text(json.dumps(data))
            (base / "ses_child.json").write_text(json.dumps(child))
            snapshot = root / "native/ses_fixture/msg_current.json"
            snapshot.parent.mkdir(parents=True)
            data["messages"] = data["messages"][2:]
            snapshot.write_text(json.dumps(data))
            binary = base / "opencode"
            binary.write_text(
                "#!" + sys.executable + "\nimport pathlib, sys\n"
                'assert sys.argv[1:3] == ["session", "export"]\n'
                "print((pathlib.Path("
                + repr(str(base))
                + ') / (sys.argv[3] + ".json")).read_text())\n'
            )
            binary.chmod(0o755)
            with patch.dict(os.environ, PATH=str(base) + os.pathsep + os.environ["PATH"]):
                report = refresh(root, "opencode").usage
                self.assertEqual(report["summary"]["tokens"]["total_tokens"]["total"], 150)
                self.assertTrue((root / "native/ses_child/msg_current.json").exists())
                self.assertFalse((root / "native/ses_child/msg_old.json").exists())
                child["info"].update(id="ses_stranger", parentID="ses_elsewhere")
                (base / "ses_stranger.json").write_text(json.dumps(child))
                task["state"]["metadata"]["sessionID"] = "ses_stranger"
                (base / "ses_fixture.json").write_text(json.dumps(data))
                report = refresh(root, "opencode").usage
                self.assertIn("opencode_parent_mismatch", report["summary"]["coverage"])
                self.assertFalse((root / "native/ses_stranger").exists())


def prompt(mid: str, time: int, text: str) -> OpenCode:
    return dict(id=mid, type="user", time=dict(created=time), text=text)


def idle(mid: str, time: int) -> OpenCode:
    return dict(id=mid, type="idle", time=dict(created=time), outcome="succeeded")


def step(mid: str, time: int, *tools: OpenCode) -> OpenCode:
    return dict(
        id=mid,
        type="assistant",
        time=dict(
            created=time, completed=max([time + 10] + [t["time"]["completed"] for t in tools])
        ),
        model=dict(id="fixture", providerID="openai"),
        tokens=dict(input=10, output=2, reasoning=0, cache=dict(read=0, write=0)),
        content=list(tools),
    )


def dispatch(cid: str, time: int, child: str, text: str) -> OpenCode:
    return dict(
        id=cid,
        type="tool",
        name="subagent",
        time=dict(created=time, ran=time, completed=time + 1),
        state=dict(status="completed", metadata=dict(sessionID=child), input=dict(prompt=text)),
    )


def notice(mid: str, time: int, child: str) -> OpenCode:
    return dict(
        id=mid,
        type="synthetic",
        time=dict(created=time),
        metadata=dict(source="subagent", childID=child),
        text='Quoted child output:\nAGENTIC_WORKFLOW {"implementation":"001_demo","task":"wrong","role":"reviewer"}',
    )


class ContinuationCaptureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "001_demo"
        binary = self.base / "opencode"
        binary.write_text(
            "#!" + sys.executable + "\nimport pathlib, sys\n"
            'assert sys.argv[1:3] == ["session", "export"]\n'
            "print((pathlib.Path("
            + repr(str(self.base))
            + ') / (sys.argv[3] + ".json")).read_text())\n'
        )
        binary.chmod(0o755)
        env = patch.dict(os.environ, PATH=str(self.base) + os.pathsep + os.environ["PATH"])
        env.start()
        self.addCleanup(env.stop)

    def host(self, sid: str, messages: list[OpenCode], parent: str | None = None) -> None:
        info: OpenCode = dict(id=sid)
        if parent:
            info["parentID"] = parent
        (self.base / (sid + ".json")).write_text(json.dumps(dict(info=info, messages=messages)))

    def seed(self, sid: str, messages: list[OpenCode]) -> Path:
        path = self.root / "native" / sid / (messages[0]["id"] + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(dict(info=dict(id=sid), messages=messages)))
        return path

    def test_background_chain_recovers_five_agents_and_one_span_per_session(self) -> None:
        tag = 'AGENTIC_WORKFLOW {"implementation":"001_demo","task":"orchestration","role":"supervisor"}'
        first = [
            prompt("root", 1000, tag),
            step(
                "r1",
                1100,
                dispatch("business", 1101, "business", "Implement business"),
                dispatch("cli", 1102, "cli", "Implement CLI"),
            ),
            idle("i1", 1200),
        ]
        rest = [
            notice("business_done", 2000, "business"),
            step("r2", 2100, dispatch("review", 2101, "review", "Review")),
            idle("i2", 2200),
            notice("review_done", 3000, "review"),
            step("r3", 3100, dispatch("fix", 3101, "business", "Fix")),
            idle("i3", 3200),
            notice("fixed", 4000, "business"),
            step("r4", 4100),
            idle("i4", 4200),
            notice("cli_done", 5000, "cli"),
            step("r5", 5100, dispatch("validate", 5101, "validator", "Validate")),
            idle("i5", 5200),
            notice("validated", 6000, "validator"),
            step("r6", 6100),
            idle("i6", 6200),
        ]
        self.host(
            "root",
            first
            + rest
            + [
                prompt("unrelated", 7000, "Other work"),
                idle("unrelated_idle", 7050),
                notice("late", 7100, "business"),
                step("excluded", 7200),
                idle("i7", 7300),
            ],
        )
        self.seed("root", first)
        self.host(
            "business",
            [
                prompt(
                    "b1", 1105, "You are a subagent spawned by another session.\nImplement business"
                ),
                step("bs1", 1300),
                idle("bi1", 1900),
                prompt("b2", 3105, "Fix"),
                step("bs2", 3300),
                idle("bi2", 3900),
            ],
            "root",
        )
        for sid, text, start, end in [
            ("cli", "Implement CLI", 1106, 4900),
            ("review", "Review", 2105, 2900),
            ("validator", "Validate", 5105, 5900),
        ]:
            self.host(
                sid,
                [prompt(sid, start, text), step(sid + "s", start + 10), idle(sid + "i", end)],
                "root",
            )
        bundle = refresh(self.root, "opencode")
        self.assertEqual(
            {s["session_id"] for s in bundle.usage["native_sources"]},
            {"root", "business", "cli", "review", "validator"},
        )
        self.assertEqual(bundle.usage["summary"]["observed_model_measurements"], 11)
        self.assertEqual(bundle.usage["summary"]["tokens"]["total_tokens"]["total"], 132)
        root_assignment = next(
            a for a in bundle.usage["assignments"] if a["agent_id"] == "opencode:root"
        )
        self.assertEqual(root_assignment["role"], "supervisor")
        self.assertEqual(len(root_assignment["turns"]), 6)
        bars = [
            e
            for e in json.loads(bundle.files["timeline.json"])["traceEvents"]
            if e.get("cat") == "agent" and e["ph"] in ("X", "B")
        ]
        self.assertEqual(len(bars), 5)
        bar = next(e for e in bars if e["args"]["agent_id"] == "opencode:root")
        self.assertEqual((bar["ts"], bar["dur"]), (1000000, 5200000))
        self.assertEqual(len(bar["args"]["turn_ids"]), 6)
        self.assertEqual(refresh(self.root, "opencode").usage, bundle.usage)
        self.assertFalse((self.root / "native/root/unrelated.json").exists())
        self.assertFalse((self.root / "native/root/late.json").exists())

    def test_dispatch_delivery_matching_and_retry(self) -> None:
        for scenario in ("late", "foreground", "steering", "missing", "ambiguous", "wrong_parent"):
            with self.subTest(scenario=scenario):
                self.root = self.base / scenario / "001_demo"
                call = dispatch("call", 100, "child", "Do work")
                if scenario == "foreground":
                    call["time"]["completed"] = 200
                parent = [prompt("root", 90, "Start"), step("r", 100, call), idle("ri", 300)]
                child = [prompt("child", 104, "Do work"), step("c", 110), idle("ci", 190)]
                if scenario == "steering":
                    child.insert(0, prompt("active", 50, "Earlier task"))
                if scenario == "missing":
                    child[0]["text"] = "Other work"
                if scenario == "ambiguous":
                    child.insert(1, prompt("repeat", 105, "Do work"))
                self.seed("root", parent)
                self.host("root", parent)
                self.host("child", child, "other" if scenario == "wrong_parent" else "root")
                report = refresh(self.root, "opencode").usage
                if scenario in ("missing", "ambiguous", "wrong_parent"):
                    code = {
                        "missing": "opencode_dispatch_unresolved",
                        "ambiguous": "ambiguous_dispatch_turn",
                        "wrong_parent": "opencode_parent_mismatch",
                    }[scenario]
                    self.assertIn(code, report["summary"]["coverage"])
                    self.assertFalse((self.root / "native/child").exists())
                    self.host("child", [prompt("retry", 104, "Do work"), idle("done", 200)], "root")
                    self.assertTrue(
                        any(
                            s["session_id"] == "child"
                            for s in refresh(self.root, "opencode").usage["native_sources"]
                        )
                    )
                else:
                    tid = "active" if scenario == "steering" else "child"
                    self.assertTrue((self.root / "native/child" / (tid + ".json")).exists())

    def test_shell_continuation_partial_exports_and_unresolved_notifications(self) -> None:
        shell: OpenCode = dict(
            id="shell",
            type="tool",
            name="shell",
            time=dict(created=110, completed=120),
            state=dict(
                status="completed",
                input=dict(command="true", background=True),
                metadata=dict(shellID="sh_1"),
            ),
        )
        first = [prompt("root", 100, "Run"), step("r", 110, shell), idle("idle", 200)]
        completion = notice("shell_done", 300, "")
        completion["metadata"] = dict(source="shell", shellID="sh_1")
        rest = [completion, step("r2", 310)]
        self.seed("root", first)
        self.host("root", first + rest)
        bundle = refresh(self.root, "opencode")
        self.assertIn("unfinished_turn", bundle.usage["summary"]["coverage"])
        bars = [
            e
            for e in json.loads(bundle.files["timeline.json"])["traceEvents"]
            if e.get("cat") == "agent" and e["ph"] in ("B", "X")
        ]
        self.assertEqual([(e["ph"], e["ts"]) for e in bars], [("B", 100000)])
        selected = self.root / "native/root/shell_done.json"
        before = selected.read_bytes()
        self.host("root", first + [completion])
        partial = refresh(self.root, "opencode").usage
        self.assertEqual(selected.read_bytes(), before)
        self.assertIn("opencode_turn_unavailable", partial["summary"]["coverage"])
        self.host("root", first + rest + [idle("done", 400), notice("unknown", 500, "stranger")])
        report = refresh(self.root, "opencode").usage
        self.assertIn("opencode_continuation_unresolved", report["summary"]["coverage"])
        self.assertFalse((self.root / "native/root/unknown.json").exists())
        manual = self.root / "native/manual.json"
        manual.write_bytes(selected.read_bytes())
        (self.base / "root.json").write_text("invalid")
        report = refresh(self.root, "opencode").usage
        self.assertEqual(manual.read_bytes(), selected.read_bytes())
        self.assertIn("opencode_export_unavailable", report["summary"]["coverage"])


if __name__ == "__main__":
    unittest.main()
