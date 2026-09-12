from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fde_doc_maintainer.policy import safe_relative_path, sha256_bytes, validate_manifest, validate_official_url


class PolicyTests(unittest.TestCase):
    def _candidate(self, root: Path) -> dict:
        target = root / "docs/volume-9-fde/README.md"
        target.parent.mkdir(parents=True)
        content = b"# Candidate\n"
        target.write_bytes(content)
        (root / "_evidence-receipts.json").write_text(json.dumps([{
            "source_id": "google-doc",
            "vendor": "google",
            "url": "https://docs.cloud.google.com/example",
            "content_sha256": "a" * 64,
        }]), encoding="utf-8")
        return {
            "schema_version": 1,
            "change_id": "change-1",
            "author": "author-agent",
            "risk": "medium",
            "evidence": [{
                "source_id": "google-doc",
                "vendor": "google",
                "url": "https://docs.cloud.google.com/example",
                "locator": "Section",
                "retrieved_at": "2026-08-02",
                "tier": 1,
                "maturity": "GA",
                "supports": "A bounded Google product claim",
                "content_sha256": "a" * 64,
            }],
            "impacts": [{
                "path": "docs/volume-9-fde/README.md",
                "claim_scope": "google-product",
                "evidence_ids": ["google-doc"],
            }],
            "files": [{"path": "docs/volume-9-fde/README.md", "sha256": sha256_bytes(content)}],
            "required_gates": ["research", "repository", "citations", "independent-review", "implementation", "fde-usability"],
            "review": {"reviewer": "reviewer-agent", "decision": "approve-draft", "material_findings": []},
        }

    def test_valid_candidate_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(validate_manifest(self._candidate(root), root), [])

    def test_google_careers_is_allowed_only_as_google_evidence(self) -> None:
        url = "https://www.google.com/about/careers/applications/jobs/results/143358812177212102-forward-deployed-engineer-genai-google-cloud"
        validate_official_url(url, vendor="google")
        with self.assertRaises(ValueError):
            validate_official_url(url, vendor="openai")
        with self.assertRaises(ValueError):
            validate_official_url("https://www.google.com/search?q=untrusted", vendor="google")

    def test_digest_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self._candidate(root)
            manifest["files"][0]["sha256"] = "0" * 64
            self.assertTrue(any("digest" in error for error in validate_manifest(manifest, root)))

    def test_non_google_evidence_cannot_support_google_claim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self._candidate(root)
            manifest["evidence"][0].update(vendor="openai", url="https://openai.com/index/example")
            (root / "_evidence-receipts.json").write_text(json.dumps([{
                "vendor": "openai",
                "url": "https://openai.com/index/example",
                "content_sha256": "a" * 64,
            }]), encoding="utf-8")
            self.assertTrue(any("Google product" in error for error in validate_manifest(manifest, root)))

    def test_unfetched_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self._candidate(root)
            manifest["evidence"][0]["content_sha256"] = "b" * 64
            self.assertTrue(any("trusted fetch receipt" in error for error in validate_manifest(manifest, root)))

    def test_protected_path_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            safe_relative_path(".github/workflows/release.yml")

    def test_author_cannot_review_own_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self._candidate(root)
            manifest["review"]["reviewer"] = manifest["author"]
            self.assertTrue(any("differ" in error for error in validate_manifest(manifest, root)))
