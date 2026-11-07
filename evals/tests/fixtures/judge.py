"""External Codex fixture for workflow launcher transport and failure cases."""
import json
import os
from pathlib import Path
import sys
import time


calls = Path(os.environ["JUDGE_CALLS"])
with calls.open("a") as stream:
    stream.write(json.dumps({"args": sys.argv[1:], "cwd": os.getcwd()}) + "\n")
print('{"type":"fixture.started"}', flush=True)
print("judge fixture stderr", file=sys.stderr, flush=True)
time.sleep(float(os.environ.get("JUDGE_SLEEP", "0")))
if "JUDGE_RESPONSE" in os.environ:
    output = Path(sys.argv[sys.argv.index("--output-last-message") + 1])
    output.write_text(os.environ["JUDGE_RESPONSE"])
sys.exit(int(os.environ.get("JUDGE_EXIT", "0")))
