# Enterprise ADK workflow companion

This package is the executable companion to Volume 3. It uses the public ADK
v2.6.1 `Workflow`, `Event`, `JoinNode`, `@node`, `Context.run_node`, and
`RequestInput` APIs, while keeping authorization, approval binding, idempotency,
and side effects in deterministic application code.

The example models an enterprise change request. The ADK graph performs parallel
identity/contract checks and stages a command. `EnterpriseWorkflow` then applies
customer policy, requires an authenticated and independently authorized approval
for high-risk changes, binds that approval to a canonical SHA-256 digest, and
calls an idempotent tool gateway. An unknown write outcome enters
`RECONCILIATION_REQUIRED`; it is never retried blindly.

## Trust boundaries

- `RequestInput` is suitable for workflow interruption and structured input. It
  is not proof of enterprise identity, authorization, or segregation of duties.
- ADK session state is workflow context, not the system of record for approvals,
  tool reservations, business transactions, or audit retention.
- `InMemoryToolGateway` is a test double. A production adapter must durably reserve
  the idempotency key and persist outcomes in a customer-owned data store.
- The checked-in graph does not invoke an irreversible customer API.

## Local deterministic verification

Python 3.12 is sufficient for all domain tests:

~~~bash
PYTHONPATH=src:. python3 -m unittest \
  tests/test_models.py tests/test_workflow.py tests/test_telemetry.py \
  tests/test_evaluation.py tests/test_deploy.py -v
PYTHONPATH=src python3 evaluate_release.py evals/release_cases.json
~~~

The ADK topology smoke test requires the pinned framework:

~~~bash
python3 -m venv .venv
.venv/bin/pip install 'google-adk==2.6.1'
PYTHONPATH=src .venv/bin/python -m unittest tests/test_adk_graph.py -v
~~~

The real graph-compilation test was run locally against a temporary, resolved
v2.6.1 installation and is repeated by CI. The temporary environment was removed
after testing because the workstation disk was nearly full; no project or global
Python environment was modified.

## Evaluations

`evals/release_cases.json` is a hermetic release gate for deterministic safety
invariants. `evals/adk_eval_config.json` records the online ADK criteria:
exact tool trajectory, response similarity, groundedness, and safety. Run the
online set only in a customer-approved project with a reviewed, non-sensitive
dataset and budgets; some criteria invoke paid Vertex AI evaluation services.

## Guarded sandbox deployment

Dry-run configuration rendering does not call Google Cloud:

~~~bash
PYTHONPATH=src python3 deploy.py \
  --project customer-agents-123 \
  --location us-central1 \
  --staging-bucket gs://customer-agents-staging
~~~

Creation requires both `--execute` and an exact `--confirm-project` value. The
script uses the official `agent_engines.AdkApp` and
`client.agent_engines.create` route with Agent Identity. It is a qualification
path, not a substitute for customer IAM, networking, CMEK, secrets, regional,
capacity, recovery, or production-release review.

Official implementation evidence and immutable source links are in the
[Volume 3 evidence ledger](../../../references/implementation/volume-3-adk.md).
