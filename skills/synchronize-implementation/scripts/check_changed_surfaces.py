#!/usr/bin/env python3
"""Suggest companion surfaces for a set of repository paths."""

from __future__ import annotations

import sys

SURFACES = {
    "docs/": {"examples", "terraform", "delivery", "labs", "operations", "references", "tests/CI"},
    "examples/": {"docs", "delivery", "labs", "operations", "references", "tests/CI"},
    "terraform/": {"docs", "delivery", "labs", "operations", "references", "tests/CI"},
    "delivery/": {"docs", "operations", "references", "tests/CI"},
    "labs/": {"docs", "delivery", "references", "tests/CI"},
    "operations/": {"docs", "labs", "references", "tests/CI"},
    "references/": {"docs", "examples", "terraform", "tests/CI"},
}


def companions(paths: list[str]) -> list[str]:
    result: set[str] = set()
    for path in paths:
        for prefix, surfaces in SURFACES.items():
            if path.startswith(prefix):
                result.update(surfaces)
    return sorted(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: check_changed_surfaces.py PATH...", file=sys.stderr)
        raise SystemExit(2)
    print("\n".join(companions(sys.argv[1:])))
