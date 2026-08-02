from pathlib import Path
import unittest

from evaluate_release import evaluate


ROOT = Path(__file__).resolve().parents[1]


class EvaluationTests(unittest.TestCase):
    def test_release_suite_passes_every_deterministic_case(self):
        report = evaluate(ROOT / "evals" / "release_cases.json")
        self.assertTrue(report["passed"])
        self.assertEqual(1.0, report["pass_rate"])
        self.assertEqual(5, len(report["results"]))


if __name__ == "__main__":
    unittest.main()
