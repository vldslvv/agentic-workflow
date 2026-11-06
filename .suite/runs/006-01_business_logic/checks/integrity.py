"""Verify frozen inputs and emit a content identity for the real candidate."""
import argparse
import hashlib
import json
from pathlib import Path
from common import identity

parser = argparse.ArgumentParser()
parser.add_argument('--app', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[4]
manifest = json.loads((Path(__file__).resolve().parents[1] / 'frozen-inventory.json').read_text())
changed = [name for name, digest in manifest['files'].items()
           if not (root / name).is_file() or hashlib.sha256((root / name).read_bytes()).hexdigest() != digest]
candidate = identity(args.app.resolve())
result = {'input_integrity': 'FAIL' if changed else 'PASS', 'changed': changed,
          'candidate_files': candidate,
          'candidate_sha256': hashlib.sha256(json.dumps(candidate, sort_keys=True).encode()).hexdigest()}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'input_integrity': result['input_integrity'], 'candidate_sha256': result['candidate_sha256'], 'changed': changed}))
raise SystemExit(bool(changed))
