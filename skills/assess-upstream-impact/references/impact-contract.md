# Impact contract

## Repository surfaces

| Surface | Expected paths | Question |
|---|---|---|
| handbook | `docs/`, `README.md`, `SUMMARY.md` | Which claims, decisions, examples, or maturity labels change? |
| implementation | `examples/`, `terraform/` | Does a contract, version, resource, dependency, or security boundary change? |
| delivery | `delivery/` | Do build, release, provenance, promotion, or acceptance controls change? |
| qualification | `labs/`, tests, evals | Which evidence or regression case proves the new behavior? |
| operations | `operations/` | Do SLOs, alerts, incident steps, recovery, rollback, or support boundaries change? |
| evidence | `references/` | Which source, baseline, research ledger, or verification date changes? |
| automation | `.github/workflows/`, `scripts/`, `skills/` | Which maintenance or validation behavior changes? |

## Risk rules

- `low`: formatting, link repair, or observation-only metadata.
- `medium`: semantic guidance or non-breaking code that cannot change customer authority.
- `high`: version promotion, Terraform, IAM, network, data, action policy, security, reliability, or production workflow behavior.
- `critical`: destructive migration, customer data movement, broad authority, regulated decision, or unsupported product assumption.

High and critical changes require independent security and implementation review. All semantic changes require human approval even when agent qualification passes.
