# Volume 6 reliability qualification lab

## Local preflight

~~~bash
PYTHONPATH=examples/python/fde-production-kit/src \
  python3 -m unittest examples/python/fde-production-kit/tests/test_reliability.py -v
python3 delivery/volumes-4-10/validate_qualification.py \
  labs/volume-6-sre/qualification.example.json --production
~~~

The example must fail production validation. It contains no observed customer
SLI, alert, capacity, restore or incident evidence.

## Authorized sandbox/game-day sequence

1. Declare customer promises, populations, good/bad/total events and invariants.
2. Instrument trace-to-terminal-workflow and operation-to-target correlations;
   prove content minimization, cardinality and missing-data behavior.
3. Replay known traffic and independently verify SLI numerators/denominators.
4. Configure customer-selected SLOs and fast/slow burn alerts; inject enough
   synthetic bad events to verify notification, deduplication and runbook routing.
5. Inject authentication/policy, model/quota, state, retrieval, tool, telemetry,
   evaluator and queue failures; exercise explicit degradation modes.
6. Create a timeout after a synthetic target commit; prove the operation becomes
   `UNKNOWN`, reconciliation finds the transaction, and no duplicate occurs.
7. Run cold/step/spike/soak/dependency-slow/retry-storm tests; record capacity,
   fairness, headroom, quota and cost per correct outcome.
8. Restore source/artifact/config, policy/secrets, state, events, data and evidence
   from controlled backups/rebuilds and measure RTO/RPO.
9. Run a regional/dependency DR exercise including DNS, identity, keys, quotas,
   in-flight work, replay, reconciliation, canary and customer communications.
10. Give the runbook to an operator who did not author it; capture competency,
    gaps, assigned improvements, dates and acceptance.

Use synthetic data and exact authorized resources. Cleanup must retain evidence
and respect shared infrastructure, backups, legal holds and business ledgers.
