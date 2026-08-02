#!/usr/bin/env python3
"""Require completed scanning, matching provenance, and no high findings."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

IMAGE = re.compile(r"^[a-z0-9.-]+/[a-z][a-z0-9-]{4,28}[a-z0-9]/[a-z0-9._/-]+@sha256:[0-9a-f]{64}$")
BUILD_ID = re.compile(r"^[0-9a-f-]{16,64}$")
REVISION = re.compile(r"^[0-9a-f]{40}$")
BLOCKED_SEVERITIES = {"CRITICAL", "HIGH"}


def _kind(item: dict[str, Any]) -> str:
    if isinstance(item.get("kind"), str):
        return item["kind"].upper()
    for candidate in ("discovery", "vulnerability", "build"):
        if candidate in item:
            return candidate.upper()
    return "UNKNOWN"


def findings(
    occurrences: list[dict[str, Any]], provenance: dict[str, Any], build_id: str
) -> list[str]:
    result: list[str] = []
    discovery = [item for item in occurrences if _kind(item) == "DISCOVERY"]
    completed = any(
        str(item.get("discovery", {}).get("analysisStatus", "")).upper()
        in {"COMPLETE", "FINISHED_SUCCESS"}
        for item in discovery
    )
    if not completed:
        result.append("Artifact Analysis has no successfully completed discovery occurrence")

    provenance_entries = provenance.get("provenance_summary", {}).get("provenance", [])
    if not provenance_entries or build_id not in json.dumps(provenance, sort_keys=True):
        result.append("Cloud Build provenance does not match the declared build ID")

    for item in occurrences:
        if _kind(item) != "VULNERABILITY":
            continue
        vulnerability = item.get("vulnerability", {})
        severity = str(
            vulnerability.get("effectiveSeverity")
            or vulnerability.get("severity")
            or "UNKNOWN"
        ).upper()
        if severity in BLOCKED_SEVERITIES:
            identifier = item.get("noteName") or item.get("name") or "unknown-occurrence"
            result.append(f"{severity} vulnerability: {identifier}")
    return sorted(set(result))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("occurrences", type=Path)
    parser.add_argument("--provenance", required=True, type=Path)
    parser.add_argument("--image", required=True)
    parser.add_argument("--build-id", required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    for value, pattern, label in (
        (args.image, IMAGE, "image digest"),
        (args.build_id, BUILD_ID, "build ID"),
        (args.revision, REVISION, "source revision"),
    ):
        if not pattern.fullmatch(value):
            print(f"Supply-chain gate failed: malformed {label}.")
            return 1
    payload = json.loads(args.occurrences.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        print("Supply-chain gate failed: occurrence evidence must be a JSON list.")
        return 1
    provenance = json.loads(args.provenance.read_text(encoding="utf-8"))
    if not isinstance(provenance, dict):
        print("Supply-chain gate failed: provenance evidence must be a JSON object.")
        return 1
    violations = findings(payload, provenance, args.build_id)
    if violations:
        print("Supply-chain gate failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("Supply-chain gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
