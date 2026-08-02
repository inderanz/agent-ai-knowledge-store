from datetime import date
import unittest

from fde_kit.reference import validate_catalog, validate_entry


def entry(**values):
    base = dict(id="runtime", fact="Python-only deployment", classification="official",
                source_url="https://docs.cloud.google.com/example", verified_at="2026-08-02",
                review_interval_days=7, owner="volume-7", maturity="GA", regions=[],
                limitations=["verify current location"], validation="weekly source check")
    base.update(values)
    return base


class ReferenceTests(unittest.TestCase):
    def test_valid_entry(self): self.assertEqual([], validate_entry(entry(), date(2026, 8, 2)))
    def test_unapproved_domain_rejected(self):
        self.assertTrue(validate_entry(entry(source_url="https://example.com/fact"), date(2026, 8, 2)))
    def test_stale_entry_rejected(self):
        self.assertIn("entry freshness is invalid", validate_entry(entry(verified_at="2026-07-01"), date(2026, 8, 2)))
    def test_duplicate_catalog_id_rejected(self):
        errors = validate_catalog({"schema_version": 1, "entries": [entry(), entry()]}, date(2026, 8, 2))
        self.assertTrue(any("duplicate" in error for error in errors))


if __name__ == "__main__": unittest.main()
