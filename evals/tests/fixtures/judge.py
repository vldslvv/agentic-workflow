"""External Codex fixture for workflow launcher transport and failure cases."""

import json
import os
import sys
import time
from pathlib import Path

calls = Path(os.environ["JUDGE_CALLS"])
with calls.open("a") as stream:
    schema = Path(sys.argv[sys.argv.index("--output-schema") + 1])
    stream.write(
        json.dumps(
            {
                "args": sys.argv[1:],
                "cwd": os.getcwd(),
                "prompt": sys.argv[-1],
                "schema": json.loads(schema.read_text()),
            }
        )
        + "\n"
    )
print('{"type":"fixture.started"}', flush=True)
role = "EDITOR" if "summary" in json.loads(schema.read_text())["properties"] else "JUDGE"
print(f"{role.lower()} fixture stderr", file=sys.stderr, flush=True)
if role == "EDITOR":
    for relative, content in json.loads(os.environ.get("EDITOR_EDITS", "{}")).items():
        Path(relative).write_text(content)
time.sleep(float(os.environ.get(f"{role}_SLEEP", "0")))
if f"{role}_RESPONSE" in os.environ:
    output = Path(sys.argv[sys.argv.index("--output-last-message") + 1])
    output.write_text(os.environ[f"{role}_RESPONSE"])
sys.exit(int(os.environ.get(f"{role}_EXIT", "0")))
