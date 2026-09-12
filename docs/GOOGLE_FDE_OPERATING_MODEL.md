# Google Forward Deployed Engineer operating model

> [!IMPORTANT]
> **Status: public-evidence-derived field model, Draft.** This document translates
> current public Google Careers and Google Cloud material into an executable
> customer-delivery system. It is not Google's private FDE handbook, an employment
> policy, a statement of service entitlement, or authority to accept customer risk.

## Google's public FDE mandate

Google's current public material makes the Google FDE role more specific than a
general solution-architecture or advisory role:

- A current Google Cloud GenAI FDE role describes an embedded builder who moves
  beyond architecture to code, debug and jointly ship agentic systems in customer
  environments. The FDE removes integration, data-readiness and state-management
  blockers, takes rapid prototypes toward production, builds evaluation and
  observability, converts field friction into reusable modules or product requests,
  and co-builds customer capability. [Google Cloud GenAI FDE role](https://www.google.com/about/careers/applications/jobs/results/143358812177212102-forward-deployed-engineer-genai-google-cloud)
- Google Cloud's senior GenAI FDE role adds ownership of ambiguous customer
  outcomes, production launches, measurable ROI, security perimeters, strategic
  account embedding and adoption. [Google Cloud FDE IV role](https://www.google.com/about/careers/applications/jobs/results/143122286080074438-forward-deployed-engineer-iv/)
- The Gemini Enterprise Customer Experience role frames the FDE as the agent
  engineer for critical initiatives, establishing early Customer User Journeys,
  debugging live agent behavior, connecting enterprise knowledge, using Terraform,
  and troubleshooting high-traffic systems. [Google Cloud GECX FDE role](https://www.google.com/about/careers/applications/jobs/results/103848231200268998-forward-deployed-engineer/)
- Google also publishes implementation guidance authored jointly by an FDE and
  product engineer, with a runnable ADK/A2A/Gemini Enterprise reference path. This
  is direct public evidence that field learning is expected to become reusable
  implementation material. [Gemini Enterprise and A2UI guide](https://cloud.google.com/blog/topics/developers-practitioners/guide-to-gemini-enterprise-and-a2ui-integration)

The presence of public roles across GenAI, Applied AI/Gemini Enterprise customer
experience, partner delivery and [Google DeepMind](https://www.google.com/about/careers/applications/jobs/results/76720917111022278-forward-deployed-engineer/)
is evidence of a deliberate field-engineering function. It does not by itself
establish investment amounts, customer entitlements or a single universal internal
methodology. Job postings are volatile, dated evidence and may be removed after a
role closes.

## Google-first FDE responsibility contract

| Google public responsibility | Required FDE behavior | Evidence the engagement must retain | Repository mechanism |
|---|---|---|---|
| embed and jointly ship | work in the customer's engineering system with named customer owners | pairing log, customer-owned commits, decisions and dependencies | Levels 0–4 of the [adoption playbook](FDE_CUSTOMER_ADOPTION_PLAYBOOK.md) |
| move prototypes to production | build a thin vertical slice and progressively qualify it | reproducible deployment, tests, production gaps and go/no-go record | Volumes 2–7, delivery gates and labs |
| connect live infrastructure | own the API, data, identity, network, legacy and action boundaries | data flow, identity map, tool contracts, integration tests and fallback | platform, ADK, security and reference-architecture volumes |
| remove enterprise blockers | turn ambiguity, data readiness, state and operational gaps into an owned backlog | RAID log, ADRs, blocker owner, decision date and escalation | engagement record plus weekly governance cadence |
| build evals and observability | measure result quality, trajectory, safety, latency, cost and user outcomes | versioned eval set, traces, thresholds, dashboards and failure taxonomy | ADK evaluation material and production qualification |
| operate critical launches | stay accountable through rollout, failures, recovery and stabilization | canary evidence, incident timeline, rollback, reconciliation and post-launch review | reliability and operations volumes |
| deliver measurable value and adoption | connect technical behavior to a baseline workflow and real user cohort | baseline, exposure, activation, task outcome, correction and unit cost | adoption levels and engagement validator |
| create reusable field patterns | sanitize repeatable code, modules, evals and lessons without customer data | pattern record, applicability boundary, tests and upstream owner | skills, examples, Terraform modules and handbook chapters |
| create a product feedback loop | translate recurring friction into reproducible evidence for product teams | minimal reproduction, affected versions, business impact and requested behavior | field-to-product feedback packet below |
| transfer customer capability | co-build, mentor and verify independent operation | teach-back, game day and customer competency sign-off | Level 4 exit and handover contract |

## Engagement execution loop

### 1. Discover the real customer workflow

The FDE observes operators, exceptions and upstream/downstream systems before
selecting an architecture. Record the business baseline, CUJ, owners, data
authority, existing controls, manual fallback and stop conditions. Technical
discovery is incomplete without a measurable workflow and an accountable acceptor.

### 2. Design with production boundaries visible

Create the target CUJ, trust boundaries, identity and action model, state lifecycle,
integration contracts, evaluation plan and non-agent alternative. Surface product
maturity, regional availability, quota, support and unsupported requirements early.
The FDE proposes options; authorized customer owners decide risk and production use.

### 3. Co-build a thin vertical slice

Implement one valuable path using a production-shaped authentication, data and tool
boundary. Use approved sandbox data, typed contracts, deterministic authorization,
tracing, timeouts, budgets, idempotency and manual fallback. Put code, Terraform,
tests and evaluation cases in customer-owned systems and pair with their engineers.

### 4. Prove behavior with evaluation and users

Evaluate final outcomes and trajectories: tool choice, parameters, grounding,
authorization, injection, partial failure, latency and cost. Pilot with a
representative user cohort. Convert corrections, overrides, abandonment and support
events into an error taxonomy and regression cases.

### 5. Productionize the complete service

Close security, data, implementation, reliability, cost, operations, adoption and
handover gates. Establish SLOs, alerts, support boundaries, canary, rollback,
recovery, reconciliation and change control. Production authorization stays with
the named customer owners.

### 6. Stabilize, transfer and scale

Stay through controlled rollout and critical-window failures. The customer must
demonstrate deploy, debug, evaluate, roll back, recover, revoke and retire
capabilities. Only then turn validated patterns into reusable platform modules,
skills, service-catalog entries and additional CUJs.

### 7. Return field evidence to Google product teams

Create a sanitized feedback packet with:

- customer segment and workflow shape, without confidential identifiers;
- product, region, version and maturity;
- minimal reproduction and expected versus observed behavior;
- trace/evaluation evidence with sensitive content removed;
- frequency, affected users, operational risk and business impact;
- workaround, its cost and why it does not scale;
- requested product behavior and acceptance test; and
- reusable field pattern or documentation correction, when applicable.

Do not send raw customer prompts, data, credentials, traces or architecture outside
approved customer and Google processes.

## Practical FDE cadence

| Cadence | Activity | Required output |
|---|---|---|
| daily | pair-build, inspect traces, resolve or escalate blockers | working code/eval delta and updated blocker owner |
| twice weekly | domain expert failure review | ranked failure clusters and new regression cases |
| weekly | architecture, security, SRE and data review | decisions, constraints, evidence gaps and gate state |
| weekly | sponsor/product adoption review | workflow value, user behavior and continue/constrain/stop decision |
| per release | qualification and controlled rollout | versioned evidence, go/no-go, canary and rollback readiness |
| per incident | technical escalation and reconciliation | contained impact, known state, recovery and prevention evidence |
| fortnightly | reusable pattern and product-friction review | sanitized module, documentation issue or feedback packet |

## FDE definition of done

The FDE's work is not complete because a model responds, a demo succeeds or a
service deploys. Completion requires:

1. a measured customer workflow outcome;
2. safe use by the intended user cohort;
3. qualified quality, safety, latency, reliability and cost;
4. tested operation, recovery, rollback and manual fallback;
5. customer ownership and demonstrated competency;
6. recorded limitations, residual risk and decision authority; and
7. reusable sanitized learning returned to the platform or product loop.

## Cross-industry evidence is secondary

OpenAI and Anthropic public material remains useful for comparison, especially on
embedded deployment and evaluation practice. For this Google-oriented repository,
however, Google's FDE roles and Google product documentation are primary. Other
vendors cannot substantiate Gemini Enterprise, ADK or Google Cloud capabilities.
