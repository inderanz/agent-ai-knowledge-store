#!/usr/bin/env python3
"""Validate customer-owned ADK production qualification evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


EXPECTED = {"adk_version": "2.6.1", "agent_platform_sdk_version": "1.163.0"}
REQUIRED_CONTROLS = {
    "region_currently_supported", "runtime_identity_least_privilege_reviewed",
    "durable_tool_ledger_configured", "authenticated_approval_provider_configured",
    "segregation_of_duties_tested", "managed_session_retention_approved",
    "event_schema_migration_tested", "redaction_and_log_sinks_tested",
    "online_eval_dataset_approved", "deterministic_eval_passed",
    "load_and_quota_tested", "restore_and_resume_tested", "rollback_tested",
    "kill_switch_tested", "on_call_and_incident_runbook_exercised",
}
REQUIRED_ACCEPTANCES = {
    "known_graph_streaming_limit_accepted", "residual_model_risk_accepted",
    "cost_envelope_approved",
}


def validate(record: dict, *, production: bool) -> list[str]:
    errors: list[str] = []
    if record.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    for key, expected in EXPECTED.items():
        if record.get(key) != expected:
            errors.append(f"{key} must equal qualified value {expected}")
    if not re.fullmatch(r"[a-z][a-z0-9-]{4,28}[a-z0-9]", record.get("project_id", "")):
        errors.append("project_id is invalid")
    if not re.fullmatch(r"[a-z]+-[a-z]+[0-9]+", record.get("location", "")):
        errors.append("location is invalid")
    if "REPLACE" in json.dumps(record):
        errors.append("qualification record contains unresolved REPLACE values")
    controls = record.get("controls", {})
    acceptances = record.get("acceptances", {})
    missing_controls = REQUIRED_CONTROLS - set(controls)
    missing_acceptances = REQUIRED_ACCEPTANCES - set(acceptances)
    if missing_controls:
        errors.append(f"missing controls: {sorted(missing_controls)}")
    if missing_acceptances:
        errors.append(f"missing acceptances: {sorted(missing_acceptances)}")
    if production:
        if record.get("environment") != "production":
            errors.append("production validation requires environment=production")
        for key in REQUIRED_CONTROLS:
            if controls.get(key) is not True:
                errors.append(f"production control not evidenced: {key}")
        for key in REQUIRED_ACCEPTANCES:
            if acceptances.get(key) is not True:
                errors.append(f"production acceptance missing: {key}")
        if record.get("data_classification") in {None, "", "synthetic"}:
            errors.append("production data classification must record the customer decision")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    failures = validate(json.loads(args.record.read_text(encoding="utf-8")), production=args.production)
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
