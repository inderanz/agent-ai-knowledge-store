# Documentation style and evidence standard

## Voice

Write as an engineering reference: direct, testable, implementation-focused, and free of marketing language. Do not use first-person speculation, guess APIs, or imply a recommendation is a Google capability.

## Classification

Every architectural section starts with one of these exact headings or callouts:

```markdown
### 🟢 Official Google Capability
### 🟡 Enterprise Architecture Recommendation
### 🔵 Field Pattern
```

A section can contain multiple classified subsections, but each claim must have an unambiguous owner. Product status is stated independently, for example: `Maturity: Public Preview as verified 2026-08-02`.

## Sources

Use the highest available tier:

1. Official Google documentation.
2. Official Google source code.
3. Official Google samples.
4. Google Cloud Architecture Center.
5. Applicable standards bodies: OpenTelemetry, CloudEvents, OAuth, OpenAPI, Kubernetes, or CNCF.
6. Industry best practice, explicitly labeled as a recommendation or field pattern.

Link a source at the sentence or paragraph it supports. A references section alone is insufficient for high-risk or fast-changing claims. Record reusable sources in `references/sources.json` with an owner, tier, and recheck interval.

## Chapter contract

Every completed chapter contains:

- front matter with status, owners, dates, baseline, and source review;
- executive summary, business problem, and customer story;
- discovery workshop and customer questions;
- architecture plus logical, physical, sequence, security, identity, deployment, data-flow, component, lifecycle, state, network, and failure diagrams where applicable;
- component deep dive and implementation;
- typed Python, Terraform, testing, Cloud Build, Cloud Deploy, and GitHub delivery guidance where applicable;
- security, operations, logging, monitoring, tracing, metrics, SLOs, runbooks, recovery, and disaster recovery;
- anti-patterns, FDE notebook answers, labs, and official references;
- every required end section listed in the chapter template.

“Not applicable” is acceptable only with a reason. Empty headings are not acceptable.

## Code

Code examples must be version-pinned, typed, configurable, logged, observable, tested, and explicit about retry and error semantics. Pseudocode must be labeled `pseudocode` and must never appear importable. Secrets, project IDs, regions, and customer identifiers must come from configuration.

## Diagrams

Use Mermaid source. Every edge must communicate a real direction or dependency. Diagram labels must distinguish control, data, identity, and telemetry flows. See [diagrams/README.md](diagrams/README.md).

## Status lifecycle

`Proposed → Researched → Draft → In review → Approved → Superseded`

Only Approved content is production guidance. A substantive upstream change returns affected content to Draft or In review.
