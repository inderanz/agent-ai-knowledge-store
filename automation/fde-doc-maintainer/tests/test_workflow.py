from __future__ import annotations

import unittest

from fde_doc_maintainer.models import ChangeSignal, GateResult, MaintenanceState
from fde_doc_maintainer.workflow import MaintenanceWorkflow


class WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = MaintenanceWorkflow()

    def test_complete_qualification_stops_at_human_review(self) -> None:
        signal = ChangeSignal.from_dict({"change_id": "c1", "detected_at": "2026-08-02", "findings": [{"kind": "release-drift"}]})
        self.assertEqual(self.workflow.detect(signal).state, MaintenanceState.RESEARCH_REQUIRED)
        self.assertEqual(self.workflow.research("c1", evidence_count=2, unknowns=[]).state, MaintenanceState.IMPACT_REQUIRED)
        self.assertEqual(self.workflow.assess_impact("c1", impact_count=1).state, MaintenanceState.CANDIDATE_REQUIRED)
        self.assertEqual(self.workflow.stage_candidate("c1", file_count=1, review_decision="approve-draft").state, MaintenanceState.QUALIFICATION_REQUIRED)
        result = self.workflow.qualify("c1", [GateResult("repository", True, "run-1")])
        self.assertEqual(result.state, MaintenanceState.HUMAN_REVIEW_REQUIRED)

    def test_failed_gate_rejects_candidate(self) -> None:
        result = self.workflow.qualify("c1", [GateResult("security", False, "finding")])
        self.assertEqual(result.state, MaintenanceState.REJECTED)

    def test_blocking_unknown_rejects_research(self) -> None:
        result = self.workflow.research("c1", evidence_count=1, unknowns=["BLOCKING: maturity unknown"])
        self.assertEqual(result.state, MaintenanceState.REJECTED)
