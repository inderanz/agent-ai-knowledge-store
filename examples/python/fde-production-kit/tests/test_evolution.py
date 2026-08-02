import unittest

from fde_kit.evolution import Severity, UpstreamChange, VersionEnvelope, affected_assets, classify, compatible


class EvolutionTests(unittest.TestCase):
    def test_security_or_removal_is_critical(self):
        self.assertEqual(Severity.CRITICAL, classify(UpstreamChange("adk", "1", "2", frozenset(), security=True)))
    def test_schema_change_is_high(self):
        self.assertEqual(Severity.HIGH, classify(UpstreamChange("adk", "1", "2", frozenset({"event-schema"}))))
    def test_dependency_map_returns_affected_assets(self):
        change = UpstreamChange("adk", "1", "2", frozenset({"session"}))
        self.assertEqual(["agent.py", "session.md"], affected_assets(change, {"adk": {"agent.py"}, "surface:session": {"session.md"}}))
    def test_topology_change_requires_event_boundary(self):
        old = VersionEnvelope(1, 1, 1, 1, 1)
        ok, blockers = compatible(old, VersionEnvelope(2, 1, 1, 1, 1))
        self.assertFalse(ok); self.assertTrue(blockers)
    def test_tool_change_requires_approval_digest_change(self):
        ok, blockers = compatible(VersionEnvelope(1,1,1,1,1), VersionEnvelope(1,1,1,2,1))
        self.assertFalse(ok); self.assertTrue(blockers)


if __name__ == "__main__": unittest.main()
