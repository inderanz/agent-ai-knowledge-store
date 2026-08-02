import unittest

from validate_plan import violations


def plan_with(*resources, changes=()):
    return {
        "planned_values": {"root_module": {"resources": list(resources)}},
        "resource_changes": list(changes),
    }


class PlanPolicyTest(unittest.TestCase):
    def test_rejects_fail_open_gateway_extension(self):
        plan = plan_with({
            "address": "extension.bad",
            "type": "google_network_services_authz_extension",
            "values": {"fail_open": True, "service": "iap.googleapis.com", "deletion_policy": "PREVENT"},
        })
        self.assertTrue(any("fail closed" in message for message in violations(plan, "production")))

    def test_allows_explicit_dry_run_outside_production(self):
        plan = plan_with({
            "address": "extension.audit",
            "type": "google_network_services_authz_extension",
            "values": {
                "fail_open": True,
                "service": "iap.googleapis.com",
                "deletion_policy": "PREVENT",
                "metadata": {"iamEnforcementMode": "DRY_RUN", "iapPolicyVersion": "V1"},
            },
        })
        self.assertEqual([], violations(plan, "staging"))

    def test_rejects_project_wide_agentspace_user(self):
        plan = plan_with({
            "address": "iam.bad",
            "type": "google_project_iam_member",
            "values": {"role": "roles/discoveryengine.agentspaceUser"},
        })
        self.assertTrue(violations(plan, "production"))

    def test_rejects_state_persistent_oauth_secret(self):
        plan = plan_with({
            "address": "identity.bad",
            "type": "google_agent_identity_auth_provider",
            "values": {"deletion_policy": "PREVENT", "auth_provider_type_params": [{"two_legged_oauth": [{"client_secret": "leak"}]}]},
        })
        self.assertTrue(any("state-persistent" in message for message in violations(plan, "production")))

    def test_rejects_production_replace(self):
        plan = plan_with(changes=[{
            "address": "registry.critical",
            "type": "google_agent_registry_service",
            "change": {"actions": ["delete", "create"]},
        }])
        self.assertTrue(any("deleted or replaced" in message for message in violations(plan, "production")))

    def test_accepts_enterprise_engine(self):
        plan = plan_with({
            "address": "engine.good",
            "type": "google_discovery_engine_search_engine",
            "values": {
                "app_type": "APP_TYPE_INTRANET",
                "deletion_policy": "PREVENT",
                "search_engine_config": [{"search_tier": "SEARCH_TIER_ENTERPRISE"}],
            },
        })
        self.assertEqual([], violations(plan, "production"))


if __name__ == "__main__":
    unittest.main()
