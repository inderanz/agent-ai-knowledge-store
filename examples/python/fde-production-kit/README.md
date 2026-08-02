# FDE production qualification kit

This dependency-free Python 3.12 package is the executable companion shared by
Volumes 4–15. It does not call Google Cloud. It converts architectural prose into
fail-closed, reviewable contracts for runtime placement, capacity, business-action
authorization, threat coverage, SLO/error budgets, retry/reconciliation, recovery
evidence, volatile reference facts, industry overlays, FDE stage gates, upstream
impact analysis, in-flight version compatibility, Registry catalog/binding safety,
Gateway route policy, per-agent identity maturity, Cloud Armor rules, and Gemini
Enterprise app/data-store/IAM admission.

Run every test:

~~~bash
PYTHONPATH=examples/python/fde-production-kit/src \
  python3 -m unittest discover -s examples/python/fde-production-kit/tests -v
~~~

These validators are preflight controls, not proof of production readiness. They
cannot determine current regional availability, contractual eligibility, IAM,
network paths, data classification, regulatory obligations, real capacity,
restore success, model quality, or customer ownership. Those decisions and tests
are collected by each volume's qualification lab.
