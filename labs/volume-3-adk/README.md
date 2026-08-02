# Volume 3 executable FDE labs

Local labs are non-mutating. Sandbox deployment is billable and must be run only
with explicit customer authority in the exact named project.

| Lab | Outcome | Local/cloud | Exit evidence |
|---|---|---|---|
| 1 | Prove contracts, authz, approval binding and idempotency | local | 19 domain/delivery tests pass |
| 2 | Compile the graph against ADK v2.6.1 | CI/local venv | topology smoke test passes |
| 3 | Prove deterministic release cases | local | 100% pass report |
| 4 | Exercise interruption/resume and managed sessions | customer sandbox | event history and resume evidence |
| 5 | Inject write timeout, replay, concurrency and dependency failure | customer sandbox | no duplicate write; reconciliation evidence |
| 6 | Qualify production controls and operate a canary | customer environment | signed qualification record and rollback drill |

## Labs 1–3: local gates

~~~bash
export PYTHONPATH=examples/python/adk-enterprise-workflow/src:examples/python/adk-enterprise-workflow
python3 -m unittest \
  examples/python/adk-enterprise-workflow/tests/test_models.py \
  examples/python/adk-enterprise-workflow/tests/test_workflow.py \
  examples/python/adk-enterprise-workflow/tests/test_telemetry.py \
  examples/python/adk-enterprise-workflow/tests/test_evaluation.py \
  examples/python/adk-enterprise-workflow/tests/test_deploy.py -v
python3 examples/python/adk-enterprise-workflow/evaluate_release.py \
  examples/python/adk-enterprise-workflow/evals/release_cases.json
python3 -m unittest discover -s delivery/volume-3-adk -p 'test_*.py' -v
python3 -m unittest discover -s labs/volume-3-adk -p 'test_*.py' -v
~~~

Install ADK only in an isolated worker with adequate disk, then run
`tests/test_adk_graph.py`. CI performs this against exactly v2.6.1.

## Lab 4: session and resume qualification

1. Create or select the approved Agent Runtime sandbox instance.
2. Use `VertexAiSessionService` with the exact project, location and Agent Engine
   ID; do not copy production content into ADK Web.
3. Run a high-risk case until it reaches an interrupt/pending boundary.
4. Record the event schema including `node_info` and `output`, restart the client,
   and resume with the matching session.
5. Verify completed nodes are not incorrectly replayed and no external write
   occurs before authenticated approval.
6. Test two concurrent invocations against the same business request; the
   durable business ledger, not session state, must suppress the duplicate.

## Lab 5: failure injection

- return an unknown outcome after the target may have committed and verify
  `RECONCILIATION_REQUIRED` without a second write;
- expire, alter, cross-tenant, or self-sign an approval and verify denial;
- interrupt after each node and compare the reconstructed event trajectory;
- exhaust repair, token, time, tool-call and concurrency budgets;
- revoke target access and confirm fail-closed behavior and actionable telemetry;
- inject duplicate and out-of-order events into the customer event adapter; and
- run the approved load profile through quota exhaustion and recovery.

## Lab 6: qualification and canary

Copy `qualification.example.json` into the customer evidence store, replace every
placeholder, and obtain the named control-owner decisions. Then run:

~~~bash
python3 labs/volume-3-adk/validate_qualification.py \
  /secure/customer/volume-3-qualification.json --production
~~~

Deploy to sandbox with the guarded dry-run/execute script, run online ADK
trajectory/groundedness/safety evaluation on an approved dataset, canary a small
customer cohort, exercise the kill switch and rollback, and attach the immutable
source revision, dependency lock, eval reports, load results and incident drill.

## Cleanup

No local command creates cloud state. For sandbox resources, use the exact
resource name emitted by deployment and the customer-approved deletion change.
Retain audit/evaluation evidence according to customer policy; never delete a
project, shared runtime, session store, evidence bucket, or encryption key as a
generic lab cleanup step.
