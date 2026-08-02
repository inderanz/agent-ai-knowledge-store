#!/usr/bin/env python3
"""Check source freshness, reachability, and pinned upstream release baselines."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


USER_AGENT = "enterprise-agent-platform-handbook-source-check/1.0"

RELEASE_APIS = {
    "google-adk-python": "https://api.github.com/repos/google/adk-python/releases/latest",
    "google-cloud-aiplatform": (
        "https://api.github.com/repos/googleapis/python-aiplatform/releases/latest"
    ),
    "googlecloudplatform-agent-starter-pack": (
        "https://api.github.com/repos/GoogleCloudPlatform/agent-starter-pack/releases/latest"
    ),
    "googlecloudplatform-cloud-foundation-fabric": (
        "https://api.github.com/repos/GoogleCloudPlatform/cloud-foundation-fabric/releases/latest"
    ),
    "terraform": "https://api.github.com/repos/hashicorp/terraform/releases/latest",
    "terraform-provider-google": (
        "https://api.github.com/repos/hashicorp/terraform-provider-google/releases/latest"
    ),
    "googlecloudplatform-terraform-google-cloud-armor": (
        "https://api.github.com/repos/GoogleCloudPlatform/terraform-google-cloud-armor/releases/latest"
    ),
}


@dataclass(frozen=True)
class Finding:
    level: str
    source_id: str
    message: str


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def freshness_findings(registry: dict[str, Any], today: date) -> list[Finding]:
    findings: list[Finding] = []
    sources = registry.get("sources")
    if not isinstance(sources, list):
        return [Finding("error", "registry", "sources must be a list")]

    seen: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            findings.append(Finding("error", "registry", "source entry must be an object"))
            continue
        source_id = str(source.get("id", "missing-id"))
        if source_id in seen:
            findings.append(Finding("error", source_id, "duplicate source id"))
        seen.add(source_id)
        try:
            verified = date.fromisoformat(str(source["verified_at"]))
            interval = int(source["review_interval_days"])
            if interval <= 0:
                raise ValueError("review interval must be positive")
        except (KeyError, TypeError, ValueError) as exc:
            findings.append(Finding("error", source_id, f"invalid freshness metadata: {exc}"))
            continue
        age = (today - verified).days
        if age < 0:
            findings.append(Finding("error", source_id, "verification date is in the future"))
        elif age > interval:
            findings.append(
                Finding("error", source_id, f"source is stale: {age} days > {interval} days")
            )
    return findings


def curl(url: str, timeout: float, *, capture: bool = False) -> str:
    command = [
        "curl",
        "--fail",
        "--location",
        "--silent",
        "--show-error",
        "--max-time",
        str(timeout),
        "--user-agent",
        USER_AGENT,
    ]
    if not capture:
        command.extend(["--output", "/dev/null"])
    command.append(url)
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout


def fetch_json(url: str, timeout: float = 20.0) -> dict[str, Any]:
    payload = json.loads(curl(url, timeout, capture=True))
    if not isinstance(payload, dict):
        raise ValueError("expected a JSON object")
    return payload


def reachability_finding(source: dict[str, Any], timeout: float) -> Finding | None:
    source_id = str(source["id"])
    try:
        curl(str(source["url"]), timeout)
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        return Finding("error", source_id, f"unreachable: {exc}")
    return None


def release_findings(versions: dict[str, Any], timeout: float) -> list[Finding]:
    findings: list[Finding] = []
    baselines = versions.get("baselines", {})
    for baseline_id, api_url in RELEASE_APIS.items():
        try:
            expected = str(baselines[baseline_id]["version"])
        except (KeyError, TypeError):
            findings.append(
                Finding("error", baseline_id, "missing version in versions registry")
            )
            continue
        try:
            release = fetch_json(api_url, timeout=timeout)
        except (
            FileNotFoundError,
            json.JSONDecodeError,
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
            ValueError,
        ) as exc:
            findings.append(
                Finding("error", baseline_id, f"release check failed: {exc}")
            )
            continue
        observed = str(release.get("tag_name", "")).removeprefix("v")
        if observed != expected:
            findings.append(
                Finding(
                    "error",
                    baseline_id,
                    f"baseline {expected} differs from latest official release "
                    f"{observed or 'unknown'}",
                )
            )
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="skip network checks")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")
    root = Path(__file__).resolve().parents[1]
    registry = load_json(root / "references" / "sources.json")
    versions = load_json(root / "references" / "versions.json")
    findings = freshness_findings(registry, args.today)

    if not args.offline:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(reachability_finding, source, args.timeout): source
                for source in registry["sources"]
            }
            for future in as_completed(futures):
                finding = future.result()
                if finding:
                    findings.append(finding)
        findings.extend(release_findings(versions, args.timeout))

    if findings:
        print("Source validation failed:")
        for finding in findings:
            print(f"- [{finding.level}] {finding.source_id}: {finding.message}")
        return 1

    mode = "offline metadata" if args.offline else "freshness, reachability, and release"
    print(f"Source validation passed ({mode}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
