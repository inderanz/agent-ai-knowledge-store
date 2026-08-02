# Volume 4 runtime qualification lab

## Local preflight

~~~bash
PYTHONPATH=examples/python/fde-production-kit/src \
  python3 -m unittest examples/python/fde-production-kit/tests/test_runtime.py -v
python3 delivery/volumes-4-10/validate_qualification.py \
  labs/volume-4-runtime/qualification.example.json --production
~~~

The example must fail production validation. Copy it to the customer evidence
store, replace every placeholder, and attach reports behind each accepted gate.

## Authorized sandbox sequence

1. Capture measured protocol, latency, concurrency, memory, event and state needs.
2. Run the placement validator and review Agent Runtime, Cloud Run and GKE options.
3. Verify every required capability's current location and maturity.
4. Build an immutable artifact through the customer pipeline and validate the
   runtime contract, identity, secrets, health, deadline and shutdown behavior.
5. Exercise PSC/DNS/private target access and prove no unintended public fallback.
6. Run step, spike, soak, cold-start, downstream-slow and quota tests.
7. Pause/resume an in-flight workflow through a compatible and incompatible release.
8. Inject an unknown target write and prove reconciliation without a duplicate.
9. Exercise the selected canary mechanism, kill switch, rollback/roll-forward and DR.
10. Validate the completed record with `--production` and obtain customer acceptance.

Cleanup uses an approved exact-resource change. Do not generically delete a
project, shared Agent Runtime instance, session store, network attachment,
evidence bucket, artifact repository, or encryption key.
