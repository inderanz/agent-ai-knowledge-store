import unittest

from fde_kit.industry import REQUIRED_DECISIONS, validate_overlay


def overlay(**values):
    base = dict(industry="healthcare", decisions={name: "customer-recorded" for name in REQUIRED_DECISIONS},
                autonomous_actions=[], uses_real_customer_data=False, legal_approval_recorded=True)
    base.update(values)
    return base


class IndustryTests(unittest.TestCase):
    def test_complete_synthetic_overlay(self): self.assertEqual([], validate_overlay(overlay()))
    def test_prohibited_healthcare_autonomy_rejected(self):
        self.assertTrue(validate_overlay(overlay(autonomous_actions=["autonomous-diagnosis"])))
    def test_missing_customer_decisions_rejected(self):
        self.assertTrue(validate_overlay(overlay(decisions={})))
    def test_real_data_and_missing_legal_approval_rejected(self):
        self.assertEqual(2, len(validate_overlay(overlay(uses_real_customer_data=True, legal_approval_recorded=False))))


if __name__ == "__main__": unittest.main()
