# Operator queries

Replace project, region, and service placeholders. Save approved queries in the customer's observability repository.

## Admission errors

~~~text
resource.type="cloud_run_revision"
resource.labels.service_name="platform-admission"
severity>=ERROR
~~~

## Policy denials by version and governed cell

~~~text
resource.type="cloud_run_revision"
resource.labels.service_name="platform-admission"
jsonPayload.outcome="denied"
~~~

Add `jsonPayload.policy_version` and `jsonPayload.governed_cell` as result fields. Do not add raw identity or request content to logs.

## A rollout-correlated window

~~~text
resource.type="cloud_run_revision"
resource.labels.service_name="platform-admission"
timestamp>="INCIDENT_START_RFC3339"
timestamp<="INCIDENT_END_RFC3339"
~~~

Correlate `resource.labels.revision_name`, `jsonPayload.correlation_id`, and `logging.googleapis.com/trace` with the Cloud Deploy rollout and image digest.

Syntax and routing behavior are documented in [Logging query language](https://docs.cloud.google.com/logging/docs/view/logging-query-language) and [log routing](https://docs.cloud.google.com/logging/docs/routing/overview).

