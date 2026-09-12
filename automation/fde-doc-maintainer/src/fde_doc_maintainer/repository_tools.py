"""Bounded tools exposed to maintainer agents and the draft-PR workflow."""

from __future__ import annotations

import json
import os
import re
import shutil
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Any

from .policy import MAX_CANDIDATE_BYTES, load_manifest, safe_relative_path, sha256_bytes, validate_manifest, validate_official_url

READ_ROOT_FILES = {"README.md", "SUMMARY.md", "ROADMAP.md"}
READ_DIRECTORY_PREFIXES = {
    "docs", "diagrams", "assets", "examples", "terraform", "delivery", "labs",
    "operations", "references", "skills",
}
DENIED_READ_FILENAMES = {
    "application_default_credentials.json", "credentials.json", "service-account.json",
    "service_account.json", "terraform.tfstate", "terraform.tfstate.backup",
}
DENIED_READ_SUFFIXES = {".key", ".pem", ".p12", ".pfx", ".tfstate", ".tfvars"}


def _read_allowed(relative: PurePosixPath) -> bool:
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        return False
    if any(part.startswith(".") for part in relative.parts):
        return False
    if len(relative.parts) == 1:
        return relative.as_posix() in READ_ROOT_FILES
    if relative.parts[0] not in READ_DIRECTORY_PREFIXES:
        return False
    lowered = relative.name.lower()
    if lowered in DENIED_READ_FILENAMES or lowered.startswith("gha-creds-"):
        return False
    return not any(lowered.endswith(suffix) for suffix in DENIED_READ_SUFFIXES)


def _root() -> Path:
    path = Path(os.environ["FDE_REPOSITORY_ROOT"]).resolve()
    if not (path / ".git").exists():
        raise ValueError("FDE_REPOSITORY_ROOT must be a Git checkout")
    return path


def _candidate_root() -> Path:
    path = Path(os.environ["FDE_CANDIDATE_DIR"]).resolve()
    repository = _root()
    if path == repository or path.is_relative_to(repository):
        raise ValueError("candidate directory must be outside the repository checkout")
    path.mkdir(parents=True, exist_ok=True)
    return path


def _reject_symlink_chain(root: Path, path: Path) -> None:
    relative = path.relative_to(root)
    current = root
    for part in relative.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise ValueError(f"symlink path component is not allowed: {current}")


def _read_path(raw: str) -> Path:
    relative = PurePosixPath(raw)
    if not _read_allowed(relative):
        raise ValueError("read path is outside allowlist")
    path = _root() / relative
    _reject_symlink_chain(_root(), path)
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(_root()):
        raise ValueError("read path is not a regular file")
    return path


def list_repository_files(prefix: str) -> list[str]:
    """List regular repository files under an allowlisted prefix."""
    relative = PurePosixPath(prefix)
    if (
        relative.is_absolute()
        or not relative.parts
        or ".." in relative.parts
        or any(part.startswith(".") for part in relative.parts)
    ):
        raise ValueError("unsafe list prefix")
    if relative.parts[0] not in READ_DIRECTORY_PREFIXES:
        raise ValueError("list prefix is outside allowlist")
    base = _root() / relative
    _reject_symlink_chain(_root(), base)
    if not base.is_dir() or base.is_symlink() or not base.resolve().is_relative_to(_root()):
        raise ValueError("list prefix is not a directory")
    return sorted(
        path.relative_to(_root()).as_posix()
        for path in base.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and _read_allowed(PurePosixPath(path.relative_to(_root()).as_posix()))
    )[:2000]


def read_repository_file(relative_path: str) -> dict[str, Any]:
    """Read one allowlisted UTF-8 repository file with its content digest."""
    path = _read_path(relative_path)
    content = path.read_bytes()
    if len(content) > MAX_CANDIDATE_BYTES:
        raise ValueError("repository file exceeds read limit")
    return {"path": relative_path, "sha256": sha256_bytes(content), "content": content.decode("utf-8")}


