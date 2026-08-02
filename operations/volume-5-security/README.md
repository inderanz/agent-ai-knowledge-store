# Volume 5 security operations

Operate from the normalized business action and its full decision chain. Raw
prompt capture is neither required nor automatically approved.

## Primary alerts

- authentication, DPoP/mTLS/token-audience or delegation anomalies;
- direct endpoint, Gateway or policy bypass;
- cross-tenant/method/parameter authorization denial spikes;
- Model Armor block/error/latency and safe-regression changes;
- unknown Registry publisher, endpoint, schema, version or lifecycle drift;
- forbidden egress, redirect, DNS, metadata/SSRF or target-auth failure;
- secret/key access anomaly or canary-secret observation;
- unsigned/changed/vulnerable artifact or unapproved policy/config drift;
- SCC/Gateway/runtime telemetry outage or actionable security finding; and
- loop/fan-out/cost anomaly and ambiguous business writes.

## Containment order

Preserve the minimal approved evidence; disable the affected action/tenant;
block direct/Gateway route or egress; revoke the narrow user delegation, agent,
runtime identity, tool or secret; freeze promotion and Registry publication;
quarantine the release; reconcile uncertain writes; then restore from trusted
source. Avoid broad project shutdown when a narrower safe containment works.

## Recovery and closure

Rebuild an immutable artifact and policy from reviewed source, rotate exposed
credentials, validate identity/network/content/action controls, restore only
approved data/state, replay idempotently, reconcile the target ledger, canary,
monitor, and attach evidence. Close only after revocation propagation, affected
subjects/data, residual exposure, customer communications, and control changes
are documented and accepted.
