# Volume 2 implementation evidence ledger

**Evidence date:** 2 August 2026  
**Scope:** executable platform-admission, Terraform, delivery, operations, and labs  
**Rule:** official product documentation is authoritative for service behavior; pinned official Google repositories are implementation evidence, not service commitments.

No handbook can guarantee permanent “100% latest” alignment because products, APIs, release stages, regions, images, and repositories change. This ledger records exactly what was checked, when it was checked, and which asset consumes it. The repository freshness gate detects scheduled review expiry and selected upstream release drift.

## Agent Platform capability and maturity

| Implemented decision | Exact official evidence | Consuming asset |
|---|---|---|
| Runtime is the managed execution plane; deployment supports source and container routes | [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime), [deploy an agent](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/deploy-an-agent) | Chapter runtime selection; qualification lab |
| Agent Gateway and Agent Identity are currently Preview | [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime) | `validate_qualification.py`; operations Day-0 gate |
| Managed Agents is Pre-GA, not intended for production/commercial use, and excludes sensitive/confidential information | [Create and manage Managed Agents](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents/create-manage) | admission policy and qualification validator reject production use |
| Runtime agents, Gateway, associated regional Registry, and Gemini Enterprise app have documented co-location constraints | [Set up Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/set-up-agent-gateway) | qualification topology validation; governed-cell pattern |
| Registry is the governed inventory plane | [Agent Registry](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-registry) | qualification record and architecture chapter |
| Model Armor template location must be compatible with the Gateway and coverage has documented boundaries | [Configure Model Armor](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/configure-model-armor) | qualification region validation; residual-control guidance |
| Location availability is capability-specific and must be checked at decision time | [Agent Platform locations](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/agent-locations) | customer region gate; no embedded allowlist claiming product availability |

## Runtime application

