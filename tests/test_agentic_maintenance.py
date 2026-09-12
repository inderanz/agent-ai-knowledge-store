from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
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


load_script("check_sources")
render_upstream_status = load_script("render_upstream_status")
build_maintenance_signal = load_script("build_maintenance_signal")
validate_skills = load_script("validate_skills")


class SignalTests(unittest.TestCase):
    def test_release_drift_is_prioritized_and_bounded(self) -> None:
        registry = {"sources": [{"id": "stale", "owner": "volume-9-fde", "url": "https://example", "verified_at": "2026-01-01", "review_interval_days": 1}]}
        versions = {"baselines": {"google-adk-python": {"version": "1.0.0"}}}
        observed = {"google-adk-python": render_upstream_status.ObservedRelease("1.1.0", "https://github.com/google/adk-python/releases/tag/v1.1.0")}
        signal = build_maintenance_signal.build_signal(registry, versions, observed, date(2026, 1, 10), limit=1)
        self.assertTrue(signal["actionable"])
        self.assertEqual(signal["findings"][0]["kind"], "release-drift")
        self.assertEqual(signal["overflow_count"], 1)

    def test_current_offline_registry_has_no_signal_on_verified_date(self) -> None:
        registry = json.loads((ROOT / "references/sources.json").read_text(encoding="utf-8"))
        versions = json.loads((ROOT / "references/versions.json").read_text(encoding="utf-8"))
        signal = build_maintenance_signal.build_signal(registry, versions, {}, date(2026, 8, 2), limit=12)
        self.assertFalse(signal["actionable"])


class SkillValidationTests(unittest.TestCase):
    def test_repository_skills_are_valid(self) -> None:
        errors = []
        for path in (ROOT / "skills").iterdir():
            if path.is_dir():
                errors.extend(validate_skills.validate_skill(path))
        self.assertEqual(errors, [])
