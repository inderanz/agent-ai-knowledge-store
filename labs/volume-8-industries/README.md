# Volume 8 industry-overlay qualification lab

Use only synthetic records and non-production infrastructure.

## Local preflight

~~~bash
PYTHONPATH=examples/python/fde-production-kit/src \
  python3 -m unittest examples/python/fde-production-kit/tests/test_industry.py -v
python3 delivery/volumes-4-10/validate_qualification.py \
  labs/volume-8-industries/qualification.example.json --production
~~~

The qualification example must fail; repository text cannot supply customer
legal, risk, domain, records, safety or production evidence.

## Customer workshop and failure lab

1. Customer authorities record jurisdiction, entity role, material actions,
   prohibited autonomy, data classes, services/contracts, locations and retention.
2. Choose one read-only/draft-only industry thin slice and its authoritative source.
3. Draw subjects, principals, fields, processors, locations, telemetry, evidence
   and business-system flow. Verify no real data is used in the lab.
4. Implement source revision/applicability/freshness and missing/conflict behavior.
5. Attempt the industry's prohibited action; prove deterministic rejection and
   visible routing to a qualified/accountable human.
6. Test wrong subject/tenant, revoked authority, indirect injection, exfiltration,
   sensitive metric/resource metadata and inaccessible/ambiguous output.
7. If a bounded synthetic write is approved, mutate it after approval and create
   a timeout after target commit; prove rejection and reconciliation without duplicate.
8. Exercise model/source/identity/connectivity outage and the approved manual or
   offline fallback. Measure business outcome and reviewer capacity.
9. Restore state/evidence, run the industry incident scenario and document every
   decision that only the customer can make.
10. Obtain domain, legal/risk, privacy/security, SRE and accountable-owner sign-off.

Do not expand the exercise to diagnosis, financial/adverse/rights decisions,
safety/OT/flight control or real regulated data. Cleanup follows customer records,
retention and legal-hold policy.
