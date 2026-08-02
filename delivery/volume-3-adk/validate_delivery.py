#!/usr/bin/env python3
"""Fail-closed static validation for the Volume 3 Cloud Build definition."""

from pathlib import Path
import sys


REQUIRED = (
    "CLOUD_LOGGING_ONLY",
    "google-adk==2.6.1",
    "--no-cache-dir",
    "test_adk_graph.py",
    "evaluate_release.py",
    "deterministic-eval-report.json",
    "${_EVIDENCE_BUCKET}/volume-3/${BUILD_ID}/",
)


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = [f"missing required control: {item}" for item in REQUIRED if item not in text]
    if "latest" in text:
        errors.append("mutable latest reference is forbidden")
    if "--execute" in text or "agent_engines.create" in text:
        errors.append("validation build must not create Agent Runtime resources")
    return errors


if __name__ == "__main__":
    failures = validate(Path(sys.argv[1]))
    for failure in failures:
        print(failure, file=sys.stderr)
    raise SystemExit(1 if failures else 0)
