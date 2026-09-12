#!/usr/bin/env python3
"""Build a bounded machine-readable signal for the documentation maintainer."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import check_sources
import render_upstream_status


def build_signal(registry: dict[str, Any], versions: dict[str, Any], observed: dict[str, render_upstream_status.ObservedRelease], today: date, *, limit: int) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    baselines = versions.get("baselines", {})
    for baseline_id, release in observed.items():
        baseline = str(baselines.get(baseline_id, {}).get("version", "missing"))
        if release.error:
            continue
        if release.version != baseline:
            findings.append({
                "kind": "release-drift",
                "source_id": baseline_id,
                "qualified": baseline,
                "observed": release.version,
                "url": release.url,
                "owner": "version-baseline",
            })
    stale = check_sources.freshness_findings(registry, today)
    source_by_id = {str(item.get("id")): item for item in registry.get("sources", []) if isinstance(item, dict)}
    for finding in stale:
        source = source_by_id.get(finding.source_id, {})
        findings.append({
            "kind": "semantic-review-due",
            "source_id": finding.source_id,
            "message": finding.message,
            "url": source.get("url"),
            "owner": source.get("owner"),
        })
    findings.sort(key=lambda item: (0 if item["kind"] == "release-drift" else 1, str(item.get("owner")), str(item.get("source_id"))))
    bounded = findings[:limit]
    generated = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)
    return {
        "schema_version": 1,
        "change_id": f"upstream-{today.isoformat()}",
        "detected_at": generated.isoformat(),
        "actionable": bool(bounded),
        "finding_count": len(findings),
        "overflow_count": max(0, len(findings) - len(bounded)),
        "findings": bounded,
        "constraints": {
            "draft_pull_request_only": True,
            "human_publication_approval_required": True,
            "customer_cloud_mutation_allowed": False,
            "official_sources_only": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    if not 1 <= args.limit <= 25:
        parser.error("--limit must be between 1 and 25")
    root = Path(__file__).resolve().parents[1]
    registry = check_sources.load_json(root / "references/sources.json")
    versions = check_sources.load_json(root / "references/versions.json")
    observed = {} if args.offline else render_upstream_status.observe_releases(args.timeout)
    signal = build_signal(registry, versions, observed, args.today, limit=args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(signal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"actionable": signal["actionable"], "finding_count": signal["finding_count"], "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
