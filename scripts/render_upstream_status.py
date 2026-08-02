#!/usr/bin/env python3
"""Render the automated upstream-status document without changing qualified baselines."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import check_sources


@dataclass(frozen=True)
class ObservedRelease:
    version: str | None
    url: str
    error: str | None = None


def observe_releases(timeout: float) -> dict[str, ObservedRelease]:
    observed: dict[str, ObservedRelease] = {}
    for baseline_id, api_url in check_sources.RELEASE_APIS.items():
        try:
            payload = check_sources.fetch_json(api_url, timeout=timeout)
            tag = str(payload.get("tag_name", "")).removeprefix("v")
            if not tag:
                raise ValueError("release has no tag_name")
            observed[baseline_id] = ObservedRelease(
                version=tag,
                url=str(payload.get("html_url") or api_url),
            )
        except Exception as exc:  # The report must survive a partial upstream outage.
            observed[baseline_id] = ObservedRelease(
                version=None,
                url=api_url,
                error=f"{type(exc).__name__}: {exc}",
            )
    return observed


def _escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_report(
    registry: dict[str, Any],
    versions: dict[str, Any],
    observed: dict[str, ObservedRelease],
    today: date,
) -> str:
    baselines = versions.get("baselines", {})
    release_rows: list[str] = []
    drift_count = 0
    error_count = 0
    for baseline_id in check_sources.RELEASE_APIS:
        baseline = str(baselines.get(baseline_id, {}).get("version", "missing"))
        release = observed.get(
            baseline_id,
            ObservedRelease(None, check_sources.RELEASE_APIS[baseline_id], "not checked"),
        )
        if release.error:
            state = "ERROR"
            observed_version = "unknown"
            error_count += 1
        elif release.version != baseline:
            state = "REVIEW REQUIRED"
            observed_version = release.version or "unknown"
            drift_count += 1
        else:
            state = "CURRENT"
            observed_version = release.version or "unknown"
        release_rows.append(
            f"| `{_escape(baseline_id)}` | `{_escape(baseline)}` | "
            f"[`{_escape(observed_version)}`]({_escape(release.url)}) | {state} |"
        )

    source_rows: list[tuple[int, str]] = []
    current_count = 0
    invalid_count = 0
    for source in registry.get("sources", []):
        try:
            verified = date.fromisoformat(str(source["verified_at"]))
            interval = int(source["review_interval_days"])
            age = (today - verified).days
            due = verified.fromordinal(verified.toordinal() + interval)
            if age < 0 or interval <= 0:
                raise ValueError("invalid date or interval")
            if age > interval:
                source_rows.append(
                    (
                        age - interval,
                        f"| `{_escape(source.get('id', 'missing-id'))}` | "
                        f"`{verified.isoformat()}` | `{due.isoformat()}` | "
                        f"{age - interval} day(s) overdue |",
                    )
                )
            else:
                current_count += 1
        except (KeyError, TypeError, ValueError):
            invalid_count += 1

    source_rows.sort(key=lambda item: (-item[0], item[1]))
    stale_count = len(source_rows)
    generated = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)

    lines = [
        "# Automated upstream status",
        "",
        f"**Generated:** {generated.date().isoformat()} UTC by the scheduled documentation-maintenance workflow.",
        "",
        "> [!IMPORTANT]",
        "> This is an observation report, not the qualified repository baseline. Automation never",
        "> changes `references/versions.json`, chapter claims, maturity labels, or `verified_at`",
        "> dates. A human reviewer must compare official documentation and code, update affected",
        "> material, and pass the repository review gates before a new baseline is accepted.",
        "",
        "## Summary",
        "",
        "| Check | Count |",
        "|---|---:|",
        f"| Tracked release baselines | {len(check_sources.RELEASE_APIS)} |",
        f"| Release drifts requiring review | {drift_count} |",
        f"| Release-query errors | {error_count} |",
        f"| Registered sources within review interval | {current_count} |",
        f"| Registered sources overdue | {stale_count} |",
        f"| Invalid source records | {invalid_count} |",
        "",
        "## Release comparison",
        "",
        "| Dependency | Qualified baseline | Latest observed official release | State |",
        "|---|---:|---:|---|",
        *release_rows,
        "",
        "## Sources requiring semantic re-verification",
        "",
    ]

    if source_rows:
        lines.extend(
            [
                "| Source | Last verified | Review due | State |",
                "|---|---:|---:|---|",
                *(row for _, row in source_rows),
            ]
        )
    else:
        lines.append("No registered source is overdue as of this report date.")

    lines.extend(
        [
            "",
            "## Required maintainer action",
            "",
            "1. Open the official release, documentation, source tag, samples, and release notes.",
            "2. Identify affected volumes, Terraform modules, examples, labs, runbooks, and claims.",
            "3. Update code and prose together; preserve capability/recommendation/field-pattern labels.",
            "4. Update `references/versions.json` only after implementation qualification.",
            "5. Update a source's `verified_at` only after semantic review, not merely reachability.",
            "6. Run all local and component CI gates and obtain required independent reviews.",
            "",
            "See [the repository workflow](../README.md#how-documentation-stays-current) and "
            "[research policy](../docs/RESEARCH_AND_REVIEW.md).",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--offline", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    registry = check_sources.load_json(root / "references" / "sources.json")
    versions = check_sources.load_json(root / "references" / "versions.json")
    observed = {} if args.offline else observe_releases(args.timeout)
    output = args.output or root / "references" / "UPSTREAM_STATUS.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_report(registry, versions, observed, args.today),
        encoding="utf-8",
    )
    print(f"Rendered {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
