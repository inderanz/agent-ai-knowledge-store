# Volume 15 implementation evidence ledger

**Verified:** 2 August 2026. **Status:** local configuration tests pass; no app,
data store, connector, IAM grant, agent, license or customer data was changed.

| Decision | Official evidence | Implemented artifact |
|---|---|---|
| Decide CMEK/location/immutable ID before app creation | [create app](https://docs.cloud.google.com/gemini/enterprise/docs/create-app) | `fde_kit.enterprise_app` and admission gates |
| Inventory data-store relationship, limit and compatibility | [apps/data stores](https://docs.cloud.google.com/gemini/enterprise/docs/apps-data-stores) | data-store contract/validator |
| Require connector access control/scopes/sync/CMEK decisions | [connector introduction](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/introduction-to-connectors-and-data-stores) | connector lifecycle/lab |
| Restrict at app level without broad project override | [app IAM](https://docs.cloud.google.com/gemini/enterprise/docs/iam-policy-for-apps) | IAM conflict rejection |
| Gate location and residency feature set | [locations](https://docs.cloud.google.com/gemini/enterprise/docs/locations) | location consistency gate |
| Enable privacy-reviewed agent observability | [settings](https://docs.cloud.google.com/gemini/enterprise/docs/manage-observability-settings), [release notes](https://docs.cloud.google.com/gemini/enterprise/docs/release-notes) | observability gate/operations |
| Govern imported MCP with Registry/Gateway | [Registry import](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/import-govern-mcp-server-agent-registry) | ungoverned-import rejection |

Production evidence still required: edition/license/allowlist, live locations and
maturity, CMEK-before-create, source ACL and negative cohorts, connector scopes/
sync/recovery, app IAM effective access, representative evaluation, governed
actions, observability/privacy, load/SLO/support, reindex/DR/exit and value.
