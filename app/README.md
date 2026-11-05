# Local TODO CLI

A local, offline checklist CLI for Linux, CPython 3.14, and uv. Application code
uses only Python's standard library.

From the repository root, prepare the locked environment:

```sh
uv sync --locked --project app
uv run --project app todo --help
uv run --project app todo --file tasks.txt add "Buy milk"
uv run --project app todo --file tasks.txt list --status open
uv run --project app todo --file tasks.txt complete 1
uv run --project app todo --file tasks.txt reopen 1
uv run --project app todo --file tasks.txt edit 1 "Buy oat milk"
uv run --project app todo --file tasks.txt delete 1
```

Inside `app/`, omit `--project app`. File paths are relative to your current
working directory. After preparation, run with
`uv run --offline --no-sync --project app todo ...` for offline operation.
Build distributions with `uv build --project app`.

Tasks are editable UTF-8 records, such as `1 [ ] Buy milk` or `2 [x] Call Sam`.
IDs are unique positive ASCII decimals without leading zeros. Text is trimmed
at its edges; internal spaces and Unicode are preserved. Control characters and
U+2028/U+2029 are invalid. LF and CRLF, blank lines, and a missing final newline
are accepted. Invalid records prevent the whole operation.

`list` defaults to all tasks and accepts `--status open|done|all`. Successful
mutations print the affected record. An unknown ID fails. A missing file is an
empty list; only `add` creates it, and its parent directory must already exist.
New IDs are one above the current maximum, so deleting the highest ID permits
reuse. Duplicate descriptions are allowed.

State changes atomically replace the checklist with canonical LF records and a
final newline; an empty list is zero bytes. Reads, failures, and no-op edits or
status changes preserve existing bytes. Use one writer at a time.

Success exits 0. Data or filesystem errors exit 1; invalid command arguments
exit 2. Errors are written to stderr.
