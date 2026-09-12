---
name: synchronize-implementation
description: Keep handbook claims synchronized with Python, ADK graphs, Terraform, delivery pipelines, labs, evaluations, runbooks, evidence records, and CI. Use after a semantic or technical documentation change, dependency upgrade, API change, architecture decision, security control change, or maturity promotion that might leave companion artifacts inconsistent.
---

# Synchronize Implementation

Update the complete delivery unit described by the impact manifest.

## Workflow

1. Read [references/synchronization-matrix.md](references/synchronization-matrix.md).
2. Run `python3 scripts/check_changed_surfaces.py <changed-path>...` for an initial gap list.
3. Trace every changed contract, resource, variable, command, role, identity, state transition, metric, and failure behavior to its implementation and test.
4. Update implementation and negative tests before changing qualified versions.
5. Keep examples bounded, typed, idempotent, observable, and explicit about external side effects.
6. Update delivery, lab, operations, evidence, and CI artifacts required by the impact manifest.
7. Add migration and rollback whenever a persisted contract or deployed resource changes.
8. Record intentional `no_change` decisions for inspected companion surfaces.

Do not broaden cloud permissions, customer authority, regions, or supported maturity as a convenience for making an example pass.
