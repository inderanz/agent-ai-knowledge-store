"""Industry overlay validation without encoding legal or clinical conclusions."""

from __future__ import annotations

from typing import Any


REQUIRED_DECISIONS = {
    "jurisdiction", "data_classification", "authoritative_system",
    "material_decisions", "human_accountability", "retention",
    "residency", "fallback", "incident_owner", "legal_owner",
}


PROHIBITED_AUTONOMY = {
    "banking": {"unreviewed-payment", "credit-adverse-decision"},
    "insurance": {"unreviewed-claim-denial"},
    "healthcare": {"autonomous-diagnosis", "autonomous-treatment"},
    "government": {"unreviewed-rights-decision"},
    "manufacturing": {"direct-safety-control"},
    "aviation": {"unreviewed-airworthiness-decision"},
}


def validate_overlay(overlay: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_DECISIONS - set(overlay.get("decisions", {}))
    if missing:
        errors.append(f"missing customer decisions: {sorted(missing)}")
    industry = str(overlay.get("industry", ""))
    actions = set(overlay.get("autonomous_actions", []))
    prohibited = PROHIBITED_AUTONOMY.get(industry, set()) & actions
    if prohibited:
        errors.append(f"prohibited autonomous actions: {sorted(prohibited)}")
    if overlay.get("uses_real_customer_data") is not False:
        errors.append("reference overlay must use synthetic data only")
    if overlay.get("legal_approval_recorded") is not True:
        errors.append("customer legal approval is not recorded")
    return errors
