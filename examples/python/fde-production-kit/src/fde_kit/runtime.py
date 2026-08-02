"""Runtime placement and capacity decisions with fail-closed evidence checks."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import math


class Runtime(StrEnum):
    AGENT_RUNTIME = "agent-runtime"
    CLOUD_RUN = "cloud-run"
    GKE = "gke"


@dataclass(frozen=True, slots=True)
class Workload:
    adk: bool
    custom_container: bool
    kubernetes_apis_required: bool
    sidecars_required: bool
    privileged_or_host_access: bool
    streaming_required: bool
    long_lived_connection_required: bool
    region_qualified: bool
    managed_runtime_contract_accepted: bool


@dataclass(frozen=True, slots=True)
class Placement:
    runtime: Runtime
    reasons: tuple[str, ...]
    blockers: tuple[str, ...]


def select_runtime(workload: Workload) -> Placement:
    blockers: list[str] = []
    if workload.privileged_or_host_access:
        blockers.append("agent workloads must not receive privileged or host access without exceptional review")
    if not workload.region_qualified:
        blockers.append("target location has not been qualified from current service documentation")
    if workload.kubernetes_apis_required or workload.sidecars_required:
        return Placement(Runtime.GKE, ("documented Kubernetes control is required",), tuple(blockers))
    if workload.adk and workload.managed_runtime_contract_accepted:
        if workload.streaming_required or workload.long_lived_connection_required:
            return Placement(
                Runtime.CLOUD_RUN,
                ("workload needs an explicitly controlled HTTP streaming/container contract",),
                tuple(blockers),
            )
        return Placement(Runtime.AGENT_RUNTIME, ("ADK managed integration and runtime contract fit",), tuple(blockers))
    return Placement(Runtime.CLOUD_RUN, ("managed stateless container execution is sufficient",), tuple(blockers))


@dataclass(frozen=True, slots=True)
class CapacityInput:
    peak_requests_per_second: float
    p95_service_seconds: float
    concurrency_per_instance: int
    headroom_ratio: float = 0.30


def required_instances(value: CapacityInput) -> int:
    if value.peak_requests_per_second <= 0 or value.p95_service_seconds <= 0:
        raise ValueError("traffic and service time must be positive")
    if not 1 <= value.concurrency_per_instance <= 1000:
        raise ValueError("concurrency must be between 1 and 1000")
    if not 0 <= value.headroom_ratio <= 2:
        raise ValueError("headroom ratio must be between 0 and 2")
    concurrent_work = value.peak_requests_per_second * value.p95_service_seconds
    return max(1, math.ceil(concurrent_work * (1 + value.headroom_ratio) / value.concurrency_per_instance))
