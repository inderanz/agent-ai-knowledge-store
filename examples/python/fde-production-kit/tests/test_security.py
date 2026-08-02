import unittest

from fde_kit.security import ActionContext, ActionPolicy, Decision, REQUIRED_THREAT_CONTROLS, authorize, missing_threat_controls


POLICY = ActionPolicy("tenant-a", frozenset({"agent-a"}),
                      frozenset({("crm", "read"), ("crm", "write")}),
                      frozenset({"alice"}), frozenset({("crm", "write")}))


def action(**values):
    base = dict(user="alice", agent="agent-a", tenant="tenant-a", tool="crm",
                method="read", environment="production", risk="low", parameters={})
    base.update(values)
    return ActionContext(**base)


class SecurityTests(unittest.TestCase):
    def test_low_risk_authorized_read(self): self.assertEqual(Decision.ALLOW, authorize(POLICY, action()))
    def test_high_risk_or_write_requires_approval(self):
        self.assertEqual(Decision.REQUIRE_APPROVAL, authorize(POLICY, action(method="write")))
        self.assertEqual(Decision.REQUIRE_APPROVAL, authorize(POLICY, action(risk="high")))
    def test_cross_tenant_and_unknown_method_deny(self):
        self.assertEqual(Decision.DENY, authorize(POLICY, action(tenant="tenant-b")))
        self.assertEqual(Decision.DENY, authorize(POLICY, action(method="delete")))
    def test_non_authorized_production_user_denied(self):
        self.assertEqual(Decision.DENY, authorize(POLICY, action(user="bob")))
    def test_threat_coverage_fails_closed(self):
        self.assertEqual(sorted(REQUIRED_THREAT_CONTROLS), missing_threat_controls({}))
        self.assertEqual([], missing_threat_controls({name: True for name in REQUIRED_THREAT_CONTROLS}))


if __name__ == "__main__": unittest.main()
