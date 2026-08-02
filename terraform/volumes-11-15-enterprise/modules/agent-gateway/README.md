# Enterprise Agent Gateway module

Creates the first-class `google_network_services_agent_gateway`, a fail-closed IAP
`google_network_services_authz_extension`, its targeted REQUEST_AUTHZ policy, and
conditional `roles/iap.egressor` bindings for Registry agents, MCP servers and
endpoints. The deprecated provider field `protocols` is intentionally omitted.

The module defaults destructive lifecycle to `PREVENT`. `ENFORCED` is fail-closed;
the explicit `DRY_RUN` mode follows Google's audit-only setup (`fail_open = true`
plus `iamEnforcementMode = DRY_RUN`) and must never be promoted to production.
Conditions must be reviewed CEL expressions using supported IAP agent attributes.
Terraform creation alone does not supply traffic evidence.

Official references: [Agent Gateway provider resource v7.42.0](https://github.com/hashicorp/terraform-provider-google/blob/v7.42.0/website/docs/r/network_services_agent_gateway.html.markdown),
[authorization policy resource](https://github.com/hashicorp/terraform-provider-google/blob/v7.42.0/website/docs/r/network_security_authz_policy.html.markdown),
[Gateway setup](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/set-up-agent-gateway), and
[IAM policies](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/policies/configure-iam-policies).
