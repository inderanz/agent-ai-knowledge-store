#!/usr/bin/env python3
"""Render customer identifiers without introducing a template dependency."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

KEY = re.compile(r"^[A-Z][A-Z0-9_]+$")
TOKEN = re.compile(r"__([A-Z][A-Z0-9_]+)__")
PROJECT = re.compile(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$")
REGION = re.compile(r"^[a-z]+-[a-z]+[0-9]+$")
SERVICE_ACCOUNT = re.compile(
    r"^[a-z][a-z0-9-]{4,28}[a-z0-9]@[a-z][a-z0-9-]{4,28}[a-z0-9]\.iam\.gserviceaccount\.com$"
)
IAP_AUDIENCE = re.compile(r"^/projects/[0-9]+/global/backendServices/[0-9]+$")
VERSION = re.compile(r"^[1-9][0-9]*$")
EXPECTED = {
    "DELIVERY_PROJECT_ID": PROJECT,
    "DELIVERY_REGION": REGION,
    "DEV_PROJECT_ID": PROJECT,
    "DEV_REGION": REGION,
    "DEV_RUNTIME_SERVICE_ACCOUNT": SERVICE_ACCOUNT,
    "DEV_DEPLOY_SERVICE_ACCOUNT": SERVICE_ACCOUNT,
    "DEV_IAP_AUDIENCE": IAP_AUDIENCE,
    "DEV_SUBJECT_HASH_SECRET_VERSION": VERSION,
    "PROD_PROJECT_ID": PROJECT,
    "PROD_REGION": REGION,
    "PROD_RUNTIME_SERVICE_ACCOUNT": SERVICE_ACCOUNT,
    "PROD_DEPLOY_SERVICE_ACCOUNT": SERVICE_ACCOUNT,
    "PROD_IAP_AUDIENCE": IAP_AUDIENCE,
    "PROD_SUBJECT_HASH_SECRET_VERSION": VERSION,
}


def read_environment(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"{path}:{number}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        if not KEY.fullmatch(key) or not value or value != value.strip():
            raise ValueError(f"{path}:{number}: invalid setting")
        if key in values:
            raise ValueError(f"{path}:{number}: duplicate {key}")
        if key not in EXPECTED or not EXPECTED[key].fullmatch(value):
            raise ValueError(f"{path}:{number}: unsupported or malformed {key}")
        values[key] = value
    missing = sorted(EXPECTED.keys() - values.keys())
    if missing:
        raise ValueError(f"{path}: missing settings: {missing}")
    for lifecycle in ("DEV", "PROD"):
        project = values[f"{lifecycle}_PROJECT_ID"]
        for identity in ("RUNTIME", "DEPLOY"):
            if not values[f"{lifecycle}_{identity}_SERVICE_ACCOUNT"].endswith(
                f"@{project}.iam.gserviceaccount.com"
            ):
                raise ValueError(
                    f"{lifecycle}_{identity}_SERVICE_ACCOUNT is not in {project}"
                )
    return values


def render(template: str, values: dict[str, str]) -> str:
    required = set(TOKEN.findall(template))
    missing = sorted(required - values.keys())
    if missing:
        raise ValueError(f"missing template values: {missing}")
    rendered = TOKEN.sub(lambda match: values[match.group(1)], template)
    if TOKEN.search(rendered):
        raise ValueError("unresolved template token")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment-file", required=True, type=Path)
    parser.add_argument("--template", type=Path, default=Path(__file__).with_name("clouddeploy.yaml.tmpl"))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = render(args.template.read_text(encoding="utf-8"), read_environment(args.environment_file))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
