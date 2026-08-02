# Volume 7 engineering-reference qualification lab

## Local validation

~~~bash
PYTHONPATH=examples/python/fde-production-kit/src \
  python3 -m unittest examples/python/fde-production-kit/tests/test_reference.py -v
python3 scripts/check_sources.py
python3 delivery/volumes-4-10/validate_qualification.py \
  labs/volume-7-reference/qualification.example.json --production
~~~

The example must fail production validation because it has no customer evidence.

## Field drill

1. Take the statement “Agent Identity is GA globally with default quota.”
2. Decompose exact product, Agent Identity API/authentication/authority mode,
   hosting runtime, endpoint/location, storage/processing/telemetry, maturity,
   quota scope, terms and support.
3. Locate primary Google feature, locations, residency, quota and release pages.
4. Record official observations with date; use `unknown` for anything not stated.
5. Compare target-project enablement and quota only in an authorized sandbox.
6. Create a customer-selection record separate from the public source catalog.
7. Introduce a stale date, duplicate source ID and non-primary domain; prove local
   validation rejects each.
8. Walk deployment, invocation/tool and missing-trace troubleshooting trees using
   a synthetic failure, then attach evidence and reviewer acceptance.

Never paste customer identifiers, support messages, contracts or topology into
the repository. The source checker performs network reads only when explicitly
configured; semantic review remains human-owned.
