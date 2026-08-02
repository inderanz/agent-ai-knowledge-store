# Enterprise Agent Registry module

Uses first-class Google provider 7.42.0 resources
`google_agent_registry_service` and `google_agent_registry_binding`. It supports
manual Agent, MCP Server and HTTPS Endpoint registrations and optional Auth
Provider bindings. Production deletion defaults to `PREVENT`.

The module rejects insecure URLs, invalid kind/spec/protocol combinations and the
documented `us`/`eu` endpoint/binding limitation. It does not claim that catalog
registration proves endpoint health or Gateway authorization. Inputs containing
Agent Cards or tool specifications are production metadata and require semantic
review before apply.

Official references: [Agent Registry Terraform provider source at v7.42.0](https://github.com/hashicorp/terraform-provider-google/blob/v7.42.0/website/docs/r/agent_registry_service.html.markdown),
[Registry data model](https://docs.cloud.google.com/agent-registry/data-model), and
[bindings](https://docs.cloud.google.com/agent-registry/manage-bindings).
