"""Idempotent side-effect boundary with explicit unknown-outcome handling."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Protocol

from .models import ChangeRequest


class ToolOutcome(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class ToolResult:
    outcome: ToolOutcome
    operation_id: str
    response: dict[str, Any]


class ToolGateway(Protocol):
    """Production implementations must durably reserve the idempotency key."""

    def execute(self, request: ChangeRequest, idempotency_key: str) -> ToolResult: ...

    def reconcile(self, operation_id: str) -> ToolResult: ...


class UnknownToolOutcome(RuntimeError):
    """Raised only when a call may have committed but confirmation was lost."""

    def __init__(self, operation_id: str) -> None:
        super().__init__("tool outcome is unknown")
        self.operation_id = operation_id


class InMemoryToolGateway:
    """Deterministic test double; never use as a production ledger."""

    def __init__(self, outcomes: list[ToolOutcome] | None = None) -> None:
        self._outcomes = list(outcomes or [ToolOutcome.SUCCEEDED])
        self._by_key: dict[str, ToolResult] = {}
        self.calls = 0

    def execute(self, request: ChangeRequest, idempotency_key: str) -> ToolResult:
        if idempotency_key in self._by_key:
            return self._by_key[idempotency_key]
        self.calls += 1
        outcome = self._outcomes.pop(0) if self._outcomes else ToolOutcome.SUCCEEDED
        result = ToolResult(
            outcome=outcome,
            operation_id=f"op-{idempotency_key[:20]}",
            response={"target": request.target, "action": request.action},
        )
        self._by_key[idempotency_key] = result
        return result

    def reconcile(self, operation_id: str) -> ToolResult:
        for result in self._by_key.values():
            if result.operation_id == operation_id:
                return result
        return ToolResult(ToolOutcome.UNKNOWN, operation_id, {})
