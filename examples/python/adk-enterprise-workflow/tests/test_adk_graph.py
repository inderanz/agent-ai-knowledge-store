import unittest

from enterprise_adk.agent import root_agent


class AdkGraphTests(unittest.TestCase):
    def test_graph_compiles_on_pinned_adk(self):
        self.assertEqual("enterprise_change_workflow", root_agent.name)
        self.assertIsNotNone(root_agent.graph)
        names = {node.name for node in root_agent.graph.nodes}
        self.assertTrue({"normalize", "verify_identity", "verify_contract",
                         "join_checks", "route_checks", "stage_command", "deny"} <= names)
        self.assertEqual(4, root_agent.max_concurrency)


if __name__ == "__main__":
    unittest.main()
