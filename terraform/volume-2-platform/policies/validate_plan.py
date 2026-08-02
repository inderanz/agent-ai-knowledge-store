#!/usr/bin/env python3
"""Fail a production Terraform plan on high-risk platform changes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

CRITICAL_TYPES = {
    "google_billing_budget",
    "google_firestore_database",
    "google_logging_metric",
    "google_monitoring_alert_policy",
    "google_project",
    "google_secret_manager_secret",
}
PROHIBITED_ROLES = {"roles/owner", "roles/editor"}
PUBLIC_MEMBERS = {"allUsers", "allAuthenticatedUsers"}


def findings(plan: dict[str, Any]) -> list[str]:
    result: list[str] = []
    changes = plan.get("resource_changes", [])
    if not isinstance(changes, list):
        return ["plan resource_changes must be a list"]
    for resource in changes:
        address = str(resource.get("address", "unknown"))
        resource_type = str(resource.get("type", ""))
        change = resource.get("change", {})
        actions = set(change.get("actions", []))
        after = change.get("after") or {}

        if "delete" in actions and resource_type in CRITICAL_TYPES:
            result.append(f"{address}: destructive change to critical resource")
        role = after.get("role")
        if role in PROHIBITED_ROLES:
            result.append(f"{address}: prohibited primitive role {role}")
        member = after.get("member")
        if member in PUBLIC_MEMBERS:
            result.append(f"{address}: prohibited public IAM member {member}")
        members = set(after.get("members") or [])
        if members.intersection(PUBLIC_MEMBERS):
            result.append(f"{address}: prohibited public IAM binding")
        if resource_type == "google_service_account_key":
            result.append(f"{address}: long-lived service-account key")
        if resource_type == "google_compute_firewall":
            ranges = set(after.get("source_ranges") or [])
            if "0.0.0.0/0" in ranges and after.get("direction", "INGRESS") == "INGRESS":
                result.append(f"{address}: unrestricted firewall ingress")
    return sorted(set(result))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan_json", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan_json.read_text(encoding="utf-8"))
    violations = findings(plan)
    if violations:
        print("Terraform plan policy failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("Terraform plan policy passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

