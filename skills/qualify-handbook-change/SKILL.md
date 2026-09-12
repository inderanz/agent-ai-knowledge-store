---
name: qualify-handbook-change
description: Qualify an agent-generated or human-authored handbook change before publication using evidence, citation, implementation, security, operations, FDE usability, and independent-review gates. Use when reviewing a documentation-maintenance proposal, version promotion, architecture change, practical customer asset, code or Terraform update, or any pull request that could influence enterprise production decisions.
---

# Qualify Handbook Change

Fail closed. Passing local tests does not prove a customer deployment.

## Workflow

1. Read [references/qualification-gates.md](references/qualification-gates.md).
2. Require the evidence packet, impact manifest, candidate-file manifest, author identity, and unresolved-risk list.
3. Confirm every changed product claim is supported by current official evidence and correctly classified.
4. Confirm candidate files and hashes exactly match the manifest; reject undeclared files.
5. Run repository and affected component gates with `python3 scripts/run_gates.py --root <repo>`.
6. Inspect security, data, identity, action, reliability, cost, support, and migration consequences.
7. Have a reviewer distinct from the author record findings and `approve-draft` or `reject`.
8. Keep all semantic changes as draft pull requests for human approval. Never allow an agent verdict to satisfy customer risk acceptance.

## Output

Return gate results, evidence gaps, residual risks, required human reviewers, and publication decision. `approve-draft` means suitable for human review; it never means automatically approved for production.
