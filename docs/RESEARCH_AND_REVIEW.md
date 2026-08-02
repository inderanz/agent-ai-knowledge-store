# Research and review workflow

## Research before prose

For each chapter:

1. Define the customer outcome and claims that require evidence.
2. Read official product documentation.
3. Inspect relevant official source at a release tag or commit.
4. Run or inspect official samples at a recorded commit.
5. review product and library release notes, deprecations, known issues, regions, quotas, and maturity.
6. Record sources and verification dates in `references/sources.json`.
7. Compare existing handbook text with upstream evidence and open update findings.
8. Design architecture and implementation only after evidence review.
9. Run all six review gates before publication.

## Evidence record

Each chapter front matter records:

```yaml
status: Draft
last_verified: YYYY-MM-DD
next_review: YYYY-MM-DD
baseline:
  python: "3.12+"
  google_adk: "2.6.1"
review_gates:
  research: pending
  architecture: pending
  implementation: pending
  security: pending
  operations: pending
  customer_delivery: pending
```

## Continuous upstream validation

The weekly `upstream-docs-refresh.yml` workflow performs reachability, age, and official release checks; renders `references/UPSTREAM_STATUS.md`; and opens or updates an automation pull request when the observation report changes. A failed, stale, unreachable, or version-drift check also opens or updates the `Upstream documentation review required` issue.

A failed or stale source does not automatically rewrite prose or change the qualified baseline. It opens a review obligation: compare the changed upstream material, identify affected claims, revise code and prose deliberately, update verification metadata only after semantic review, and re-run all applicable gates.

Automated checks cannot prove semantic accuracy. The named chapter owner remains accountable for interpreting release notes and product status.

## Freshness policy

- Fast-moving ADK, Agent Platform, model, preview, and release-note sources: recheck at least every 14 days.
- Stable managed-service architecture sources: every 30 days.
- Standards and long-lived architecture guidance: every 90 days.
- Before every production customer engagement or major platform release: recheck all sources used by the affected chapters, regardless of age.
