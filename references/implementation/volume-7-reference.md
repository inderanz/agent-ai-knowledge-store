# Volume 7 implementation evidence ledger

**Verified:** 2 August 2026.

| Decision | Evidence | Artifact |
|---|---|---|
| Preserve product-name versus API/resource identifier distinctions | [Agent Platform release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes), [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime) | naming compatibility table |
| Route region decisions to current feature pages | [Agent locations](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/agent-locations) | location record schema |
| Split storage and processing residency | [Data residency](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/data-residency) | data-location schema |
| Split published quota, target allocation, demand and tested capacity | [Quotas and limits](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/quotas) | capacity observation record |
| Treat official source/sample code as versioned evidence with limitations | [ADK releases](https://github.com/google/adk-python/releases), [Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) | evidence hierarchy |

Local evidence: `references/sources.json` is machine-readable;
`fde_kit.reference` tests primary-domain, date, uniqueness and freshness rules;
repository source/link checks are included in CI. A reachable URL does not prove
semantic correctness, and local freshness does not qualify a customer project.

Production evidence still required: exact selected capability/mode/location/API,
observed quota and service enablement, customer contract/support, region and data
processing approval, semantic source review, troubleshooting exercise and owner
acceptance. These values stay outside the public handbook.
