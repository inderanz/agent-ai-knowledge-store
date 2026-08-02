from datetime import datetime, timedelta, timezone
import unittest

from enterprise_adk.models import ApprovalDecision, ChangeRequest, Principal, Risk


NOW = datetime(2026, 8, 2, 1, 0, tzinfo=timezone.utc)


def request(**overrides):
    values = {
        "request_id": "chg-001",
        "tenant_id": "tenant-a",
        "action": "rotate-key",
        "target": "service-api",
        "justification": "Scheduled rotation",
        "risk": Risk.HIGH,
        "parameters": {"generation": 7},
        "requested_by": "user-requester",
    }
    values.update(overrides)
    return ChangeRequest(**values)


def approval(req, **overrides):
    values = {
        "request_id": req.request_id,
        "tenant_id": req.tenant_id,
        "action_digest": req.approval_digest(),
        "approver": "user-approver",
        "approved": True,
        "issued_at": NOW - timedelta(minutes=1),
        "expires_at": NOW + timedelta(minutes=10),
        "decision_id": "decision-001",
    }
    values.update(overrides)
    return ApprovalDecision(**values)


class ModelTests(unittest.TestCase):
    def test_digest_is_canonical_and_changes_with_parameters(self):
        self.assertEqual(request(parameters={"a": 1, "b": 2}).approval_digest(),
                         request(parameters={"b": 2, "a": 1}).approval_digest())
        self.assertNotEqual(request(parameters={"a": 1}).approval_digest(),
                            request(parameters={"a": 2}).approval_digest())

    def test_rejects_unknown_or_missing_input_fields(self):
        with self.assertRaises(ValueError):
            ChangeRequest.from_dict({"request_id": "x", "surprise": True})

    def test_approval_is_bound_to_digest_and_separation_of_duties(self):
        req = request()
        approval(req).validate_for(req, NOW)
        with self.assertRaises(PermissionError):
            approval(req, approver=req.requested_by).validate_for(req, NOW)
        with self.assertRaises(PermissionError):
            approval(req).validate_for(request(parameters={"generation": 8}), NOW)

    def test_expired_approval_is_denied(self):
        req = request()
        expired = approval(req, expires_at=NOW - timedelta(seconds=1),
                           issued_at=NOW - timedelta(minutes=2))
        with self.assertRaises(PermissionError):
            expired.validate_for(req, NOW)

    def test_principal_identifiers_are_strict(self):
        Principal("user-1", frozenset({"operators"}))
        with self.assertRaises(ValueError):
            Principal("user with spaces")


if __name__ == "__main__":
    unittest.main()
