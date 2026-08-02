import tempfile
import unittest
from pathlib import Path

from render_config import read_environment, render
from validate_delivery import validate


class DeliveryTests(unittest.TestCase):
    def test_render_replaces_required_value(self) -> None:
        self.assertEqual(render("x=__PROJECT_ID__", {"PROJECT_ID": "customer-prod"}), "x=customer-prod")

    def test_render_rejects_missing_value(self) -> None:
        with self.assertRaises(ValueError):
            render("__PROJECT_ID__", {})

    def test_environment_rejects_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "env"
            path.write_text("A=one\nA=two\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_environment(path)

    def test_environment_rejects_yaml_injection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "env"
            path.write_text("DEV_PROJECT_ID=valid-project\nPROD_REGION=x: injected\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_environment(path)

    def test_delivery_rejects_public_member(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config"
            path.write_text("allUsers", encoding="utf-8")
            self.assertTrue(validate([path]))

    def test_delivery_requires_verified_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config"
            path.write_text("requireApproval: true\ninternal-and-cloud-load-balancing\n@sha256:\nserviceAccount:\nrun.googleapis.com/binary-authorization: default\nsupply_chain_gate.py\n", encoding="utf-8")
            self.assertIn("Cloud Build verified provenance is not required", validate([path]))


if __name__ == "__main__":
    unittest.main()
