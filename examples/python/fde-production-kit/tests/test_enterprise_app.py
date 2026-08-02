import unittest
from fde_kit.enterprise_app import DataStore, EnterpriseApp, qualify_app


class EnterpriseAppTests(unittest.TestCase):
    def app(self, **changes):
        store = DataStore("knowledge", "global", "projects/p/locations/global/keyRings/r/cryptoKeys/k", True, "same-domain")
        values = dict(app_id="employee-assistant", location="global", data_stores=(store,),
                      app_level_iam=True, broad_project_role_removed=True,
                      observability_enabled=True)
        values.update(changes)
        return EnterpriseApp(**values)

    def test_qualified_app(self): self.assertEqual([], qualify_app(self.app(), production=True))
    def test_location_and_access_fail(self):
        bad = DataStore("bad", "eu", None, False, "same-domain")
        self.assertGreaterEqual(len(qualify_app(self.app(data_stores=(bad,)), production=True)), 2)
    def test_registry_import_requires_gateway(self):
        self.assertTrue(qualify_app(self.app(registry_imports=("mcp/crm",)), production=True))


if __name__ == "__main__": unittest.main()
