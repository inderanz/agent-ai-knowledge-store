---
name: assess-upstream-impact
description: Convert a validated upstream evidence packet into a risk-classified repository impact plan. Use when an official release, documentation change, deprecation, maturity change, security advisory, source drift, or overdue review might affect handbook volumes, code, Terraform, delivery controls, labs, operations, citations, or qualified baselines.
---

# Assess Upstream Impact

Map evidence to the complete delivery unit before authoring.

## Workflow

1. Require a validated evidence packet from `research-official-agent-sources`.
2. Read [references/impact-contract.md](references/impact-contract.md).
3. Search source IDs, product names, versions, API names, resource types, and cited URLs across the repository.
4. Trace each affected claim through documentation, code, infrastructure, delivery, lab, operations, evidence, and CI surfaces.
5. Classify each impact as mechanical, semantic, behavioral, breaking, security, operational, or maturity.
6. Assign risk, owner, required reviewers, validation gates, rollback, and customer consequence.
7. Include a justified `no_change` decision for inspected surfaces that remain valid.
8. Stop if an affected path or owner cannot be determined.

## Output

Produce one impact manifest. Do not edit files during impact assessment. Every proposed path must cite one or more evidence IDs and state why the existing content is now incomplete, incorrect, unsafe, or insufficiently practical.
