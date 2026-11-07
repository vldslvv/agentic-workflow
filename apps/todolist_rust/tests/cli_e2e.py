"""Real public CLI/API/PostgreSQL contracts; owns and cleans a unique compose project."""
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
import uuid


def main():
    source = Path(__file__).resolve().parents[1]
    project_name = "todo-test-" + uuid.uuid4().hex[:12]
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = dict(os.environ, TODO_DB_PORT=str(port))
    url = f"postgres://todo:todo@127.0.0.1:{port}/todo"
    env["DATABASE_URL"] = url
    compose = ["docker", "compose", "-p", project_name, "-f", str(source / "compose.yaml")]

    def docker(*args, capture=False):
        return subprocess.run(compose + list(args), env=env, check=True,
                              capture_output=capture, text=True).stdout

    def sql(query, database="todo"):
        return docker("exec", "-T", "db", "psql", "-U", "todo", "-d", database,
                      "-At", "-v", "ON_ERROR_STOP=1", "-c", query, capture=True).strip()

    try:
        docker("up", "-d", "--wait", "db")
        print(f"Ready: owned compose project {project_name}, port {port}", flush=True)
        with tempfile.TemporaryDirectory(prefix="todo-cli-") as directory:
            root = Path(directory)
            project = root / "project"
            project.mkdir()
            for filename in ("Cargo.toml", "Cargo.lock"):
                shutil.copy2(source / filename, project / filename)
            for folder in ("src", "tests", "examples"):
                shutil.copytree(source / folder, project / folder)
            invocation = root / "invocation"
            invocation.mkdir()
            # A stale JSON file must be ignored, even if malformed.
            storage = project / "tasks.json"
            storage.write_text("unrelated malformed JSON; preserve me")
            cargo = ["cargo", "--offline", "--manifest-path"]
            # Cargo's manifest option belongs to each subcommand.
            def cargo_run(command, *args, database="todo"):
                test_env = dict(env, DATABASE_URL=url.rsplit("/", 1)[0] + "/" + database)
                subprocess.run([cargo[0], command, cargo[1], cargo[2], str(project / "Cargo.toml"),
                                "--target-dir", str(source / "target"), *args],
                               env=test_env, cwd=invocation, check=True)
            sql("CREATE DATABASE api_contract")
            cargo_run("test", database="api_contract")
            sql("CREATE DATABASE example_contract")
            cargo_run("run", "--example", "lifecycle", database="example_contract")
            cargo_run("build")
            binary = source / "target" / "debug" / "todolist_rust"

            def run(args, status=0, contains=None, selected_url=url):
                result = subprocess.run([os.fsencode(binary), *args], cwd=invocation,
                                        env=dict(env, DATABASE_URL=selected_url),
                                        capture_output=True, timeout=12)
                stdout, stderr = result.stdout.decode(), result.stderr.decode()
                assert result.returncode == status, (args, result.returncode, stdout, stderr)
                output = stdout if status == 0 else stderr
                assert not (stderr if status == 0 else stdout), (args, stdout, stderr)
                assert output.strip(), args
                if contains is not None:
                    assert contains in output, (args, output, contains)
                assert storage.read_text() == "unrelated malformed JSON; preserve me"
                assert not (invocation / "tasks.json").exists()
                print(f"{args!r}: exit {status}; {output.strip()!r}", flush=True)
                return stdout

            def rows():
                return json.loads(sql('SELECT coalesce(json_agg(t ORDER BY id), \'[]\') FROM tasks t'))

            def snapshot():
                return (rows(), sql("SELECT last_value, is_called FROM tasks_id_seq"))

            def stamp(value):
                return dt.datetime.fromisoformat(value)

            def changed(before, after, status, earliest):
                for key in ("id", "description", "added"):
                    assert after[key] == before[key], (before, after)
                assert after["status"] == status
                assert stamp(after["update"]) > stamp(before["update"])
                assert earliest <= stamp(after["update"]) <= dt.datetime.now(dt.timezone.utc)

            assert run(["list"]) == "No tasks.\n"
            columns = json.loads(sql("SELECT json_agg(x ORDER BY ordinal_position) FROM (SELECT column_name, data_type, is_nullable, is_identity, ordinal_position FROM information_schema.columns WHERE table_schema='public' AND table_name='tasks') x"))
            assert [(c["column_name"], c["data_type"], c["is_nullable"]) for c in columns] == [
                ("id", "integer", "NO"), ("description", "text", "NO"),
                ("added", "timestamp with time zone", "NO"),
                ("update", "timestamp with time zone", "NO"), ("status", "USER-DEFINED", "NO")]
            assert columns[0]["is_identity"] == "YES"
            assert sql("SELECT string_agg(e.enumlabel, ',' ORDER BY e.enumsortorder) FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid WHERE t.typname='task_status'") == "Completed,New,Deleted"
            assert sql("SELECT count(*) FROM pg_constraint WHERE conrelid='tasks'::regclass AND contype='p'") == "1"
            print("Schema:", columns, "enum=Completed,New,Deleted; primary key present", flush=True)
            start = dt.datetime.now(dt.timezone.utc)
            run(["add", "Buy milk"], contains="1")
            run(["add", "-urgent"], contains="2")
            initial = rows()
            assert [(r["id"], r["description"], r["status"]) for r in initial] == [(1, "Buy milk", "New"), (2, "-urgent", "New")]
            for row in initial:
                assert row["added"] == row["update"]
                assert start <= stamp(row["added"]) <= dt.datetime.now(dt.timezone.utc)
            assert run(["list"]) == "1 [ ] Buy milk\n2 [ ] -urgent\n"
            time.sleep(0.02)
            start = dt.datetime.now(dt.timezone.utc)
            run(["complete", "1"], contains="1")
            completed = rows()
            changed(initial[0], completed[0], "Completed", start)
            assert completed[1] == initial[1]
            assert run(["list"]) == "1 [x] Buy milk\n2 [ ] -urgent\n"
            run(["complete", "1"], contains="1")
            assert rows() == completed
            time.sleep(0.02)
            start = dt.datetime.now(dt.timezone.utc)
            run(["delete", "2"], contains="2")
            deleted_b = rows()
            changed(completed[1], deleted_b[1], "Deleted", start)
            assert run(["list"]) == "1 [x] Buy milk\n"
            time.sleep(0.02)
            start = dt.datetime.now(dt.timezone.utc)
            run(["delete", "1"], contains="1")
            changed(completed[0], rows()[0], "Deleted", start)
            assert run(["list"]) == "No tasks.\n"
            for identifier, description in ((3, "C"), (4, ""), (5, "  spaced  "), (6, 'Quoted "café"')):
                run(["add", description], contains=str(identifier))
            assert [(r["id"], r["description"]) for r in rows()[2:]] == [(3, "C"), (4, ""), (5, "  spaced  "), (6, 'Quoted "café"')]
            assert run(["list"]) == '3 [ ] C\n4 [ ] \n5 [ ]   spaced  \n6 [ ] Quoted "café"\n'
            before = snapshot()
            for args in ([], ["help"], ["-h"], ["--help"]):
                output = run(args)
                for phrase in ("add <description>", "delete <id>", "complete <id>", "list", "help", "quote", "PostgreSQL", "DATABASE_URL", "2147483647", "[ ]", "[x]"):
                    assert phrase in output, (args, phrase)
            invalid = [["unknown"], ["--unknown"], ["add"], ["add", "a", "b"], ["list", "extra"], ["help", "extra"], ["-h", "extra"], ["--help", "extra"]]
            for command in ("complete", "delete"):
                invalid.extend([[command], [command, "1", "2"]])
                invalid.extend([[command, value] for value in ("", "-1", "+1", "1a", "1.0", " 1", "١", "2147483648")])
            if os.name == "posix":
                invalid.extend([[b"\xff"], ["add", b"\xff"]])
            for args in invalid:
                run(args, 2, "help")
            for command in ("complete", "delete"):
                for identifier in ("0", "999", "2147483647", "1", "2"):
                    run([command, identifier], 1, "does not exist")
            assert snapshot() == before
            run(["complete", "0003"], contains="3")
            assert rows()[2]["status"] == "Completed"
            before = snapshot()
            print("Pre-outage snapshot:", before, flush=True)
            docker("stop", "db")
            outage = [["add", "must not save"], ["list"], ["complete", "3"], ["delete", "3"], [], ["help"], ["-h"], ["--help"], *invalid]
            for args in outage:
                run(args, 1, "database")
            run(["help"], 1, "database", "postgres://todo:todo@127.0.0.1:1/todo")
            docker("start", "--wait", "db")
            assert snapshot() == before
            assert "3 [x] C" in run(["list"])
            run(["complete", "4"], contains="4")
            run(["add", "After restart"], contains="7")
            assert rows()[-1]["id"] == 7
            print("Restart retained rows/timestamps/sequence; next ID=7", flush=True)
            sql("CREATE DATABASE incompatible")
            sql("CREATE TABLE tasks (id integer PRIMARY KEY, preserved text); INSERT INTO tasks VALUES (42, 'keep')", "incompatible")
            run(["help"], 1, "database", url.rsplit("/", 1)[0] + "/incompatible")
            assert sql("SELECT * FROM tasks", "incompatible") == "42|keep"
            assert sql("SELECT count(*) FROM information_schema.columns WHERE table_name='tasks'", "incompatible") == "2"
            # Same column names are insufficient: status must be the native enum.
            sql("CREATE DATABASE incompatible_type")
            sql('CREATE TABLE tasks (id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY, description text NOT NULL, added timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP, "update" timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP, status text NOT NULL DEFAULT \'New\'); INSERT INTO tasks (description) VALUES (\'keep typed row\')', "incompatible_type")
            def incompatible_snapshot():
                return (sql("SELECT json_agg(t ORDER BY id) FROM tasks t", "incompatible_type"),
                        sql("SELECT last_value, is_called FROM tasks_id_seq", "incompatible_type"),
                        sql("SELECT data_type FROM information_schema.columns WHERE table_name='tasks' AND column_name='status'", "incompatible_type"))
            original = incompatible_snapshot()
            for args in (["help"], ["add", "must not write"]):
                run(args, 1, "incompatible", url.rsplit("/", 1)[0] + "/incompatible_type")
                assert incompatible_snapshot() == original
            # Creation owns its initial state and instant, regardless of stored defaults.
            sql("CREATE DATABASE creation_defaults")
            sql('CREATE TYPE task_status AS ENUM (\'Completed\', \'New\', \'Deleted\'); CREATE TABLE tasks (id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY, description text NOT NULL, added timestamptz NOT NULL DEFAULT \'2000-01-01 UTC\', "update" timestamptz NOT NULL DEFAULT \'2001-01-01 UTC\', status task_status NOT NULL DEFAULT \'Deleted\')', "creation_defaults")
            start = dt.datetime.now(dt.timezone.utc)
            defaults_url = url.rsplit("/", 1)[0] + "/creation_defaults"
            run(["add", "Explicit creation state"], contains="1", selected_url=defaults_url)
            created = json.loads(sql("SELECT row_to_json(t) FROM tasks t", "creation_defaults"))
            assert (created["id"], created["description"], created["status"]) == (1, "Explicit creation state", "New")
            assert created["added"] == created["update"]
            assert start <= stamp(created["added"]) <= dt.datetime.now(dt.timezone.utc)
            assert run(["list"], selected_url=defaults_url) == "1 [ ] Explicit creation state\n"
            print("PASS: real API, example, CLI lifecycle/schema/timestamps/errors/outage/restart; incompatible data preserved; creation invariants independent of defaults", flush=True)
    finally:
        docker("down", "-v", "--remove-orphans")
        print(f"Cleaned only owned project {project_name}", flush=True)


if __name__ == "__main__":
    main()
