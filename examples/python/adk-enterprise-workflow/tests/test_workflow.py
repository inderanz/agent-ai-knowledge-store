from datetime import datetime, timedelta, timezone
import unittest

from enterprise_adk.models import ApprovalDecision, ChangeRequest, Principal, Risk, Status
from enterprise_adk.policy import Policy
from enterprise_adk.tools import InMemoryToolGateway, ToolOutcome, UnknownToolOutcome
from enterprise_adk.workflow import EnterpriseWorkflow, bounded_repair


NOW = datetime(2026, 8, 2, 1, 0, tzinfo=timezone.utc)
REQUESTER = Principal("requester", frozenset({"change-executors"}))
APPROVER = Principal("approver", frozenset({"change-approvers"}))


def policy(**overrides):
    values = dict(
        tenant_id="tenant-a",
        allowed_actions=frozenset({"read-status", "rotate-key"}),
        executor_group="change-executors",
        approval_group="change-approvers",
        force_approval_actions=frozenset({"rotate-key"}),
        deny_all=False,
    )
    values.update(overrides)
    return Policy(**values)


def request(action="rotate-key", risk=Risk.HIGH, **overrides):
    values = dict(request_id="change-1", tenant_id="tenant-a", action=action,
                  target="service-a", justification="Customer-approved test",
                  risk=risk, parameters={}, requested_by="requester")
    values.update(overrides)
    return ChangeRequest(**values)


def approval(req, approver="approver"):
    return ApprovalDecision(
        request_id=req.request_id, tenant_id=req.tenant_id,
        action_digest=req.approval_digest(), approver=approver, approved=True,
        issued_at=NOW - timedelta(minutes=1), expires_at=NOW + timedelta(minutes=10),
        decision_id="decision-1",
    )


class WorkflowTests(unittest.TestCase):
    def test_deny_all_fails_closed(self):
        flow = EnterpriseWorkflow(policy(deny_all=True), InMemoryToolGateway(), clock=lambda: NOW)
        self.assertEqual(Status.DENIED, flow.run(principal=REQUESTER, request=request()).status)

    def test_low_risk_allowlisted_action_executes(self):
        tools = InMemoryToolGateway()
        flow = EnterpriseWorkflow(policy(), tools, clock=lambda: NOW)
        result = flow.run(principal=REQUESTER, request=request("read-status", Risk.LOW))
        self.assertEqual(Status.SUCCEEDED, result.status)
        self.assertEqual(1, tools.calls)

    def test_policy_can_force_approval_despite_claimed_low_risk(self):
        flow = EnterpriseWorkflow(policy(), InMemoryToolGateway(), clock=lambda: NOW)
        result = flow.run(principal=REQUESTER, request=request(risk=Risk.LOW))
        self.assertEqual(Status.AWAITING_APPROVAL, result.status)

    def test_high_risk_requires_authenticated_approver(self):
        req = request()
        flow = EnterpriseWorkflow(policy(), InMemoryToolGateway(), clock=lambda: NOW)
        self.assertEqual(Status.AWAITING_APPROVAL, flow.run(principal=REQUESTER, request=req).status)
        wrong = Principal("approver", frozenset({"other"}))
        result = flow.run(principal=REQUESTER, request=req, approval=approval(req), approver_principal=wrong)
        self.assertEqual(Status.DENIED, result.status)

    def test_high_risk_approved_execution(self):
        req = request()
        flow = EnterpriseWorkflow(policy(), InMemoryToolGateway(), clock=lambda: NOW)
        result = flow.run(principal=REQUESTER, request=req, approval=approval(req), approver_principal=APPROVER)
        self.assertEqual(Status.SUCCEEDED, result.status)

    def test_idempotency_prevents_duplicate_side_effect(self):
        tools = InMemoryToolGateway()
        flow = EnterpriseWorkflow(policy(), tools, clock=lambda: NOW)
        req = request("read-status", Risk.LOW)
        first = flow.run(principal=REQUESTER, request=req)
        second = flow.run(principal=REQUESTER, request=req)
        self.assertEqual(first.operation_id, second.operation_id)
        self.assertEqual(1, tools.calls)

    def test_unknown_write_outcome_requires_reconciliation(self):
        tools = InMemoryToolGateway([ToolOutcome.UNKNOWN])
        flow = EnterpriseWorkflow(policy(), tools, clock=lambda: NOW)
        result = flow.run(principal=REQUESTER, request=request("read-status", Risk.LOW))
        self.assertEqual(Status.RECONCILIATION_REQUIRED, result.status)
        self.assertEqual(1, tools.calls)

    def test_unknown_outcome_exception_requires_reconciliation(self):
        class RaisingGateway:
            def execute(self, request, idempotency_key):
                raise UnknownToolOutcome("target-op-123")

            def reconcile(self, operation_id):
                raise AssertionError("not called")

        flow = EnterpriseWorkflow(policy(), RaisingGateway(), clock=lambda: NOW)
        result = flow.run(principal=REQUESTER, request=request("read-status", Risk.LOW))
        self.assertEqual(Status.RECONCILIATION_REQUIRED, result.status)
        self.assertEqual("target-op-123", result.operation_id)

    def test_cross_tenant_request_denied(self):
        flow = EnterpriseWorkflow(policy(), InMemoryToolGateway(), clock=lambda: NOW)
        result = flow.run(principal=REQUESTER, request=request(tenant_id="tenant-b"))
        self.assertEqual(Status.DENIED, result.status)

    def test_repair_loop_is_bounded(self):
        with self.assertRaisesRegex(ValueError, "budget exhausted"):
            bounded_repair("bad", validate=lambda value: ["bad"],
                           repair=lambda value, errors: value, max_attempts=2)
        self.assertEqual("good", bounded_repair(
            "bad", validate=lambda value: [] if value == "good" else ["bad"],
            repair=lambda value, errors: "good", max_attempts=1))


if __name__ == "__main__":
    unittest.main()
