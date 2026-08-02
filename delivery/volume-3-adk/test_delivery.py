from pathlib import Path
import tempfile
import unittest

from validate_delivery import validate


ROOT = Path(__file__).resolve().parent


class DeliveryTests(unittest.TestCase):
    def test_checked_in_build_passes(self):
        self.assertEqual([], validate(ROOT / "cloudbuild.yaml"))

    def test_mutable_or_deploying_build_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.yaml"
            path.write_text("image: latest\ncommand: agent_engines.create\n", encoding="utf-8")
            errors = validate(path)
        self.assertTrue(any("latest" in error for error in errors))
        self.assertTrue(any("must not create" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
