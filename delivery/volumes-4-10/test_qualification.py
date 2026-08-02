import json
from pathlib import Path
import unittest

from validate_qualification import validate


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


class QualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gates = json.loads((HERE / "required-gates.json").read_text())

    def test_every_example_is_deliberately_not_production_qualified(self):
        for volume in self.gates["volumes"]:
            path = ROOT / "labs" / f"volume-{volume}" / "qualification.example.json"
            if path.exists():
                record = json.loads(path.read_text())
                self.assertTrue(validate(record, self.gates, production=True), volume)

    def test_complete_record_passes_each_volume(self):
        for volume, names in self.gates["volumes"].items():
            record = {
                "schema_version": 1, "volume": volume, "environment": "production",
                "project_id": "customer-agents-123", "location": "us-central1",
                "source_revision": "0123456789abcdef",
                "owners": {"product": "p", "security": "s", "operations": "o", "customer_acceptor": "c"},
                "evidence": {name: True for name in names},
            }
            self.assertEqual([], validate(record, self.gates, production=True), volume)

    def test_unknown_volume_fails(self):
        self.assertTrue(validate({"volume": "unknown"}, self.gates, production=False))


if __name__ == "__main__": unittest.main()
