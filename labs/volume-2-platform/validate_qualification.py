#!/usr/bin/env python3
"""Validate recorded Agent Platform topology and maturity acceptance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def findings(record: dict[str, Any]) -> list[str]:
    result: list[str] = []
    environment = record.get("environment")
    if environment not in {"dev", "test", "stage", "prod"}:
        result.append("environment is invalid")
    runtime = record.get("agent_runtime", {})
    registry = record.get("agent_registry", {})
    gateway = record.get("agent_gateway", {})
    if gateway.get("enabled"):
        if not gateway.get("preview_terms_accepted"):
            result.append("Agent Gateway preview terms are not accepted")
        for key in ("project_id", "region"):
            values = {runtime.get(key), registry.get(key), gateway.get(key)}
            if None in values or len(values) != 1:
                result.append(f"Runtime, Registry, and Gateway {key} must match")
    identity = record.get("agent_identity", {})
    if identity.get("enabled") and not identity.get("preview_terms_accepted"):
        result.append("Agent Identity preview terms are not accepted")
    managed = record.get("managed_agents", {})
    if managed.get("enabled"):
        if environment == "prod":
            result.append("Managed Agents are prohibited in production by this baseline")
        if not managed.get("pre_ga_terms_accepted"):
            result.append("Managed Agents Pre-GA terms are not accepted")
        if managed.get("contains_sensitive_or_confidential_data"):
            result.append("Managed Agents record includes sensitive or confidential data")
    armor = record.get("model_armor", {})
    if gateway.get("enabled") and armor.get("enabled") and armor.get("template_region") != gateway.get("region"):
        result.append("Model Armor template and Agent Gateway regions must match")
    owners = record.get("owners", {})
    for owner in ("security", "privacy", "legal", "operations", "product"):
        if not owners.get(owner) or owners.get(owner) == "replace-me":
            result.append(f"missing accountable owner: {owner}")
    return sorted(set(result))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    violations = findings(record)
    if violations:
        print("Agent Platform qualification failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("Agent Platform qualification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

