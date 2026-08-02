# Bootstrap research audit — 2 August 2026

## Outcome

The three imported chapters are retained as Drafts. Their core ADK 2.x framing is supported, and all 57 extracted external links returned HTTP 200 during the bootstrap check. They do not yet satisfy the new chapter contract, evidence classification, implementation tests, or six review gates.

## 🟢 Official Google Capability

- ADK Python v2.0.0 reached GA on 19 May 2026 and introduced the Workflow Runtime, including graph-based, dynamic, and collaborative workflows. [Official ADK 2.0 overview](https://adk.dev/2.0/)
- The latest official ADK Python release at audit time is v2.6.1, published 31 July 2026 UTC. [Official release](https://github.com/google/adk-python/releases/tag/v2.6.1)
- The v2.6.1 source exports `Agent`, `Context`, `Event`, `Runner`, and `Workflow` from `google.adk`; it exports `node` from `google.adk.workflow`. This supports the draft import paths, but not every example's runtime semantics. [Official source at v2.6.1](https://github.com/google/adk-python/tree/v2.6.1)
- Agent Gateway and Agent Registry reached GA on 18 June 2026. Agent Observability also reached GA that day. [Agent Platform release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes)
- Agent Identity has a mixed maturity surface: the core capability is documented as GA, while the newer `agentidentity.googleapis.com` management API and some authentication models or integrations remain Preview. [Agent Identity overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-identity-overview)
- Agent Runtime is the current product name, while the API resource can remain `ReasoningEngine` for backward compatibility. [Agent Runtime documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime)

## Draft findings

### Graph engineering chapter

- Strong conceptual foundation and valid primary links.
- Uses a placeholder `google-adk==2.x.y`; this is intentionally non-runnable and must become an exact qualified patch version in implementation material.
- Does not implement the repository's required chapter ending or classification on every architectural section.

### Agent Platform reference architecture

- Covers relevant planes and components, but every gateway topology, project/region co-location, identity, and Model Armor statement needs paragraph-local evidence.
- Product maturity must be refreshed to reflect June 2026 GA transitions and mixed-maturity sub-capabilities.
- The monolithic diagram needs concern-specific logical, physical, identity, security, network, deployment, data, lifecycle, state, and failure diagrams.

### ADK workflow engineering

- Top-level ADK imports used by the draft exist in v2.6.1.
- The draft pins v2.0.0 in one dependency example, so it is not the current implementation baseline.
- Import existence is not execution validation. Node signatures, event construction, resume behavior, retry behavior, and runtime deployment examples require tests against v2.6.1.

## 🟡 Enterprise Architecture Recommendation

Promote the chapters independently. For each one: update its research record; assign paragraph-local classifications; extract runnable code into `examples/`; add relevant Terraform and labs; run the six review gates; then relocate it into its volume and add it to the published handbook contents.

## Evidence captured

- ADK release: v2.6.1 (`740582e9f283cd23ff5cec1389400b422513f765` at the official tag during source audit).
- ADK docs main: `308c7831800d4543ac230f5a64da335796575135`.
- ADK samples main: `739bb34c0bd22516dbbda88f3e5a9f9375bb963c`.
- Link check: 57 unique imported-draft URLs, all reachable on 2 August 2026.
