# Volume 4 runtime operations

Operate by request, runtime/revision, workflow/node, session, tool operation,
artifact digest and trace. Do not log raw prompts, response bodies, secrets or
arbitrary tool parameters without explicit approval.

## Primary alerts

- entry error-budget burn and tail latency;
- runtime instance/quota saturation and rejected work;
- model/tool dependency latency and failures;
- session/resume incompatibility or stuck joins;
- unknown write outcomes and reconciliation age;
- PSC/DNS/proxy/target authentication failure;
- canary quality/safety/SLO regression; and
- old vulnerable or directly queryable revisions.

## Containment order

Disable the affected action/tenant, stop new invocations, freeze promotion,
preserve evidence, revoke the narrow identity or network path if compromised,
reconcile uncertain writes, then route to a qualified revision or manual process.
Traffic rollback never reverses business side effects.

## Recovery

Restore source/artifact/configuration, policies/secrets/identity, sessions/state,
queues and business ledgers according to their separate RTO/RPO. Replay only
through the idempotent consumer and reconcile target operations. Canary after
recovery and attach the result to the incident and qualification record.
