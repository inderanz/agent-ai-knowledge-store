import json
import unittest

from enterprise_adk.telemetry import make_audit_event


class TelemetryTests(unittest.TestCase):
    def test_audit_event_hashes_tenant_and_excludes_payload(self):
        event = make_audit_event(event_type="workflow.completed", request_id="r1",
                                 tenant_id="tenant-sensitive", status="SUCCEEDED",
                                 workflow_version="3.1.0", details={"attempt": 1})
        payload = json.loads(event.to_json())
        self.assertNotEqual("tenant-sensitive", payload["tenant_hash"])
        self.assertNotIn("tenant_id", payload)

    def test_sensitive_detail_keys_are_rejected(self):
        event = make_audit_event(event_type="bad", request_id="r1", tenant_id="t1",
                                 status="FAILED", workflow_version="3.1.0",
                                 details={"token": "secret"})
        with self.assertRaises(ValueError):
            event.to_json()

    def test_nested_sensitive_detail_keys_are_rejected(self):
        event = make_audit_event(event_type="bad", request_id="r1", tenant_id="t1",
                                 status="FAILED", workflow_version="3.1.0",
                                 details={"context": [{"authorization": "secret"}]})
        with self.assertRaises(ValueError):
            event.to_json()


if __name__ == "__main__":
    unittest.main()
