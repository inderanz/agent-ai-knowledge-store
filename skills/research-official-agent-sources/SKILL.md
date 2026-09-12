---
name: research-official-agent-sources
description: Research agent-platform, agentic-AI, and FDE delivery changes using current official Google, OpenAI, or Anthropic documentation and source repositories. Use for upstream release review, citation refresh, product maturity verification, implementation research, or an evidence packet that will support handbook, code, Terraform, lab, or runbook changes.
---

# Research Official Agent Sources

Produce a bounded evidence packet before proposing a technical change.

## Workflow

1. Read [references/evidence-contract.md](references/evidence-contract.md).
2. Restate the research question, decision, affected customer outcome, and as-of date.
3. Search official sources in this order: product documentation, release notes, tagged source, official samples, architecture guidance, then official engineering or careers material.
4. Pin software evidence to a release tag or full commit SHA. Do not cite a moving branch as implementation proof.
5. Capture each supported claim with source ID, URL, exact section or code path, retrieval date, evidence tier, maturity, and a short paraphrase.
6. Mark inferences explicitly. Never convert another vendor's delivery practice into a Google product claim.
7. Record contradictions, missing evidence, regional or quota uncertainty, and what would falsify the recommendation.
8. Run `python3 scripts/validate_evidence.py <packet.json>` before handoff.

## Stop conditions

- Stop when a material claim has no official support.
- Stop when Preview, allowlist, region, quota, pricing, or support status cannot be established.
- Stop when source code and current product documentation conflict; escalate the conflict rather than choosing silently.
- Never use search snippets, community posts, generated summaries, or this handbook as primary proof.

## Output

Return the validated evidence packet and a concise list of facts, inferences, unknowns, and impacted repository surfaces. Do not edit qualified baselines during research.
