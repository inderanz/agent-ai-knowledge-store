# Volume 3 operations pack

This runbook set operates the workflow as a governed business system, not merely
as a model endpoint. The primary operational keys are customer tenant,
request/invocation/session ID, workflow and prompt version, node path/run ID,
tool operation ID, approval decision ID, release revision and trace ID. Payloads,
credentials, raw prompts, and approval tokens must not be logged.

## Day-0 production gates

- qualification record passes `validate_qualification.py --production`;
- exact source revision and transitive dependency lock are archived;
- Agent Runtime location, feature availability, quotas and identity are checked
  from current product documentation and the target project;
- session/event schema migration, retention, deletion and restore are exercised;
- durable idempotency ledger and target reconciliation APIs are tested;
- approval identity, authorization, expiry, action digest and segregation are tested;
- deterministic plus approved online ADK evaluations meet release thresholds;
- latency, concurrency, token/tool-call/cost budgets and error budgets are set;
- log/trace redaction and evidence-sink access are independently reviewed; and
- rollback, kill switch, on-call ownership and customer communications are drilled.

## Core indicators

Track invocation/node latency, completion by terminal state, retry and repair
attempts, interrupt duration, resume success, approval wait/deny rates, duplicate
suppression, unknown write outcomes, reconciliation age, tool dependency errors,
model/token usage, evaluation drift and per-tenant cost. Alert on security or
irreversible-action control failures immediately; do not hide them inside an
aggregate availability metric.

Use the [incident runbook](incident-response.md) and [query catalogue](queries.md).
Product behavior and source evidence are linked from the
[implementation ledger](../../references/implementation/volume-3-adk.md).
