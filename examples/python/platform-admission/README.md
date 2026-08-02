# Platform admission service

This is the executable companion to Volume 2. It accepts an authenticated workload-onboarding request, validates it against customer-owned policy, creates a deterministic governed-cell placement, and persists an idempotent decision in Firestore.

It does **not** create projects or grant IAM. The decision is desired state consumed by a separately authorized Terraform workflow.

## Security boundary

Production requests must arrive through Identity-Aware Proxy (IAP). The service validates the signed `X-Goog-IAP-JWT-Assertion`, including signature, audience, issuer, expiry, subject, and email. Unsigned `X-Goog-Authenticated-User-*` headers are never trusted.

The Cloud Run service is configured for internal and Cloud Load Balancing ingress. The customer must attach it to an IAP-protected load balancer or replace the adapter with another reviewed identity verifier.

## Local verification

The domain and policy tests require only Python 3.12:

~~~bash
python3 -m unittest discover -s tests -v
~~~

Validate every Python file:

~~~bash
python3 -m compileall -q src tests main.py
~~~

Runtime dependencies are pinned in `requirements.lock`. Create an isolated environment only when sufficient disk is available:

~~~bash
python3 -m venv .venv
.venv/bin/pip install --requirement requirements.lock
PYTHONPATH=src .venv/bin/gunicorn --bind :8080 main:app
~~~

## Required production configuration

| Variable | Purpose |
|---|---|
| `GOOGLE_CLOUD_PROJECT` | Project used for Firestore and trace correlation |
| `IAP_EXPECTED_AUDIENCE` | Exact IAP audience for the Cloud Run service |
| `POLICY_PATH` | Mounted reviewed policy document |
| `SUBJECT_HASH_KEY` | Secret value with at least 32 characters |
| `FIRESTORE_COLLECTION` | Decision collection; defaults to `platform-admission-decisions` |
| `OTEL_ENABLED` | Enable direct OTLP trace export |
| `OTEL_REQUIRED` | Fail startup if telemetry cannot initialize |
| `OTEL_TRACE_SAMPLE_RATIO` | Trace sampling ratio from 0 through 1 |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Defaults to `https://telemetry.googleapis.com:443/v1/traces` |

Mount `SUBJECT_HASH_KEY` from Secret Manager. Do not commit its value.

The checked-in policy is valid but has `deny_all: true`, so a newly deployed service can become healthy without admitting any workload. Create a reviewed customer policy, set `deny_all: false`, add the authorized IAP subject or access level and real folder numbers, then rebuild it into the immutable container. Policy and code therefore promote under the same image digest; do not edit policy inside a running revision.

## API

`POST /v1/admissions` requires:

- a valid IAP signed assertion;
- `Idempotency-Key` containing a UUID;
- JSON matching the strict workload schema; and
- an identity allowed by the reviewed policy.

The response contains placement and required controls, never credentials or Terraform authority.

## Official implementation evidence

- [IAP signed-header validation](https://docs.cloud.google.com/iap/docs/signed-headers-howto)
- [Cloud Run container runtime contract](https://docs.cloud.google.com/run/docs/container-contract)
- [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity)
- [Cloud Run structured logging](https://docs.cloud.google.com/run/docs/logging)
- [Firestore transaction API 2.28.0](https://docs.cloud.google.com/python/docs/reference/firestore/latest/google.cloud.firestore_v1.transaction)
- [Direct OTLP trace export to Google Cloud](https://docs.cloud.google.com/trace/docs/migrate-to-otlp-endpoints)
- [Official OTLP Python sample at reviewed commit](https://github.com/GoogleCloudPlatform/opentelemetry-samples/tree/4cdacf711acb9d106fcc3a4ba5b0cd55cd192b26/python/otlptrace)
- [Official Cloud Run Python sample at reviewed commit](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/19f0efaa4a58007c9aa17ffe70e8101e6810abe6/run/helloworld)
