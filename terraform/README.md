# Terraform engineering standard

Terraform examples must represent a reusable production pattern, not a copy-paste demo.

## Module contract

Each module provides `README.md`, `versions.tf`, `variables.tf`, `main.tf`, and `outputs.tf`; constrains Terraform and provider versions; avoids embedded project IDs and regions; exposes labels; documents IAM effects; and includes at least one validated example.

State is remote, encrypted, access-controlled, versioned where supported, and isolated by environment. State bucket/project design is a bootstrap concern and must not depend circularly on the state it creates.

CI runs formatting, validation, linting, security scanning, and a plan using non-production credentials. Apply uses an explicitly approved promotion identity. Examples must not grant primitive roles, create service-account keys, or embed secrets.

No empty module is claimed as implemented. The production-oriented implementation for Agent Registry, Agent Gateway, Agent Identity, Cloud Armor, and Gemini Enterprise is in [volumes-11-15-enterprise](volumes-11-15-enterprise/README.md); other directories remain examples or placeholders unless their own README states otherwise.
