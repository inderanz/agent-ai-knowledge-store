import unittest

from fde_kit.delivery import GATES, Stage, missing_gate_evidence, next_stage


class DeliveryTests(unittest.TestCase):
    def test_incomplete_stage_fails(self): self.assertEqual(sorted(GATES[Stage.FRAME]), missing_gate_evidence(Stage.FRAME, {}))
    def test_complete_stage_advances(self):
        evidence = {name: True for name in GATES[Stage.FRAME]}
        self.assertEqual(Stage.DISCOVER, next_stage(Stage.FRAME, evidence))
    def test_missing_evidence_blocks_advance(self):
        with self.assertRaises(ValueError): next_stage(Stage.LAUNCH, {})
    def test_handover_is_terminal(self):
        evidence = {name: True for name in GATES[Stage.HANDOVER]}
        self.assertEqual(Stage.HANDOVER, next_stage(Stage.HANDOVER, evidence))


if __name__ == "__main__": unittest.main()
