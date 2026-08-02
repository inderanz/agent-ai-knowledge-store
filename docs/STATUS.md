# Content status

**Overall status: Complete draft; independent and customer production reviews remain.** All fifteen volumes now contain long-form FDE engineering content. Local reference implementations and qualification controls exist, but no chapter is Approved and no customer production environment is claimed.

## Publication totals

| Measure | Count |
|---|---:|
| Detailed volume maps | 15 |
| Planned chapters/reference sets | 158 |
| Full long-form volume drafts | 15 |
| Imported long-form drafts awaiting normalization | 2 |
| Chapters in review | 0 |
| Approved chapters | 0 |
| Superseded chapters | 0 |

## Draft content status

| Content | Status | Baseline | Required next action |
|---|---|---|---|
| From loop to graph engineering | Draft | Authored against ADK 2.x; latest verified release now v2.6.1 | Re-run six review gates and normalize chapter contract |
| Agent Platform reference architecture | Draft | Product docs researched 29 July 2026 | Recheck paragraph evidence, capability maturity, regions, gateway topology, and v2.6.1 impact |
| Volume 3 — ADK workflow engineering | Draft | 2,824 lines plus 31 implementation/delivery/lab/operations files; official docs and ADK v2.6.1 source rechecked 2 August 2026; 26 dependency-free local tests and the real v2.6.1 graph-compilation test pass; CI repeats all gates | Deploy to a customer sandbox, execute managed-session/resume/integration/security/recovery/load/online-eval gates, and complete five independent review gates |
| Volume 1 — Foundations | Draft | 2,369 lines; official docs and tagged ADK v2.6.1 source verified 2 August 2026 | Extract and execute implementation artifacts; complete five remaining review gates |
| Volume 2 — Platform architecture | Draft | 3,373 lines plus 58 companion source/configuration files; official docs and pinned Google source verified 2 August 2026; 30 dependency-free local tests passing plus 2 HTTP adapter tests configured for dependency-installed CI | Run provider/module initialization and validation in CI, apply in a customer sandbox, execute integration/recovery/load/security tests, and complete five independent review gates |
| Volume 4 — Runtime and deployment | Draft | 574-line FDE handbook plus placement/capacity implementation, tests, qualification lab, operations and evidence; official runtime/contract/PSC/revision/Cloud Run/GKE sources checked 2 August 2026 | Deploy only in an authorized sandbox; prove target runtime, private path, load, session compatibility, canary, rollback, restore and DR; complete independent reviews |
| Volume 5 — Security and governance | Draft | 701-line FDE handbook plus fail-closed method/parameter policy, security lab, SOC runbook and evidence; current Gateway/Identity/Registry/Model Armor/SCC/IAM sources checked 2 August 2026 | Implement customer DFD/policies and run red-team, data/privacy, egress, supply-chain, revocation and incident gates; complete independent reviews |
| Volume 6 — Reliability and operations | Draft | 572-line FDE handbook plus SLO/recovery logic, game-day lab, runbook and evidence; current Agent Observability/online-eval/Cloud Monitoring sources checked 2 August 2026 | Prove deployed SLI data, alerts, failure injection, idempotency, capacity/cost, restore/DR and operator competency; complete independent reviews |
| Volume 7 — Engineering reference | Draft | 483-line dated reference system plus source validator, field drill, operations and evidence; volatile locations/quotas/releases remain live-linked | Perform semantic source review, add customer-private observed values, exercise troubleshooting and complete independent reviews |
| Volume 8 — Industry architectures | Draft | 565-line cross-industry handbook plus conservative overlay validator, synthetic lab, operations and evidence; Google compliance/FS/healthcare guidance checked 2 August 2026 | Customer legal/risk/domain authorities must decide jurisdiction, service eligibility, material actions and controls; run domain evaluation/fallback/incident and independent reviews |
| Volume 9 — FDE delivery handbook | Draft | 574-line engagement system plus stage-gate implementation, delivery simulation, exit operations and evidence | Execute with a customer: charter, discovery, vertical slice, six reviews, launch, competency handover and value measurement |
| Volume 10 — Evolution and migrations | Draft | 581-line lifecycle handbook plus impact/version-envelope implementation, migration lab, operations and evidence; ADK v2.6.1 and July 2026 platform/model change sources checked | Execute dual-version/customer-state/model/IaC migration evidence, canary, reconciliation and safe retirement; complete independent reviews |
| Volume 11 — Agent Registry | Draft | 572-line catalog/governance handbook plus registration/binding admission logic, tests, lab, operations and evidence; current Registry docs and pinned Google source checked 2 August 2026 | Create and govern a customer sandbox catalog; prove IAM, provenance, search, health overlay, Gateway resolution, revocation/reconstruction and independent reviews |
| Volume 12 — Agent Gateway | Draft | 574-line ingress/egress handbook plus fail-closed route qualification, tests, lab, operations and evidence; current Gateway/extension/monitoring docs and pinned Google APIs checked 2 August 2026 | Prove topology, Registry/Identity/IAP, dry-run policy, request/content authorization, failure/load/SLO/rollback and independent reviews |
| Volume 13 — Agent Identity | Draft | 557-line identity/credential handbook plus maturity/non-disclosure admission, tests, lab, operations and evidence; current Identity/Runtime docs, SDK and pinned Google APIs checked 2 August 2026 | Prove effective principals, least privilege, default CAA, exact mode maturity, credential containment, audit/revocation/recovery and independent reviews |
| Volume 14 — Cloud Armor | Draft | 540-line edge-security handbook plus narrow pinned Terraform, rule safety logic, tests, lab, operations and evidence; current Armor docs and Google module/API source checked 2 August 2026 | Plan/apply only in an authorized sandbox; prove attachment/origin boundary, preview-tuned WAF/rate/bot, attack/load/logging/rollback and independent reviews |
| Volume 15 — Gemini Enterprise app | Draft | 639-line app handbook plus app/data-store/IAM admission, tests, lab, operations and evidence; current create/data/ACL/location/observability/release docs and pinned Google source checked 2 August 2026 | Establish license/allowlist and build a synthetic sandbox vertical slice; prove CMEK/ACL/quality/agents/SLO/reindex/exit and independent reviews |

