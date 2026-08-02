# Volume 9 FDE engagement simulation

## Local preflight

~~~bash
PYTHONPATH=examples/python/fde-production-kit/src \
  python3 -m unittest examples/python/fde-production-kit/tests/test_delivery.py -v
python3 delivery/volumes-4-10/validate_qualification.py \
  labs/volume-9-fde/qualification.example.json --production
~~~

The example must fail. A repository cannot assert customer charter, launch,
operating ownership, competency or value.

## Simulation

Use a synthetic regulated case-workflow and assign sponsor/product, FDE,
domain/security/SRE reviewer and receiving engineer/operator roles.

1. Frame outcome, baseline/target, scope, decision rights and stop criteria.
2. Discover the workflow, exceptions, data, identities, actions, systems, NFRs,
   operations and economics. Maintain a live RAID log.
3. Assess agent suitability and autonomy; compare a deterministic/non-agent option.
4. Produce architecture options and ADRs with current Google evidence and reversal triggers.
5. Pair-build one vertical slice with auth, authoritative source, governed tool,
   durable operation record, telemetry, evaluation, immutable build and failure path.
6. Inject stale source, forbidden action, policy outage and unknown target write;
   capture hardening gaps and correct behavior.
7. Conduct the six reviews with one reviewer who did not author the solution.
8. Simulate canary, quality regression, action containment, reconciliation,
   rollback/roll-forward, manual fallback and go/no-go.
9. Reverse-shadow: the receiving team deploys, diagnoses, revokes, restores and
   communicates while the FDE observes without hidden intervention.
10. Present outcome evidence, residual risk, roadmap and expand/redesign/retire decision.

Passing requires customer-owned artifacts and demonstrated competency, not all
green scores. Preserve honest blockers and expiring exceptions.
