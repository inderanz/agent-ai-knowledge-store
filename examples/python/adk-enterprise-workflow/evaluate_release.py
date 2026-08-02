#!/usr/bin/env python3
"""Hermetic release gate for deterministic enterprise invariants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from enterprise_adk.models import ChangeRequest, Principal
from enterprise_adk.policy import Policy
from enterprise_adk.tools import InMemoryToolGateway, ToolOutcome
from enterprise_adk.workflow import EnterpriseWorkflow


def evaluate(path: Path) -> dict:
    suite = json.loads(path.read_text(encoding="utf-8"))
    if suite.get("schema_version") != 1:
        raise ValueError("unsupported evaluation schema")
    results = []
    for case in suite["cases"]:
        principal = Principal(
            case["principal"]["subject"], frozenset(case["principal"]["groups"])
        )
        request = ChangeRequest.from_dict(case["request"])
        outcome = ToolOutcome(case.get("tool_outcome", "SUCCEEDED"))
        workflow = EnterpriseWorkflow(
            Policy(
                tenant_id="tenant-a",
                allowed_actions=frozenset({"read-status", "rotate-key"}),
                executor_group="change-executors",
                approval_group="change-approvers",
                force_approval_actions=frozenset({"rotate-key"}),
                deny_all=False,
            ),
            InMemoryToolGateway([outcome]),
        )
        actual = workflow.run(principal=principal, request=request).status.value
        results.append({
            "id": case["id"], "expected": case["expected_status"],
            "actual": actual, "passed": actual == case["expected_status"],
        })
    pass_rate = sum(item["passed"] for item in results) / max(len(results), 1)
    return {
        "passed": pass_rate >= float(suite["minimum_pass_rate"]),
        "pass_rate": pass_rate,
        "minimum_pass_rate": suite["minimum_pass_rate"],
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("suite", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate(args.suite)
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
