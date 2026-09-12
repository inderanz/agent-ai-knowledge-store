# Agentic AI FDE Navigator

This is the entry point for the WhatsApp knowledge collection. Do **not** begin by reading all 307 links or comparing all 44 repositories. Start with the customer outcome, select one default stack, build a narrow vertical slice, and use the larger catalogue only when the default fails a requirement.

## Use this navigator in 60 seconds

1. Pick the outcome closest to your problem in the table below.
2. Open the linked local README for the default component.
3. Follow the matching implementation blueprint.
4. Pass its exit gate before adding another framework, memory layer, protocol, or agent.
5. Use the [repository index](knowledge-repos/README.md) for alternatives and the [full research catalogue](whatsapp-links-Inder-Australia-2026-08-04-research.md) for source-level evidence.

To build and navigate the same kind of interactive repository map in Codex,
Copilot CLI, Gemini CLI, Claude Code, or Antigravity, use the
[repository knowledge graph and AI CLI playbook](docs/REPOSITORY_KNOWLEDGE_GRAPH_CLI_PLAYBOOK.md).

## What are you trying to build?

| Desired outcome | Start with | Add only when needed | First proof to build |
|---|---|---|---|
| An enterprise agent that reads data and takes governed actions | [Google ADK](knowledge-repos/google--adk-python/README.md) | [ContextForge](knowledge-repos/IBM--mcp-context-forge/README.md) for multiple governed tools; Vertex AI Agent Engine for managed deployment | One user journey, one data source, at most three tools, and human approval before writes |
| A vendor-neutral Python agent product | [Pydantic AI Harness](knowledge-repos/pydantic--pydantic-ai-harness/README.md) | ContextForge for tool governance; [MemMachine](knowledge-repos/MemMachine--MemMachine/README.md) only if cross-session memory is required | The same task running against two model providers with identical tests |
| A PDF, Office-document, or multimodal knowledge product | [MinerU](knowledge-repos/opendatalab--mineru/README.md) for extraction, then [RAG-Anything](knowledge-repos/HKUDS--RAG-Anything/README.md) if multimodal retrieval is needed | ADK/Pydantic for agent behavior; a gateway only when tools or tenants multiply | Five representative customer documents, cited answers, and a documented failure set |
| A web-research or web-monitoring agent | [Scrapling](knowledge-repos/D4Vinci--Scrapling/README.md) | [ScrapeGraphAI](knowledge-repos/ScrapeGraphAI--Scrapegraph-ai/README.md) if AI-directed extraction is justified | One permitted website, a provenance-preserving extraction, and a change-detection report |
| A codebase intelligence or modernization assistant | [Graphify](knowledge-repos/Graphify-Labs--graphify/README.md) | [gortex](knowledge-repos/zzet--gortex/README.md) for local multi-language code intelligence; [RTK](knowledge-repos/rtk-ai--rtk/README.md) for leaner command output | Ask ten architecture/change-impact questions and verify every answer against source files |
| A shared internal platform for multiple agent teams | [Omnigent](knowledge-repos/omnigent-ai--omnigent/README.md) for harness portability or ADK for a Google-centred platform | ContextForge, MemMachine, and [Uber ADR](knowledge-repos/uber--ADR/README.md) as separate control-plane capabilities | Two bounded agents sharing a governed tool catalogue, traces, and revocable credentials |
| Reliable long-horizon coding-agent work | [Beads](knowledge-repos/gastownhall--beads/README.md) | RTK for output efficiency; [cctop](knowledge-repos/stefanprodan--cctop/README.md) for session monitoring; [Hivemind](knowledge-repos/activeloopai--hivemind/README.md) only for shared trace/skill recall | Complete one multi-session feature with dependency-aware state and a clean handoff |
| An FDE portfolio that demonstrates customer delivery | [Awesome FDE Roadmap](knowledge-repos/pierpaolo28--Awesome-FDE-Roadmap/README.md) plus one of the vertical slices above | Career tools only after you have architecture, eval, security, and outcome evidence | A public-safe case study containing baseline, design, evals, risk controls, cost, SLOs, and adoption result |

## The default shortlist

