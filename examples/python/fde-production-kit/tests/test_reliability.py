import unittest

from fde_kit.reliability import FailureClass, RecoveryAction, RecoveryObjective, SloWindow, recovery_action, recovery_findings


class ReliabilityTests(unittest.TestCase):
    def test_sli_and_budget(self):
        value = SloWindow(good=995, valid=1000, target=0.99)
        self.assertEqual(0.995, value.sli)
        self.assertAlmostEqual(0.5, value.budget_consumed)

    def test_bad_counts_rejected(self):
        with self.assertRaises(ValueError): _ = SloWindow(2, 1, .99).sli

    def test_unknown_write_never_retries(self):
        self.assertEqual(RecoveryAction.RECONCILE, recovery_action(FailureClass.UNKNOWN_WRITE, idempotency_reserved=True))

    def test_retry_requires_reservation(self):
        self.assertEqual(RecoveryAction.FAIL, recovery_action(FailureClass.TRANSIENT_READ, idempotency_reserved=False))
        self.assertEqual(RecoveryAction.RETRY, recovery_action(FailureClass.TRANSIENT_READ, idempotency_reserved=True))

    def test_stale_restore_evidence_detected(self):
        self.assertEqual(["sessions: restore evidence is stale"], recovery_findings([RecoveryObjective("sessions", 60, 15, 91)]))


if __name__ == "__main__": unittest.main()
