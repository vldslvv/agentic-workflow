"""Inventory comparison and candidate identity without application imports."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reviewer", action="store_true")
    args = parser.parse_args()
    result = {}
    if args.inventory:
        inventory = json.loads(args.inventory.read_text())
        excluded = []
        observed = {}
        for name, expected in inventory["files"].items():
            if args.reviewer and (Path(name).name in {"plan.md", "implementation-order.md"}):
                excluded.append(name)
                continue
            path = Path(name)
            observed[name] = {"expected": expected, "actual": digest(path) if path.is_file() else None}
        result["integrity"] = all(x["actual"] == x["expected"] for x in observed.values())
        result["inputs"] = observed
        result["excluded_from_reviewer_access"] = excluded
    if args.candidate:
        files = {}
        for path in sorted(args.candidate.rglob("*")):
            if not path.is_file() or any(x in {".venv", "__pycache__", "build", "dist", ".pytest_cache"} or x.endswith(".egg-info") for x in path.parts):
                continue
            files[str(path.relative_to(args.candidate))] = digest(path)
        result["candidate_files"] = files
        result["candidate_sha256"] = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k in {"integrity", "candidate_sha256"}}))
    return int(result.get("integrity") is False)


if __name__ == "__main__":
    raise SystemExit(main())
