from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "registry-lock.json"
SOURCE_REPOSITORY = "https://github.com/NeoCognitus70/portfolio-prompts"
SOURCE_PATH = "registry.yml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lock canonical portfolio fields from an exact commit.")
    parser.add_argument("--repository", type=Path, required=True, help="Local portfolio-prompts checkout.")
    parser.add_argument("--commit", required=True, help="Full or abbreviated commit to lock.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def git(repository: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


def build_lock(repository: Path, commit: str) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required; install requirements-dev.txt") from exc

    full_commit = git(repository, "rev-parse", f"{commit}^{{commit}}")
    registry_text = git(repository, "show", f"{full_commit}:{SOURCE_PATH}")
    data = yaml.safe_load(registry_text)
    projects = []
    for row in data["projects"]:
        projects.append(
            {
                "project": row["project"],
                "github": row["github"],
                "presentation_role": row["presentation_role"],
            }
        )
    projects.sort(key=lambda row: row["project"])
    return {
        "schemaVersion": 1,
        "source": {
            "repository": SOURCE_REPOSITORY,
            "commit": full_commit,
            "path": SOURCE_PATH,
        },
        "projects": projects,
    }


def main() -> int:
    args = parse_args()
    try:
        lock = build_lock(args.repository.resolve(), args.commit)
    except (KeyError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"lock-registry: ERROR — {exc}", file=sys.stderr)
        return 2
    output = (json.dumps(lock, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output)
    print(f"lock-registry: wrote {args.output} at {lock['source']['commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
