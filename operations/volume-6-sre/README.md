# Volume 6 reliability operations

## Triage order

Confirm customer impact and invariants; identify release/tenant/action scope;
contain risky writes; verify signal continuity; split entry, Gateway/policy,
runtime, model, workflow/state, retrieval, tool/target, human and evaluation
failures; preserve minimal evidence; then recover and reconcile.

## Primary pages

- immediate or projected fast/slow error-budget exhaustion;
- unauthorized, cross-tenant or duplicate business effect;
- stuck workflow, loop/fan-out, unknown-write or reconciliation-age breach;
- model/tool quota, latency and error dependency exhaustion;
- severe quality/safety regression with defined containment;
- queue/concurrency/runtime saturation or cost-budget enforcement;
- telemetry/SLI/evaluator coverage gap; and
- backup/restore/DR evidence staleness beyond accepted limit.

## Safe recovery

Traffic rollback does not reverse business effects. Check workflow, session,
event, schema and target compatibility; stop blind retries; reconcile the target
ledger; restore each asset to its own RTO/RPO; replay idempotently; canary outcome,
quality, safety, latency and cost; communicate residual uncertainty; then update
tests, evaluations, capacity, runbooks or architecture with named owners.
