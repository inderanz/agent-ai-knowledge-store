# Volume 11 implementation evidence ledger

**Verified:** 2 August 2026. **Status:** local controls pass; no customer Registry
was changed and no production qualification is claimed.

| Decision | Official evidence | Implemented artifact |
|---|---|---|
| Treat Registry as project catalog with explicit migration | [overview](https://docs.cloud.google.com/agent-registry/overview), [setup](https://docs.cloud.google.com/agent-registry/setup) | topology/migration gates |
| Preserve writable Service versus query projections | [data model](https://docs.cloud.google.com/agent-registry/data-model) | resource contract and catalog validator |
| Separate privileged metadata editing from agents | [roles](https://docs.cloud.google.com/agent-registry/roles-permissions) | IAM separation gate |
| Apply endpoint/binding location restrictions | [endpoints](https://docs.cloud.google.com/agent-registry/register-endpoints), [bindings](https://docs.cloud.google.com/agent-registry/manage-bindings) | binding validation and lab |
| Resolve through pinned ADK then mediate invocation | [ADK resolution](https://docs.cloud.google.com/agent-registry/resolve-endpoints-and-build-orchestrators) | `fde_kit.registry`, Gateway gate |
| Review external skills as code | [google/skills reviewed commit](https://github.com/google/skills/tree/41f503f7d7f878bf77f0700487d60cf0490d72fd) | supply-chain checklist |

Production evidence still required: live API/location, exported registrations and
projections, IAM/audit, source/deployment provenance, protocol/health/load,
search uniqueness, binding/Gateway behavior, revocation/cache convergence,
reconstruction and customer acceptance.
