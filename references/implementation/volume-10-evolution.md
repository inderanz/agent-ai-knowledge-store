# Volume 10 implementation evidence ledger

**Verified:** 2 August 2026.

| Decision | Official evidence | Artifact |
|---|---|---|
| Pin ADK/SDK/source baselines and preserve exact identifiers | [ADK v2.6.1](https://github.com/google/adk-python/tree/v2.6.1), [SDK v1.163.0](https://github.com/googleapis/python-aiplatform/releases/tag/v1.163.0) | `references/versions.json` and CI |
| Treat model upgrade/retirement as application migration | [model lifecycle](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions), [migration](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate) | evaluation/canary/retirement plan |
| Use current release notes for breaking behavior and maturity changes | [release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes) | change examples and intake schema |
| Keep runtime revision maturity/bypass in release planning | [revisions/traffic](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/manage-revisions-and-traffic) | route/canary caveat |

Local evidence: official git remote confirms ADK `v2.6.1` commit; Volume 3 graph
compiles against ADK 2.6.1; `fde_kit.evolution` tests change severity, dependency
impact and version-envelope constraints. Repository package/source validation and
qualification schemas run in CI. No dual-version customer state or production
model migration has been executed.

Production evidence still required: private deployment inventory, official/source
semantic diff, current/candidate locks and SBOM, dual-version API/state/session/
event/tool/auth/telemetry tests, representative model evaluation, capacity/cost,
in-flight routing, backup/migration/restore, canary, rollback/roll-forward,
business reconciliation, publication reviews and retirement acceptance.
