# Customer adoption contract

## Google FDE field contract

Public Google FDE material is primary for this repository. A practical delivery
unit must demonstrate all applicable responsibilities:

- embed and co-build in the customer's engineering system;
- take a production-shaped path from prototype through launch and stabilization;
- integrate live APIs, data, identity, network and security boundaries;
- build evaluation and observability for quality, safety, latency and cost;
- measure workflow value, user adoption and operational burden;
- transfer demonstrated customer capability;
- sanitize repeatable patterns into reusable modules or guidance; and
- produce reproducible product-friction evidence without customer-confidential data.

Google role descriptions are dated organizational evidence, not product contracts
or customer risk approval. Product claims still require current Google product
documentation or official implementation sources.

| Level | Outcome | Required evidence before advancing |
|---|---|---|
| 0 — Frame | Measurable workflow, owner, population, constraints, stop condition | Signed charter and baseline |
| 1 — Learn | Team understands agent limits, data, tools, risks, and alternatives | Use-case and autonomy assessment |
| 2 — Prove | One production-shaped thin slice works in a sandbox | Golden evals, negative tests, architecture decision |
| 3 — Pilot | Real users complete bounded work with support and fallback | Adoption, quality, safety, latency and cost evidence |
| 4 — Produce | Controlled production service is operable and recoverable | Six review gates, SLO, runbooks, rollback, go/no-go |
| 5 — Scale | Multiple teams reuse governed platform capabilities | Registry, templates, paved road, FinOps and tenancy evidence |
| 6 — Evolve | Customer safely changes models, agents and controls | Drift loop, regression evals, migration and retirement evidence |

At every level record exit criteria, accountable customer owner, evidence location, residual risks, and the exact decision to advance, remain, constrain, or stop.
