"""Machine-verifiable contract for high-volatility reference facts."""

from __future__ import annotations

from datetime import date
from typing import Any
from urllib.parse import urlparse


REQUIRED = {
    "id", "fact", "classification", "source_url", "verified_at",
    "review_interval_days", "owner", "maturity", "regions", "limitations",
    "validation",
}


def validate_entry(entry: dict[str, Any], today: date) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED - set(entry)
    if missing:
        return [f"missing fields: {sorted(missing)}"]
    if entry["classification"] not in {"official", "recommendation", "field-pattern"}:
        errors.append("classification is invalid")
    parsed = urlparse(str(entry["source_url"]))
    if parsed.scheme != "https" or parsed.netloc not in {
        "cloud.google.com", "docs.cloud.google.com", "adk.dev", "github.com"
    }:
        errors.append("source URL is not an approved primary-source domain")
    try:
        age = (today - date.fromisoformat(str(entry["verified_at"]))).days
        interval = int(entry["review_interval_days"])
        if interval <= 0 or age > interval or age < 0:
            errors.append("entry freshness is invalid")
    except (TypeError, ValueError):
        errors.append("freshness fields are invalid")
    if entry["maturity"] == "unknown" and not entry["limitations"]:
        errors.append("unknown maturity requires an explicit limitation")
    if not isinstance(entry["regions"], list):
        errors.append("regions must be a list; use an empty list for unknown")
    return errors


def validate_catalog(catalog: dict[str, Any], today: date) -> list[str]:
    if catalog.get("schema_version") != 1 or not isinstance(catalog.get("entries"), list):
        return ["catalog envelope is invalid"]
    errors: list[str] = []
    seen: set[str] = set()
    for entry in catalog["entries"]:
        entry_id = str(entry.get("id", "missing"))
        if entry_id in seen:
            errors.append(f"{entry_id}: duplicate ID")
        seen.add(entry_id)
        errors.extend(f"{entry_id}: {error}" for error in validate_entry(entry, today))
    return errors
