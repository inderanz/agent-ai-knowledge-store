# Volume 10 evolution and migration lab

## Local preflight

~~~bash
PYTHONPATH=examples/python/fde-production-kit/src \
  python3 -m unittest examples/python/fde-production-kit/tests/test_evolution.py -v
python3 scripts/check_sources.py
python3 delivery/volumes-4-10/validate_qualification.py \
  labs/volume-10-evolution/qualification.example.json --production
~~~

The example must fail production validation. Source freshness is not migration evidence.

## Simulation

1. Create synthetic change records for an ADK event-schema change and a model
   request-breaking change with a retirement deadline.
2. Map official source IDs to code, lockfiles, workflow/session/event/tool/state,
   policies, evaluation, IaC, telemetry, runbooks and a fictional customer release.
3. Run current and candidate in an isolated matrix; compare normalized graph,
   events, tools, sessions/resume, auth, traces and deterministic evaluation.
4. Build old/new `VersionEnvelope` records; prove topology/tool changes without
   required event/approval versions are rejected.
5. Seed synthetic old sessions and events. Route/drain compatible work, quarantine
   incompatible work, and validate backup/restore and exact migration counts.
6. Compare model task/grounding/tool/safety/adversarial/latency/token/cost results.
   Insert a critical-segment regression and prove rollout stops.
7. Canary immutable candidate traffic, exercise action kill switch, roll forward
   or back only where schema-compatible, and reconcile an unknown target write.
8. Update docs, dashboards, alerts, support and competency material; conduct the
   required reviews.
9. Stop new old-version use, drain/route in-flight work, revoke old access and
   prove zero authorized traffic while retaining required evidence.
10. Complete qualification only with dated environment-specific attachments and owners.

Never migrate real customer state or delete old resources/evidence in this lab.
Production retirement uses exact customer-approved plans, retention and legal hold.
