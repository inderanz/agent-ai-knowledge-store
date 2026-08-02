"""Deterministic application workflow surrounding ADK orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .models import ApprovalDecision, ChangeRequest, Principal, Risk, Status, utc_now
from .policy import Policy
from .tools import ToolGateway, ToolOutcome, UnknownToolOutcome


@dataclass(frozen=True, slots=True)
class WorkflowResult:
    request_id: str
    status: Status
    reason: str
    operation_id: str | None = None
    output: dict[str, Any] | None = None


class EnterpriseWorkflow:
    """Enforces authz, approval binding, and idempotent execution.

    ADK chooses and connects workflow nodes; this service owns the business
    transition invariants. A production ToolGateway must persist reservations
    and outcomes in a customer system of record before calling the target.
    """

    def __init__(self, policy: Policy, tools: ToolGateway, *, clock=utc_now) -> None:
        self._policy = policy
        self._tools = tools
        self._clock = clock

    def run(self, *, principal: Principal, request: ChangeRequest,
            approval: ApprovalDecision | None = None,
            approver_principal: Principal | None = None) -> WorkflowResult:
        try:
            effective_risk = self._policy.authorize_request(principal, request)
        except PermissionError as exc:
            return WorkflowResult(request.request_id, Status.DENIED, str(exc))

        if effective_risk is Risk.HIGH:
            if approval is None or approver_principal is None:
                return WorkflowResult(
                    request.request_id,
                    Status.AWAITING_APPROVAL,
                    f"approval required for digest {request.approval_digest()}",
                )
            try:
                self._policy.authorize_approver(approver_principal, request)
                if approval.approver != approver_principal.subject:
                    raise PermissionError("approval signer does not match authenticated approver")
                approval.validate_for(request, self._clock())
            except PermissionError as exc:
                return WorkflowResult(request.request_id, Status.DENIED, str(exc))

        try:
            result = self._tools.execute(request, request.idempotency_key())
        except UnknownToolOutcome as exc:
            return WorkflowResult(
                request.request_id, Status.RECONCILIATION_REQUIRED,
                "tool outcome unknown; do not retry the write blindly",
                exc.operation_id,
            )
        if result.outcome is ToolOutcome.SUCCEEDED:
            return WorkflowResult(
                request.request_id, Status.SUCCEEDED, "tool confirmed success",
                result.operation_id, result.response,
            )
        if result.outcome is ToolOutcome.UNKNOWN:
            return WorkflowResult(
                request.request_id, Status.RECONCILIATION_REQUIRED,
                "tool outcome unknown; do not retry the write blindly",
                result.operation_id,
            )
        return WorkflowResult(
            request.request_id, Status.FAILED, "tool confirmed failure",
            result.operation_id, result.response,
        )

    def reconcile(self, operation_id: str) -> WorkflowResult:
        result = self._tools.reconcile(operation_id)
        status = {
            ToolOutcome.SUCCEEDED: Status.SUCCEEDED,
            ToolOutcome.FAILED: Status.FAILED,
            ToolOutcome.UNKNOWN: Status.RECONCILIATION_REQUIRED,
        }[result.outcome]
        return WorkflowResult("reconciliation", status, "reconciliation result", operation_id, result.response)


def bounded_repair(initial: Any, *, validate, repair, max_attempts: int = 2) -> Any:
    """Bounded repair helper; raises instead of creating an unbounded model loop."""
    if max_attempts < 0 or max_attempts > 5:
        raise ValueError("max_attempts must be between 0 and 5")
    candidate = initial
    for attempt in range(max_attempts + 1):
        errors = list(validate(candidate))
        if not errors:
            return candidate
        if attempt == max_attempts:
            raise ValueError(f"repair budget exhausted: {errors}")
        candidate = repair(candidate, errors)
    raise AssertionError("unreachable")