def fetch_official_source(url: str, vendor: str) -> dict[str, Any]:
    """Fetch one allowlisted official source with a bounded response."""
    validate_official_url(url, vendor=vendor)
    request = urllib.request.Request(url, headers={"User-Agent": "enterprise-handbook-maintainer/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        validate_official_url(response.geturl(), vendor=vendor)
        content_type = response.headers.get_content_type()
        if content_type not in {"text/html", "text/plain", "application/json", "text/markdown"}:
            raise ValueError(f"unsupported official-source content type: {content_type}")
        content = response.read(MAX_CANDIDATE_BYTES + 1)
    if len(content) > MAX_CANDIDATE_BYTES:
        raise ValueError("official source exceeds fetch limit")
    text = content.decode("utf-8", errors="replace")
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    digest = sha256_bytes(content)
    receipt_path = _candidate_root() / "_evidence-receipts.json"
    if receipt_path.exists():
        receipts = json.loads(receipt_path.read_text(encoding="utf-8"))
    else:
        receipts = []
    receipt = {"url": url, "vendor": vendor, "content_sha256": digest}
    if receipt not in receipts:
        receipts.append(receipt)
    receipt_path.write_text(json.dumps(receipts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"url": url, "vendor": vendor, "sha256": digest, "content": text}


def stage_candidate_file(relative_path: str, content: str) -> dict[str, Any]:
    """Stage one declared candidate file outside the repository checkout."""
    relative = safe_relative_path(relative_path)
    encoded = content.encode("utf-8")
    if len(encoded) > MAX_CANDIDATE_BYTES:
        raise ValueError("candidate exceeds size limit")
    target = _candidate_root() / relative
    _reject_symlink_chain(_candidate_root(), target)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(encoded)
    return {"path": relative.as_posix(), "sha256": sha256_bytes(encoded), "bytes": len(encoded)}


def record_proposal(manifest_json: str) -> dict[str, Any]:
    """Record an author proposal; full review validation occurs later."""
    value = json.loads(manifest_json)
    if not isinstance(value, dict):
        raise ValueError("manifest must be an object")
    value.setdefault("review", {"reviewer": "pending", "decision": "pending", "material_findings": ["independent review pending"]})
    path = _candidate_root() / "proposal.json"
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"path": str(path), "sha256": sha256_bytes(path.read_bytes())}


def read_candidate_bundle() -> dict[str, Any]:
    """Read the author manifest and candidate-file digests for independent review."""
    root = _candidate_root()
    manifest = load_manifest(root / "proposal.json")
    files = {
        path.relative_to(root).as_posix(): sha256_bytes(path.read_bytes())
        for path in root.rglob("*") if path.is_file() and path.name not in {"proposal.json", "_evidence-receipts.json"}
    }
    return {"manifest": manifest, "files": files}


def record_review(reviewer: str, decision: str, material_findings: list[str], notes: list[str]) -> dict[str, Any]:
    """Record the independent agent review without granting publication approval."""
    if decision not in {"approve-draft", "reject"}:
        raise ValueError("decision must be approve-draft or reject")
    path = _candidate_root() / "proposal.json"
    manifest = load_manifest(path)
    if reviewer == manifest.get("author"):
        raise ValueError("reviewer must differ from author")
    manifest["review"] = {
        "reviewer": reviewer,
        "decision": decision,
        "material_findings": list(material_findings),
        "notes": list(notes),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    errors = validate_manifest(manifest, _candidate_root()) if decision == "approve-draft" else []
    return {"recorded": True, "validation_errors": errors}


def apply_candidate_for_draft(repository_root: Path, candidate_dir: Path) -> list[str]:
    """Apply a validated candidate to a checkout intended only for a draft PR."""
    manifest = load_manifest(candidate_dir / "proposal.json")
    errors = validate_manifest(manifest, candidate_dir)
    if errors:
        raise ValueError("candidate failed policy: " + "; ".join(errors))
    changed: list[str] = []
    for item in manifest["files"]:
        relative = safe_relative_path(str(item["path"]))
        source = candidate_dir / relative
        destination = repository_root / relative
        _reject_symlink_chain(repository_root, destination)
        if destination.is_symlink() or not destination.parent.resolve().is_relative_to(repository_root.resolve()):
            raise ValueError(f"destination escapes through a symlink: {relative}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        changed.append(relative.as_posix())
    return sorted(changed)
