from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from validate_plan import findings  # noqa: E402


def plan(resource_type: str, after: dict, actions: list[str] | None = None) -> dict:
    return {
        "resource_changes": [
            {
                "address": f"{resource_type}.test",
                "type": resource_type,
                "change": {"actions": actions or ["create"], "after": after},
            }
        ]
    }


class PlanPolicyTests(unittest.TestCase):
    def test_owner_role_is_rejected(self) -> None:
        self.assertTrue(
            findings(plan("google_project_iam_member", {"role": "roles/owner"}))
        )

    def test_public_member_is_rejected(self) -> None:
        self.assertTrue(
            findings(
                plan("google_cloud_run_service_iam_member", {"member": "allUsers"})
            )
        )

    def test_service_account_key_is_rejected(self) -> None:
        self.assertTrue(findings(plan("google_service_account_key", {})))

    def test_critical_delete_is_rejected(self) -> None:
        self.assertTrue(
            findings(plan("google_firestore_database", {}, ["delete"]))
        )

    def test_bounded_resource_is_allowed(self) -> None:
        self.assertFalse(
            findings(
                plan(
                    "google_project_iam_member",
                    {
                        "role": "roles/run.developer",
                        "member": "serviceAccount:deploy@example.iam.gserviceaccount.com",
                    },
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
