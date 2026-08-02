# Chapter and artifact inventory

This inventory is the completion ledger for the handbook. Volume READMEs define the substantive chapter contracts; this file records their delivery state.

## Volume inventory

| Volume | Planned units | Draft | In review | Approved | Detailed map |
|---|---:|---:|---:|---:|---|
| 1 — Foundations | 8 | 1 full volume + 1 imported | 0 | 0 | [Open](volume-1-foundations/README.md) |
| 2 — Platform architecture | 10 | 1 full volume + 1 imported | 0 | 0 | [Open](volume-2-platform/README.md) |
| 3 — ADK engineering | 12 | 1 full volume | 0 | 0 | [Open](volume-3-adk/README.md) |
| 4 — Runtime and deployment | 10 | 1 full volume | 0 | 0 | [Open](volume-4-runtime/README.md) |
| 5 — Security and governance | 12 | 1 full volume | 0 | 0 | [Open](volume-5-security/README.md) |
| 6 — Reliability and operations | 10 | 1 full volume | 0 | 0 | [Open](volume-6-sre/README.md) |
| 7 — Engineering reference | 13 reference sets | 1 full volume | 0 | 0 | [Open](volume-7-reference/README.md) |
| 8 — Industry architectures | 9 | 1 full volume | 0 | 0 | [Open](volume-8-industries/README.md) |
| 9 — FDE delivery handbook | 10 | 1 full volume | 0 | 0 | [Open](volume-9-fde/README.md) |
| 10 — Evolution and migrations | 9 | 1 full volume | 0 | 0 | [Open](volume-10-evolution/README.md) |
| 11 — Agent Registry | 11 | 1 full volume | 0 | 0 | [Open](volume-11-agent-registry/README.md) |
| 12 — Agent Gateway | 11 | 1 full volume | 0 | 0 | [Open](volume-12-agent-gateway/README.md) |
| 13 — Agent Identity | 11 | 1 full volume | 0 | 0 | [Open](volume-13-agent-identity/README.md) |
| 14 — Cloud Armor | 11 | 1 full volume | 0 | 0 | [Open](volume-14-cloud-armor/README.md) |
| 15 — Gemini Enterprise app | 11 | 1 full volume | 0 | 0 | [Open](volume-15-gemini-enterprise-app/README.md) |
| **Total** | **158** | **15 full volumes plus imported source chapters** | **0** | **0** | |

## Required artifact coverage

Every chapter issue identifies applicable artifacts. An artifact can be marked not applicable only with an approved reason.

| Artifact family | Expected evidence | Current state |
|---|---|---|
| Research record | Official docs, tagged source, sample commit, release notes, change comparison | Dated Volume 1–15 records complete; semantic/independent reviews pending |
| Architecture | Logical, physical, component, network, security, identity, deployment, and data-flow diagrams | Full draft coverage in Volumes 1 and 2; review pending |
| Behavior | Sequence, lifecycle, state, failure, retry, recovery, and approval diagrams | Full draft coverage in Volumes 1 and 2; review pending |
| Python | Typed runnable package, configuration, logging, errors, retries, OTel, tests, lock | Volume 2 admission, Volume 3 ADK workflow, and Volumes 4–15 FDE production kit implemented; customer integrations pending |
| Terraform | Modules, remote-state pattern, variables, outputs, examples, docs, validation | Volume 2 governed cell/WIF and narrow Volume 14 Cloud Armor policy module implemented; customer plans/applies pending |
| Delivery | GitHub Actions, Cloud Build, Artifact Registry, Cloud Deploy, promotion, rollback | Volume 2 build/promote, Volume 3 ADK qualification, and Volumes 4–10 local CI/qualification gates implemented; cloud execution pending |
| Security | Threat model, IAM, identity, network, content, data, tool, supply chain, audit | Full Volume 5 control handbook and shared policy tests plus cross-volume coverage; customer and independent review pending |
| Operations | Logs, metrics, traces, SLOs, alerts, runbooks, capacity, recovery, DR, cost | Volume 2–15 operations packs and reliability/control-plane tests implemented; cloud exercises pending |
| Customer delivery | Story, discovery workshop, questions, decisions, FDE notebook, checklist | Full Volume 9 delivery system plus workshops/notebooks/checklists in Volumes 1–10; customer simulation pending |
| Labs | Setup, validation, failure injection, cleanup, troubleshooting | Executable/local Volume 2–15 labs implemented; customer sandbox evidence pending |
| ADR | Context, options, decision, consequences, validation, evidence | Repository ADR plus full draft ADRs in Volumes 1 and 2 |

## Definition of real chapter content

A chapter is substantive only when it:

1. Answers a bounded customer engineering problem end to end.
2. Separates 🟢 official capability, 🟡 recommendation, and 🔵 field pattern at claim level.
3. Contains paragraph-local official evidence and a dated baseline.
4. Includes all applicable architecture and behavior views.
5. Provides runnable, tested implementation artifacts rather than illustrative fragments.
6. Covers security, operations, SLOs, recovery, DR, performance, and cost.
7. Includes an executable lab, ADR, workshop, production checklist, and next-chapter dependency.
8. Passes research, architecture, implementation, security, operations, and customer-delivery review.

## Delivery order

1. Approve repository and evidence standards through Issues #1–#9.
2. Normalize and verify the three imported Drafts as the first chapters of Volumes 1–3.
3. Build one production-shaped vertical slice across ADK, runtime, security, SRE, Terraform, CI/CD, and labs.
4. Use that slice as the tested reference implementation for later chapters.
5. Expand volumes in dependency order while the upstream-change workflow continuously revalidates Approved material.
