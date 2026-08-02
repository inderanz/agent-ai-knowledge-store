#!/usr/bin/env python3
"""Fail-closed qualification validator for Volumes 11–15."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


def validate(record: dict, gates: dict, *, production: bool) -> list[str]:
    required = set(gates.get("volumes", {}).get(record.get("volume"), []))
    if gates.get("schema_version") != 1 or not required:
        return ["unknown volume or invalid gate registry"]
    errors: list[str] = []
    if record.get("schema_version") != 1:
        errors.append("record schema_version must be 1")
    if not re.fullmatch(r"[a-z][a-z0-9-]{4,28}[a-z0-9]", record.get("project_id", "")):
        errors.append("project_id is invalid")
    location = record.get("location", "")
    if location != "global" and not re.fullmatch(r"[a-z]+-[a-z]+[0-9]+", location):
        errors.append("location is invalid")
    if "REPLACE" in json.dumps(record):
        errors.append("record contains unresolved REPLACE values")
    for owner in ("product", "security", "operations", "customer_acceptor"):
        if not record.get("owners", {}).get(owner):
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
        revision = record.get("source_revision", "")
        if not re.fullmatch(r"[0-9a-f]{12,64}", revision):
            errors.append("immutable hexadecimal source revision is required")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--production", action="store_true")
    parser.add_argument("--gates", type=Path, default=Path(__file__).with_name("required-gates.json"))
    args = parser.parse_args()
    errors = validate(json.loads(args.record.read_text()), json.loads(args.gates.read_text()), production=args.production)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__": sys.exit(main())
