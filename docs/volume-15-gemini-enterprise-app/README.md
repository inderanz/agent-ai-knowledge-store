# Volume 15 — Gemini Enterprise app production engineering

> [!CAUTION]
> **Status: complete draft, not production authorization.** Revalidated 2 August
> 2026. Gemini Enterprise app features, editions, connectors, regions, agents,
> skills and allowlists change frequently. Verify the exact feature/location/
> edition and contract before committing to a customer outcome.

**Audience:** forward deployed engineers, enterprise search/knowledge and app
teams, data owners, IAM/security/privacy/legal, agent engineers, SRE/support,
change/adoption leaders and customer executives.  
**Invariant:** a user receives only source-authorized information and permitted
actions, with attributable evidence; an answer or action is not production-ready
unless relevance, grounding, ACLs, safety, latency, operations and recovery pass.

## Executive outcome

Gemini Enterprise is the employee-facing search, assistant and agent application
surface. Apps connect data stores/connectors and can expose search, actions and
agents. In API context, Google uses app and engine interchangeably: a Gemini
Enterprise app is a Discovery Engine `Engine` with `app_type=APP_TYPE_INTRANET`,
as documented in [create an app](https://docs.cloud.google.com/gemini/enterprise/docs/create-app).

This volume covers business case, edition/location/CMEK-before-create, immutable
app identity, data/connector and ACL engineering, app IAM, retrieval/answer/action
evaluation, Registry/Gateway/Identity integration, observability, SLO/support,
reindex/recovery, adoption/value and exit.

## Evidence legend

- 🟢 official Google capability; 🟡 enterprise recommendation; 🔵 FDE pattern.
- “GA with allowlist” is not equivalent to generally accessible GA; Preview and
  Private Preview require their own risk/terms/exit decision.

## Product boundary: app versus platform

```mermaid
flowchart TB
    U[Employees/approved users] --> APP[Gemini Enterprise app / Engine]
    APP --> AS[Core Assistant/search]
    APP --> DS[Data stores/connectors]
    APP --> AG[Built/imported agents and skills where enabled]
    AG --> RG[Agent Registry]
    AG --> GW[Agent Gateway]
    GW --> AI[Agent Identity/Auth Manager]
    GW --> T[Agents/MCP/tools/endpoints]
    SEC[IAM, ACL, CMEK, VPC-SC, audit] --> APP
    OBS[Metrics, traces, logs, evaluation] --> APP
```

Gemini Enterprise is the governed end-user app. Gemini Enterprise Agent Platform
supplies build/run/govern components such as Runtime, Registry, Gateway and
Identity. Names are adjacent; architecture and commercial/maturity decisions are
not interchangeable.

## Customer outcome and discovery

Start with a bounded business journey, such as finding current policy and opening
an approved support ticket. Do not start by connecting every repository.

### Executive questions

- Which measurable outcome: search time, case deflection, onboarding, resolution,
  research quality, controlled workflow or employee experience?
- Who is the accountable business owner, data owners and risk acceptor?
- What material decisions/actions must remain human-approved or prohibited?
- Which edition/licensing/user population and adoption/support model apply?
- What baseline, target, measurement window and counter-metrics prevent gaming?

### Data and security questions

- Which systems are authoritative; ingest or federate; sync/freshness expectation?
- Are item-level source ACLs available and correctly mapped to enterprise identity?
- Which PII, secrets, regulated, residency, retention, deletion and legal-hold
  constraints apply?
- Is CMEK required? Which location/key/project and disaster/rotation process?
- Are cross-domain Drive sources proposed, and who accepts search-manipulation/
  prompt-injection risk documented by Google?
- Which third-party scopes/admin credentials/static egress are required?

### Experience and operations questions

- Which queries, languages, devices, channels and accessibility needs matter?
- What answer/citation/abstention and action approval UX is acceptable?
- Which retrieval/answer/action metrics and human judgments define quality?
- What is the SLO, support desk, escalation, connector owner and recovery objective?
- How will users report wrong/unsafe/inaccessible results, and how fast is removal?

Deliver outcome charter, app/location/CMEK ADR, data-store/ACL inventory, threat
model, evaluation set, agent/action boundary, SLOs/runbooks, launch/adoption plan,
qualification record and exit plan.

## Current capability and maturity baseline

| Surface | Official baseline | FDE qualification |
|---|---|---|
| App creation | console/API; app ID cannot be changed | select stable ID/location/CMEK before create |
| Data stores | multiple stores per app; many-to-many model | source authority, ACL, CMEK/location consistency |
| Current limit | docs state up to 50 data stores per app | live quota/limit and performance; avoid needless blending |
| Third-party sources | connector-specific setup/maturity; often console workflows | scopes, admin, sync, ACL, egress, terms, exit |
| App-level IAM | supported | remove conflicting broad project role to restrict app |
| Registry MCP import | supported governance workflow | Registry ownership + Gateway egress + Identity |
| Agent observability | GA announced 24 June 2026 | app/agent toggle, privacy-safe logs, dashboards/traces |
| Workflow agents | GA with allowlist announced 18 June | verify project allowlist and admin feature toggle |
| Skills | GA with allowlist announced 17 June | verify exact access and supply-chain governance |

Use current [release notes](https://docs.cloud.google.com/gemini/enterprise/docs/release-notes)
at every design/launch review. Never promise a connector/agent/skill from a general
marketing category.

## App creation decisions that are hard to reverse

The [create app guide](https://docs.cloud.google.com/gemini/enterprise/docs/create-app)
states:

- register CMEK before creating the app when required; apps created before CMEK
  registration remain unprotected by that key;
- app ID cannot be changed after creation;
- select multi-region/location; `global` is recommended when there is no residency
  constraint because it generally has newer features/models and response benefits;
- existing data store is needed for some CLI paths;
- cross-domain Drive can introduce prompt injection/search manipulation risks.

🟡 Make these an admission form, not console choices during a demo.

```yaml
app_contract_version: 1
project_id: customer-search-prod
app_id: employee-knowledge
display_name: Employee Knowledge
location: global
edition: CUSTOMER_APPROVED_EDITION
cmek:
  required: true
  registration_evidence: gs://EVIDENCE/cmek-before-app/
data_stores:
  - resource: DATA_STORE_RESOURCE
    source: approved-policy-repository
    mode: ingested
    acl: item-level
    freshness_slo_minutes: 60
agents:
  registry_resources: [APPROVED_RESOURCE]
  gateway_required: true
observability:
  traces_logs: true
  sensitive_prompt_response_logging: false
owner: employee-experience
security_owner: enterprise-search-security
```

## Location, residency and encryption

The current [data residency page](https://docs.cloud.google.com/gemini/enterprise/docs/locations)
separates at-rest data-residency zones and AI/ML processing commitments and lists
limitations by global, multi-region and in-country region. Validate all selected
features—connectors, assistant, agents, Registry/Runtime/Gateway, grounding and
observability—not merely data-store location.

CMEK design includes key location compatibility, service-agent permissions,
separation of duty, rotation, disable/destroy incident, monitoring and DR. All
connected data stores need a compatible uniform encryption posture. Never “test”
key disablement in production without an accepted impact/recovery plan.

```mermaid
flowchart LR
    D[Data residency + feature requirements] --> L[Location decision]
    L --> K[CMEK registration if required]
    K --> A[Create immutable app ID]
    A --> S[Create/connect compatible data stores]
    S --> Q[ACL/security/evaluation qualification]
```

## Data stores and connectors

The [apps and data stores guide](https://docs.cloud.google.com/gemini/enterprise/docs/apps-data-stores)
defines the many-to-many relationship and source/type limitations. The [connector
introduction](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/introduction-to-connectors-and-data-stores)
requires decisions on access control, ingest versus federation, sync, CMEK, PII/
autocomplete and connector-specific scopes; supported sources and maturity vary.

For each data store record:

| Field | Evidence |
|---|---|
| source and business owner | authoritative system and escalation |
| connector/mode/maturity/location | current official page and accepted terms |
| identity/admin credential/scopes | least privilege and rotation owner |
| ACL mapping | source principal → Google identity; negative tests |
| ingestion/federation/freshness | watermark, deletions, retries, backfill |
| schema/content parsing | IDs, title/body/time/ACL/classification |
| CMEK/retention/deletion | key and lifecycle evidence |
| evaluation segment | representative queries/docs/access cohorts |
| recovery/exit | reauth/reindex/export/delete procedure |

### Ingestion state machine

```mermaid
stateDiagram-v2
    [*] --> Discovered
    Discovered --> Authorized: owner/scopes/ACL accepted
    Authorized --> InitialSync
    InitialSync --> Evaluated: completeness + ACL + quality tests
    Evaluated --> Serving
    Serving --> Degraded: auth/quota/schema/freshness failure
    Degraded --> Resyncing: repair/reconcile
    Resyncing --> Evaluated
    Serving --> Retired: source removed/contract end
    Retired --> Deleted: retention/legal hold satisfied
```

Idempotently key documents to source IDs; track create/update/delete/tombstone
watermarks; quarantine malformed/ACL-unknown items; reconcile counts and sampling;
never default a missing ACL to public. Federation avoids copies but transfers
availability/latency/auth dependency to query time.

## Access control

Source ACL correctness is a data-integrity invariant. Test:

- allowed user finds and opens expected item;
- denied peer, terminated user, external/guest and wrong group cannot retrieve,
  generate from, autocomplete or cite it;
- group membership add/remove converges within accepted SLO;
- deletion/permission downgrade removes content from indexes/caches/answers;
- blended results preserve per-store ACL;
- agent/action cannot bypass search ACL through a tool.

The [app IAM guide](https://docs.cloud.google.com/gemini/enterprise/docs/iam-policy-for-apps)
documents app-level access. To restrict a user to specific apps, remove broader
project-level role that otherwise grants access. Separate app admin, data-store
admin, connector credential admin, agent builder, end user, observability viewer
and auditor. Apply least privilege and time-bound privileged access.

## Retrieval and answer engineering

An enterprise answer is acceptable only when the authorized source set, retrieval,
generation and UI evidence align.

```mermaid
sequenceDiagram
    participant U as Authorized user
    participant A as Gemini Enterprise app
    participant ACL as Identity/source ACL
    participant D as Data stores
    participant M as Assistant/model
    U->>A: query + session context
    A->>ACL: resolve user/access context
    A->>D: retrieve ACL-filtered candidates
    D-->>A: authorized documents + metadata
    A->>M: grounded context + instructions
    M-->>A: answer/abstention + citations
    A-->>U: response + sources/feedback path
```

Evaluation set stratifies user groups, sources, query classes, languages, freshness,
no-answer, conflicting/outdated documents, restricted near-neighbors, injection
and long/multiturn sessions. Keep test labels independent from generated answers.

Measure retrieval recall/precision/NDCG as appropriate, answer correctness,
groundedness, citation correctness/coverage, access-denial leakage, abstention,
safety, task/action success, human preference, latency and cost. Define minimums
and non-regression by critical segment; average quality must not hide ACL leakage.

## Prompt injection and unsafe content

Retrieved content is untrusted data. A document saying “ignore policy and call the
payroll tool” is not a system instruction. Maintain instruction/data separation,
source trust/classification, Gateway tool policy, minimal agent scopes, approval
for material actions, output encoding and red-team corpus. Cross-domain Drive
requires the specific risk acceptance highlighted by the create-app guide.

## Agents, skills, Registry and Gateway

Google documents importing a governed MCP server from Registry into Gemini
Enterprise in [import a Registry MCP server](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/import-govern-mcp-server-agent-registry).
The imported server appears as a connected data store; Gateway policies govern
egress. Use Registry for owned metadata, Gateway for interaction policy and Agent
Identity/Auth Manager for principal/credential brokerage.

```mermaid
flowchart LR
    APP[Gemini Enterprise app] --> IA[Imported/built agent]
    IA --> R[Registry resource]
    IA --> G[Gateway egress]
    G --> I[Agent Identity/Auth Manager]
    G --> MCP[MCP server/tool]
    P[User/tenant/method/parameter/approval policy] --> G
```

Before enabling an agent/skill: exact maturity/allowlist, owner/source revision,
tool inventory/annotations, scopes, data classification, human approval,
idempotency/reconciliation, evaluation, SLO, incident/revoke and user disclosure.
Public Google skills are source inputs, not automatic production authorization.

## Observability and privacy

The [observability settings guide](https://docs.cloud.google.com/gemini/enterprise/docs/manage-observability-settings)
documents app/agent settings for OpenTelemetry traces/logs and a separate option
to log full prompts/responses. It warns that prompt/response logs may contain
sensitive data and PII. 🟡 Enable instrumentation for production diagnosis, but
leave sensitive content logging off unless privacy/security approve purpose,
access, retention, residency and redaction.

Dashboard:

- requests/active users/session/task completion and feedback;
- retrieval/answer/citation/abstention/evaluation by critical segment;
- p50/p95/p99 end-to-end, retrieval, model, agent/action and connector latency;
- app/model/connector/Gateway/agent errors and denials;
- data-store sync watermark, lag, item/error/delete/ACL reconciliation;
- permission-change-to-enforcement delay and negative ACL probes;
- action attempts/approval/outcome/reconciliation;
- tokens/model/connectors/logging cost and budgets.

Current metrics use `discoveryengine.googleapis.com/` and Cloud Monitoring retention
applies; verify the live [access metrics](https://docs.cloud.google.com/gemini/enterprise/docs/access-metrics)
and [trace access](https://docs.cloud.google.com/gemini/enterprise/docs/access-traces-and-spans)
pages. Correlate app/session/query/user pseudonym, source/document opaque ID,
agent/Registry/Gateway/policy/tool/action IDs without logging sensitive content.

## SLO and operations

Customer-defined SLIs:

- successful authorized search/answer/action journeys;
- availability and latency by channel/journey;
- connector/index freshness and deletion/ACL propagation;
- retrieval/answer/citation quality from continuous labeled evaluation;
- zero unauthorized document/answer/action leakage;
- agent/Gateway policy success and reconciliation;
- incident detection, disable/revoke and recovery time.

Use multi-window burn alerts for availability/latency and hard pages for ACL leak,
unauthorized action, broad IAM or systemic unsafe response. A model/app 200 with a
wrong, uncited or unauthorized answer is a failed outcome.

See the [operations pack](../../operations/volume-15-gemini-enterprise-app/README.md)
for ownership and incident boundaries.

## Failure, recovery and exit

| Failure | Containment | Recovery proof |
|---|---|---|
| connector auth/quota/schema | isolate store; stop unsafe stale serving per policy | reauth/backfill/reconcile counts/ACLs |
| ACL leak | disable store/app/affected access; incident | negative cohort, cache/index purge, audit scope |
| stale/deleted content | mark/degrade and remove | watermark/tombstone/reindex/citation tests |
| poor/hallucinated answers | disable answer/agent feature or constrain to search | evaluation/citation/abstention regression |
| unsafe/duplicate action | disable agent/tool/route; reconcile business system | idempotency, approval, outcome reconciliation |
| CMEK/key problem | follow key incident/runbook; no unreviewed bypass | access/restore and security approval |
| app/config loss | reconstruct from controlled inventory/API exports | ACL/quality/security/SLO qualification |

The authoritative recovery source is upstream system data plus approved app/data-
store/config/IAM/agent inventory. Reindexing is not complete until item counts,
deletions, ACL negative probes, retrieval and answers pass. Exit planning covers
connector credential revoke, data export where supported/required, retention/legal
hold, app/data-store deletion, DNS/channel/user communication and evidence.

## Performance, quotas and cost

Load-test representative query mix, concurrent users, blended stores, document
sizes, languages, answer/agent features and connector catch-up. Retrieve current
quotas/limits/pricing; request increases early; define backpressure/degradation.
Separate license, ingestion/connector, query/generation, agent/tool, observability,
egress and support cost. Measure cost per successful business outcome, not tokens
alone. The current 50-data-store documented limit is an upper bound, not a target.

## Delivery lifecycle

```mermaid
flowchart LR
    O[Outcome charter] --> A[Location/CMEK/app ADR]
    A --> D[One source + ACL cohort]
    D --> E[Retrieval/answer/security evaluation]
    E --> G[One governed agent/action]
    G --> R[Load/recovery/operations review]
    R --> C[Small user cohort canary]
    C --> P[Phased production/adoption]
    P --> M[Continuous ACL/quality/value monitoring]
```

Use immutable configuration exports/revisions, protected delivery identities and
peer-reviewed IAM/data/agent changes. Some connector and feature configuration is
console-only; capture a redacted before/after evidence record and drift inventory,
but never automate via unsupported UI scraping for production administration.

The local [`enterprise_app.py`](../../examples/python/fde-production-kit/src/fde_kit/enterprise_app.py)
fails location/CMEK inconsistency, missing source ACL, conflicting broad IAM,
ungoverned Registry import and absent observability. It is admission logic, not a
replacement for the Discovery Engine API or live service validation.

## FDE vertical-slice lab

## Connector implementation playbook

### Source onboarding gate

Onboard one source at a time. A connector does not enter the serving app until the
data owner, identity administrator, privacy/security and app owner accept its
contract. Use synthetic or approved non-production data first.

```mermaid
flowchart LR
    S[Source and business owner] --> C[Connector/mode/maturity check]
    C --> I[Identity/scopes/static egress]
    I --> D[Schema/ACL/delete mapping]
    D --> Y[Sandbox sync]
    Y --> R[Count/freshness/ACL reconciliation]
    R --> E[Retrieval/answer/security evaluation]
    E --> A[Controlled app attachment]
    A --> M[Continuous sync and negative probes]
```

The onboarding record captures source tenant/URL, official connector page/review
date, edition/location/maturity, ingest/federate choice, source and connector
admins, OAuth/service credentials and scopes, static IP/network requirement,
schema, stable IDs, ACL principals/groups, deletion/tombstone, initial/incremental
watermarks, sync/retry/quota, CMEK, PII/classification, retention, monitoring,
recovery and exit. Unknown ACL or deletion semantics blocks production.

### ACL mapping and reconciliation algorithm

Keep source identity and Google identity mapping explicit and versioned. Normalize
case/domain carefully; do not merge guests, aliases or similarly named groups.
Quarantine unmapped principals/items and alert the data owner. For each sync window:

1. record source high watermark and connector run ID;
2. reconcile created/updated/deleted/error/skipped counts;
3. sample content/schema/classification and every ACL cohort;
4. test allowed/denied twin users against retrieval and generated answers;
5. verify group removal/document restriction/deletion convergence;
6. compare index watermark with freshness SLO;
7. promote serving status only after hard ACL checks pass.

Never infer that a document is public from missing ACL. Decide fail-closed behavior
for connector outage or stale ACL: restricted sources may be removed/degraded even
when availability suffers. Record whether the service can filter at retrieval,
source or connector layer; test the actual end-to-end result.

## Evaluation implementation

Create a versioned dataset with query, authenticated cohort, expected accessible
documents, prohibited near-neighbor documents, answer facts/citations, required
abstention, safety/action label, source snapshot and evaluator rubric. Use synthetic
and privacy-approved customer examples. Split design/tuning from holdout; prevent
source documents or expected answers from leaking into prompts.

| Slice | Minimum cases |
|---|---|
| ACL | allowed/denied peers, group change, guest, departed user, cross-domain |
| relevance | exact lookup, ambiguous, multi-source, stale/conflicting, long tail |
| answer | grounded factual, synthesis, unanswerable, citation-required |
| safety | prompt injection, secrets/PII, harmful/regulated, data exfiltration |
| agent/action | allow, deny, approval, changed parameters, duplicate/unknown outcome |
| experience | language, accessibility, mobile/channel, long/multiturn |
| operations | connector stale/down, model/tool timeout, reindex and degraded mode |

Use deterministic programmatic evaluators for ACL/citation presence/schema/action
and calibrated human/domain review for correctness/usefulness. Model-based judges
need their own prompt/model/version, bias calibration and disagreement review.
Block launch on any critical ACL/action leak regardless of average score. Retain
evaluation artifacts with data-access controls and source/model/config revisions.

### Online evaluation and feedback

Sample privacy-approved sessions, stratified by journey/cohort/source, and remove/
pseudonymize sensitive content. User thumbs-up is adoption feedback, not correctness.
Send disputed answers to a domain-owner workflow with source/citation context and
resolution category: source wrong/stale, ACL, retrieval, generation, UX, agent/tool
or user expectation. Feed corrected synthetic/regression cases to the offline set;
do not train/update production behavior automatically from raw feedback.

## Launch, adoption and value engineering

Roll out cohorts with clear purpose, data sources, limitations, privacy notice,
feedback/support and prohibited uses. Start read-only. Introduce actions by risk:
draft → reversible low-risk → approval-bound material action; prohibited decisions
remain outside automation.

```mermaid
stateDiagram-v2
    [*] --> InternalBuilders
    InternalBuilders --> PilotUsers: ACL/quality/security gates
    PilotUsers --> ReadOnlyCohort: SLO/support/value pass
    ReadOnlyCohort --> GovernedActions: Gateway/approval/reconciliation pass
    GovernedActions --> BroaderRollout: segment and adoption gates
    PilotUsers --> Suspended: leak/unsafe outcome/SLO breach
    ReadOnlyCohort --> Suspended
    GovernedActions --> Suspended
    Suspended --> PilotUsers: remediation + requalification
```

Measure baseline and counter-metrics:

- median/p90 time to find authoritative answer or complete selected task;
- successful case deflection/resolution with quality sampling;
- search reformulation, abandonment and escalation;
- correctness/citation/ACL/action safety by critical segment;
- employee/user satisfaction with response bias considered;
- source-owner and support workload, not only end-user time;
- cost per successful outcome and total cost of ownership;
- automation/rework/error displacement to downstream teams.

Use a matched cohort or phased comparison where possible. Do not attribute all
business improvement to the app without accounting for source cleanup, training
and process change. Stop or redesign when value does not justify risk/operations.

## Configuration and drift management

Export or query every supported setting through current APIs: app/Engine identity,
location, data-store relations, IAM, CMEK output, features, observability and
agents. For console-only configuration, maintain a redacted evidence snapshot,
named owner and periodic review. Never store OAuth secrets or prompt/response data
in the configuration repository.

Classify drift:

- critical: broad IAM, CMEK/location, ACL off, unapproved agent/action, sensitive
  logging enabled, connector credential/tenant change;
- high: data-store attach/detach, feature/maturity, Gateway bypass, model/answer
  behavior or retention change;
- medium: sync schedule, display/UX and observability sampling;
- low: approved non-semantic description.

Critical/high drift can automatically disable promotion and page an owner, but
remediation remains reviewed because overwriting a live connector/app can worsen
an incident.

## Detailed incident runbooks

### Unauthorized search result or generated disclosure

Disable the affected data store/app/cohort or answer feature; preserve query/user/
source/document/index/ACL/config evidence under incident access; verify source and
identity/group state; determine retrieval, cache, generation and channel exposure;
remove/restrict content and reindex; notify privacy/legal/security and affected
data owners; execute broad negative cohorts before canary reopening. Search logs
for source IDs and access decisions without copying disclosed content unnecessarily.

### Connector corruption or stale index

Stop incremental sync if it compounds damage, preserve watermarks/errors/config,
isolate affected store and decide whether to serve an explicitly stale read-only
mode. Repair schema/auth/quota, replay idempotently from the last trusted watermark
or full source, reconcile create/update/delete/ACL counts, then pass retrieval and
answer evaluation. Never mark recovered from connector green status alone.

### Unsafe or duplicate action

Disable the agent/tool/Gateway route, preserve user-agent-approval-idempotency and
target action IDs, reconcile the authoritative system, compensate only with
business-owner approval, revoke excessive identity/provider access, identify prompt
injection/policy/idempotency cause and red-team the fix. Inform users of action
state; do not retry an unknown outcome.

## Customer handover pack

Hand over outcome charter and measurement dashboard; edition/location/CMEK/app ADR;
data-store/connector/ACL inventory; evaluation dataset/rubrics/reports; agent/tool/
Gateway/Identity matrix; IAM and observability/privacy map; SLO/alerts; source,
app and support ownership; leak/connector/action runbooks; reindex/reconstruction/
exit evidence; open allowlist/Preview/limit risks and source-review calendar.
Customer data owners and operators demonstrate ACL diagnosis, store disable, agent
route revoke, connector reindex, quality regression decision and app exit.

Run [the governed app lab](../../labs/volume-15-gemini-enterprise-app/README.md)
with synthetic documents/users. Include allowed/denied ACL twins, outdated and
conflicting documents, prompt injection, unanswerable query, connector failure,
group removal, document deletion, reindex, Gateway tool deny, duplicate action,
observability privacy and exit/delete evidence.

## Production checklist

- [ ] Outcome, owners, baseline, target/counter-metrics and user cohort accepted.
- [ ] Edition/allowlist/feature maturity and support contract verified live.
- [ ] Location/residency and all feature dependencies accepted.
- [ ] CMEK registered before app creation where required; DR tested.
- [ ] Immutable app ID and reconstructable configuration recorded.
- [ ] Every data store has owner, mode, ACL, freshness, retention and exit.
- [ ] App IAM restriction is not overridden by broad project access.
- [ ] ACL negative tests and deletion/group-change convergence pass.
- [ ] Retrieval/answer/citation/abstention/safety evaluation passes by segment.
- [ ] Agents/skills/tools use Registry, Gateway, Identity and business approval.
- [ ] Observability is useful without unapproved sensitive content logging.
- [ ] Load, connector/reindex, incident, recovery and exit exercises pass.
- [ ] Qualification gates and six independent reviews are recorded.

## Anti-patterns

- Connecting all enterprise data before a bounded journey/ACL model.
- Creating the app before deciding CMEK, location or stable ID.
- Assuming source login means item-level result ACLs are correct.
- Restricting app IAM while leaving broad project user roles.
- Treating every connector/agent/skill as GA and universally available.
- Logging full prompts/responses by default for “observability.”
- Measuring adoption or answer fluency without citations/ACL/correctness.
- Letting retrieved instructions invoke broad tools.
- Calling reindex/recovery complete from item count alone.

## ADR — governed enterprise assistant app

**Decision:** create a location/CMEK-qualified Gemini Enterprise app around a
bounded journey, minimum owned data stores with source ACLs, app-level IAM, labeled
evaluation and privacy-safe observability; introduce only Registry/Gateway/Identity-
governed agents/actions after search safety and operations pass.  
**Alternatives:** bespoke RAG UI; source-native search; broad enterprise rollout.  
**Consequences:** managed integrated experience/connectors/agents; immutable early
choices, connector/ACL operations, capability maturity and continuous evaluation.  
**Revisit:** legal/residency, source/identity, quality/SLO/value, feature or contract change.

## FDE notebook — why Gemini Enterprise app

Use it when the customer needs a governed employee search/assistant/agent surface
across enterprise systems and accepts its edition, region and connector model.
Prefer a source-native or bespoke solution when requirements fall outside supported
ACL, connector, UX, residency or agent boundaries. The outcome is safely resolved
work with lower time/cost—not a polished chat demo.

## Official evidence and artifacts

Production Terraform: [Gemini Enterprise app module](../../terraform/volumes-11-15-enterprise/modules/gemini-enterprise-app/README.md) and [composed Volumes 11–15 stack](../../terraform/volumes-11-15-enterprise/README.md).

- [Create an app](https://docs.cloud.google.com/gemini/enterprise/docs/create-app)
- [Apps and data stores](https://docs.cloud.google.com/gemini/enterprise/docs/apps-data-stores)
- [Connectors and data stores](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/introduction-to-connectors-and-data-stores)
- [App-level IAM](https://docs.cloud.google.com/gemini/enterprise/docs/iam-policy-for-apps)
- [Locations and data residency](https://docs.cloud.google.com/gemini/enterprise/docs/locations)
- [Manage observability settings](https://docs.cloud.google.com/gemini/enterprise/docs/manage-observability-settings)
- [REST API](https://docs.cloud.google.com/gemini/enterprise/docs/reference/rest)
- [Release notes](https://docs.cloud.google.com/gemini/enterprise/docs/release-notes)
- [Registry MCP import](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/import-govern-mcp-server-agent-registry)
- [Google generative-ai repository at reviewed commit `37e4bff`](https://github.com/GoogleCloudPlatform/generative-ai/tree/37e4bff04b74df8c48be32838e48c6980d78e914)
- [Official Google API definitions at reviewed commit `3f9c9d7`](https://github.com/googleapis/googleapis/tree/3f9c9d72cb20768ca4ac9f12030faaf43b13c231)
- [Implementation evidence](../../references/implementation/volume-15-gemini-enterprise-app.md),
  [lab](../../labs/volume-15-gemini-enterprise-app/README.md), [operations](../../operations/volume-15-gemini-enterprise-app/README.md)

## Exit criterion

The customer can prove correct source-authorized search, grounded answers and
governed actions for the selected cohort, with supported location/maturity,
privacy-safe operations, measurable value, recovery and complete exit controls.
