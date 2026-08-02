# Volume 4 implementation evidence ledger

**Verified:** 2 August 2026. Service documentation is authoritative; every
location, maturity, quota and contractual decision is rechecked in the target
customer project before deployment.

| Decision implemented | Exact official evidence | Artifact |
|---|---|---|
| Agent Runtime is the managed ADK-first option; API resources retain `ReasoningEngine` naming | [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime) | placement chapter and validator |
| Object, source, Dockerfile, image and Developer Connect deployment routes are distinct; deployment is Python-only | [Deploy an agent](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/deploy-an-agent) | deployment selection and release record |
| Custom Agent Runtime containers bind `0.0.0.0:8080` and implement method-mode routing endpoints for SDK/playground integration | [Runtime contract](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/runtime-contract) | runtime contract tests/lab |
| Private egress uses PSC interface/network attachment and DNS peering; public egress needs an explicit controlled path | [PSC interface](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/private-service-connect-interface) | network diagram and failure lab |
| Revisions/traffic are Preview, currently `v1beta1`, and direct revision requests bypass root splitting | [Manage revisions and traffic](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/manage-revisions-and-traffic) | canary caveat and qualification gate |
| Built-in runtime metrics use the ReasoningEngine monitored resource | [Monitoring](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/monitoring) | SLI plan |
| Current `AdkApp` tracing uses telemetry environment variables; prompt/response capture is separate | [Tracing](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/tracing) | privacy/telemetry gate |
| Logging coverage does not automatically include every Agent Runtime subresource | [Logging](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/logging) | application telemetry requirement |
| Cloud Run ingress binds to `0.0.0.0`, has multiple concurrency, no privileged mode, and distinct service/job/worker contracts | [Cloud Run container contract](https://docs.cloud.google.com/run/docs/container-contract), [concurrency](https://docs.cloud.google.com/run/docs/about-concurrency) | runtime matrix/capacity lab |
| GKE workloads should use Workload Identity Federation rather than key files | [Workload Identity Federation for GKE](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/workload-identity) | GKE security baseline |

Local evidence: six runtime placement/capacity tests pass as part of the 33-test
shared FDE kit. The shared qualification validator adds three tests. No cloud
resource, network, IAM policy, runtime revision, or traffic configuration was changed.

Production evidence still required: customer location and support eligibility,
saved infrastructure plans, IAM/network/PSC/DNS tests, artifact/SBOM/provenance,
real runtime contract, sessions/state compatibility, load/quota/cost, canary,
rollback/roll-forward, restoration/DR, security review and operator exercise.
