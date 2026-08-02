import copy
import json
from pathlib import Path
import unittest

from validate_qualification import REQUIRED_ACCEPTANCES, REQUIRED_CONTROLS, validate


ROOT = Path(__file__).resolve().parent


class QualificationTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / "qualification.example.json").read_text())
        self.record["source_revision"] = "0123456789abcdef"
        self.record["owners"] = {key: f"customer-{key}" for key in self.record["owners"]}

    def test_example_is_not_production_qualified(self):
        self.assertTrue(validate(self.record, production=True))

    def test_complete_customer_record_passes(self):
        self.record["environment"] = "production"
        self.record["data_classification"] = "customer-confidential"
        self.record["controls"] = {key: True for key in REQUIRED_CONTROLS}
        self.record["acceptances"] = {key: True for key in REQUIRED_ACCEPTANCES}
        self.assertEqual([], validate(self.record, production=True))

    def test_version_drift_fails(self):
        record = copy.deepcopy(self.record)
        record["adk_version"] = "2.0.0"
        self.assertTrue(any("qualified value" in error for error in validate(record, production=False)))


if __name__ == "__main__":
    unittest.main()
