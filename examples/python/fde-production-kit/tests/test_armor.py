import unittest
from fde_kit.armor import ArmorAction, ArmorRule, evaluate_ip, validate_policy


class ArmorTests(unittest.TestCase):
    def test_priority_order(self):
        rules = (ArmorRule(100, ArmorAction.DENY, ("203.0.113.0/24",), False),
                 ArmorRule(2147483647, ArmorAction.ALLOW, (), False))
        self.assertEqual(ArmorAction.DENY, evaluate_ip(rules, "203.0.113.9"))
        self.assertEqual(ArmorAction.ALLOW, evaluate_ip(rules, "198.51.100.9"))
        self.assertEqual([], validate_policy(rules, logging_enabled=True, attached_backend=True, production=True))

    def test_duplicate_invalid_and_unattached_fail(self):
        rules = (ArmorRule(100, ArmorAction.ALLOW, ("bad",), True), ArmorRule(100, ArmorAction.DENY))
        self.assertGreaterEqual(len(validate_policy(rules, logging_enabled=False, attached_backend=False, production=True)), 4)


if __name__ == "__main__": unittest.main()
