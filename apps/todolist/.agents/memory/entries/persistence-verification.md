# Persistence verification

TaskStore defaults to the application-root tasks.json, independent of cwd. CLI integration tests copy the package to a temporary app directory and invoke real subprocesses with PYTHONPATH from a separate cwd. This covers persistence across commands without a testing flag or writes to actual user storage. Keep detailed schema validation in business API tests.

Final assembled verification must still exercise the actual app, preserving/restoring preexisting tasks.json in a finally block. See tests/test_cli.py and repository evidence .suite/runs/006-02_cli/verify_assembled.py and assembled.md. Run tests with uv run python -m unittest discover -s tests -v from apps/todolist.
