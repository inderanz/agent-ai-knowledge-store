#!/usr/bin/env python3
"""Run dependency-free repository gates used for candidate qualification."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def commands(root: Path) -> list[list[str]]:
    return [
        [sys.executable, str(root / "scripts/validate_repository.py")],
        [sys.executable, "-m", "unittest", "discover", "-s", str(root / "tests"), "-v"],
        [sys.executable, str(root / "scripts/check_sources.py"), "--offline"],
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / ".git").exists():
        print("root must be a Git repository", file=sys.stderr)
        return 2
    for command in commands(root):
        result = subprocess.run(command, cwd=root, check=False)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
