"""Deterministic lifecycle guard around probabilistic author and reviewer agents."""

from __future__ import annotations

from dataclasses import dataclass

from .models import ChangeSignal, GateResult, MaintenanceState


@dataclass(frozen=True, slots=True)
class WorkflowResult:
    change_id: str
    state: MaintenanceState
    reason: str


class MaintenanceWorkflow:
    """Advance only on explicit evidence and preserve human publication authority."""

    def detect(self, signal: ChangeSignal) -> WorkflowResult:
        return WorkflowResult(signal.change_id, MaintenanceState.RESEARCH_REQUIRED, "official-source research required")

    def research(self, change_id: str, *, evidence_count: int, unknowns: list[str]) -> WorkflowResult:
        if evidence_count < 1:
            return WorkflowResult(change_id, MaintenanceState.REJECTED, "no official evidence")
        if any(item.startswith("BLOCKING:") for item in unknowns):
            return WorkflowResult(change_id, MaintenanceState.REJECTED, "blocking research unknown")
        return WorkflowResult(change_id, MaintenanceState.IMPACT_REQUIRED, "evidence packet ready")

    def assess_impact(self, change_id: str, *, impact_count: int) -> WorkflowResult:
        if impact_count < 1:
            return WorkflowResult(change_id, MaintenanceState.REJECTED, "no repository impact decision")
        return WorkflowResult(change_id, MaintenanceState.CANDIDATE_REQUIRED, "impact manifest ready")

    def stage_candidate(self, change_id: str, *, file_count: int, review_decision: str) -> WorkflowResult:
        if file_count < 1 or review_decision != "approve-draft":
            return WorkflowResult(change_id, MaintenanceState.REJECTED, "candidate or independent review incomplete")
        return WorkflowResult(change_id, MaintenanceState.QUALIFICATION_REQUIRED, "candidate ready for deterministic gates")

    def qualify(self, change_id: str, gates: list[GateResult]) -> WorkflowResult:
        if not gates or any(not gate.passed for gate in gates):
            return WorkflowResult(change_id, MaintenanceState.REJECTED, "one or more qualification gates failed")
        return WorkflowResult(
            change_id,
            MaintenanceState.HUMAN_REVIEW_REQUIRED,
            "agent qualification passed; human publication review is mandatory",
        )
