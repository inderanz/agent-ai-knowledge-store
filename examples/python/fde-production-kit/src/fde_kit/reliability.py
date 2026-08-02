"""SLO, error-budget, retry, and recovery calculations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class SloWindow:
    good: int
    valid: int
    target: float

    @property
    def sli(self) -> float:
        if self.valid <= 0 or not 0 <= self.good <= self.valid:
            raise ValueError("good and valid event counts are invalid")
        return self.good / self.valid

    @property
    def budget_consumed(self) -> float:
        allowed_bad = self.valid * (1 - self.target)
        actual_bad = self.valid - self.good
        return float("inf") if allowed_bad <= 0 and actual_bad else actual_bad / max(allowed_bad, 1e-12)


def burn_rate(short: SloWindow, long: SloWindow) -> tuple[float, float]:
    return short.budget_consumed, long.budget_consumed


class FailureClass(StrEnum):
    TRANSIENT_READ = "transient-read"
    CONFIRMED_NO_WRITE = "confirmed-no-write"
    UNKNOWN_WRITE = "unknown-write"
    PERMANENT = "permanent"
    POLICY = "policy"


class RecoveryAction(StrEnum):
    RETRY = "retry"
    RECONCILE = "reconcile"
    FAIL = "fail"
    DENY = "deny"


def recovery_action(failure: FailureClass, *, idempotency_reserved: bool) -> RecoveryAction:
    if failure is FailureClass.POLICY:
        return RecoveryAction.DENY
    if failure is FailureClass.UNKNOWN_WRITE:
        return RecoveryAction.RECONCILE
    if failure in {FailureClass.TRANSIENT_READ, FailureClass.CONFIRMED_NO_WRITE}:
        return RecoveryAction.RETRY if idempotency_reserved else RecoveryAction.FAIL
    return RecoveryAction.FAIL


@dataclass(frozen=True, slots=True)
class RecoveryObjective:
    name: str
    rto_minutes: int
    rpo_minutes: int
    restore_test_age_days: int


def recovery_findings(objectives: list[RecoveryObjective], *, maximum_test_age_days: int = 90) -> list[str]:
    findings: list[str] = []
    for item in objectives:
        if item.rto_minutes < 0 or item.rpo_minutes < 0:
            findings.append(f"{item.name}: negative RTO/RPO")
        if item.restore_test_age_days > maximum_test_age_days:
            findings.append(f"{item.name}: restore evidence is stale")
    return findings
