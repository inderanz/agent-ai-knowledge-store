# Verified upstream baseline

**Verification date:** 2 August 2026 (Australia/Melbourne)

## 🟢 Official Google Capability

- ADK Python 2.0 reached GA on 19 May 2026 and introduced the Workflow Runtime with graph-based, dynamic, and collaborative workflows.
- The latest stable ADK Python release observed from the official GitHub Releases API is `v2.6.1`, published 31 July 2026 UTC.
- Gemini Enterprise Agent Platform release notes document the April 2026 platform naming transition, including Agent Engine becoming Agent Runtime.
- The documented API resource name can remain `ReasoningEngine` for backward compatibility even where product documentation says Agent Runtime.
- Agent Gateway, Agent Registry, Agent Identity, and related sub-capabilities have independent maturity and topology constraints. Never assign one blanket maturity label to the whole platform.

## 🟡 Enterprise Architecture Recommendation

Pin `google-adk==2.6.1` for the current qualification cycle; do not use an unconstrained `2.x` range. Requalify before upgrading. For managed services without semantic product versions, pin provider/API inputs where possible and record release-note verification, region, maturity, quota, and contractual constraints.

## Naming rule

Use the current product name in prose and the exact API/resource name in code. When they differ, state both at first use. Do not mechanically rename API symbols.

## Limitations of this baseline

This file confirms the repository starting point, not every service version. Each chapter owns its narrower dependency and capability matrix in front matter and its research record.
