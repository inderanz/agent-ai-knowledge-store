from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validate_repository = load_script("validate_repository")
check_sources = load_script("check_sources")
render_upstream_status = load_script("render_upstream_status")


class RepositoryValidationTests(unittest.TestCase):
    def test_current_repository_is_valid(self) -> None:
        self.assertEqual(validate_repository.validate_repository(ROOT), [])

    def test_broken_relative_link_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in validate_repository.REQUIRED_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                if path.suffix == ".json":
                    path.write_text("{}", encoding="utf-8")
                else:
                    path.write_text("# Test\n", encoding="utf-8")
            for relative in validate_repository.REQUIRED_DIRECTORIES:
                (root / relative).mkdir(parents=True, exist_ok=True)
            for number in range(1, 11):
                volume = root / f"docs/volume-{number}-test"
                volume.mkdir(parents=True)
                (volume / "README.md").write_text("[missing](nope.md)\n", encoding="utf-8")
            errors = validate_repository.validate_repository(root)
            self.assertTrue(any("broken local link" in error for error in errors))


class SourceValidationTests(unittest.TestCase):
    def test_stale_source_is_detected(self) -> None:
        registry = {
            "sources": [
                {
                    "id": "test",
                    "verified_at": "2026-01-01",
                    "review_interval_days": 7,
                }
            ]
        }
        findings = check_sources.freshness_findings(registry, date(2026, 1, 10))
        self.assertEqual(len(findings), 1)
        self.assertIn("stale", findings[0].message)

    def test_source_registry_is_current(self) -> None:
        registry = json.loads((ROOT / "references/sources.json").read_text(encoding="utf-8"))
        self.assertEqual(check_sources.freshness_findings(registry, date(2026, 8, 2)), [])

    def test_release_drift_is_detected(self) -> None:
        versions = {
            "baselines": {
                baseline_id: {"version": "1.0.0"}
                for baseline_id in check_sources.RELEASE_APIS
            }
        }
        with patch.object(
            check_sources, "fetch_json", return_value={"tag_name": "v1.0.1"}
        ):
            findings = check_sources.release_findings(versions, timeout=1.0)
        self.assertEqual(len(findings), len(check_sources.RELEASE_APIS))
        self.assertTrue(all("differs" in finding.message for finding in findings))


class UpstreamStatusTests(unittest.TestCase):
    def test_report_distinguishes_observation_from_baseline(self) -> None:
        registry = {
            "sources": [{
                "id": "official-doc",
                "verified_at": "2026-01-01",
                "review_interval_days": 7,
            }]
        }
        versions = {
            "baselines": {
                baseline_id: {"version": "1.0.0"}
                for baseline_id in check_sources.RELEASE_APIS
            }
        }
        observed = {
            baseline_id: render_upstream_status.ObservedRelease(
                "1.0.1", "https://github.com/example/releases/tag/v1.0.1"
            )
            for baseline_id in check_sources.RELEASE_APIS
        }
        report = render_upstream_status.render_report(
            registry, versions, observed, date(2026, 1, 10)
        )
        self.assertIn("observation report, not the qualified repository baseline", report)
        self.assertIn("REVIEW REQUIRED", report)
        self.assertIn("2 day(s) overdue", report)

    def test_current_release_is_reported_current(self) -> None:
        versions = {
            "baselines": {
                baseline_id: {"version": "1.0.0"}
                for baseline_id in check_sources.RELEASE_APIS
            }
        }
        observed = {
            baseline_id: render_upstream_status.ObservedRelease(
                "1.0.0", "https://github.com/example/releases/tag/v1.0.0"
            )
            for baseline_id in check_sources.RELEASE_APIS
        }
        report = render_upstream_status.render_report(
            {"sources": []}, versions, observed, date(2026, 1, 1)
        )
        self.assertNotIn("REVIEW REQUIRED", report)
        self.assertIn("| Release drifts requiring review | 0 |", report)


if __name__ == "__main__":
    unittest.main()
