import unittest

from validate_qualification import findings


def baseline() -> dict:
    return {
        "environment": "dev",
        "agent_runtime": {"project_id": "p", "region": "r"},
        "agent_registry": {"project_id": "p", "region": "r"},
        "agent_gateway": {"enabled": True, "preview_terms_accepted": True, "project_id": "p", "region": "r"},
        "agent_identity": {"enabled": True, "preview_terms_accepted": True},
        "managed_agents": {"enabled": False},
        "model_armor": {"enabled": True, "template_region": "r"},
        "owners": {name: "team" for name in ("security", "privacy", "legal", "operations", "product")},
    }


class QualificationTests(unittest.TestCase):
    def test_qualified_topology_passes(self) -> None:
        self.assertEqual(findings(baseline()), [])

    def test_gateway_region_mismatch_fails(self) -> None:
        record = baseline()
        record["agent_gateway"]["region"] = "other"
        self.assertTrue(findings(record))

    def test_managed_agents_production_fails(self) -> None:
        record = baseline()
        record["environment"] = "prod"
        record["managed_agents"] = {"enabled": True, "pre_ga_terms_accepted": True, "contains_sensitive_or_confidential_data": False}
        self.assertIn("Managed Agents are prohibited in production by this baseline", findings(record))


if __name__ == "__main__":
    unittest.main()
