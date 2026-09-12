#!/usr/bin/env python3
"""Validate repository-owned skill structure without external dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    skill_file = path / "SKILL.md"
    interface_file = path / "agents/openai.yaml"
    if not skill_file.is_file():
        return [f"{path}: missing SKILL.md"]
    values = _frontmatter(skill_file.read_text(encoding="utf-8"))
    if set(values) != {"name", "description"}:
        errors.append(f"{path}: frontmatter must contain only name and description")
    name = values.get("name", "")
    if name != path.name or len(name) > 64 or not NAME_RE.fullmatch(name):
        errors.append(f"{path}: invalid or mismatched skill name")
    description = values.get("description", "")
    if not description or len(description) > 1024 or "TODO" in description:
        errors.append(f"{path}: invalid skill description")
    if "TODO" in skill_file.read_text(encoding="utf-8"):
        errors.append(f"{path}: unresolved TODO")
    if not interface_file.is_file():
        errors.append(f"{path}: missing agents/openai.yaml")
    else:
        interface = interface_file.read_text(encoding="utf-8")
        if f"$${name}" in interface or f"${name}" not in interface:
            errors.append(f"{path}: default prompt must mention ${name}")
        for key in ("display_name:", "short_description:", "default_prompt:"):
            if key not in interface:
                errors.append(f"{path}: openai.yaml missing {key}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    for path in sorted(item for item in args.root.iterdir() if item.is_dir()):
        errors.extend(validate_skill(path))
    for error in errors:
        print(f"- {error}")
    if not errors:
        print(f"Validated {len([item for item in args.root.iterdir() if item.is_dir()])} skills.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
