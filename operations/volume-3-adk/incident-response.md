# ADK workflow incident response

## Severity triggers

- **SEV-1:** unauthorized or cross-tenant action, approval bypass, suspected
  credential/prompt/customer-data disclosure, duplicate irreversible write, or
  loss of control over agent execution.
- **SEV-2:** widespread stuck workflows, resume corruption, unknown outcomes
  beyond the reconciliation SLO, evaluation/safety regression in production, or
  sustained critical dependency failure.
- **SEV-3:** localized degradation with a safe workaround and no control failure.

## First 15 minutes

1. Establish an incident commander, customer technical lead and security owner.
2. Activate the narrowest rehearsed kill switch: disable a tool/action/tenant,
   pause new invocations, or route to manual processing. Preserve read-only status
   where safe.
3. Revoke or narrow the affected runtime/tool identity if misuse is suspected.
4. Freeze promotion and prompt/model/config changes; record exact revisions.
5. Preserve immutable event, approval, idempotency, target-system and deployment
   evidence with access logging. Do not copy raw sensitive payloads into chat.
6. For every unknown write, reconcile against the target operation ID before any retry.

## Diagnosis order

1. Determine affected tenants, actions, releases and first/last occurrence.
2. Correlate business request → invocation/session → node path/run → approval
   decision → idempotency key hash → target operation.
3. Separate model-quality failures from deterministic policy/tool/runtime failures.
4. Check event ordering, interruption, resume/replay, concurrency and schema version.
5. Compare live policy, identity and dependency state with the approved release evidence.

## Recovery rules

- Never bulk-replay writes from ADK event history.
- Never treat a timeout as a confirmed failure.
- Resume only workflows whose graph/event versions are compatible and whose
  approvals remain valid for the exact action digest.
- Prefer compensation only when the business owner defined and tested it; a
  compensating action is another governed write, not a rollback guarantee.
- Restore service through a previously qualified artifact/configuration, then
  canary and rerun deterministic and online evaluation gates.

## Closure evidence

Record timeline, impact, customers/tenants, data and actions affected, root and
contributing causes, control performance, every reconciliation/compensation,
release and dependency versions, evaluation delta, communications, owners and
dated corrective actions. Update tests and runbooks before closing the incident.
