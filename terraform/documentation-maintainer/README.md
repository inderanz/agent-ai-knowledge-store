# Documentation maintainer identity

This root stack creates the dedicated keyless Google Cloud identity used by the
agentic documentation-maintenance workflow. It does not create customer runtime
resources and must be deployed to a separately governed documentation project.

The provider condition requires all of the following token claims:

- immutable GitHub repository ID and owner ID;
- the expected case-sensitive `owner/repository`;
- the exact maintainer workflow from `refs/heads/main`;
- the `main` ref; and
- a scheduled or manually dispatched event.

The service account receives a custom role containing only
`aiplatform.endpoints.predict` and `serviceusage.services.use`. The workflow uses
Workload Identity Federation; no service-account key is created.

Google references:

- [Secure deployment pipelines with Workload Identity Federation](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines)
- [Vertex AI access control](https://docs.cloud.google.com/vertex-ai/docs/general/access-control)
- [GitHub Actions OIDC claim reference](https://docs.github.com/en/actions/reference/security/oidc)

## Deploy

1. Create or select a dedicated project and a protected GCS Terraform state
   bucket through the organization's normal bootstrap process.
2. Copy `terraform.tfvars.example` outside the repository as `terraform.tfvars`
   and replace every example value. Get immutable IDs with
   `gh api repos/inderanz/agent-ai-knowledge-store --jq '{repository_id: .id, owner_id: .owner.id}'`.
3. Authenticate as the approved infrastructure-deployment identity, then run:

   ```bash
   terraform init -backend-config="bucket=STATE_BUCKET" -backend-config="prefix=fde-documentation-maintainer"
   terraform plan -out=tfplan
   terraform apply tfplan
   ```

4. Copy the four Terraform outputs to the matching GitHub repository variables,
   set an explicitly qualified `DOC_MAINTAINER_MODEL`, and leave
   `ENABLE_AGENTIC_DOC_PROPOSALS=false` until the first detect-only run passes.

Never commit the real `.tfvars`, plan, state, credentials, or customer content.
