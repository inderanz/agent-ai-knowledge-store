from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from platform_admission.models import (  # noqa: E402
    Principal,
    RequestValidationError,
    WorkloadRequest,
)
from platform_admission.policy import AdmissionError, PlatformPolicy  # noqa: E402


def policy() -> PlatformPolicy:
    return PlatformPolicy.from_mapping(
        {
            "schema_version": 1,
            "policy_version": "2026-08-02.1",
            "deny_all": False,
            "approved_regions": ["australia-southeast1"],
            "allowed_subjects": ["subject-1"],
            "required_access_level": None,
            "production_folder": "folders/100",
            "nonproduction_folder": "folders/200",
            "profiles": {
                "pooled": {
                    "allowed_risk_tiers": ["low"],
                    "required_controls": ["identity"],
                },
                "domain": {
                    "allowed_risk_tiers": ["low", "moderate", "high"],
                    "required_controls": ["identity", "audit"],
                },
                "dedicated-project": {
                    "allowed_risk_tiers": [
                        "low",
                        "moderate",
                        "high",
                        "regulated",
                    ],
                    "required_controls": ["identity", "audit", "perimeter"],
                },
            },
        }
    )


def request(**updates: object) -> WorkloadRequest:
    value: dict[str, object] = {
        "name": "claims-assistant",
        "owner_group": "claims-platform",
        "environment": "prod",
        "region": "australia-southeast1",
        "risk_tier": "high",
        "tenant_model": "dedicated-project",
        "writes_business_data": True,
        "uses_sensitive_data": True,
        "requires_agent_gateway": False,
        "requires_agent_identity": False,
        "requires_managed_agents": False,
    }
    value.update(updates)
    return WorkloadRequest.from_mapping(value)


class PolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.principal = Principal("subject-1", "fde@example.com", frozenset())

    def test_high_risk_write_requires_approval_and_reconciliation(self) -> None:
        result = policy().admit(self.principal, request())
        self.assertTrue(result.requires_human_approval)
        self.assertIn("reconciliation", result.required_controls)
        self.assertEqual(result.folder, "folders/100")

    def test_managed_agents_is_rejected_for_production(self) -> None:
        with self.assertRaisesRegex(AdmissionError, "Pre-GA"):
            policy().admit(
                self.principal, request(requires_managed_agents=True)
            )

    def test_bootstrap_policy_denies_every_request(self) -> None:
        bootstrap = PlatformPolicy.from_mapping(
            {
                **{
                    "schema_version": 1,
                    "policy_version": "2026-08-02.1",
                    "deny_all": True,
                    "approved_regions": ["australia-southeast1"],
                    "allowed_subjects": [],
                    "required_access_level": None,
                    "production_folder": "folders/0",
                    "nonproduction_folder": "folders/0",
                },
                "profiles": {
                    model: {
                        "allowed_risk_tiers": tiers,
                        "required_controls": [],
                    }
                    for model, tiers in {
                        "pooled": ["low"],
                        "domain": ["low"],
                        "dedicated-project": ["low"],
                    }.items()
                },
            }
        )
        with self.assertRaisesRegex(AdmissionError, "deny-all"):
            bootstrap.admit(self.principal, request(risk_tier="low"))

    def test_regulated_pooled_workload_is_rejected(self) -> None:
        with self.assertRaises(AdmissionError):
            policy().admit(
                self.principal,
                request(risk_tier="regulated", tenant_model="pooled"),
            )

    def test_sensitive_pooled_workload_is_rejected(self) -> None:
        with self.assertRaisesRegex(AdmissionError, "sensitive"):
            policy().admit(
                self.principal,
                request(
                    risk_tier="low",
                    tenant_model="pooled",
                    uses_sensitive_data=True,
                ),
            )

    def test_unapproved_region_is_rejected(self) -> None:
        with self.assertRaisesRegex(AdmissionError, "region"):
            policy().admit(
                self.principal, request(region="europe-west1")
            )

    def test_unknown_request_field_is_rejected(self) -> None:
        with self.assertRaisesRegex(RequestValidationError, "unknown"):
            request(extra="not-allowed")

    def test_request_hash_is_stable(self) -> None:
        self.assertEqual(request().canonical_hash(), request().canonical_hash())


if __name__ == "__main__":
    unittest.main()
