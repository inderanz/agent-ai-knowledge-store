#!/usr/bin/env python3
"""Fail closed on dangerous or unresolved delivery configuration."""

from __future__ import annotations

import argparse
from pathlib import Path

FORBIDDEN = ("allUsers", "allAuthenticatedUsers", ":latest", "__DEV_", "__PROD_")


def validate(paths: list[Path]) -> list[str]:
    findings: list[str] = []
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    for value in FORBIDDEN:
        if value in combined:
            findings.append(f"prohibited or unresolved value: {value}")
    if "requireApproval: true" not in combined:
        findings.append("production approval is not configured")
    if "internal-and-cloud-load-balancing" not in combined:
        findings.append("Cloud Run ingress boundary is absent")
    if "@sha256:" not in combined:
        findings.append("build images are not digest pinned")
    if "serviceAccount:" not in combined:
        findings.append("user-specified build identity is absent")
    if "run.googleapis.com/binary-authorization: default" not in combined:
        findings.append("Cloud Run Binary Authorization is absent")
    if "requestedVerifyOption: VERIFIED" not in combined:
        findings.append("Cloud Build verified provenance is not required")
    if "supply_chain_gate.py" not in combined:
        findings.append("the release does not execute the supply-chain gate")
    if "\n      - push\n" in combined or "\n      - docker push\n" in combined:
        findings.append("explicit docker push bypasses Cloud Build provenance generation")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    findings = validate(args.files)
    if findings:
        print("Delivery policy failed:")
        for item in findings:
            print(f"- {item}")
        return 1
    print("Delivery policy passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
