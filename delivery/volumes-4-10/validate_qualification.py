#!/usr/bin/env python3
"""Fail-closed qualification validator shared by Volumes 4–10."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


def validate(record: dict, gates: dict, *, production: bool) -> list[str]:
    errors: list[str] = []
    volume = record.get("volume")
    required = set(gates.get("volumes", {}).get(volume, []))
    if gates.get("schema_version") != 1 or not required:
        return ["unknown volume or invalid gate registry"]
    if record.get("schema_version") != 1:
        errors.append("record schema_version must be 1")
    if not re.fullmatch(r"[a-z][a-z0-9-]{4,28}[a-z0-9]", record.get("project_id", "")):
        errors.append("project_id is invalid")
    if not re.fullmatch(r"[a-z]+-[a-z]+[0-9]+", record.get("location", "")):
        errors.append("location is invalid")
    if "REPLACE" in json.dumps(record):
        errors.append("record contains unresolved REPLACE values")
    owners = record.get("owners", {})
    for owner in ("product", "security", "operations", "customer_acceptor"):
        if not owners.get(owner):
            errors.append(f"missing owner: {owner}")
    evidence = record.get("evidence", {})
    missing = required - set(evidence)
    if missing:
        errors.append(f"missing evidence fields: {sorted(missing)}")
    if production:
        if record.get("environment") != "production":
            errors.append("production validation requires environment=production")
        for gate in required:
            if evidence.get(gate) is not True:
                errors.append(f"production evidence not accepted: {gate}")
        if record.get("source_revision", "").startswith("REPLACE"):
            errors.append("immutable source revision is required")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--production", action="store_true")
    parser.add_argument("--gates", type=Path,
                        default=Path(__file__).with_name("required-gates.json"))
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    gates = json.loads(args.gates.read_text(encoding="utf-8"))
    errors = validate(record, gates, production=args.production)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__": sys.exit(main())