These are defaults for **fit**, not universal winners. The maturity number is the dated public-repository evidence score from the [research scorecard](whatsapp-links-Inder-Australia-2026-08-04-research.md#productrepository-maturity-scorecard).

| Capability | Default | Score | Use it when | Use an alternative when |
|---|---|---:|---|---|
| Google-centred agent framework | [Google ADK](knowledge-repos/google--adk-python/README.md) | 96 | The customer uses Google Cloud/Gemini or you need a code-first agent/workflow toolkit | Use Pydantic when provider portability and typed Python composition matter more |
| Vendor-neutral Python harness | [Pydantic AI Harness](knowledge-repos/pydantic--pydantic-ai-harness/README.md) | 82 | You want reusable capabilities, multiple model providers, MCP, evaluation/observability integration, or sandboxed code modes | Use ADK for a Google-first deployment; Omnigent when switching whole harnesses is the core requirement |
| Harness portability/meta-orchestration | [Omnigent](knowledge-repos/omnigent-ai--omnigent/README.md) | 95 | You must operate agents implemented across Codex, Claude Code, Cursor, Pi, or custom harnesses | Avoid the abstraction if one framework already satisfies the product |
| MCP/tool control plane | [IBM ContextForge](knowledge-repos/IBM--mcp-context-forge/README.md) | 93 | Multiple tools/servers need central discovery, authentication, policy, observability, and lifecycle management | Directly connect one MCP server during an early proof; use Google-managed MCP when the required Google service and status fit |
| Complex-document extraction | [MinerU](knowledge-repos/opendatalab--mineru/README.md) | 94 | PDFs/Office files, tables, formulas, images, or layout quality are the ingestion bottleneck | Use a simpler parser for clean text/HTML; review MinerU's additional licence terms before commercial use |
| Multimodal retrieval | [RAG-Anything](knowledge-repos/HKUDS--RAG-Anything/README.md) | 97 | Questions depend on text, images, tables, or equations together | Do not add RAG when a deterministic lookup or SQL query can answer the task |
| Web acquisition | [Scrapling](knowledge-repos/D4Vinci--Scrapling/README.md) | 94 | Permitted websites require robust crawling/extraction | Use ScrapeGraphAI only after measuring that AI-directed extraction beats deterministic selectors |
| Codebase knowledge graph | [Graphify](knowledge-repos/Graphify-Labs--graphify/README.md) | 94 | You need explainable relationships across code, docs, schemas, configs, and PDFs | Use gortex for a lean local code-intelligence service across many languages/repos |
| Agent/user memory | [MemMachine](knowledge-repos/MemMachine--MemMachine/README.md) | 96 | Product behavior genuinely needs durable user/agent memories across sessions | Use Beads for work state, Hivemind for trace-to-skill sharing, or no memory for a single-session task |
| Coding-agent work state | [Beads](knowledge-repos/gastownhall--beads/README.md) | 100 | Agents must resume dependency-aware work across sessions | A normal issue tracker is enough when humans own task state and agents are short-lived |
| Security/agent detection | [Uber ADR](knowledge-repos/uber--ADR/README.md) | 82 | You need an agent-specific security and observability evaluation surface | It complements rather than replaces IAM, sandboxing, secrets management, and application security |
| Behaviour evaluation | [OpenAI Evals](knowledge-repos/openai--evals/README.md) | 74 | Its evaluation model and registry fit your test workflow | Use the framework-native evaluator when it gives simpler task, trace, and CI integration |
| Token-efficient terminal context | [RTK](knowledge-repos/rtk-ai--rtk/README.md) | 96 | Command output is consuming agent context without improving task success | Skip it until you have a baseline proving context/output is the bottleneck |

## Three decisions that prevent tool sprawl

### 1. Workflow or autonomous agent?

Use a deterministic workflow when the steps and decision rules are known. Use an agent only where the path cannot be reliably hard-coded and the extra latency, cost, and failure surface are justified. A production system can combine both: deterministic outer workflow, bounded agentic decisions inside it.

### 2. Direct integration or MCP gateway?

- One agent plus one stable tool: integrate directly first.
- Several tools, teams, tenants, or policies: introduce ContextForge or a managed MCP control plane.
- Customer-impacting writes: require scoped identity, idempotency, audit logging, approval policy, and rollback regardless of protocol.

### 3. Stateless, task state, or memory?

- **Stateless:** default for simple support, lookup, and transformation tasks.
- **Task state:** use Beads or an application database for resumable work and dependencies.
- **Memory:** use MemMachine when past user/agent facts must be retrieved later.
- **Organisational learning:** consider Hivemind when traces should become shared skills, subject to its data/privacy controls.

Do not use one of these products to solve all four state problems.

## Implementation blueprint A: governed customer action agent

Use this for support operations, finance operations, infrastructure operations, or other workflows where an agent reads customer data and may take an action.

### Recommended stack

- Agent/workflow: Google ADK for Google-centred customers; Pydantic AI Harness otherwise.
- Tool access: direct integration for the first tool; ContextForge when governance must span multiple tools.
- State: application database for workflow state; no long-term memory initially.
- Evaluation: repository-native tests plus a task dataset and trace review.
- Runtime: local/container proof first; managed runtime after quality and control gates pass.

### Build order

1. Write one sentence: “For **user**, when **trigger** occurs, the system will **action**, improving **metric**, while never **prohibited outcome**.”
2. Record the current human baseline: completion rate, time, error/rework, and escalation rate.
3. Implement one read-only tool and its typed input/output contract.
4. Add the agent/workflow with a maximum-step limit and explicit stop/escalate conditions.
5. Create representative success, ambiguity, missing-data, permission, tool-error, and malicious-input cases.
6. Add one write action behind preview, confirmation, idempotency, and audit logging.
7. Pilot with a small user group and compare against the baseline.

### Exit gate

Do not add multi-agent orchestration, memory, or more tools until the single-agent slice meets an agreed task-success target, never performs an unauthorised write in the test set, reports traceable tool activity, and has a tested fallback/rollback path.

## Implementation blueprint B: cited document-intelligence product

This is the best first portfolio product from this collection because it exercises customer discovery, ingestion, retrieval, evaluation, security, and adoption without requiring broad autonomous actions.

### Recommended stack

- MinerU for difficult PDF/Office extraction.
- RAG-Anything only if images, tables, or equations materially affect answers.
- Google ADK or Pydantic AI Harness for question decomposition and tools.
- Direct retrieval first; ContextForge only when multiple governed tools or teams appear.
- ADR/evaluation tooling for quality and security checks.

### Two-week MVP

1. Select five customer-representative documents that you are permitted to process.
2. Create a golden set of questions with answer locations, including unanswerable and conflicting-document cases.
3. Parse documents and retain document/page/section provenance.
4. Return an answer, citations, confidence/limitations, and “not found” where appropriate.
5. Add one business rule, such as flagging a missing contractual/compliance clause, but keep the final decision human-approved.
6. Report extraction failures, retrieval failures, answer failures, latency, and cost separately.
7. Demo the workflow using a before/after customer task, not a generic chat interface.

### Exit gate

Proceed only if users can verify every material answer, the system abstains on unsupported questions, access control is enforced before retrieval, document deletion/update propagates correctly, and measured workflow improvement justifies operating cost.

## Implementation blueprint C: codebase modernisation assistant

### Recommended stack

- Graphify for an explainable graph spanning code and adjacent engineering artifacts.
- gortex when local, cross-repository, multi-language code intelligence is the dominant requirement.
- RTK for command-output reduction only after a token/context baseline.
- Beads for persistent migration work and dependencies.
- ADK/Pydantic for a bounded change-planning agent; keep code changes human-reviewed.

### First proof

1. Select one service and ten questions engineers currently answer manually.
2. Include dependency, data-flow, ownership, blast-radius, configuration, and test-coverage questions.
3. Require every answer to point to specific source artifacts.
4. Add one safe output: a proposed migration plan or architecture decision record, not an automatic deployment.
5. Measure answer correctness, engineer verification time, missed dependencies, and context/token cost.

### Exit gate

Do not automate code changes until the context layer is fresh, incremental updates work, cross-repo references are tested, and reviewers trust the evidence behind change-impact answers.

## Build a new product, not a bundle of repositories

A product needs a buyer, painful workflow, distribution path, proprietary learning loop, and measurable outcome. Open-source components reduce build time; they are not the differentiation.

| Product wedge | Buyer and pain | Reuse from this collection | What you must build | Smallest validation |
|---|---|---|---|---|
| Contract and policy change-assurance agent | Compliance/legal/operations teams manually compare changing documents and prove impact | MinerU, RAG-Anything, ADK/Pydantic, ContextForge, ADR | Domain rules, change model, reviewer workflow, access controls, audit evidence, customer integrations | One document family, one change event, ten known impacts, and a reviewer time comparison |
| Governed agent-tool gateway accelerator | Platform/security teams cannot inventory and control fast-growing agent tools | ContextForge, Google-managed MCP references, ADR | Opinionated policy packs, onboarding workflow, risk scoring, enterprise identity integrations, operational dashboard | Connect three tools, demonstrate least privilege/revocation, and produce an audit trail |
| Codebase modernisation mapper | Engineering leaders cannot see cross-service dependencies before migration | Graphify, gortex, RTK, Beads | Organisation-specific ownership/data/dependency model, migration workflow, verified recommendations | One migration decision where the system finds dependencies faster without missing known ones |
| FDE pilot factory | AI delivery teams repeatedly rebuild discovery, eval, security, and handover artifacts | ADK/Pydantic, Beads, OpenAI Evals, ADR, FDE roadmap | Reusable discovery templates, domain task packs, success dashboards, customer handover workflow | Deliver the same bounded pilot process in two domains with less setup time and preserved quality |
| Memory governance service | Enterprises cannot explain, correct, retain, or delete what agents remember | MemMachine, exxperts, Hivemind | Consent, policy, correction/deletion, retention, tenant isolation, memory quality evaluation | Demonstrate a memory lifecycle with retrieval precision, user correction, deletion, and audit evidence |
| Agent operations/SRE copilot | Operations teams lose time correlating incidents, runbooks, telemetry, and safe remediations | ADK, managed MCP, cctop/agent-flow patterns, ADR, SRE resources | Tool permissions, incident context model, approval/rollback, SLO-aware evaluation, customer integrations | One read-only incident workflow that reduces diagnosis time without unsafe remediation |

## Product validation gates

Use these gates before writing a larger product:

| Gate | Evidence required | Stop or change direction when |
|---|---|---|
| Problem | Repeated workflow, named user, baseline cost/risk, current workaround | The problem is occasional, has no owner, or is cheaper to solve deterministically |
| Data/access | Available representative data, clear owner, lawful/approved processing | Useful data cannot be accessed, isolated, updated, or deleted correctly |
| Technical | Narrow task works on representative and adversarial cases | The model demo works only on curated happy paths |
| Economic | Estimated model, infrastructure, support, and review cost versus outcome | Human review and failure handling erase the workflow benefit |
| Adoption | Users integrate it into the real workflow and can override/escalate | Users keep exporting results into another manual process or cannot trust evidence |
| Defensibility | Domain workflow, data feedback, integration, or distribution advantage | The product is only a thin UI over interchangeable models/open-source components |

## A practical 30-day FDE build plan

### Week 1 — choose and baseline

- Interview three target users about one workflow.
- Capture the current process, systems, permissions, exceptions, and measurable baseline.
- Select one blueprint and one primary framework.
- Create the initial task/evaluation set before building the agent.

### Week 2 — vertical slice

- Implement one end-to-end happy path and its read-only tools.
- Add provenance, traces, structured errors, timeouts, and deterministic fallbacks.
- Demonstrate with representative customer-safe data.

### Week 3 — failure and control engineering

- Add ambiguous, conflicting, stale, missing, malicious, and tool-failure cases.
- Add identity/authorisation, secrets handling, tenant isolation, approval gates, audit logs, and rollback appropriate to the risk.
- Measure task success, latency, cost, and human-review effort.

### Week 4 — adoption and portfolio proof

- Run a small user pilot against the baseline.
- Write the architecture decision, threat model, eval report, SLO/runbook, cost model, and limitations.
- Publish only sanitised/non-customer evidence.
- Decide: deepen this product, change the wedge, or stop.

## What not to do

- Do not combine ADK, Pydantic, Omnigent, and another orchestration framework in the first product.
- Do not add vector retrieval, knowledge graphs, or memory without a measured information problem.
- Do not use repository popularity as a substitute for licence, security, operational, and workload fit.
- Do not let an agent perform customer-impacting writes without scoped identity, preview/approval policy, idempotency, auditability, and rollback.
- Do not treat a successful demo as a production result; test failures, abuse, updates/deletion, cost, SLOs, and user adoption.
- Do not build a generic “AI assistant.” Name the buyer, triggering workflow, measurable outcome, and prohibited failures.

## Where everything lives

| Need | Open this |
|---|---|
| Decide what to build | This navigator |
| Browse all 44 cloned repositories by category | [Repository index](knowledge-repos/README.md) |
| Compare maturity and overlapping products | [Research report](whatsapp-links-Inder-Australia-2026-08-04-research.md#productrepository-maturity-scorecard) |
| Inspect every original URL | [Link-by-link catalogue](whatsapp-links-Inder-Australia-2026-08-04-research.md#link-by-link-research-catalogue) |
| See the unprocessed WhatsApp context | [Source archive](whatsapp-links-Inder-Australia-2026-08-04.md) |
| Regenerate the research report | [`scripts/build_whatsapp_link_research.py`](scripts/build_whatsapp_link_research.py) |

## Commercialisation and safety note

Before building a commercial product, review each repository's current licence and all dependency/model/data terms. The local maturity score is not legal or security approval. In particular, MinerU's local licence file states Apache 2.0 plus additional terms; read those terms directly. Recheck current product availability, privacy, data residency, support, and Preview/GA status before a customer deployment.
