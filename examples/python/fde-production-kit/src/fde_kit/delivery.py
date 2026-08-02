"""Forward-deployed engagement evidence and stage gates."""

from __future__ import annotations

from enum import StrEnum


class Stage(StrEnum):
    FRAME = "frame"
    DISCOVER = "discover"
    DESIGN = "design"
    SLICE = "slice"
    HARDEN = "harden"
    LAUNCH = "launch"
    HANDOVER = "handover"


GATES = {
    Stage.FRAME: {"sponsor", "outcome", "scope", "decision-rights", "success-measures"},
    Stage.DISCOVER: {"workflow-map", "data-map", "identity-map", "nfrs", "raid-log"},
    Stage.DESIGN: {"adrs", "threat-model", "nfr-traceability", "cost-model"},
    Stage.SLICE: {"real-identity", "authoritative-data", "governed-tool", "telemetry", "evaluation"},
    Stage.HARDEN: {"security-tests", "load-tests", "recovery-tests", "runbooks", "supply-chain"},
    Stage.LAUNCH: {"six-reviews", "go-no-go", "rollback", "on-call", "customer-acceptance"},
    Stage.HANDOVER: {"raci", "service-catalog", "training", "competency-check", "evidence-pack"},
}


def missing_gate_evidence(stage: Stage, evidence: dict[str, bool]) -> list[str]:
    return sorted(item for item in GATES[stage] if evidence.get(item) is not True)


def next_stage(stage: Stage, evidence: dict[str, bool]) -> Stage:
    missing = missing_gate_evidence(stage, evidence)
    if missing:
        raise ValueError(f"stage {stage} blocked by {missing}")
    order = list(Stage)
    index = order.index(stage)
    return order[min(index + 1, len(order) - 1)]
