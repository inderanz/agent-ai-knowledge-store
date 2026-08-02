import unittest

from deploy import build_config


class DeployConfigTests(unittest.TestCase):
    def test_config_pins_adk_and_agent_platform_sdk(self):
        result = build_config("customer-agents-123", "us-central1",
                              "gs://customer-agents-staging", None)
        self.assertEqual(
            ["google-adk==2.6.1", "google-cloud-aiplatform[agent_engines,adk]==1.163.0"],
            result["config"]["requirements"],
        )

    def test_rejects_implicit_bucket_or_cross_project_identity(self):
        with self.assertRaises(ValueError):
            build_config("customer-agents-123", "us-central1", "bucket", None)
        with self.assertRaises(ValueError):
            build_config("customer-agents-123", "us-central1", "gs://valid-bucket",
                         "runtime@other-project.iam.gserviceaccount.com")


if __name__ == "__main__":
    unittest.main()
