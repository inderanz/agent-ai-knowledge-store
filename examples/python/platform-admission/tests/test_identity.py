from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from platform_admission.identity import IAP_ISSUER, IapJwtVerifier, IdentityError  # noqa: E402


class IdentityTests(unittest.TestCase):
    def test_verified_claims_create_principal(self) -> None:
        verifier = IapJwtVerifier(
            "/projects/1/locations/australia-southeast1/services/admission",
            decoder=lambda token, audience: {
                "iss": IAP_ISSUER,
                "sub": "stable-subject",
                "email": "fde@example.com",
                "google": {"access_levels": ["accessPolicies/1/accessLevels/fde"]},
            },
        )
        principal = verifier.verify("signed-value")
        self.assertEqual(principal.subject, "stable-subject")
        self.assertIn(
            "accessPolicies/1/accessLevels/fde", principal.access_levels
        )

    def test_missing_signed_header_is_rejected(self) -> None:
        verifier = IapJwtVerifier("audience", decoder=lambda token, audience: {})
        with self.assertRaisesRegex(IdentityError, "missing"):
            verifier.verify(None)

    def test_wrong_issuer_is_rejected(self) -> None:
        verifier = IapJwtVerifier(
            "audience",
            decoder=lambda token, audience: {
                "iss": "attacker",
                "sub": "subject",
                "email": "fde@example.com",
            },
        )
        with self.assertRaisesRegex(IdentityError, "issuer"):
            verifier.verify("signed-value")


if __name__ == "__main__":
    unittest.main()

