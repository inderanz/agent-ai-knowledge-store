from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from platform_admission.configuration import Settings  # noqa: E402
from platform_admission.models import Principal  # noqa: E402
from platform_admission.policy import PlatformPolicy  # noqa: E402
from platform_admission.repository import InMemoryDecisionRepository  # noqa: E402
from platform_admission.telemetry import Telemetry  # noqa: E402


class StubVerifier:
    def verify(self, encoded_jwt: str | None) -> Principal:
        if encoded_jwt != "trusted-token":
            from platform_admission.identity import IdentityError

            raise IdentityError("untrusted")
        return Principal("subject-1", "fde@example.com", frozenset())


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
                "pooled": {"allowed_risk_tiers": ["low"], "required_controls": []},
                "domain": {"allowed_risk_tiers": ["low"], "required_controls": []},
                "dedicated-project": {"allowed_risk_tiers": ["low"], "required_controls": []},
            },
        }
    )


def payload() -> dict[str, object]:
    return {
        "name": "claims-assistant",
        "owner_group": "claims-platform",
        "environment": "dev",
        "region": "australia-southeast1",
        "risk_tier": "low",
        "tenant_model": "dedicated-project",
        "writes_business_data": False,
        "uses_sensitive_data": False,
        "requires_agent_gateway": False,
        "requires_agent_identity": False,
        "requires_managed_agents": False,
    }


@unittest.skipUnless(importlib.util.find_spec("flask"), "Flask is installed in CI/container validation")
class HttpAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from platform_admission.app import create_app

        settings = Settings(
            project_id="customer-project",
            iap_expected_audience="expected-audience",
            policy_path=Path("unused"),
            subject_hash_key=b"x" * 32,
            firestore_collection="test",
            repository_backend="memory",
            otel_enabled=False,
            otel_required=False,
            trace_sample_ratio=0.0,
            otlp_endpoint="unused",
        )
        cls.client = create_app(
            settings=settings,
            policy=policy(),
            repository=InMemoryDecisionRepository(),
            verifier=StubVerifier(),
            telemetry=Telemetry(),
        ).test_client()

    def test_missing_iap_assertion_is_denied(self) -> None:
        response = self.client.post(
            "/v1/admissions",
            headers={"Idempotency-Key": "11111111-1111-4111-8111-111111111111"},
            json=payload(),
        )
        self.assertEqual(response.status_code, 403)

    def test_authenticated_request_and_replay(self) -> None:
        headers = {
            "X-Goog-IAP-JWT-Assertion": "trusted-token",
            "Idempotency-Key": "22222222-2222-4222-8222-222222222222",
        }
        created = self.client.post("/v1/admissions", headers=headers, json=payload())
        replayed = self.client.post("/v1/admissions", headers=headers, json=payload())
        self.assertEqual(created.status_code, 201)
        self.assertEqual(replayed.status_code, 200)
        self.assertFalse(replayed.get_json()["created"])


if __name__ == "__main__":
    unittest.main()

