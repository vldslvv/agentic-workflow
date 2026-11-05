"""Requirement-owned black-box acceptance for TODO-CLI, C01 through C12."""
import argparse
import errno
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from adapter import Adapter


class Checks:
    def __init__(self, app, evidence, root):
        self.adapter = Adapter(app, evidence)
        self.root = root
        self.file = root / "tasks.txt"

    def seed(self, content):
        self.file.write_bytes(content if isinstance(content, bytes) else content.encode())

    def run(self, *args, code=0, out=None, path=None, namespace=False):
        path = self.file if path is None else path
        before = path.read_bytes() if path.is_file() and os.access(path, os.R_OK) else None
        p = self.adapter.execute(["--file", str(path), *args], self.root, path, namespace)
        assert p.returncode == code, (args, p.returncode, p.stdout, p.stderr)
        if out is not None:
            assert p.stdout == out.encode(), (args, p.stdout, out)
        if code == 0:
            assert p.stderr == b"", (args, p.stderr)
        else:
            assert p.stdout == b"", (args, p.stdout)
            assert p.stderr.strip() and b"Traceback" not in p.stderr, p.stderr
            if before is not None:
                assert path.read_bytes() == before, (args, "failure changed file")
        return p

    def unchanged(self, *args, out):
        before = self.file.read_bytes()
        self.run(*args, out=out)
        assert self.file.read_bytes() == before

    def C01(self):
        assert sys.version_info[:2] == (3, 14)
        assert (self.adapter.app / "uv.lock").is_file()
        assert (self.adapter.app / "pyproject.toml").is_file()
        for args in (["--help"], *[[x, "--help"] for x in ["add", "list", "complete", "reopen", "edit", "delete"]]):
            p = self.adapter.execute(args, self.root, self.file)
            assert p.returncode == 0 and p.stdout and not p.stderr, (args, p.stderr)
            assert not self.file.exists()
        for args in [["add", "task"], ["list"], ["complete", "1"], ["reopen", "1"], ["edit", "1", "new"], ["delete", "1"]]:
            p = self.adapter.execute(args, self.root, self.file)
            assert p.returncode == 2 and not p.stdout and b"file" in p.stderr.lower()
        probe = "import socket,errno; s=socket.socket(); s.settimeout(2); result=s.connect_ex(('198.51.100.1',9)); print(result); assert result==errno.ENETUNREACH"
        p = self.adapter.execute([sys.executable, "-c", probe], self.root, offline_namespace=True, raw=True)
        assert p.returncode == 0, ("offline mechanism unavailable", p.stderr)
        relative = Path("tasks.txt")
        # Path arguments stay relative to the deliberately different caller cwd.
        for args, out in [(["add", "Offline"], "1 [ ] Offline\n"), (["list"], "1 [ ] Offline\n"), (["edit", "1", "Changed"], "1 [ ] Changed\n"), (["complete", "1"], "1 [x] Changed\n"), (["reopen", "1"], "1 [ ] Changed\n"), (["delete", "1"], "1 [ ] Changed\n")]:
            p = self.adapter.execute(["--file", str(relative), *args], self.root, self.file, True)
            assert p.returncode == 0 and p.stdout == out.encode() and not p.stderr, p
        assert self.file.read_bytes() == b""

    def C02(self):
        valid = [(b"", ""), (b" \t\r\n\n\v\n", ""), ("9 [x]  café  世界  \r\n\r\n2 [ ] internal   spaces", "9 [x] café  世界\n2 [ ] internal   spaces\n"), ("1 [ ] invisible\u200btext\n", "1 [ ] invisible\u200btext\n")]
        for content, expected in valid:
            self.seed(content)
            self.unchanged("list", out=expected)
        invalid = ["0 [ ] x", "01 [ ] x", "-1 [ ] x", "+1 [ ] x", "١ [ ] x", "1 [X] x", "1 [-] x", "1  [ ] x", "1\t[ ] x", "1 [ ]\tx", " 1 [ ] x", "1 [ ] ", "# comment", "2 [ ] duplicate", "1 [ ] a\tb", "1 [ ] a\x00b", "1 [ ] a\x7fb", "1 [ ] a\x85b", "1 [ ] a\u2028b", "1 [ ] a\u2029b", "1 [ ] a\rb", "1 [ ] \ttext"]
        operations = [("list",), ("add", "fresh"), ("complete", "2"), ("reopen", "2"), ("edit", "2", "fresh"), ("delete", "2")]
        for line in invalid:
            self.seed("2 [ ] valid\n" + line + "\n")
            for operation in operations:
                p = self.run(*operation, code=1)
                assert b"2" in p.stderr and b"line" in p.stderr.lower(), p.stderr
        self.seed(b"2 [ ] valid\n1 [ ] invalid\xff\n")
        for operation in operations:
            self.run(*operation, code=1)

    def C03(self):
        self.run("add", "  buy  café  ", out="1 [ ] buy  café\n")
        assert self.file.read_text() == "1 [ ] buy  café\n"
        self.seed("8 [x] eight\r\n\r\n2 [ ] two")
        self.run("add", "eight", out="9 [ ] eight\n")
        assert self.file.read_bytes() == b"8 [x] eight\n2 [ ] two\n9 [ ] eight\n"
        self.run("delete", "9", out="9 [ ] eight\n")
        self.run("add", "eight", out="9 [ ] eight\n")
        assert self.file.read_text().endswith("9 [ ] eight\n")

    def C04(self):
        self.seed("8 [x] done\r\n\r\n3 [ ] open\r\n2 [x] later")
        for args, expected in [((), "8 [x] done\n3 [ ] open\n2 [x] later\n"), (("--status", "all"), "8 [x] done\n3 [ ] open\n2 [x] later\n"), (("--status", "open"), "3 [ ] open\n"), (("--status", "done"), "8 [x] done\n2 [x] later\n")]:
            self.unchanged("list", *args, out=expected)
        self.seed("1 [x] done\r\n")
        self.unchanged("list", "--status", "open", out="")
        self.seed(b"")
        self.unchanged("list", out="")

    def C05(self):
        self.seed("9 [ ] first\r\n\r\n2 [ ]  middle  \r\n4 [x] last")
        self.run("complete", "2", out="2 [x] middle\n")
        assert self.file.read_bytes() == b"9 [ ] first\n2 [x] middle\n4 [x] last\n"
        self.run("reopen", "2", out="2 [ ] middle\n")
        assert self.file.read_bytes() == b"9 [ ] first\n2 [ ] middle\n4 [x] last\n"
        for command, marker in [("complete", "x"), ("reopen", " ")]:
            self.seed(f"\r\n2 [{marker}]  same  \r\n\r\n")
            self.unchanged(command, "2", out=f"2 [{marker}] same\n")

    def C06(self):
        self.seed("9 [ ] first\r\n2 [x] second\r\n4 [ ] last")
        self.run("edit", "9", "  café   世界  ", out="9 [ ] café   世界\n")
        self.run("edit", "2", "changed", out="2 [x] changed\n")
        assert self.file.read_text() == "9 [ ] café   世界\n2 [x] changed\n4 [ ] last\n"
        self.seed("\r\n2 [x]  same  \r\n")
        self.unchanged("edit", "2", " same ", out="2 [x] same\n")
        for text in ["", "   ", "a\nb", "a\tb", "a\u2028b", "a\u2029b", "a\x85b"]:
            self.run("edit", "2", text, code=2)

    def C07(self):
        self.seed("3 [ ] first\n1 [x] middle\n9 [ ] highest\n2 [ ] last\n")
        for task_id, output, remaining in [("3", "3 [ ] first\n", "1 [x] middle\n9 [ ] highest\n2 [ ] last\n"), ("9", "9 [ ] highest\n", "1 [x] middle\n2 [ ] last\n"), ("1", "1 [x] middle\n", "2 [ ] last\n"), ("2", "2 [ ] last\n", "")]:
            self.run("delete", task_id, out=output)
            assert self.file.read_text() == remaining

    def C08(self):
        self.run("list", out="")
        assert not self.file.exists()
        for operation in [("complete", "1"), ("reopen", "1"), ("edit", "1", "new"), ("delete", "1")]:
            self.run(*operation, code=1)
            assert not self.file.exists()
        self.run("add", "created", out="1 [ ] created\n")
        assert self.file.read_bytes() == b"1 [ ] created\n"
        missing = self.root / "absent" / "tasks.txt"
        self.run("add", "new", path=missing, code=1)
        assert not missing.parent.exists()

    def C09(self):
        self.seed("1 [ ] keep\n")
        for operation in [("complete", "99"), ("reopen", "99"), ("edit", "99", "new"), ("delete", "99")]:
            p = self.run(*operation, code=1)
            assert b"99" in p.stderr
        for task_id in ["0", "01", "-1", "+1", "1.0", "١", " 1", "1 ", "abc"]:
            for command in ["complete", "reopen", "edit", "delete"]:
                args = [command, task_id] + (["new"] if command == "edit" else [])
                self.run(*args, code=2)
        for args in [(), ("bogus",), ("add",), ("add", "a", "b"), ("list", "extra"), ("list", "--status", "unknown"), ("complete",), ("complete", "1", "2"), ("reopen",), ("delete",), ("edit", "1"), ("edit", "1", "a", "b")]:
            self.run(*args, code=2)
        for text in ["", " \u00a0 ", "a\nb", "a\rb", "a\tb", "a\x7fb", "a\x85b", "a\u2028b", "a\u2029b", "\ttrimmed"]:
            self.run("add", text, code=2)

    def C10(self):
        # Cross-cutting exact output assertions in C03–C09 own the mutation cases.
        # This checks the independent documented invocation form from app/.
        p = self.adapter.execute(["uv", "run", "--offline", "--no-sync", "todo", "--file", str(self.file), "add", "plain"], self.adapter.app, self.file, raw=True)
        assert p.returncode == 0 and p.stdout == b"1 [ ] plain\n" and p.stderr == b""
        self.run("list", out="1 [ ] plain\n")

    def C11(self):
        assert os.geteuid() != 0, "permission fixture requires non-root execution"
        self.seed("1 [ ] preserved\n")
        self.file.chmod(0)
        try:
            p = self.run("list", code=1)
            assert b"tasks.txt" in p.stderr
            p = self.run("add", "new", code=1)
            assert b"tasks.txt" in p.stderr
        finally:
            self.file.chmod(0o600)
        assert self.file.read_bytes() == b"1 [ ] preserved\n"
        directory = self.root / "directory"
        directory.mkdir()
        p = self.run("list", path=directory, code=1)
        assert b"directory" in p.stderr
        self.root.chmod(0o500)
        try:
            self.run("add", "new", code=1)
            self.run("add", "new", path=self.root / "new.txt", code=1)
            assert not (self.root / "new.txt").exists()
        finally:
            self.root.chmod(0o700)
        assert self.file.read_bytes() == b"1 [ ] preserved\n"

    def C12(self):
        self.run("add", "first", out="1 [ ] first\n")
        with self.file.open("rb") as previous:
            self.run("add", "second", out="2 [ ] second\n")
            assert previous.read() == b"1 [ ] first\n", "old open file changed during replacement"
            assert os.fstat(previous.fileno()).st_ino != self.file.stat().st_ino
        self.run("edit", "1", "edited", out="1 [ ] edited\n")
        self.run("complete", "1", out="1 [x] edited\n")
        self.run("list", "--status", "done", out="1 [x] edited\n")
        self.seed("8 [x] manual\r\n\r\n1 [x] edited\r\n2 [ ] second")
        self.run("reopen", "1", out="1 [ ] edited\n")
        self.run("delete", "2", out="2 [ ] second\n")
        self.run("add", "after manual", out="9 [ ] after manual\n")
        self.run("list", out="8 [x] manual\n1 [ ] edited\n9 [ ] after manual\n")
        before = self.file.read_bytes()
        self.root.chmod(0o500)
        try:
            self.run("edit", "1", "cannot persist", code=1)
        finally:
            self.root.chmod(0o700)
        assert self.file.read_bytes() == before
        assert sorted(p.name for p in self.root.iterdir()) == ["tasks.txt"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--only", choices=[f"C{i:02}" for i in range(1, 13)])
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=True)
    results = []
    for name in ([args.only] if args.only else [f"C{i:02}" for i in range(1, 13)]):
        result = {"check": name, "requirement": f"TODO-R{int(name[1:]):03}", "status": "PASS"}
        with tempfile.TemporaryDirectory(prefix=f"todo-{name}-") as directory:
            root = Path(directory)
            try:
                getattr(Checks(args.app, args.evidence / name, root), name)()
            except Exception:
                result.update(status="FAIL", traceback=traceback.format_exc())
            finally:
                root.chmod(0o700)
        results.append(result)
        print(name, result["status"], flush=True)
        if result.get("traceback"):
            print(result["traceback"], flush=True)
    (args.evidence / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    return int(any(x["status"] != "PASS" for x in results))


if __name__ == "__main__":
    raise SystemExit(main())
