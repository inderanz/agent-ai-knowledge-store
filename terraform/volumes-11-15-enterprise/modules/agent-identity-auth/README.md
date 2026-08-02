# Agent Identity OAuth module

Production-oriented configuration for Google Cloud Agent Identity auth providers. The service and provider resource are Preview as of the pinned baseline; obtain customer approval, record the Preview exception, and test rollback before production adoption.

Security invariants:

- OAuth scopes are explicit allowlists; an empty allowlist is rejected because Google interprets it as all scopes.
- every provider is bound to one or more `principal://` workload identities;
- OAuth secrets enter Terraform through an `ephemeral` variable and the provider's `client_secret_wo` write-only field;
- PKCE is mandatory for three-legged OAuth;
- API-key providers are excluded because `api_key` is a sensitive but state-persistent provider argument;
- deletion is protected with `PREVENT`.

Supply secrets only at `terraform apply`, ideally from an ephemeral CI job fed by an approved secret broker. Increment `client_secret_version` whenever the upstream secret rotates.

Official references: [Agent Identity overview](https://cloud.google.com/iam/docs/agent-identity-overview), [auth manager overview](https://cloud.google.com/iam/docs/auth-manager-overview), [manage auth providers](https://cloud.google.com/iam/docs/manage-auth-providers-v2), [Terraform resource at provider v7.42.0](https://github.com/hashicorp/terraform-provider-google/blob/v7.42.0/website/docs/r/agent_identity_auth_provider.html.markdown), and [Terraform ephemeral values](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/ephemeral).
