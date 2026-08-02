import unittest
from fde_kit.registry import CatalogEntry, ResourceKind, validate_binding, validate_catalog


class RegistryTests(unittest.TestCase):
    def entry(self, **changes):
        values = dict(name="orders", kind=ResourceKind.AGENT, uri="https://agents.example/a2a",
                      location="us-central1", owner="orders-team", protocol="a2a")
        values.update(changes)
        return CatalogEntry(**values)

    def test_valid_catalog(self):
        self.assertEqual([], validate_catalog((self.entry(),), production=True))

    def test_insecure_duplicate_and_preview_fail(self):
        bad = self.entry(uri="http://internal", owner="", maturity="Preview")
        errors = validate_catalog((bad, bad), production=True)
        self.assertGreaterEqual(len(errors), 4)

    def test_multiregion_binding_fails(self):
        self.assertTrue(validate_binding(self.entry(location="us"), self.entry(name="target"),
                                         gateway_location="us-central1"))


if __name__ == "__main__": unittest.main()
