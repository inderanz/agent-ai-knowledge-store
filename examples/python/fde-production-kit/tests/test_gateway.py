import unittest
from fde_kit.gateway import GatewayMode, GatewayRoute, qualify_route


class GatewayTests(unittest.TestCase):
    def route(self, **changes):
        values = dict(name="orders-egress", mode=GatewayMode.EGRESS, source="orders",
                      destination="crm", destination_registered=True, agent_identity=True,
                      request_authorization=True, content_authorization=True,
                      audit_logging=True, fail_open=False, dry_run=False)
        values.update(changes)
        return GatewayRoute(**values)

    def test_production_route_passes(self): self.assertEqual([], qualify_route(self.route(), production=True))
    def test_unregistered_and_fail_open_rejected(self):
        self.assertGreaterEqual(len(qualify_route(self.route(destination_registered=False, fail_open=True), production=True)), 2)
    def test_dry_run_not_enforcement(self): self.assertTrue(qualify_route(self.route(dry_run=True), production=True))


if __name__ == "__main__": unittest.main()
