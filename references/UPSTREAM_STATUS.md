# Automated upstream status

**Generated:** 2026-10-06 UTC by the scheduled documentation-maintenance workflow.

> [!IMPORTANT]
> This is an observation report, not the qualified repository baseline. Automation never
> changes `references/versions.json`, chapter claims, maturity labels, or `verified_at`
> dates. A human reviewer must compare official documentation and code, update affected
> material, and pass the repository review gates before a new baseline is accepted.

## Summary

| Check | Count |
|---|---:|
| Tracked release baselines | 7 |
| Release drifts requiring review | 6 |
| Release-query errors | 0 |
| Registered sources within review interval | 0 |
| Registered sources overdue | 106 |
| Invalid source records | 0 |

## Release comparison

| Dependency | Qualified baseline | Latest observed official release | State |
|---|---:|---:|---|
| `google-adk-python` | `2.6.1` | [`2.11.0`](https://github.com/google/adk-python/releases/tag/v2.11.0) | REVIEW REQUIRED |
| `google-cloud-aiplatform` | `1.163.0` | [`2.3.0`](https://github.com/googleapis/python-aiplatform/releases/tag/v2.3.0) | REVIEW REQUIRED |
| `googlecloudplatform-agent-starter-pack` | `0.41.3` | [`0.41.3`](https://github.com/GoogleCloudPlatform/agent-starter-pack/releases/tag/v0.41.3) | CURRENT |
| `googlecloudplatform-cloud-foundation-fabric` | `57.0.0` | [`59.0.0`](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/releases/tag/v59.0.0) | REVIEW REQUIRED |
| `terraform` | `1.15.8` | [`1.16.5`](https://github.com/hashicorp/terraform/releases/tag/v1.16.5) | REVIEW REQUIRED |
| `terraform-provider-google` | `7.42.0` | [`8.5.0`](https://github.com/hashicorp/terraform-provider-google/releases/tag/v8.5.0) | REVIEW REQUIRED |
| `googlecloudplatform-terraform-google-cloud-armor` | `8.1.1` | [`9.0.0`](https://github.com/GoogleCloudPlatform/terraform-google-cloud-armor/releases/tag/v9.0.0) | REVIEW REQUIRED |

## Sources requiring semantic re-verification

| Source | Last verified | Review due | State |
|---|---:|---:|---|
| `adk-python-releases` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `agent-platform-data-residency` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `agent-platform-locations` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `agent-platform-model-lifecycle` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `agent-platform-open-model-deprecations` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `agent-platform-quotas` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `agent-platform-release-notes` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `agent-runtime-revisions` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `gemini-enterprise-locations` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `google-cloud-fde-genai-role-2026` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `google-cloud-fde-iv-role-2026` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `google-cloud-gecx-fde-role-2026` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `google-deepmind-fde-role-2026` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `managed-agents-maturity` | `2026-08-02` | `2026-08-09` | 58 day(s) overdue |
| `adk-2-overview` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `adk-evaluation` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `adk-graph-workflows-reviewed` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `adk-python-v2-6-1-source` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `adk-samples` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `adk-workflow-source-v2-6-1` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-gateway-delegated-auth` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-gateway-monitoring` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-gateway-setup-topology` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-gateway` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-identity-runtime` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-identity` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-observability` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-online-evaluation` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-platform-gemini-migration` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-platform-overview` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-platform-sdk-v1-163-0` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-platform-sessions-adk` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-platform-threat-detection` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-registry-adk-resolution` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-registry-data-model` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-registry-overview-2026` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-registry` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-runtime-adk-quickstart` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-runtime-contract` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-runtime-deployment` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-runtime-psc-interface` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-runtime` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `cloud-armor-overview` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `cloud-armor-policy-overview` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `cloud-armor-rate-limiting` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `cloud-deploy-run-targets` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `cloud-deploy-service-accounts` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `cloud-run-binary-authorization` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `gemini-enterprise-apps-data-stores` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `gemini-enterprise-create-app` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `gemini-enterprise-observability-settings` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `google-adk-evaluation-2026` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `google-adk-skills-2026` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `model-armor-agent-gateway` | `2026-08-02` | `2026-08-16` | 51 day(s) overdue |
| `agent-starter-pack-reviewed` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `agentic-architecture-components` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `ai-ml-reliability` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `anthropic-applied-ai-engineer-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `anthropic-building-effective-agents` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `anthropic-cookbooks-observed-2026-08-02` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `anthropic-demystifying-agent-evals-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `anthropic-skills-observed-2026-08-02` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `artifact-analysis-container-scanning` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `cloud-build-provenance` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `cloud-build-user-specified-identity` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `cloud-deploy-samples-reviewed` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `cloud-foundation-fabric-v57` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `cloud-healthcare-api` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `cloud-monitoring-slo` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `cloud-run-container-contract` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `cloud-run-python-reviewed` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `cloud-run-service-identity` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `deploy-operate-generative-ai` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `enterprise-foundations-blueprint` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `eventarc-event-driven-architecture` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `financial-services-perspective` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `github-actions-oidc-claims-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-agent-platform-access-control-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-ai-ml-well-architected` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-beyond-pilot-lessons-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-cloud-adoption-framework` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-cloud-compliance` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-cloud-hipaa-guide` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-cloud-otlp-endpoints` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-fde-gemini-enterprise-a2ui-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-multi-tenant-agentic-ai-architecture-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-skills-reviewed` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `google-wif-deployment-pipelines-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `googleapis-reviewed-2026-08-02` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `googlecloudplatform-generative-ai-reviewed-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `iap-signed-headers` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `multi-tenant-agentic-ai-sample` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `multi-tenant-agentic-ai` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `openai-agents-python-observed-2026-08-02` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `openai-cookbook-observed-2026-08-02` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `openai-deployment-company-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `openai-fde-role-2026` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `opentelemetry-python-reviewed` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `pubsub-event-driven-architecture` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `resource-hierarchy` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `shared-vpc` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `terraform-google-cloud-armor-reviewed` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `vpc-sc-dry-run` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `vpc-sc-perimeter-architecture` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `well-architected-operational-excellence` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |
| `workload-identity-federation` | `2026-08-02` | `2026-09-01` | 35 day(s) overdue |

## Required maintainer action

1. Open the official release, documentation, source tag, samples, and release notes.
2. Identify affected volumes, Terraform modules, examples, labs, runbooks, and claims.
3. Update code and prose together; preserve capability/recommendation/field-pattern labels.
4. Update `references/versions.json` only after implementation qualification.
5. Update a source's `verified_at` only after semantic review, not merely reachability.
6. Run all local and component CI gates and obtain required independent reviews.

See [the repository workflow](../README.md#how-documentation-stays-current) and [research policy](../docs/RESEARCH_AND_REVIEW.md).