The draft source files remain at the repository root until their first review branches intentionally relocate and normalize them. This prevents unreviewed material from appearing as published handbook content.

## Workstream state

| Workstream | State |
|---|---|
| Repository structure and navigation | Implemented; awaiting peer review |
| Evidence classification and source hierarchy | Implemented; awaiting peer review |
| Source freshness and release drift checks | Implemented and passing |
| Volume-level engineering content maps | Implemented and expanded into fifteen long-form drafts |
| Production Python examples | Volume 2 standalone admission package implemented; 12 domain/identity/idempotency tests passing; cloud integration pending |
| Production ADK workflow | Volume 3 v2.6.1 graph plus deterministic policy, approval, idempotency, reconciliation, telemetry, evaluation and guarded deployment package implemented; real ADK CI and customer adapters pending |
| Production Terraform modules | Volume 2 governed-cell and GitHub WIF modules implemented; formatting and 5 plan-policy tests pass; provider-backed validation and customer plan pending |
| Cloud Build and Cloud Deploy implementations | Volume 2 digest-addressed build, cross-project targets, identities, production approval, and exact-plan GitHub workflow implemented; cloud execution pending |
| Executable labs | Volume 2 local labs and Agent Platform qualification gate implemented; customer sandbox lab pending |
| ADK delivery and operations | Volume 3 Cloud Build/GitHub CI, qualification validator, six-lab path, query catalogue and incident response implemented; cloud execution pending |
| Volumes 4–10 shared production kit | Original 33 dependency-free tests now run inside the consolidated 47-test kit, plus 3 qualification-validator tests; CI added; customer cloud evidence pending |
| Volumes 11–15 control-plane/app kit | 14 additional Registry/Gateway/Identity/Armor/app tests plus 3 fail-closed qualification-validator tests, five labs/operations/evidence ledgers, CI and validated Cloud Armor Terraform implemented; customer cloud evidence pending |
| Chapter-level security and SRE reviews | All volumes contain self-review content; independent review not started |
| Approved production handbook | Not started |

## Approval rule

A chapter becomes Approved only when its front matter records all six passed review gates, its examples and infrastructure pass CI, its source evidence is current, and this status file is updated in the same pull request. A README or chapter outline does not count as a completed chapter.
