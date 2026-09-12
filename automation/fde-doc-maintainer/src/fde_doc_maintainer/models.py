"""Typed maintenance records shared by deterministic policy and ADK tools."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class Risk(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MaintenanceState(StrEnum):
    DETECTED = "detected"
    RESEARCH_REQUIRED = "research-required"
    IMPACT_REQUIRED = "impact-required"
    CANDIDATE_REQUIRED = "candidate-required"
    QUALIFICATION_REQUIRED = "qualification-required"
    HUMAN_REVIEW_REQUIRED = "human-review-required"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class ChangeSignal:
    change_id: str
    detected_at: str
    findings: tuple[dict[str, Any], ...]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "ChangeSignal":
        findings = value.get("findings")
        if not isinstance(findings, list) or not findings:
            raise ValueError("signal findings must be a non-empty list")
        return cls(
            change_id=str(value["change_id"]),
            detected_at=str(value["detected_at"]),
            findings=tuple(dict(item) for item in findings),
        )


@dataclass(frozen=True, slots=True)
class GateResult:
    name: str
    passed: bool
    evidence: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "GateResult":
        return cls(str(value["name"]), value.get("passed") is True, str(value.get("evidence", "")))
