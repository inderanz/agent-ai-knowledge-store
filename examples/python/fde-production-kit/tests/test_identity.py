import unittest
from fde_kit.identity import AuthMode, IdentityBinding, qualify_identity


class IdentityTests(unittest.TestCase):
    def binding(self, **changes):
        values = dict(agent_resource="projects/p/locations/us-central1/reasoningEngines/a",
                      mode=AuthMode.GOOGLE_CLOUD, target="projects/p/buckets/b",
                      agent_identity_enabled=True, caa_enforced=True,
                      least_privilege_reviewed=True)
        values.update(changes)
        return IdentityBinding(**values)

    def test_cloud_identity_passes(self): self.assertEqual([], qualify_identity(self.binding(), production=True))
    def test_preview_needs_exception(self): self.assertTrue(qualify_identity(self.binding(mode=AuthMode.OAUTH_3LO), production=True))
    def test_raw_secret_and_caa_opt_out_fail(self):
        self.assertGreaterEqual(len(qualify_identity(self.binding(raw_secret_visible_to_agent=True, caa_enforced=False), production=True)), 2)


if __name__ == "__main__": unittest.main()
