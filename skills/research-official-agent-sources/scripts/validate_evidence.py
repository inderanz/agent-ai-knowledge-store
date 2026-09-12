#!/usr/bin/env python3
"""Validate the minimum evidence packet contract without external packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_HOSTS = {
    "adk.dev", "anthropic.com", "www.anthropic.com", "cloud.google.com", "developers.google.com",
    "docs.anthropic.com", "docs.cloud.google.com", "github.com",
    "job-boards.greenhouse.io", "openai.com", "platform.openai.com",
}
REQUIRED_PACKET = {"schema_version", "question", "as_of", "evidence", "facts", "inferences", "unknowns", "affected_paths"}
REQUIRED_EVIDENCE = {"source_id", "vendor", "url", "locator", "retrieved_at", "tier", "maturity", "supports", "content_sha256"}
GITHUB_VENDOR_ORGS = {
    "google": {"google", "googleapis", "GoogleCloudPlatform"},
    "openai": {"openai"},
    "anthropic": {"anthropics"},
}


def validate(packet: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(packet, dict):
        return ["packet must be an object"]
    missing = REQUIRED_PACKET - set(packet)
    if missing:
        errors.append(f"missing packet fields: {sorted(missing)}")
    evidence = packet.get("evidence", [])
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence must be a non-empty list")
        return errors
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            errors.append(f"evidence[{index}] must be an object")
            continue
        missing_item = REQUIRED_EVIDENCE - set(item)
        if missing_item:
            errors.append(f"evidence[{index}] missing: {sorted(missing_item)}")
            continue
        host = (urlparse(str(item["url"])).hostname or "").lower()
        if host not in ALLOWED_HOSTS:
            errors.append(f"evidence[{index}] host is not allowlisted: {host}")
        if host == "job-boards.greenhouse.io" and not urlparse(str(item["url"])).path.startswith("/anthropic/"):
            errors.append(f"evidence[{index}] is not an Anthropic Greenhouse posting")
        if host == "github.com":
            parts = [part for part in urlparse(str(item["url"])).path.split("/") if part]
            if len(parts) < 2 or parts[0] not in GITHUB_VENDOR_ORGS.get(str(item["vendor"]), set()):
                errors.append(f"evidence[{index}] GitHub organization does not match vendor")
        if item["vendor"] not in {"google", "openai", "anthropic"}:
            errors.append(f"evidence[{index}] has invalid vendor")
        if not isinstance(item["tier"], int) or not 1 <= item["tier"] <= 5:
            errors.append(f"evidence[{index}] tier must be 1..5")
        if not re.fullmatch(r"[0-9a-f]{64}", str(item["content_sha256"])):
            errors.append(f"evidence[{index}] has invalid content_sha256")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_evidence.py PACKET.json", file=sys.stderr)
        return 2
    packet = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate(packet)
    for error in errors:
        print(f"- {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
