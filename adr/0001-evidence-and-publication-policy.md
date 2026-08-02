# ADR-0001: Evidence-gated publication

- Status: Accepted
- Date: 2026-08-02
- Owners: repository maintainers
- Related chapter: repository-wide
- Supersedes: none
- Superseded by: none

## Context

The platform and ADK change rapidly. Unqualified prose can confuse previews, recommendations, and supported product behavior.

## Decision

The handbook uses three claim classifications, a machine-readable source registry, dated baselines, and six review gates. Only Approved chapters are production guidance. Existing prose enters as Draft even when technically strong.

## Consequences

Publication is slower but auditable. Upstream changes create an explicit re-review obligation. CI can detect stale evidence but cannot replace engineering review.

## Validation

Repository validation fails when required structure or approved-chapter contracts are absent. Scheduled source checks detect unreachable and overdue evidence.

## Official references

- [Gemini Enterprise Agent Platform release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes)
- [ADK Python releases](https://github.com/google/adk-python/releases)
