#!/usr/bin/env python3
"""Validate handbook structure and local documentation invariants."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FILES = (
    "README.md",
    "SUMMARY.md",
    "CONTRIBUTING.md",
    "STYLE_GUIDE.md",
    "ROADMAP.md",
    "docs/STATUS.md",
    "docs/RESEARCH_AND_REVIEW.md",
    "docs/templates/CHAPTER_TEMPLATE.md",
    "references/sources.json",
    "references/versions.json",
    "references/UPSTREAM_STATUS.md",
    "scripts/check_sources.py",
    "scripts/render_upstream_status.py",
    ".github/workflows/docs-quality.yml",
    ".github/workflows/upstream-docs-refresh.yml",
    "adr/0000-template.md",
)

REQUIRED_DIRECTORIES = (
    "diagrams",
    "terraform",
    "examples",
    "labs",
    "adr",
    "assets",
    "references",
    "scripts",
    "tests",
    *(f"docs/volume-{number}" for number in ()),
)

VOLUME_GLOBS = tuple(f"docs/volume-{number}-*" for number in range(1, 16))

FINAL_SECTIONS = (
    "Production Checklist",
    "Architecture Decision Record",
    "Customer Workshop",
    "Common Mistakes",
    "Performance Considerations",
    "Security Considerations",
    "Operations Checklist",
    "Cost Optimisation",
    "Official References",
    "Next Chapter",
)

CLASSIFICATIONS = (
    "🟢 Official Google Capability",
    "🟡 Enterprise Architecture Recommendation",
    "🔵 Field Pattern",
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def _front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def _markdown_files(root: Path) -> list[Path]:
    ignored = {".git", ".venv", ".terraform"}
    return [
        path
        for path in root.rglob("*.md")
        if not ignored.intersection(path.relative_to(root).parts)
    ]


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for relative in REQUIRED_DIRECTORIES:
        if not (root / relative).is_dir():
            errors.append(f"missing required directory: {relative}")

    for pattern in VOLUME_GLOBS:
        matches = list(root.glob(pattern))
        if len(matches) != 1 or not (matches[0] / "README.md").is_file():
            errors.append(f"expected one documented volume matching: {pattern}")

    for relative in ("references/sources.json", "references/versions.json"):
        path = root / relative
        if not path.exists():
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON in {relative}: {exc}")

    for path in _markdown_files(root):
        relative = path.relative_to(root)
        text = path.read_text(encoding="utf-8")

        if re.search(r"\bI think\b", text, flags=re.IGNORECASE):
            errors.append(f"prohibited unsupported phrasing in {relative}: 'I think'")

        if text.count("```mermaid") > text.count("```"):
            errors.append(f"unclosed Mermaid fence in {relative}")

        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"broken local link in {relative}: {raw_target}")

        metadata = _front_matter(text)
        if metadata.get("status", "").lower() == "approved":
            for section in FINAL_SECTIONS:
                if not re.search(rf"^##+\s+{re.escape(section)}\s*$", text, re.MULTILINE):
                    errors.append(f"approved chapter {relative} is missing: {section}")
            for classification in CLASSIFICATIONS:
                if classification not in text:
                    errors.append(
                        f"approved chapter {relative} is missing classification: {classification}"
                    )

    return sorted(set(errors))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
