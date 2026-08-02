# Cloud Logging query catalogue

These are templates for the structured application fields defined by the
customer telemetry contract. Replace resource/project values; do not weaken
redaction or add raw request/model content merely to simplify debugging.

## Unknown outcomes requiring reconciliation

~~~text
jsonPayload.event_type="workflow.completed"
jsonPayload.status="RECONCILIATION_REQUIRED"
~~~

## Denials by workflow version

~~~text
jsonPayload.event_type="workflow.completed"
jsonPayload.status="DENIED"
jsonPayload.workflow_version="3.1.0"
~~~

## One request trajectory

~~~text
jsonPayload.request_id="CUSTOMER_APPROVED_REQUEST_ID"
~~~

Sort ascending by timestamp and correlate with the target operation and approval
stores. Request ID is a correlation key, not proof that event ordering or writes
are correct.

## Sensitive-field leakage detector

Use a customer-approved log router/DLP control to detect forbidden structured
keys such as `authorization`, `cookie`, `prompt`, `parameters`, `secret`, and
`token`. Treat a match as a security incident. Avoid a broad free-text query that
would expose suspected secret values to operators.

## SLO metrics to derive

- terminal success/denial/failure/reconciliation-required count;
- end-to-end and per-node latency distributions;
- approval pending age and resume success;
- retry/repair exhaustion and duplicate suppression;
- tool dependency outcomes and reconciliation age; and
- per-release/per-tenant evaluation and cost signals.

Cloud Logging queries scan retained data and can incur cost. Route only the
minimum approved fields, set retention deliberately, restrict access, and record
the customer evidence location separately from runtime logs.
