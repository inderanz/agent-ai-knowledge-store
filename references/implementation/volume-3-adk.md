# Volume 3 implementation evidence ledger

**Evidence date:** 2 August 2026  
**Qualified ADK:** Python v2.6.1  
**ADK release commit:** `740582e9f283cd23ff5cec1389400b422513f765`  
**Rule:** product documentation defines service behavior; pinned Google source
proves the reviewed implementation shape but is not a service commitment.

“Latest” is dated evidence, never a permanent guarantee. Every customer release
must rerun the repository freshness gate, inspect release notes, rebuild the
transitive lock, and repeat compatibility/evaluation tests.

## ADK workflow API

| Implemented decision | Exact official evidence | Consuming asset |
|---|---|---|
| Import `Context`, `Event`, and `Workflow` from the public package root | [`google.adk.__init__` at v2.6.1](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/src/google/adk/__init__.py) | `enterprise_adk/agent.py` |
| Import `JoinNode`, `RetryConfig`, `START`, and `node` from the public workflow package | [workflow public exports at v2.6.1](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/src/google/adk/workflow/__init__.py) | graph and chapter API guidance |
| Declare sequences, fan-out, join and route maps through `Workflow(edges=...)`; cap graph-scheduled concurrency | [Workflow implementation at v2.6.1](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/src/google/adk/workflow/_workflow.py), [official route sample](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/contributing/samples/workflows/route/agent.py), [official fan-out/join sample](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/contributing/samples/workflows/fan_out_fan_in/agent.py) | `root_agent`, topology CI test |
| Return/yield `Event(output=...)`, `Event(state=...)`, or `Event(route=...)` from function nodes | [Event implementation at v2.6.1](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/src/google/adk/events/event.py), [data-handling docs at reviewed commit](https://github.com/google/adk-docs/blob/308c7831800d4543ac230f5a64da335796575135/docs/graphs/data-handling.md) | graph nodes and event-schema chapter |
| A join needs output from every predecessor; missing output can stop progress | [graph routes and JoinNode warning at reviewed docs commit](https://github.com/google/adk-docs/blob/308c7831800d4543ac230f5a64da335796575135/docs/graphs/routes.md), [JoinNode source](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/src/google/adk/workflow/_join_node.py) | explicit outputs from both verification branches; SRE guidance |
| Dynamic code uses a resumable `@node` and awaits `Context.run_node`; dynamic task count remains application-bounded | [dynamic workflow docs at reviewed commit](https://github.com/google/adk-docs/blob/308c7831800d4543ac230f5a64da335796575135/docs/graphs/dynamic.md), [official v2.6.1 dynamic sample](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/contributing/samples/workflows/dynamic_nodes/agent.py), [`Context.run_node` source](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/src/google/adk/agents/context.py) | `bounded_dynamic_checks` and lab resume tests |
| Graph workflows currently have no live streaming | [known limitations at reviewed docs commit](https://github.com/google/adk-docs/blob/308c7831800d4543ac230f5a64da335796575135/docs/graphs/index.md) | qualification acceptance and architecture caveat |
| v2.6.1 supports task-mode agents in workflow execution | [task-mode handling in v2.6.1 Workflow source](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/src/google/adk/workflow/_workflow.py) | correction to imported v2.0-era limitation |

## Interrupts, state and enterprise controls

| Implemented decision | Exact official evidence | Consuming asset |
|---|---|---|
| Use `RequestInput` for typed workflow interruption, not as proof of authorization | [`RequestInput` source at v2.6.1](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/src/google/adk/events/request_input.py), [human-input docs at reviewed commit](https://github.com/google/adk-docs/blob/308c7831800d4543ac230f5a64da335796575135/docs/graphs/human-input.md), [official request-input sample](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/contributing/samples/workflows/request_input_advanced/agent.py) | clarification example; external approval boundary |
| Persist workflow node output and metadata through the event/session contract | [v2.6.1 event `output`/`node_info` fields](https://github.com/google/adk-python/blob/740582e9f283cd23ff5cec1389400b422513f765/src/google/adk/events/event.py), [sessions and state](https://adk.dev/sessions/) | migration lab and trace correlation |
| Connect local ADK Runner to managed sessions with `VertexAiSessionService`; `AdkApp` is already connected when using the deployment path | [Manage sessions with ADK](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/sessions/manage-with-adk) | managed-session lab and chapter |

Approval digest binding, segregation of duties, durable idempotency, unknown-outcome
reconciliation, tool authorization, business-ledger ownership and log redaction
are handbook production patterns. The cited ADK features enable workflow execution;
they do not claim to supply these customer controls automatically.

## Evaluation and deployment

| Implemented decision | Exact official evidence | Consuming asset |
|---|---|---|
| Gate exact tool trajectories and response similarity in CI; use groundedness and safety in an approved online gate | [ADK evaluation guide](https://adk.dev/evaluate/), [criteria reference](https://adk.dev/evaluate/criteria/), [reviewed evaluation docs source](https://github.com/google/adk-docs/blob/308c7831800d4543ac230f5a64da335796575135/docs/evaluate/index.md) | `adk_eval_config.json`, labs, CI separation |
| Deploy a qualification agent as `agent_engines.AdkApp` using `client.agent_engines.create` and Agent Identity | [current Agent Runtime ADK quickstart](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart-adk) | guarded `deploy.py` |
| Pin deployment dependencies and keep object deployment a sandbox/qualification route | [current deploy-an-agent guidance](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/deploy-an-agent) | exact direct pins and production caveat |
| Production teams can choose source, Dockerfile, container image, or Developer Connect; Agent Runtime deployment is Python-only | [deployment methods and language statement](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/deploy-an-agent) | chapter target-selection table |

`google-cloud-aiplatform==1.163.0` was the current package-index release checked on
2 August 2026 and was cross-checked against the official Google API client
[v1.163.0 release](https://github.com/googleapis/python-aiplatform/releases/tag/v1.163.0)
at commit `6845eaf9c5513198f6eba11d2c091a4a29c35565`. The official container
deployment page currently requires at least 1.144 for BYOC. A library release is
not a Google Cloud service availability guarantee; the exact version still
requires customer qualification.

## Tests and evidence presently available

- 21 dependency-free domain/evaluation/deployment tests pass locally.
- 2 delivery-policy tests and 3 qualification-validator tests pass locally.
- Five deterministic release cases pass at the required 100% threshold.
- Every Python file compiles locally.
- The ADK graph import/topology test passes against a temporary fully resolved
  `google-adk==2.6.1` installation and is repeated in GitHub Actions and Cloud
  Build. The temporary installation was removed after the test; the workstation's
  global environment was not modified.
- No Google Cloud resource was created, modified or deleted.

## Evidence still required before production approval

Official citations cannot prove the customer's data classification, contractual
eligibility, current target-region availability, org-policy compatibility,
network reachability, runtime/tool IAM, CMEK/secrets design, quota/capacity,
managed-session retention/deletion/restore, business-ledger durability, target
reconciliation behavior, real approval-provider identity, prompt/model quality,
privacy redaction, latency/cost envelope, rollback, disaster recovery, on-call
competence, or threat acceptance. The chapter remains **Draft** until those gates
and the repository's independent architecture, security, SRE, FDE, and editorial
reviews pass.
