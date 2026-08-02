import unittest

from supply_chain_gate import findings


class SupplyChainTests(unittest.TestCase):
    def test_clean_completed_build_passes(self) -> None:
        evidence = [
            {"kind": "DISCOVERY", "discovery": {"analysisStatus": "FINISHED_SUCCESS"}},
        ]
        provenance = {"provenance_summary": {"provenance": [{"build": {"id": "abc-123-build"}}]}}
        self.assertEqual(findings(evidence, provenance, "abc-123-build"), [])

    def test_pending_scan_fails(self) -> None:
        evidence = [{"kind": "DISCOVERY", "discovery": {"analysisStatus": "SCANNING"}}]
        self.assertTrue(findings(evidence, {}, "abc-123-build"))

    def test_high_vulnerability_fails(self) -> None:
        evidence = [
            {"kind": "DISCOVERY", "discovery": {"analysisStatus": "COMPLETE"}},
            {"kind": "VULNERABILITY", "name": "CVE-test", "vulnerability": {"effectiveSeverity": "HIGH"}},
        ]
        provenance = {"provenance_summary": {"provenance": [{"build": {"id": "abc-123-build"}}]}}
        self.assertIn("HIGH vulnerability: CVE-test", findings(evidence, provenance, "abc-123-build"))


if __name__ == "__main__":
    unittest.main()
