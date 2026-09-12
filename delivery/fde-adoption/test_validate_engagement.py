from __future__ import annotations

import json
import unittest
from pathlib import Path

from validate_engagement import validate


ROOT = Path(__file__).resolve().parent


class EngagementValidationTests(unittest.TestCase):
    def test_example_is_valid_as_a_starting_record(self) -> None:
        record = json.loads((ROOT / "customer-engagement.example.json").read_text(encoding="utf-8"))
        self.assertEqual(validate(record), [])

    def test_example_cannot_claim_production(self) -> None:
        record = json.loads((ROOT / "customer-engagement.example.json").read_text(encoding="utf-8"))
        errors = validate(record, production=True)
        self.assertTrue(any("synthetic" in error for error in errors))
        self.assertTrue(any("current_level" in error for error in errors))

    def test_invalid_autonomy_is_rejected(self) -> None:
        record = json.loads((ROOT / "customer-engagement.example.json").read_text(encoding="utf-8"))
        record["use_cases"][0]["autonomy_level"] = 9
        self.assertTrue(any("autonomy" in error for error in validate(record)))

    def test_complete_customer_record_can_pass_production_contract(self) -> None:
        record = json.loads((ROOT / "customer-engagement.example.json").read_text(encoding="utf-8"))
        record.update(synthetic=False, current_level=4)
        for gate in record["gates"].values():
            gate.update(passed=True, evidence=["customer://evidence/gate"])
        record["artifacts"] = [
            {"type": name, "uri": f"customer://artifact/{name}"}
            for name in ("architecture", "evaluation", "threat-model", "runbooks", "rollback", "slo", "cost", "adoption")
        ]
        record["customer_signoffs"] = [
            {"role": role, "decision": "approve", "evidence": f"customer://signoff/{role}"}
            for role in ("product", "technical", "security", "risk", "sre")
        ]
        record["handover_competencies"] = [
            {"name": name, "passed": True, "evidence": f"customer://competency/{name}"}
            for name in ("deploy", "rollback", "evaluate-change", "diagnose", "incident", "recover", "retire")
        ]
        self.assertEqual(validate(record, production=True), [])
