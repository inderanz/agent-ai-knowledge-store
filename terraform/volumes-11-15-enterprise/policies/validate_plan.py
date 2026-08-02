#!/usr/bin/env python3
"""Fail closed on enterprise invariants in a Terraform JSON plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


PROTECTED_TYPES = {
    "google_agent_identity_auth_provider",
    "google_agent_registry_binding",
    "google_agent_registry_service",
    "google_discovery_engine_cmek_config",
    "google_discovery_engine_data_store",
    "google_discovery_engine_search_engine",
    "google_network_security_authz_policy",
    "google_network_services_agent_gateway",
    "google_network_services_authz_extension",
}


def resources(module: dict[str, Any]) -> Iterable[dict[str, Any]]:
    yield from module.get("resources", [])
    for child in module.get("child_modules", []):
        yield from resources(child)


def changes(plan: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for change in plan.get("resource_changes", []):
        yield change


def contains_non_write_only_secret(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"api_key", "client_secret"} and child not in (None, ""):
                return True
            if contains_non_write_only_secret(child):
                return True
    elif isinstance(value, list):
        return any(contains_non_write_only_secret(child) for child in value)
    return False


def violations(plan: dict[str, Any], environment: str) -> list[str]:
    errors: list[str] = []
    root = plan.get("planned_values", {}).get("root_module", {})
    planned = list(resources(root))

    if environment == "production":
        for change in changes(plan):
            if change.get("type") in PROTECTED_TYPES and "delete" in change.get("change", {}).get("actions", []):
                errors.append(f"{change.get('address')}: protected production resource is deleted or replaced")

    for resource in planned:
        rtype = resource.get("type")
        address = resource.get("address", rtype)
        values = resource.get("values") or {}

        if rtype in PROTECTED_TYPES and "deletion_policy" in values and values.get("deletion_policy") != "PREVENT":
            errors.append(f"{address}: deletion_policy must be PREVENT")

        if rtype == "google_network_services_agent_gateway" and values.get("protocols") not in (None, [], {}):
            errors.append(f"{address}: deprecated protocols must not be configured")

        if rtype == "google_network_services_authz_extension":
            metadata = values.get("metadata") or {}
            if environment == "production" and values.get("fail_open") is not False:
                errors.append(f"{address}: production authorization extension must fail closed")
            if environment == "production" and metadata.get("iamEnforcementMode") == "DRY_RUN":
                errors.append(f"{address}: DRY_RUN IAP enforcement cannot be promoted to production")
            if environment != "production" and values.get("fail_open") is True and metadata.get("iamEnforcementMode") != "DRY_RUN":
                errors.append(f"{address}: fail-open is allowed only for explicit IAP DRY_RUN qualification")
            if values.get("service") != "iap.googleapis.com":
                errors.append(f"{address}: authorization extension must use IAP")

        if rtype == "google_network_security_authz_policy":
            if values.get("action") != "CUSTOM" or values.get("policy_profile") != "REQUEST_AUTHZ":
                errors.append(f"{address}: gateway authorization policy must be CUSTOM/REQUEST_AUTHZ")

        if rtype == "google_agent_identity_auth_provider" and contains_non_write_only_secret(values):
            errors.append(f"{address}: API key or state-persistent client_secret is forbidden")

        if rtype == "google_discovery_engine_search_engine":
            if values.get("app_type") != "APP_TYPE_INTRANET":
                errors.append(f"{address}: Gemini Enterprise engine must be APP_TYPE_INTRANET")
            configs = values.get("search_engine_config") or []
            if not configs or configs[0].get("search_tier") != "SEARCH_TIER_ENTERPRISE":
                errors.append(f"{address}: enterprise search tier is required")

        if rtype == "google_project_iam_member" and values.get("role") == "roles/discoveryengine.agentspaceUser":
            errors.append(f"{address}: agentspaceUser must be granted on the app, not the project")

        if rtype and rtype.startswith("google_iap_agent_registry_") and rtype.endswith("_iam_member"):
            if values.get("role") != "roles/iap.egressor" or not values.get("condition"):
                errors.append(f"{address}: IAP egress needs roles/iap.egressor and an IAM condition")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--environment", choices=["development", "staging", "production"], required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    errors = violations(plan, args.environment)
    if errors:
        print("Terraform plan rejected:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Terraform plan satisfies the volumes 11-15 policy baseline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
