# Volume 2 production operations pack

This pack turns the platform chapter into an operator-owned service. It is a baseline, not evidence that a customer environment is production approved.

## Day-0 gates

Do not expose the admission service or onboard an agent until all of these have named customer owners and attached evidence:

- the organization, folder, billing, project, and Shared VPC decisions;
- data classification, residency, retention, encryption, and recovery requirements;
- allowed regions checked against each product's current location page;
- IAP-protected load balancer, signed JWT audience, and negative authentication tests;
- workload service account with no user-managed keys and resource-level access where possible;
- tested Firestore recovery and idempotency behavior;
- log sinks, alert notification paths, SLOs, paging policy, and cost ownership;
- immutable artifact digest, vulnerability/provenance decision, rollback evidence, and production approver;
- enforced Binary Authorization policy in each target project; if the `built-by-cloud-build` attestor is selected, explicit acceptance that Google currently documents the Cloud Run path as Preview;
- product-maturity acceptance for every preview or Pre-GA dependency; and
- a support and exit plan if a preview capability changes.

As verified on 2 August 2026, Agent Gateway and Agent Identity are marked Preview in the current Runtime documentation. The Managed Agents page marks that capability Pre-GA, says it is not intended for commercial or production use, and says not to use sensitive or confidential information. Therefore this implementation rejects Managed Agents for a production workload.

## Service-level objectives

Set customer objectives from the business journey, not from a generic template. A reasonable starting workshop uses four indicators:

| Indicator | What to measure | Initial decision required |
|---|---|---|
| Availability | valid admission requests receiving a non-5xx response | target and measurement window |
| Correctness | decisions matching the reviewed policy oracle | test corpus and error budget |
| Latency | request duration by outcome and tenant class | percentile and target |
| Durability | accepted decisions recoverable and replayable | RPO, RTO, restore test cadence |

Do not count policy denials as availability failures. Do count identity verifier, Firestore, or telemetry-required startup failures according to the customer dependency model.

## Release evidence

Every production rollout record must contain:

- commit and build ID;
- container image digest, never only a mutable tag;
- unit, policy, delivery, vulnerability, and integration-test results;
- rendered Cloud Run manifest and Terraform plan digest;
- preview/Pre-GA acceptance record where applicable;
- approver, change ticket, start/end time, rollback owner, and observed SLO impact.

## Incident control

Follow [incident-response.md](incident-response.md). Queries in [queries.md](queries.md) intentionally avoid raw user identity. The runtime hashes the IAP subject with a customer-owned HMAC key before persistence.

## Official evidence

- [Agent Runtime and current maturity labels](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime)
- [Managed Agents restrictions](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents/create-manage)
- [Agent Gateway setup and topology constraints](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/set-up-agent-gateway)
- [Configure Model Armor with Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/configure-model-armor)
- [Google SRE incident management](https://sre.google/workbook/incident-response/)
- [Cloud Run structured logging](https://docs.cloud.google.com/run/docs/logging)
- [Cloud Logging routing](https://docs.cloud.google.com/logging/docs/routing/overview)
