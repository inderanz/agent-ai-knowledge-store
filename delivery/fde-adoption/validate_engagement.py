#!/usr/bin/env python3
"""Validate completeness of an FDE customer-adoption evidence record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_OWNERS = {"sponsor", "product", "technical", "security", "data", "sre", "risk"}
REQUIRED_OUTCOME = {"workflow", "baseline", "target", "measurement_source", "owner", "stop_condition"}
REQUIRED_GATES = {
    "research-architecture", "implementation-supply-chain", "security-data-responsible-ai",
    "evaluation-reliability-cost", "operations-recovery-support", "delivery-adoption-handover",
}
PRODUCTION_ARTIFACTS = {"architecture", "evaluation", "threat-model", "runbooks", "rollback", "slo", "cost", "adoption"}
PRODUCTION_SIGNOFFS = {"product", "technical", "security", "risk", "sre"}
PRODUCTION_COMPETENCIES = {"deploy", "rollback", "evaluate-change", "diagnose", "incident", "recover", "retire"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(record: object, *, production: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["engagement record must be an object"]
    for field in ("engagement_id", "customer_id"):
        if not _nonempty(record.get(field)):
            errors.append(f"{field} is required")
    if record.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    current = record.get("current_level")
    target = record.get("target_level")
    if not isinstance(current, int) or not 0 <= current <= 6:
        errors.append("current_level must be 0..6")
    if not isinstance(target, int) or not 0 <= target <= 6:
        errors.append("target_level must be 0..6")
    if isinstance(current, int) and isinstance(target, int) and target < current:
        errors.append("target_level cannot be below current_level")
    outcome = record.get("outcome")
    if not isinstance(outcome, dict):
        errors.append("outcome must be an object")
    else:
        for field in sorted(REQUIRED_OUTCOME):
            if not _nonempty(outcome.get(field)):
                errors.append(f"outcome.{field} is required")
    owners = record.get("owners")
    if not isinstance(owners, dict):
        errors.append("owners must be an object")
    else:
        for field in sorted(REQUIRED_OWNERS):
            if not _nonempty(owners.get(field)):
                errors.append(f"owners.{field} is required")
    use_cases = record.get("use_cases")
    if not isinstance(use_cases, list) or not use_cases:
        errors.append("at least one use case is required")
    else:
        for index, use_case in enumerate(use_cases):
            autonomy = use_case.get("autonomy_level") if isinstance(use_case, dict) else None
            if not isinstance(autonomy, int) or not 0 <= autonomy <= 5:
                errors.append(f"use_cases[{index}].autonomy_level must be 0..5")
    gates = record.get("gates")
    if not isinstance(gates, dict) or set(gates) != REQUIRED_GATES:
        errors.append("gates must contain exactly the six required gates")
    if not production:
        return errors
    if record.get("synthetic") is not False:
        errors.append("production evidence cannot be synthetic")
    if not isinstance(current, int) or current < 4:
        errors.append("production evidence requires current_level >= 4")
    if isinstance(gates, dict):
        for name in sorted(REQUIRED_GATES):
            gate = gates.get(name)
            if not isinstance(gate, dict) or gate.get("passed") is not True or not gate.get("evidence"):
                errors.append(f"production gate is incomplete: {name}")
    artifacts = {item.get("type") for item in record.get("artifacts", []) if isinstance(item, dict) and item.get("uri")}
    if missing := PRODUCTION_ARTIFACTS - artifacts:
        errors.append(f"production artifacts missing: {sorted(missing)}")
    signoffs = {item.get("role") for item in record.get("customer_signoffs", []) if isinstance(item, dict) and item.get("decision") == "approve" and item.get("evidence")}
    if missing := PRODUCTION_SIGNOFFS - signoffs:
        errors.append(f"customer sign-offs missing: {sorted(missing)}")
    competencies = {item.get("name") for item in record.get("handover_competencies", []) if isinstance(item, dict) and item.get("passed") is True and item.get("evidence")}
    if missing := PRODUCTION_COMPETENCIES - competencies:
        errors.append(f"handover competencies missing: {sorted(missing)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    errors = validate(record, production=args.production)
    for error in errors:
        print(f"- {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
