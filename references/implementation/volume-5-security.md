# Volume 5 implementation evidence ledger

**Verified:** 2 August 2026. Product pages and release notes are current evidence;
target-project configuration, contractual terms and support confirmation remain
customer production gates.

| Decision implemented | Exact official evidence | Repository artifact |
|---|---|---|
| Capability and maturity are recorded per Gateway/identity/authentication mode | [Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview), [Identity](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-identity-overview), [release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes) | maturity baseline and qualification gate |
| Registry inventory is separated from action authorization | [Agent Registry](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-registry) | lifecycle metadata and negative tests |
| Gateway-integrated Model Armor is a content layer, not business authorization | [Configure Model Armor](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/configure-model-armor) | inspection matrix and adversarial plan |
| External delivery identity avoids durable service-account keys | [Workload Identity Federation](https://docs.cloud.google.com/iam/docs/workload-identity-federation) | pipeline design and claims restrictions |
| SCC Agent Platform Threat Detection is Preview and detective | [Threat Detection overview](https://docs.cloud.google.com/security-command-center/docs/agent-platform-threat-detection-overview) | SOC qualification and residual-risk gate |
| Perimeter and secrets claims are limited to selected supported configuration | [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/overview), [Secret Manager](https://docs.cloud.google.com/secret-manager/docs/best-practices) | data/network/secrets checklist |

Local evidence: `fde_kit.security` implements fail-closed tool/method/parameter,
approval and mandatory-control decisions. Its tests are part of the 33-test shared
kit. The shared qualification validator adds schema, missing-gate and production-
rejection coverage. This is control logic reference code—not a Google service
emulator, customer policy, penetration test or certification.

Production evidence still required: customer DFD/threat approval, selected
identity and Gateway mode tests, actual IAM/organization/perimeter/network plans,
Registry publisher/revocation test, Model Armor configuration and adversarial
results, data/privacy/legal approvals, key/secret rotation, artifact provenance,
SOC integration, red-team authorization/report, incident and revocation exercise,
Pre-GA acceptance and residual-risk sign-off.