| Implemented control | Exact official evidence | Code |
|---|---|---|
| Listen on the injected `PORT`, run a stateless HTTP container, and handle termination through the container process | [Cloud Run container contract](https://docs.cloud.google.com/run/docs/container-contract) | `examples/python/platform-admission/Dockerfile`, `main.py` |
| Use the Cloud Run service identity and ADC rather than service-account keys | [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity) | runtime Terraform identity and service manifest |
| Validate the signed IAP assertion, audience, signature, issuer, expiry, and identity; do not trust unsigned identity headers | [IAP signed headers](https://docs.cloud.google.com/iap/docs/signed-headers-howto) | `identity.py`, identity tests |
| Emit structured JSON to stdout/stderr | [Cloud Run logging](https://docs.cloud.google.com/run/docs/logging) | `logging_json.py`, request event fields |
| Use a Firestore transaction for idempotent create-or-replay behavior | [Firestore transaction API 2.28.0](https://docs.cloud.google.com/python/docs/reference/firestore/latest/google.cloud.firestore_v1.transaction), [Firestore best practices](https://docs.cloud.google.com/firestore/native/docs/best-practices) | `repository.py`, repository tests |
| Export OTLP traces through Google Cloud Telemetry API with ADC | [OTLP endpoints](https://docs.cloud.google.com/trace/docs/migrate-to-otlp-endpoints), [Python instrumentation](https://docs.cloud.google.com/stackdriver/docs/instrumentation/setup/python) | `telemetry.py` |
| Dependency and exporter pattern was compared with current official Google sample | [OpenTelemetry samples at commit `4cdacf711acb9d106fcc3a4ba5b0cd55cd192b26`](https://github.com/GoogleCloudPlatform/opentelemetry-samples/tree/4cdacf711acb9d106fcc3a4ba5b0cd55cd192b26/python/otlptrace) | `requirements.lock`, `telemetry.py` |
| Cloud Run Python container shape was compared with official sample | [Python docs samples at commit `19f0efaa4a58007c9aa17ffe70e8101e6810abe6`](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/19f0efaa4a58007c9aa17ffe70e8101e6810abe6/run/helloworld) | Dockerfile and Gunicorn entry point |

## Infrastructure

| Implemented control | Exact official evidence | Terraform |
|---|---|---|
| Create the project through a pinned official foundation module | [Cloud Foundation Fabric project module v57.0.0](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/e70658563e38197eebc8e5399b7f0be828c4dab1/modules/project) | root `module.project` pins `v57.0.0` |
| Attach service project to an existing Shared VPC and grant subnet-level Network User | [Provision Shared VPC with Terraform](https://docs.cloud.google.com/vpc/docs/provisioning-shared-vpc) | optional Shared VPC resources |
| Create regional Docker repository with immutable tags | [Artifact Registry Terraform](https://docs.cloud.google.com/artifact-registry/docs/repositories/terraform) | governed-cell module |
| Configure alert policies through Terraform | [Monitoring alerts with Terraform](https://docs.cloud.google.com/monitoring/alerts/terraform) | log metric, alert, dashboard |
| Federate GitHub OIDC without service-account keys and restrict trust by immutable repository ID | [Workload Identity Federation for deployment pipelines](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines), [deployment pipeline service-account practices](https://docs.cloud.google.com/iam/docs/best-practices-for-using-service-accounts-in-deployment-pipelines) | GitHub WIF module |

Pinned infrastructure baseline: Terraform [`v1.15.8`](https://github.com/hashicorp/terraform/releases/tag/v1.15.8), Google provider [`v7.42.0`](https://github.com/hashicorp/terraform-provider-google/releases/tag/v7.42.0), and Cloud Foundation Fabric [`v57.0.0`](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/releases/tag/v57.0.0).

## Delivery and operations

| Implemented control | Exact official evidence | Asset |
|---|---|---|
| A user-specified Cloud Build identity uses Cloud Logging-only storage | [Configure user-specified build service accounts](https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts) | `cloudbuild.yaml` |
| Cloud Build pushes a declared `images` artifact so it can generate provenance; explicit `docker push` is not used | [Generate and validate build provenance](https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance) | `cloudbuild.yaml`, separate `release.yaml` |
| Release fails until Artifact Analysis completes and High/Critical findings are absent | [Container scanning overview](https://docs.cloud.google.com/artifact-analysis/docs/container-scanning-overview), [occurrence analysis status](https://docs.cloud.google.com/artifact-analysis/docs/reference/rest/v1/projects.locations.occurrences), [gcloud vulnerability command](https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/vulnerabilities/list) | `supply_chain_gate.py`, scanning API, repository scanning configuration |
| Cloud Run opts into the target project's Binary Authorization policy; policy configuration remains separation-of-duties owned | [Enable Binary Authorization for Cloud Run](https://docs.cloud.google.com/binary-authorization/docs/run/enabling-binauthz-cloud-run), [configure policy](https://docs.cloud.google.com/binary-authorization/docs/configuring-policy-cli) | `service.yaml`, Day-0 gate |
| Cloud Build can automatically sign produced images; the built-by-Cloud-Build path for Cloud Run is currently Preview | [Deploy only images built by Cloud Build](https://docs.cloud.google.com/binary-authorization/docs/deploy-cloud-build), [Cloud Run Binary Authorization setup](https://docs.cloud.google.com/binary-authorization/docs/run/overview) | maturity acceptance and customer policy decision |
| Build once, identify the pushed digest, and promote the same artifact | [Cloud Deploy Cloud Run targets](https://docs.cloud.google.com/deploy/docs/run-targets) | build/release commands |
| Separate execution identity needs Cloud Deploy Job Runner plus runtime permissions; releaser needs act-as permission | [Cloud Deploy service accounts](https://docs.cloud.google.com/deploy/docs/cloud-deploy-service-account) | Terraform build/deploy roles |
| Cross-project Cloud Run targets require repository Reader for the deployer and Cloud Run service agent | [Deploy images from another project](https://docs.cloud.google.com/run/docs/deploying#other-projects), [Artifact Registry integration](https://docs.cloud.google.com/artifact-registry/docs/integrate-cloud-run) | `artifact_consumers` repository IAM |
| Raw Cloud Run manifest and Skaffold Cloud Run deploy stanza follow current documented forms | [Cloud Run YAML reference](https://docs.cloud.google.com/run/docs/reference/yaml/v1), [Cloud Deploy Run targets](https://docs.cloud.google.com/deploy/docs/run-targets) | `service.yaml`, `skaffold.yaml` |
| Per-target environment/service-account/audience values use documented post-render parameters | [Cloud Deploy parameters](https://docs.cloud.google.com/deploy/docs/parameters) | target definitions and `# from-param` directives |
| Current official sample was reviewed at an immutable source revision | [Cloud Deploy samples at commit `3ea194851eaf3451c0d59ca211f5176e4070b3d6`](https://github.com/GoogleCloudPlatform/cloud-deploy-samples/tree/3ea194851eaf3451c0d59ca211f5176e4070b3d6) | delivery layout |
| Log queries use Cloud Logging query syntax; routing/retention is a customer control | [Logging query language](https://docs.cloud.google.com/logging/docs/view/logging-query-language), [log routing](https://docs.cloud.google.com/logging/docs/routing/overview) | operations queries and Day-0 gate |

## Supply-chain pins used by CI

| Dependency | Immutable pin | Provenance |
|---|---|---|
| Python base | `mirror.gcr.io/library/python:3.12.11-slim@sha256:47ae396f09c1303b8653019811a8498470603d7ffefc29cb07c88f1f8cb3d19f` | qualified registry manifest on 2026-08-02 |
| Cloud Build Docker builder | `gcr.io/cloud-builders/docker@sha256:f8b08c609fdc392ee6827ff3e1725e4980f7d96bde9f76f4695086405c96c147` | qualified registry manifest on 2026-08-02 |
| Google Cloud CLI stable index | `gcr.io/google.com/cloudsdktool/google-cloud-cli@sha256:39f4c48c083fb1d8d182eedc7de97545980afb646b1afdfec61a3f560969bc96` | qualified OCI index on 2026-08-02 |
| `actions/checkout` | `3d3c42e5aac5ba805825da76410c181273ba90b1` (`v7.0.1`) | [official repository](https://github.com/actions/checkout/tree/3d3c42e5aac5ba805825da76410c181273ba90b1) |
| `actions/setup-python` | `ece7cb06caefa5fff74198d8649806c4678c61a1` (`v6`) | [official repository](https://github.com/actions/setup-python/tree/ece7cb06caefa5fff74198d8649806c4678c61a1) |
| `google-github-actions/auth` | `7c6bc770dae815cd3e89ee6cdf493a5fab2cc093` (`v3`) | [official Google repository](https://github.com/google-github-actions/auth/tree/7c6bc770dae815cd3e89ee6cdf493a5fab2cc093) |
| `google-github-actions/setup-gcloud` | `aa5489c8933f4cc7a4f7d45035b3b1440c9c10db` (`v3.0.1`) | [official Google repository](https://github.com/google-github-actions/setup-gcloud/tree/aa5489c8933f4cc7a4f7d45035b3b1440c9c10db) |
| `hashicorp/setup-terraform` | `dfe3c3f87815947d99a8997f908cb6525fc44e9e` (`v4.0.1`) | [official repository](https://github.com/hashicorp/setup-terraform/tree/dfe3c3f87815947d99a8997f908cb6525fc44e9e) |

## Required customer evidence not supplied by source citations

The following cannot be established from documentation or a local test: contractual eligibility for Preview/Pre-GA products, customer data classification, regional availability at deployment time, organization policy interaction, quotas, IAM allowed-policy constraints, network reachability, real IAP audience, threat acceptance, latency/capacity, backup restoration, support response, or operator competence. Those remain explicit production gates; this draft must not be marked Approved until they are exercised and independently reviewed.
