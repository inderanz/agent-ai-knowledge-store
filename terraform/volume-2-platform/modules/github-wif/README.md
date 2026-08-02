# GitHub Workload Identity Federation

Separate pools prevent a token admitted through the planning provider from impersonating the apply identity. Both providers require the immutable GitHub `repository_id`. The apply provider additionally requires the configured protected ref and a GitHub OIDC `environment` claim ending in `-apply`.

The customer must configure protected `dev-apply`, `test-apply`, `stage-apply`, and `prod-apply` environments, with required reviewers for production, plus protected branches and restricted workflow changes. Federation removes service-account keys; it does not make an untrusted workflow safe.
