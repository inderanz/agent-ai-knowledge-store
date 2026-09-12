"""Fail-closed policy for agent-generated candidate changes."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

from .models import Risk

ALLOWED_HOSTS = {
    "adk.dev", "anthropic.com", "www.anthropic.com", "cloud.google.com", "developers.google.com",
    "docs.anthropic.com", "docs.cloud.google.com", "github.com",
    "google.com", "www.google.com", "job-boards.greenhouse.io", "openai.com", "platform.openai.com",
}
ALLOWED_GITHUB_ORGS = {"google", "googleapis", "GoogleCloudPlatform", "openai", "anthropics"}
GITHUB_VENDOR_ORGS = {
    "google": {"google", "googleapis", "GoogleCloudPlatform"},
    "openai": {"openai"},
    "anthropic": {"anthropics"},
}
ALLOWED_PREFIXES = (
    "README.md", "SUMMARY.md", "ROADMAP.md", "docs/", "examples/", "terraform/",
    "delivery/", "diagrams/", "assets/", "labs/", "operations/", "references/",
)
PROTECTED_PREFIXES = (".git/", ".github/", "skills/", "scripts/", "automation/", "SECURITY.md")
MAX_CANDIDATE_BYTES = 1_000_000
REQUIRED_MANIFEST_FIELDS = {
    "schema_version", "change_id", "author", "risk", "evidence", "impacts",
    "files", "required_gates", "review",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def safe_relative_path(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError(f"unsafe repository path: {raw}")
    normalized = path.as_posix()
    if any(
        normalized.startswith(prefix) if prefix.endswith("/") else normalized == prefix
        for prefix in PROTECTED_PREFIXES
    ):
        raise ValueError(f"protected repository path: {raw}")
    if not any(
        normalized.startswith(prefix) if prefix.endswith("/") else normalized == prefix
        for prefix in ALLOWED_PREFIXES
    ):
        raise ValueError(f"path is outside candidate allowlist: {raw}")
    return path


def validate_official_url(url: str, *, vendor: str) -> None:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or host not in ALLOWED_HOSTS:
        raise ValueError(f"source URL is not allowlisted: {url}")
    if host == "github.com":
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) < 2 or parts[0] not in ALLOWED_GITHUB_ORGS:
            raise ValueError(f"GitHub organization is not allowlisted: {url}")
        if vendor not in GITHUB_VENDOR_ORGS or parts[0] not in GITHUB_VENDOR_ORGS[vendor]:
            raise ValueError(f"GitHub organization does not match vendor {vendor}: {url}")
    if host == "job-boards.greenhouse.io" and not parsed.path.startswith("/anthropic/"):
        raise ValueError(f"Greenhouse source is not an Anthropic posting: {url}")
    if host in {"google.com", "www.google.com"} and not parsed.path.startswith("/about/careers/"):
        raise ValueError(f"Google source is not a Google Careers posting: {url}")
    vendor_hosts = {
        "google": {"adk.dev", "cloud.google.com", "developers.google.com", "docs.cloud.google.com", "github.com", "google.com", "www.google.com"},
        "openai": {"openai.com", "platform.openai.com", "github.com"},
        "anthropic": {"anthropic.com", "www.anthropic.com", "docs.anthropic.com", "github.com", "job-boards.greenhouse.io"},
    }
    if vendor not in vendor_hosts or host not in vendor_hosts[vendor]:
        raise ValueError(f"source host does not match vendor {vendor}: {url}")


def required_gates(risk: Risk) -> set[str]:
    gates = {"research", "repository", "citations", "independent-review"}
    if risk in {Risk.MEDIUM, Risk.HIGH, Risk.CRITICAL}:
        gates.update({"implementation", "fde-usability"})
    if risk in {Risk.HIGH, Risk.CRITICAL}:
        gates.update({"security", "operations", "rollback"})
    if risk is Risk.CRITICAL:
        gates.add("authorized-risk-owner")
    return gates


def _has_relative_symlink(root: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def validate_manifest(manifest: dict[str, Any], candidate_dir: Path) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_MANIFEST_FIELDS - set(manifest)
    if missing:
        return [f"manifest missing fields: {sorted(missing)}"]
    try:
        risk = Risk(str(manifest["risk"]))
    except ValueError:
        errors.append("invalid risk")
        risk = Risk.CRITICAL
    evidence_ids: set[str] = set()
    google_evidence_ids: set[str] = set()
    receipt_path = candidate_dir / "_evidence-receipts.json"
    try:
        receipts_value = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipts = {
            (str(item["vendor"]), str(item["url"]), str(item["content_sha256"]))
            for item in receipts_value
            if isinstance(item, dict)
        }
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        receipts = set()
        errors.append("trusted evidence receipts are missing or invalid")
    evidence = manifest.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence must be a non-empty list")
    else:
        for index, item in enumerate(evidence):
            try:
                if not isinstance(item, dict):
                    raise ValueError("must be an object")
                source_id = str(item["source_id"])
                vendor = str(item["vendor"])
                validate_official_url(str(item["url"]), vendor=vendor)
                if not str(item.get("locator", "")).strip():
                    raise ValueError("locator is required")
                if not re.fullmatch(r"[0-9a-f]{64}", str(item.get("content_sha256", ""))):
                    raise ValueError("content_sha256 must be lowercase SHA-256")
                if not str(item.get("retrieved_at", "")).strip():
                    raise ValueError("retrieved_at is required")
                if not isinstance(item.get("tier"), int) or not 1 <= item["tier"] <= 5:
                    raise ValueError("tier must be 1..5")
                if not str(item.get("maturity", "")).strip() or not str(item.get("supports", "")).strip():
                    raise ValueError("maturity and supports are required")
                receipt = (vendor, str(item["url"]), str(item["content_sha256"]))
                if receipt not in receipts:
                    raise ValueError("evidence does not match a trusted fetch receipt")
                evidence_ids.add(source_id)
                if vendor == "google":
                    google_evidence_ids.add(source_id)
            except (KeyError, ValueError) as exc:
                errors.append(f"evidence[{index}]: {exc}")
    impacts = manifest.get("impacts")
    if not isinstance(impacts, list) or not impacts:
        errors.append("impacts must be a non-empty list")
    else:
        for index, impact in enumerate(impacts):
            try:
                if not isinstance(impact, dict):
                    raise ValueError("must be an object")
                safe_relative_path(str(impact["path"]))
                cited = set(map(str, impact.get("evidence_ids", [])))
                if not cited or not cited <= evidence_ids:
                    raise ValueError("must reference declared evidence IDs")
                if impact.get("claim_scope") == "google-product" and not cited & google_evidence_ids:
                    raise ValueError("Google product impact requires Google evidence")
            except (KeyError, ValueError) as exc:
                errors.append(f"impacts[{index}]: {exc}")
    declared_files: set[str] = set()
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        errors.append("files must be a non-empty list")
    else:
        for index, item in enumerate(files):
            try:
                if not isinstance(item, dict):
                    raise ValueError("must be an object")
                relative = safe_relative_path(str(item["path"]))
                declared_files.add(relative.as_posix())
                candidate = candidate_dir / relative
                if (
                    not candidate.is_file()
                    or candidate.is_symlink()
                    or not candidate.resolve().is_relative_to(candidate_dir.resolve())
                    or _has_relative_symlink(candidate_dir, candidate)
                ):
                    raise ValueError("candidate is missing, not a file, or a symlink")
                content = candidate.read_bytes()
                if len(content) > MAX_CANDIDATE_BYTES:
                    raise ValueError("candidate exceeds size limit")
                if sha256_bytes(content) != item.get("sha256"):
                    raise ValueError("candidate digest does not match manifest")
            except (KeyError, OSError, ValueError) as exc:
                errors.append(f"files[{index}]: {exc}")
    actual_files = {
        path.relative_to(candidate_dir).as_posix()
        for path in candidate_dir.rglob("*")
        if path.is_file() and path.name not in {"proposal.json", "_evidence-receipts.json"}
    }
    if actual_files != declared_files:
        errors.append(f"candidate file set differs from manifest: actual={sorted(actual_files)} declared={sorted(declared_files)}")
    declared_gates = set(map(str, manifest.get("required_gates", [])))
    missing_gates = required_gates(risk) - declared_gates
    if missing_gates:
        errors.append(f"required gates are missing: {sorted(missing_gates)}")
    review = manifest.get("review")
    if not isinstance(review, dict):
        errors.append("review must be an object")
    else:
        if review.get("reviewer") == manifest.get("author"):
            errors.append("reviewer must differ from author")
        if review.get("decision") != "approve-draft":
            errors.append("review decision must be approve-draft")
        if review.get("material_findings"):
            errors.append("material review findings must be resolved")
    return errors


def load_manifest(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("proposal manifest must be an object")
    return value
