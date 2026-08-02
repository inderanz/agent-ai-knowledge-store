import unittest

from fde_kit.runtime import CapacityInput, Runtime, Workload, required_instances, select_runtime


def workload(**values):
    base = dict(adk=True, custom_container=False, kubernetes_apis_required=False,
                sidecars_required=False, privileged_or_host_access=False,
                streaming_required=False, long_lived_connection_required=False,
                region_qualified=True, managed_runtime_contract_accepted=True)
    base.update(values)
    return Workload(**base)


class RuntimeTests(unittest.TestCase):
    def test_managed_adk_fit_selects_agent_runtime(self):
        self.assertEqual(Runtime.AGENT_RUNTIME, select_runtime(workload()).runtime)

    def test_kubernetes_requirement_selects_gke(self):
        self.assertEqual(Runtime.GKE, select_runtime(workload(sidecars_required=True)).runtime)

    def test_streaming_need_selects_controlled_cloud_run_contract(self):
        self.assertEqual(Runtime.CLOUD_RUN, select_runtime(workload(streaming_required=True)).runtime)

    def test_unqualified_region_and_privilege_are_blockers(self):
        result = select_runtime(workload(region_qualified=False, privileged_or_host_access=True))
        self.assertEqual(2, len(result.blockers))

    def test_capacity_includes_headroom(self):
        self.assertEqual(17, required_instances(CapacityInput(100, 10, 80, 0.30)))

    def test_capacity_rejects_invalid_values(self):
        with self.assertRaises(ValueError):
            required_instances(CapacityInput(0, 1, 1))


if __name__ == "__main__": unittest.main()
