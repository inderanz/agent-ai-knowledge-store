# Repository knowledge graph and AI CLI playbook

> **Audience:** developers, FDEs, architects, technical product builders, and
> anyone opening an unfamiliar repository.
>
> **Progression:** beginner → productive user → advanced operator.
>
> **Last command review:** 4 August 2026. AI CLI commands change quickly. Check
> the linked official documentation before putting them into CI or enterprise
> policy.

This playbook explains how to turn almost any repository into an interactive
knowledge map, how to navigate it without reading every file, and how to use the
same workflow from Codex, GitHub Copilot CLI, Gemini CLI, Claude Code, or Google
Antigravity CLI.

The key idea is simple:

```text
repository
   │
   ├── structural extraction: code, imports, calls, inheritance, schemas
   ├── semantic extraction: documents, decisions, concepts, rationale
   ▼
knowledge graph
   ├── graph.html       visual exploration
   ├── GRAPH_REPORT.md  architecture overview and investigation prompts
   └── graph.json       reusable machine-readable graph
```

The graph is an orientation and retrieval layer. It does **not** replace source
code, tests, documentation, or engineering judgement.

## Choose your starting point

| Experience | Start here | Outcome |
|---|---|---|
| New to terminals and AI coding tools | [Level 0 — first map](#level-0--build-your-first-repository-map) | Open an interactive graph in a browser |
| Comfortable with a CLI | [Level 1 — daily navigation](#level-1--navigate-without-reading-the-entire-repository) | Answer architecture and change-impact questions quickly |
| Maintaining a repository | [Level 2 — make it persistent](#level-2--make-the-graph-part-of-the-repository) | Keep the map fresh for the team |
| Operating multiple agents or repositories | [Level 3 — advanced operation](#level-3--advanced-operation) | MCP access, automation, cross-repository analysis, and governance |
| Evaluating an enterprise product | [Enterprise SDLC product](#the-enterprise-product-hiding-inside-the-graph) | Problems, differentiation, maturity, and the first product wedge |
| Something failed | [Troubleshooting](#troubleshooting) | Diagnose the common installation, backend, and graph-quality failures |

## What Graphify produces

After a successful build, the important outputs are:

```text
graphify-out/
├── graph.html          interactive browser view
├── GRAPH_REPORT.md     communities, god nodes, surprising links, questions
├── graph.json          complete graph for query/path/explain and MCP
├── manifest.json       portable state for incremental updates
└── cache/              optional extraction cache
```

Use each output for a different job:

- Start in `graph.html` when you do not yet know what exists.
- Read only the relevant sections of `GRAPH_REPORT.md` for a broad architecture
  review.
- Use `graphify query`, `graphify explain`, or `graphify path` for focused work.
- Open the referenced source file before making a material claim or change.
- Treat `graph.json` as generated data, not as a file to edit manually.

## The enterprise product hiding inside the graph

Graphify by itself is a repository knowledge-graph engine. The stronger
enterprise product is a **vendor-neutral SDLC evidence graph and change-assurance
gateway for human and AI engineering teams**.

Its promise should be:

> Before an engineer or agent changes a system, show which requirements,
> decisions, code, tests, infrastructure, owners, controls, and runbooks are
> affected. After the change, prove which required evidence still holds and
> identify what is missing.

This is a better position than “visualise your repository.” Visualisation is a
feature. The enterprise outcome is fewer missed dependencies, faster review,
less specification drift, safer agent-generated changes, and an auditable path
from intent to production evidence.

### The enterprise SDLC problems it can solve

| Enterprise problem | Why the present workflow fails | Product behaviour to build on Graphify | Pilot measure |
|---|---|---|---|
| Change impact is discovered during review or production | Dependencies are split across code, tickets, architecture documents, infrastructure, tests, and people | Compute a source-linked blast radius before implementation and again after the diff | Time to identify affected surfaces; escaped dependency count |
| Requirement-to-production traceability is incomplete | Ticket links normally stop at a PR or test; design decisions, configuration, runbooks, and runtime proof live elsewhere | Maintain a trace from business requirement to acceptance criterion, design, code, test, deployment, runtime evidence, and owner | Percentage of release requirements with a complete evidence chain |
| Specifications and implementation silently drift | Specs are reviewed at creation time but are rarely revalidated after code, API, or dependency changes | Detect changed nodes and invalidate affected specification or evidence edges until re-qualified | Drift detection precision/recall; age of unresolved drift |
| Cross-repository changes have an unknown blast radius | Service teams and repositories have separate search indexes, release cycles, and ownership models | Preserve repository origin while calculating paths across APIs, schemas, events, clients, and infrastructure | Cross-repository issues found before merge |
| Architecture decisions become historical prose | ADRs explain intent but are not continuously connected to the components and controls that implement them | Link decisions and constraints to their implementation and flag orphaned or contradicted decisions | Orphaned ADRs; decisions with verified implementation links |
| Modernisation and deprecation are risky | Static search finds names but misses semantic consumers, operational dependencies, and migration obligations | Build a retirement impact map and block removal while required consumers or evidence remain | Discovery time; rollback or regression rate |
| Audit evidence is assembled manually | Approvals, tests, controls, source baselines, and deployment proof are copied into spreadsheets after delivery | Generate a bounded, source-linked evidence packet from the exact commit and environment | Audit preparation hours; unverifiable claims |
| Onboarding and handover depend on tribal knowledge | Search returns files, while experienced engineers provide relationships and exceptions from memory | Provide role-specific paths, communities, owners, runbooks, and verified starter questions | Time to first safe change; expert interruption hours |
| AI-generated pull requests are difficult to trust | A plausible diff does not prove requirement coverage, blast-radius review, or operational safety | Require agent preflight, evidence-backed plan, bounded change, tests, post-change graph refresh, and missing-evidence report | Agent PR review time; failed-change rate; unsupported claims |

This repository already contains patterns that support the product direction:

- the [impact contract](../skills/assess-upstream-impact/references/impact-contract.md)
  defines handbook, implementation, delivery, qualification, operations,
  evidence, and automation surfaces;
- the [synchronisation matrix](../skills/synchronize-implementation/references/synchronization-matrix.md)
  maps changed concerns to the artefacts that normally need revalidation;
- the [qualification gates](../skills/qualify-handbook-change/references/qualification-gates.md)
  define research, architecture, implementation, security, operations,
  delivery, and independent-review pass conditions; and
- [ADR-0001](../adr/0001-evidence-and-publication-policy.md) demonstrates
  evidence-gated publication, dated baselines, and explicit re-review.

The knowledge graph turns these separate controls into a navigable model. The
enterprise product must then enforce completeness, freshness, authority, and
release policy around that model.

### What spec-driven development means at enterprise scale

Generating `requirements.md`, `design.md`, and `tasks.md` is useful, but it is
only the planning part of spec-driven development. In an enterprise product,
the specification becomes a continuously verified control plane:

```text
business outcome
   → requirement
   → acceptance criterion
   → architecture decision and constraint
   → component / API / schema / infrastructure
   → test and evaluation
   → build and deployment
   → runtime evidence and SLO
   → owner, approval, and control
```

Every arrow needs a source, relationship type, commit or version, confidence,
owner, and freshness state. A release is not “spec compliant” merely because an
agent says it is. Compliance is a graph policy evaluated over verified links.

Examples of enforceable rules are:

- every active requirement has at least one acceptance criterion and owner;
- every high-risk acceptance criterion has a negative test;
- every implementation node has a source location and commit;
- every security-sensitive change reaches an identity, policy, audit, and
  incident-response node in its impact path;
- every passed test is tied to the build and environment in which it ran;
- every production claim has current evidence rather than an example record;
- every changed API or schema re-qualifies known consumers; and
- an inferred or ambiguous relationship cannot satisfy a mandatory release
  gate without human verification.

Graphify can ingest the artifacts and expose nodes, paths, provenance, and
confidence. It does **not** currently guarantee this traceability model. Stable
enterprise identifiers, required edge types, lifecycle states, policy rules,
and integration-generated evidence are part of the product you would build on
top.

### Agentic AI problems this product can solve

The recurring problem in agentic software delivery is not simply a lack of
tokens. It is the absence of shared, durable, verifiable system context.

1. **Context fragmentation across agents.** Codex, Copilot, Gemini, Claude, and
   future agents can all use different sessions and indexes. A local graph plus
   CLI/MCP interface can give them one repository-owned evidence substrate.
2. **Retrieval without relationship proof.** Vector retrieval can find similar
   text but does not by itself prove that a test verifies a requirement or that
   a service consumes a schema. Typed graph paths make the claim inspectable.
3. **Stale context presented as current truth.** Store commit, source, extraction
   time, environment, and validity state on evidence so an agent can abstain or
   refresh instead of silently using old context.
4. **Plans that ignore blast radius.** Make an impact query a required preflight
   before an agent edits and a second graph comparison a required postflight.
5. **Multi-agent work that loses decisions.** Persist verified findings,
   rejected paths, approvals, and corrections outside any model's context
   window, while keeping conversation memory separate from engineering truth.
6. **Agent output without an assurance case.** Require every material claim in
   a plan or pull request to resolve to source nodes, test evidence, or an
   explicit unknown.
7. **Instruction and authority confusion.** Model agent instructions, owners,
   policies, and tool permissions separately so retrieved content cannot grant
   itself authority to change production.
8. **Agent observability separated from software intent.** Join execution traces
   and tool calls to the requirements, components, and controls they were meant
   to satisfy, not just to latency and token dashboards.

The high-value feature is therefore an **agent change-assurance gateway**:

```text
agent or engineer
      │
      ├── preflight: intent + impact + policy + missing evidence
      ▼
bounded implementation
      │
      ├── postflight: diff + tests + graph refresh + drift check
      ▼
PR evidence packet / release decision / explicit unknowns
```

The gateway should never decide that a high-risk change is safe solely from an
LLM judgement. Deterministic policies, real test results, environment identity,
and independent approval remain separate evidence.

### What large providers already solve—and the remaining opening

The defensible claim is not that large cloud and AI providers solve none of
this. They solve important adjacent parts:

| Existing capability | Verified example | What remains fragmented |
|---|---|---|
| Structured specs and implementation planning | [Kiro Specs](https://kiro.dev/docs/specs/) creates requirements, design, and task artifacts; [Analyze Requirements](https://kiro.dev/docs/specs/analyze-requirements/) checks inconsistencies, ambiguities, and gaps | Continuous vendor-neutral traceability from those artifacts into code, infrastructure, operations, and runtime evidence |
| Requirements and delivery traceability | [Azure DevOps](https://learn.microsoft.com/en-us/azure/devops/cross-service/end-to-end-traceability?view=azure-devops) links work items, commits, PRs, builds, releases, tests, and bugs | An open graph spanning non-Azure tools, semantic decisions, agent reasoning, and source-level confidence |
| Repository-specific agent context | [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide) supports repository/path instructions and `AGENTS.md`; custom agents can use tools and MCP | A shared evidence model reusable by competing agents, with explicit relationship provenance and lifecycle policies |
| Private codebase retrieval | [Gemini Code Assist Enterprise](https://docs.cloud.google.com/gemini/docs/codeassist/code-customization-overview) indexes private repositories and refreshes its code customisation index | Mixed-artifact SDLC relationships, release-gate completeness, and portability outside the provider's retrieval surface |
| Agent hooks and external tools | [Claude Code](https://code.claude.com/docs/en/hooks) supports lifecycle hooks and MCP tools; [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md) supports durable repository instructions and MCP-based external tools | One repository-owned state and evidence layer that survives the choice of coding agent |
| Agent runtime memory and telemetry | [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/) provides memory, gateway, runtime, and observability and supports multiple model providers | Direct connection between runtime traces and the SDLC intent, specification, source, test, control, and release decision |

As of the review date at the top of this document, the official capabilities
reviewed did not document one product combining all of the following:

1. local-first and vendor-neutral operation;
2. a unified graph across code, specifications, ADRs, tests, infrastructure,
   runbooks, owners, and evidence;
3. source-linked typed relationships with extracted, inferred, or ambiguous
   confidence;
4. the same query and assurance interface for multiple AI agents and CLIs;
5. incremental, Git-aware invalidation and re-qualification; and
6. pre-change impact plus post-change evidence enforcement.

That is a dated gap analysis, not proof that no competitor has an internal or
newly released equivalent. Recheck it before customer or investor claims.
Cloud providers can also build graphs. The durable advantage must come from the
enterprise SDLC ontology, verified correction data, cross-tool integrations,
policy and evaluation engine, customer-specific evidence history, and ability
to remain useful when the customer changes model or cloud.

### Product maturity scorecard

This scorecard rates the Graphify-based foundation observed in this repository,
not an audited commercial service. Score meanings are: 1 = absent, 2 = early,
3 = usable with engineering support, 4 = strong, 5 = enterprise proven.

| Capability | Today | Why | Needed for enterprise product |
|---|---:|---|---|
| Mixed code and document graph | 4/5 | Structural and semantic extraction produce a persistent graph | Supported-format contracts, scale tests, and data classification |
| Source provenance and confidence | 4/5 | Nodes retain sources; edges distinguish extracted, inferred, and ambiguous | Evidence signing, commit/environment identity, reviewer state |
| Query, path, explain, and visual navigation | 4/5 | CLI, JSON, HTML, and MCP-compatible access cover core exploration | Stable APIs, latency SLOs, saved enterprise views, accessibility |
| Incremental freshness | 3/5 | Manifest/update and watch workflows exist | Distributed ingestion, freshness SLOs, deletion and failure reconciliation |
| Cross-repository analysis | 3/5 | Graphs can be merged while preserving origin | Identity resolution, access-aware traversal, ownership and release boundaries |
| Spec-to-code-to-test traceability | 2/5 | The graph is a suitable substrate but links are not a guaranteed contract | Spec IDs, required edge schema, completeness policies, drift engine |
| Change-assurance and release enforcement | 2/5 | Impact, qualification, and evidence patterns exist in repository documents | PR/CI gates, signed evidence packets, exception and approval workflow |
| Agent interoperability | 3/5 | CLI, files, instructions, and MCP enable several assistants to use the graph | Versioned tool contract, identity, permissions, concurrent-write semantics |
| Enterprise integrations | 1/5 | No complete GitHub/GitLab/Jira/ADO/ServiceNow integration suite is established | Connectors, webhooks, reconciliation, admin configuration |
| RBAC, tenancy, and audit | 1/5 | Local files do not constitute enterprise access control | SSO, SCIM, tenant isolation, ACL-aware graph traversal, immutable audit |
| Accuracy evaluation and operational SLOs | 2/5 | Health checks and honest confidence rules exist | Golden datasets, precision/recall, freshness, availability, incident process |

**Overall interpretation:** approximately **2.6/5—strong technical
foundation, early enterprise product**. Do not sell the CLI as a completed SDLC
governance platform. Sell a bounded pilot and measure whether the graph improves
one costly decision.

### The best product wedge

Start with **spec-to-production drift and agent change assurance for high-risk
pull requests**. Avoid beginning with a generic enterprise knowledge portal;
that market is broad and the value is hard to measure.

An initial customer workflow can be:

1. Ingest one critical service, its specifications, ADRs, infrastructure,
   tests, ownership, runbooks, and the last 90 days of pull requests.
2. Establish stable IDs and required relationships for the customer's top ten
   requirements or controls.
3. On every selected PR, show changed nodes, probable blast radius, missing
   evidence, stale specifications, and required reviewers.
4. Let any approved coding agent query the same evidence through MCP, but keep
   policy evaluation deterministic.
5. Refresh after tests and deployment, then produce a source-linked evidence
   packet with explicit unknowns.
6. Compare discovery time, review time, missed dependencies, rollback rate, and
   evidence completeness with the previous baseline.

Three later product wedges reuse the same graph:

- a modernisation and safe-deprecation planner for legacy estates;
- a regulated release evidence and audit-assurance product; and
- a multi-agent engineering memory and context control plane.

The moat is not the visual graph. It is the accumulating, verified model of how
an enterprise's intent, software, controls, and production evidence actually
relate—and the policies that stop humans or agents from treating missing proof
as success.

## Level 0 — build your first repository map

### 1. Prepare the repository safely

Clone or open the repository and enter its root directory:

```bash
git clone https://github.com/OWNER/REPOSITORY.git
cd REPOSITORY
git status --short
```

Before giving any AI tool access:

1. Confirm this is the intended repository.
2. Check whether the working tree already contains somebody else's changes.
3. Remove secrets from tracked and untracked files; do not rely on an ignore
   rule to make exposed credentials safe.
4. Decide whether documents may be sent to the selected model provider.
5. Start with read-only or plan mode when the repository is unfamiliar.

For a large repository, create `.graphifyignore` using `.gitignore` syntax:

```gitignore
# Dependencies and build products
node_modules/
vendor/
dist/
build/
coverage/
.venv/

# Generated or duplicated material
*.min.js
*.generated.*
tmp/
fixtures/large-binaries/

# Nested clones or corpora that should be mapped separately
knowledge-repos/**
!knowledge-repos/README.md

# Graphify must never index its own output
graphify-out/
```

Do not blindly copy this file. A generated file may be essential in one
repository and noise in another.

### 2. Install Graphify

Graphify requires Python 3.10 or later. `uv` is the recommended isolated
installer:

```bash
uv tool install graphifyy
graphify --help
```

If the command is not found after installation:

```bash
uv tool update-shell
```

Then open a fresh terminal. `pipx install graphifyy` is a supported alternative.
The package is named `graphifyy`; the executable is named `graphify`.

Install optional parsers only when the repository needs them. For example:

```bash
uv tool install --upgrade "graphifyy[terraform]"
```

The upstream [Graphify README](../knowledge-repos/Graphify-Labs--graphify/README.md)
contains the current parser and document-format extras.

### 3. Pick one AI CLI

You need only one assistant to begin. The knowledge graph outputs can later be
used by all five tools.

| CLI | Install and launch | Native repository guidance | Graphify project install |
|---|---|---|---|
| Codex | `npm install -g @openai/codex`, then `codex` | `AGENTS.md`; create a starter with `/init` | `graphify install --project --platform codex` |
| GitHub Copilot CLI | `npm install -g @github/copilot`, then `copilot`; authenticate with `/login` | `.github/copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`; bootstrap with `copilot init` | `graphify install --project --platform copilot` |
| Gemini CLI | `npm install -g @google/gemini-cli`, then `gemini` | `GEMINI.md`; bootstrap with `/init` | `graphify install --project --platform gemini` |
| Claude Code | `npm install -g @anthropic-ai/claude-code`, then `claude` | `CLAUDE.md`; bootstrap with `/init` | `graphify install --project --platform claude` |
| Antigravity CLI | install from the official script, then launch `agy` | workspace rules in `.agents/rules/` | `graphify install --project --platform antigravity` |

Official setup references:

- [Codex developer documentation](https://developers.openai.com/codex/)
- [GitHub Copilot CLI getting started](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started)
- [Gemini CLI repository and installation](https://github.com/google-gemini/gemini-cli)
- [Claude Code setup](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- [Antigravity CLI getting started](https://antigravity.google/docs/cli/getting-started)

For Antigravity on macOS or Linux, the official fast-path installation is:

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
agy
```

Review remote installation scripts before executing them if your security policy
requires it. Windows installation commands are in the official Antigravity guide.

### 4. Build from inside the assistant

This distinction prevents the most common Graphify error.

**Recommended for a mixed repository containing code and documents:** launch the
AI CLI first, then enter this in the assistant prompt:

```text
/graphify .
```

For example, with Codex:

```bash
codex
```

Then, inside Codex—not in the shell—type:

```text
/graphify .
```

Code is structurally parsed locally. When no supported Graphify backend key is
configured, the installed skill can use the active assistant session for the
semantic document pass. You do not need to install Claude or invent an API key
when you are already using Codex, Copilot, Gemini, Claude, or Antigravity as the
host assistant.

If you only want local structural code extraction from a normal terminal:

```bash
graphify extract . --code-only
```

Headless semantic extraction of documents is different: it needs an explicitly
configured backend. Decide that based on data residency, cost, and organisational
policy rather than exporting whichever API key happens to be available.

### 5. Open the view

When the build finishes, open `graphify-out/graph.html`:

```bash
# macOS
open graphify-out/graph.html

# Linux
xdg-open graphify-out/graph.html

# Windows PowerShell
start graphify-out/graph.html
```

You can also open the file directly from your editor or file manager. No server
is required for the standard HTML export.

### Beginner success checklist

- [ ] `graphify-out/graph.html` opens in a browser.
- [ ] `GRAPH_REPORT.md` contains communities and connected concepts.
- [ ] `graph.json` parses successfully and is not empty.
- [ ] At least one graph node links back to a real source file.
- [ ] You can distinguish `EXTRACTED` from `INFERRED` relationships.
- [ ] Private files and duplicated dependencies were excluded intentionally.

## Level 1 — navigate without reading the entire repository

### The navigation pyramid

Use the smallest layer that can answer the question:

```text
1. graph.html                 discover vocabulary and communities
2. graphify query             retrieve a scoped subgraph
3. graphify explain/path      inspect one concept or relationship chain
4. referenced source files   verify the claim
5. tests/runtime evidence     prove behaviour before changing or shipping
```

Avoid starting with a full-repository read, a giant recursive search, or the
entire raw `graph.json`. Those approaches consume context before you know which
context matters.

### Use the browser graph

Start broad:

1. Search for the business concept, feature name, API, table, or service—not
   only a filename.
2. Click a likely node and inspect its immediate neighbours.
3. Notice the node's community: it is a candidate subsystem, not automatically
   a true ownership boundary.
4. Look for high-degree nodes that connect multiple communities.
5. Follow the source path and verify the important relationship in the file.

Useful first searches include `authentication`, `entry point`, `database`,
`configuration`, `deployment`, `tests`, `policy`, and the product's main domain
noun.

### Use focused terminal queries

These commands work independently of which AI CLI created the graph:

```bash
graphify query "How does authentication reach the data layer?"
graphify explain "AuthenticationService"
graphify path "HTTP Request" "UserDatabase"
```

Use them for different purposes:

| Command | Best use | Example |
|---|---|---|
| `graphify query` | Natural-language discovery over several relevant nodes | `graphify query "what validates a deployment?"` |
| `graphify explain` | One symbol, service, decision, or concept | `graphify explain "RateLimiter"` |
| `graphify path` | Shortest connection between two known labels | `graphify path "API Gateway" "Audit Log"` |

If a query is too broad, add the subsystem, feature, or exact graph label. If it
returns nothing, inspect `GRAPH_REPORT.md` for the vocabulary Graphify extracted
and retry with that vocabulary.

### Ask evidence-shaped questions

Weak prompt:

```text
Explain the repo.
```

Better prompt:

```text
Using the knowledge graph first, explain how an authenticated request reaches
the persistence layer. Show the path, cite source files, distinguish extracted
from inferred relationships, and list anything that still needs source or test
verification. Do not edit files.
```

Reusable question pattern:

```text
Goal: what decision am I trying to make?
Scope: which service, package, feature, or community?
Evidence: graph path, source files, tests, runtime data?
Output: explanation, table, change plan, or risk list?
Authority: read-only analysis, or are edits allowed?
```

### Ten questions for a new repository

1. What are the main entry points?
2. Which nodes are the most connected, and why?
3. What communities look like deployable or ownership boundaries?
4. How does a request move from ingress to storage or an external service?
5. Where are authentication and authorisation enforced?
6. Which configuration values select production behaviour?
7. What tests cover the critical path?
8. Which components have no obvious tests or operational evidence?
9. What will be affected if the target component changes?
10. Which relationships are inferred and require manual verification?

### Find the best component or product

When a repository contains many tools or cloned projects, do not ask “which one
is best?” without a target outcome. Use this sequence:

1. State the customer problem and measurable success condition.
2. Query for the capability, not the vendor name.
3. Compare only products in the same capability community.
4. Inspect maturity evidence: releases, tests, maintenance, documentation,
   security policy, licence, and operational examples.
5. Verify the shortlisted product's actual README and source.
6. Build the smallest representative proof before adding another product.

Example:

```text
Query the graph for document extraction products. Compare only products that
preserve page/table provenance. Show maturity evidence and source paths. Then
recommend the smallest proof for five representative customer documents.
```

### Understand confidence correctly

- `EXTRACTED` means the relationship was explicit in a parsed source artifact.
- `INFERRED` means the extraction process reasoned that a relationship probably
  exists.
- `AMBIGUOUS` means the evidence was weak or conflicting.

An extracted edge can still describe outdated documentation. An inferred edge
can be useful and correct. Confidence labels tell you what to verify; they do
not replace verification.

### Generate additional navigation documents

The default build intentionally creates only the core HTML, report, and JSON.
Add another output only when somebody will use it:

```text
/graphify . --wiki
```

This creates a Markdown wiki under `graphify-out/wiki/`. Start from
`graphify-out/wiki/index.md` and follow community or node pages instead of
opening hundreds of raw source files.

For additional visual views:

```bash
graphify export callflow-html
graphify tree --graph graphify-out/graph.json --root .
```

The call-flow export emphasizes architecture and execution relationships. The
tree export emphasizes filesystem hierarchy with graph relationships available
for inspection. These are complementary views, not additional sources of truth.

## The five CLI workflows

All five assistants should follow the same graph-first method. Their repository
instruction files and session controls differ.

### Codex workflow

```bash
cd REPOSITORY
codex
```

Inside Codex:

```text
/init
/graphify .
/plan Trace the authentication flow and propose a minimal change plan.
/diff
/review
```

Use `AGENTS.md` for durable repository commands, architectural rules, validation
steps, and the instruction to query Graphify before broad source reads. Codex
supports nested `AGENTS.md` files, with more specific guidance applying closer
to the working directory. Use `codex exec "..."` for non-interactive automation
only after the interactive workflow is stable.

Recommended first prompt:

```text
Use graphify query before broad source inspection. Orient me to this repository,
identify the main execution path and its tests, cite every source file, and make
no changes.
```

### GitHub Copilot CLI workflow

Copilot CLI currently requires Node.js 22 or later for the npm installation:

```bash
npm install -g @github/copilot
cd REPOSITORY
copilot
```

Inside Copilot:

```text
/login
/init
/graphify .
/plan Map the change impact before implementation.
/mcp list
```

`copilot init` creates or updates `.github/copilot-instructions.md`. Copilot CLI
also loads `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`, which makes it useful in a
multi-assistant repository. Use `/plan` for enforced planning before project
edits and review the diff before approving changes.

Official references: [Copilot CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)
and [Copilot CLI setup](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli).

### Gemini CLI workflow

```bash
npm install -g @google/gemini-cli
cd REPOSITORY
gemini
```

Inside Gemini:

```text
/init
/memory show
/graphify .
/plan
/mcp list
```

Use `GEMINI.md` for hierarchical project memory. `/memory list`, `/memory show`,
and `/memory refresh` help verify which instructions are active. Use `@path` to
attach a focused file or directory after the graph has identified it, rather
than attaching the whole repository first.

Official references: [Gemini CLI commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md)
and [Gemini CLI tools](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/tools.md).

### Claude Code workflow

```bash
npm install -g @anthropic-ai/claude-code
cd REPOSITORY
claude
```

Inside Claude Code:

```text
/init
/graphify .
/memory
/permissions
/mcp
```

Use `CLAUDE.md` for project architecture, build/test commands, and graph-first
navigation rules. Claude Code can import another instruction file from
`CLAUDE.md`, so a team may keep shared rules in a canonical file and reference
it rather than maintaining long duplicate instructions. Start a read-only
planning session with:

```bash
claude --permission-mode plan
```

Official references: [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
and [Claude Code setup](https://docs.anthropic.com/en/docs/claude-code/getting-started).

### Antigravity CLI workflow

```bash
cd REPOSITORY
agy
```

Inside Antigravity:

```text
/graphify .
/planning
/context
/diff
/permissions
/agents
/mcp
```

Use `.agents/rules/` for workspace rules. Antigravity can mark rules as always
on, manually activated, model-selected, or glob-scoped. Use `/planning` for a
complex change, `/context` to inspect context use, `/artifact` or `/diff` to
review outputs, and `/agents` only when independent work can be delegated safely.

Official references: [Antigravity CLI reference](https://antigravity.google/docs/cli/reference)
and [Antigravity rules and workflows](https://antigravity.google/docs/rules-workflows).

## Level 2 — make the graph part of the repository

### Add durable graph-first instructions

The platform installer should create the native integration. Independently of
the assistant, the durable rule should express this behaviour:

```markdown
## Repository knowledge graph

This repository has a Graphify knowledge graph in `graphify-out/`.

- For architecture or codebase questions, run `graphify query "<question>"`
  before broad grep or raw source browsing.
- Use `graphify explain "<concept>"` for one node and
  `graphify path "<A>" "<B>"` for a relationship chain.
- Verify material conclusions against the source paths returned by the graph.
- Distinguish EXTRACTED from INFERRED relationships.
- After code changes, run `graphify update .` and the relevant tests.
```

Place or reference the rule through each assistant's native instruction surface:

| Assistant | Durable project surface |
|---|---|
| Codex | `AGENTS.md` |
| Copilot CLI | `.github/copilot-instructions.md` and/or shared `AGENTS.md` |
| Gemini CLI | `GEMINI.md` |
| Claude Code | `CLAUDE.md` |
| Antigravity | `.agents/rules/` |

Keep instructions short and executable. A rule such as “understand the code
well” is not testable. A rule such as “run `graphify query` before broad source
reads and cite returned paths” is.

### Keep the graph current

For an explicit update from an assistant:

```text
/graphify . --update
```

For structural code updates from the terminal:

```bash
graphify update .
```

For automatic AST refresh after commits:

```bash
graphify hook install
```

Re-run `graphify hook install` after reinstalling or upgrading the isolated
Graphify tool, because the hook records the interpreter path.

### Decide what to commit

A team can commit the shared navigation artifacts:

```text
graphify-out/graph.html
graphify-out/GRAPH_REPORT.md
graphify-out/graph.json
graphify-out/manifest.json
```

Common local-only candidates are `graphify-out/cost.json` and, depending on
repository size and team preference, `graphify-out/cache/`.

Before committing:

1. Check that source paths are portable or intentionally relative.
2. Confirm the graph contains no private content that the repository must not
   distribute.
3. Review graph size and generated diff.
4. Ensure the graph was built from the intended scope.
5. Record health warnings rather than presenting a partial graph as complete.

### The safe change workflow

```text
1. Ask the graph for the execution path and blast radius.
2. Verify the important nodes in source and tests.
3. Enter plan/read-only mode.
4. Agree on the smallest change and validation evidence.
5. Implement.
6. Run focused tests, then broader repository checks as risk requires.
7. Review the diff.
8. Refresh the graph.
9. Query the affected path again to detect unexpected structural change.
```

Reusable implementation prompt:

```text
Use the existing graph first to identify the target path, callers, configuration,
tests, and likely blast radius. Verify against source. Propose a minimal plan and
wait for plan approval before editing. Preserve unrelated user changes. After
implementation, run the relevant tests, review the diff, update the graph, and
report evidence plus remaining uncertainty.
```

## Level 3 — advanced operation

### Use Graphify as an MCP server

For repeated tool-level access from an MCP-compatible assistant:

```bash
$(cat graphify-out/.graphify_python) -m graphify.serve graphify-out/graph.json
```

The server exposes scoped graph operations such as querying, neighbours,
communities, central nodes, statistics, and shortest paths. In a JSON MCP
configuration, use the absolute interpreter path printed by:

```bash
cat graphify-out/.graphify_python
```

Use the absolute path to `graphify-out/graph.json` as an argument. Do not put
shell command substitution such as `$(cat ...)` inside a JSON configuration;
desktop clients do not evaluate it.

### Separate the three operating modes

| Mode | Use when | Data/model considerations |
|---|---|---|
| Assistant-driven `/graphify` | Mixed code and documentation; interactive judgement is available | Semantic content uses the active assistant or an explicitly configured backend |
| Headless `graphify extract` | CI, scheduled generation, repeatable automation | Mixed semantic corpora require a supported backend and explicit data policy |
| `--code-only` | Source code must remain local or no semantic backend is available | Local structural graph; documentation concepts are intentionally absent |

Never interpret a code-only graph as proof that the repository contains no
documentation decisions. It only means those documents were not semantically
indexed.

### Map multiple repositories intentionally

Choose one of two patterns:

1. **Separate graphs:** best when repositories have different owners, access
   policies, release cycles, or sensitive content.
2. **Merged graph:** useful when the question genuinely crosses services or
   repositories and node origin is preserved.

For a repository containing many clones, index a curated catalogue first. Map
individual clones separately, then merge only the shortlisted graphs. Indexing
every dependency, fork, vendor tree, and duplicate README usually creates a
larger graph without creating a better decision surface.

### Tune communities, not truth

Clustering controls how the graph is presented. It does not alter what the
source code does. When communities are too broad or hubs dominate:

```text
/graphify . --cluster-only --resolution 1.5
/graphify . --cluster-only --exclude-hubs 99
```

Record the settings used when comparing graph reports over time.

### Add formats only when the decision needs them

Examples:

```bash
uv tool install --upgrade "graphifyy[terraform]"
uv tool install --upgrade "graphifyy[pdf]"
uv tool install --upgrade "graphifyy[office]"
uv tool install --upgrade "graphifyy[sql]"
```

Every additional format increases scope, privacy considerations, and extraction
time. Add it because a question depends on that artifact—not because the parser
exists.

### Run a graph quality review

A mature graph workflow records:

- scanned, indexed, ignored, unsupported, and failed file counts;
- structural and semantic node counts;
- missing or dangling endpoints;
- duplicate or collapsed edges;
- self-loops;
- files that produced no nodes;
- inferred/ambiguous edge counts;
- graph freshness relative to the current commit;
- query answers that failed source verification.

“Zero hallucination” is not a defensible guarantee. The defensible standard is:

1. attach provenance to every material relationship;
2. label extracted, inferred, and ambiguous claims;
3. preserve failed or skipped file warnings;
4. verify important answers against source and tests;
5. abstain when the evidence is insufficient.

### Create a repository learning loop

For each important investigation:

1. Save the question.
2. Save the graph nodes and paths used.
3. Record the verified source files.
4. Record incorrect or missing graph relationships.
5. Improve repository docs, names, tests, or extraction scope.
6. Refresh the graph.
7. Repeat the original query and compare the answer.

The goal is not just a clever map. The goal is a repository that becomes easier
for both humans and agents to understand correctly.

## Troubleshooting

### Error: `no LLM API key found`

Cause: Graphify was run headlessly against documents, papers, or images without
a semantic backend.

Choose one intentional solution:

1. Recommended interactive path: launch Codex, Copilot, Gemini, Claude, or
   Antigravity and enter `/graphify .` inside the assistant.
2. Local code-only path: `graphify extract . --code-only`.
3. Headless semantic path: configure a supported backend that your security and
   data-residency policy permits.

Installing or setting a random provider key is not a valid fix.

### `graphify: command not found`

```bash
uv tool update-shell
```

Open a new terminal. If installed with pipx, use `pipx ensurepath` instead.

### `No solution found` for package `graphify`

The PyPI package name is `graphifyy`:

```bash
uvx --from graphifyy graphify --help
```

### Terraform or HCL files were skipped

```bash
uv tool install --upgrade "graphifyy[terraform]"
```

Then rebuild or update the graph.

### The graph is enormous and difficult to navigate

1. Inspect the detected file and directory counts.
2. Exclude dependencies, generated output, caches, nested clones, large test
   fixtures, and Graphify's own output in `.graphifyignore`.
3. Keep a curated index README for excluded repositories.
4. Map important subprojects separately.
5. Rebuild and compare whether important queries improved.

Do not narrow solely to reduce a number. Preserve every artifact needed for the
decisions the graph must support.

### The graph is stale

```bash
graphify update .
graphify hook install
```

Also confirm `graphify-out/manifest.json` exists and the hook points to the
current Graphify interpreter.

### Query results are too broad

- Use exact vocabulary from the graph report.
- Add a subsystem or file-type boundary to the question.
- Switch from `query` to `explain` when one known concept is the target.
- Use `path` only after identifying valid endpoint labels.
- Verify the returned source paths instead of requesting a larger answer.

### The graph reports dangling or collapsed edges

Do not hide the warning. Determine whether the edges represent:

- external dependencies intentionally outside the graph;
- unresolved identifiers;
- partial or failed extraction;
- duplicate relationships between the same endpoints;
- AST and semantic IDs that do not align;
- genuine repository documentation gaps.

The graph may remain useful, but reports must describe the limitation.

### A rebuild wants to replace a larger graph with a smaller graph

Treat this as a possible partial extraction, scope error, parser failure, or
unexpected ignore rule. Confirm the intended corpus before forcing replacement.
Use a force/partial option only when the shrink is understood and intentional.

## Reusable quick-reference card

```bash
# Install
uv tool install graphifyy
graphify install --project --platform codex
# Replace codex with: copilot, gemini, claude, or antigravity

# Build from inside the selected AI assistant
/graphify .

# Navigate from any terminal
graphify query "QUESTION"
graphify explain "CONCEPT"
graphify path "NODE A" "NODE B"

# Maintain
graphify update .
graphify hook install

# Open
open graphify-out/graph.html            # macOS
xdg-open graphify-out/graph.html        # Linux
start graphify-out/graph.html           # Windows PowerShell
```

## Final operating principles

1. Start from the customer or engineering decision, not the tool list.
2. Query the graph before reading the entire repository.
3. Use the graph to find evidence, not to replace evidence.
4. Keep durable instructions native to each assistant.
5. Prefer plan/read-only mode in unfamiliar or high-risk repositories.
6. Preserve unrelated human changes.
7. Review every diff and run tests proportional to risk.
8. Refresh the graph after changes.
9. Record extraction gaps and confidence honestly.
10. Make the repository easier to understand, not merely easier to search.

## Primary references

- [Graphify upstream README](../knowledge-repos/Graphify-Labs--graphify/README.md)
- [OpenAI Codex documentation](https://developers.openai.com/codex/)
- [GitHub Copilot CLI documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started)
- [Gemini CLI documentation](https://github.com/google-gemini/gemini-cli/tree/main/docs)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- [Google Antigravity CLI documentation](https://antigravity.google/docs/cli/getting-started)
