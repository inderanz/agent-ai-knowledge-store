# Gemini Agent Platform enterprise Terraform

Deployable Terraform for the five platform capabilities covered by Volumes 11–15:

| Capability | Google resource/module | Enterprise control |
|---|---|---|
| Agent Registry | `google_agent_registry_service`, `google_agent_registry_binding` | HTTPS interfaces, typed specifications, protected deletion |
| Agent Gateway | `google_network_services_agent_gateway` plus IAP authz extension/policy | governed access, fail-closed IAP, conditional `roles/iap.egressor` |
| Agent Identity | `google_agent_identity_auth_provider` | workload binding, scope allowlist, PKCE, ephemeral/write-only OAuth secrets |
| Cloud Armor | official `GoogleCloudPlatform/cloud-armor/google` `8.1.1` | default deny, preview-first WAF, enforcement approval gate |
| Gemini Enterprise | Discovery Engine datastore/search engine/CMEK/ACL/IAM | intranet app, app-scoped users, protected deletion, ordered CMEK |

## Qualified versions

- Terraform `1.15.8`
- `hashicorp/google` `7.42.0`
- `hashicorp/google-beta` `7.42.0` transitively required by Google's Cloud Armor module
- `GoogleCloudPlatform/cloud-armor/google` `8.1.1`

Exact provider selections are committed in `.terraform.lock.hcl`. Upgrade them through a qualification PR, never by an unreviewed floating constraint.

## Deployment workflow

1. Bootstrap a dedicated, versioned GCS state bucket with public access prevention, uniform bucket-level access, customer-required CMEK/retention, and a separate deployment project. That bootstrap stack must not use its own bucket as state.
2. Use Workload Identity Federation from CI; do not create service-account keys. Split plan and apply identities and grant only the resource permissions required by this stack.
3. Copy `backend.hcl.example` and `terraform.tfvars.example` outside source control and replace every placeholder.
4. For a staging qualification, set `gateway.iam_enforcement_mode = "DRY_RUN"`; Google maps this to audit-only IAP behavior. Production must use `ENFORCED`, which is fail-closed and is checked by the plan policy.
5. Run:

   ```bash
   terraform init -backend-config=/secure/path/backend.hcl
   terraform fmt -check -recursive
   terraform validate
   terraform plan -out=reviewed.tfplan
   terraform show -json reviewed.tfplan > reviewed.tfplan.json
   python policies/validate_plan.py --environment production reviewed.tfplan.json
   ```

6. Have platform, security, IAM, network, data and application owners review the immutable plan. Apply that exact plan artifact under the promotion identity.
7. Complete both handoffs reported by `mandatory_handoffs`: attach Cloud Armor to every applicable backend and configure/verify Gemini Enterprise observability.

For non-empty `identity_providers`, supply `oauth_client_secrets` only during apply using an ephemeral CI value obtained from the approved secret broker. Never write it to a `.tfvars`, saved plan, log, artifact, or environment shared across jobs. Increment each provider's `client_secret_version` for rotation.

## Important boundaries

- Agent Registry, Agent Gateway, and Agent Identity are shown as Preview in the pinned provider/product documentation at this baseline; obtain explicit customer exceptions and rollback agreements.
- The gateway module creates the authorization control plane. Customer network attachments, private DNS zones, endpoint certificates, and destination workloads remain owned by their respective landing-zone stacks.
- Cloud Armor is ineffective until its policy is attached in the load-balancer stack. Preview results must be analyzed before enforcement.
- Datastore ingestion, connector authorization, schema promotion, source ACL verification, license assignment, and observability configuration are operational workflows outside this stack.
- The exact IAM permissions required to run this code should be converted into customer-specific custom roles after a dry-run audit; primitive roles are not acceptable.

Official sources: [Agent Registry](https://cloud.google.com/agent-registry/overview), [Agent Gateway](https://cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview), [Agent Identity](https://cloud.google.com/iam/docs/agent-identity-overview), [Cloud Armor module](https://github.com/GoogleCloudPlatform/terraform-google-cloud-armor/tree/v8.1.1), and [Gemini Enterprise documentation](https://cloud.google.com/gemini/enterprise/docs/overview).
