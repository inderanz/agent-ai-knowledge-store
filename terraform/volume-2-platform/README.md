# Volume 2 platform foundation

This Terraform composition creates a production-shaped governed cell for the Volume 2 admission service:

- a project created through Cloud Foundation Fabric `v57.0.0`;
- explicit Google APIs;
- optional Shared VPC service-project attachment and subnet-level use;
- dedicated runtime, build, deploy, plan, and apply identities;
- Artifact Registry with immutable tags;
- Firestore for idempotent admission decisions;
- a regional Secret Manager secret without a committed secret version;
- log-based metrics, alerting, and a dashboard;
- a project budget; and
- an optional GitHub OIDC Workload Identity Federation provider.

It intentionally does not create Agent Gateway, Agent Registry, Agent Identity, Managed Agents, or Gemini Enterprise app resources. Their current APIs, maturity, regional placement, and customer terms must be qualified through the official product workflow. No undocumented Terraform resource is invented.

## Qualified versions

- Terraform `1.15.8`
- Google provider `7.42.0`
- Cloud Foundation Fabric `v57.0.0` at commit `e70658563e38197eebc8e5399b7f0be828c4dab1`

## State

The `gcs` backend is deliberately empty. Bootstrap the state project/bucket separately, then pass reviewed values:

~~~bash
terraform init \
  -backend-config="bucket=CUSTOMER_STATE_BUCKET" \
  -backend-config="prefix=agent-platform/ENVIRONMENT/governed-cell"
~~~

The bucket must have versioning, retention/recovery, restricted IAM, and customer-approved encryption/location controls. This stack must not own the controls that recover its own state.

The state bucket, identity project, initial plan/apply identities, and their first federation binding are bootstrap dependencies. A workflow cannot use federation that the same unapplied stack is expected to create. Provision or approve that bootstrap through the customer's existing landing-zone process, then either import/adopt it here or keep it in a separately owned bootstrap stack.

## Validate without credentials

~~~bash
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
~~~

`terraform init` downloads the pinned provider and Fabric module. CI must run it in an isolated worker with sufficient disk and approved network access.

## Plan

Copy `terraform.tfvars.example` outside source control, replace every placeholder, and run:

~~~bash
terraform plan -input=false -lock-timeout=5m -out=tfplan
terraform show -json tfplan > tfplan.json
python3 policies/validate_plan.py tfplan.json
~~~

Never apply a newly generated plan after approval. Apply the exact approved `tfplan` artifact and retain its digest.

## Existing project and Firestore

The root composition creates a project through Fabric. Customers with an existing project should use Fabric's documented `project_reuse` input or adopt only the `modules/governed-cell` module.

When `create_firestore_database=true` and a default database already exists, import it before planning. Firestore location is not a casual update; align it with the customer residency and recovery decision.

## IAM boundary

The module does not grant organization-wide roles. Plan/apply project roles are explicit variables and reject `roles/owner` and `roles/editor`. Network User is granted at the named subnet, not the entire Shared VPC host project. GitHub plan and apply federation use separate pools; apply also requires the protected ref and an OIDC environment ending in `-apply`.

The Secret Manager resource contains no secret version. Security operations creates and rotates `SUBJECT_HASH_KEY` through the customer-approved process.

## Cross-project Cloud Deploy

The baseline uses the development cell as the Cloud Deploy control project and promotes the same artifact to a separate production cell. In the production stack, set `cloud_deploy_control_plane` to the development project ID/number and its build service account. The module then grants the documented Cloud Deploy Job Runner, release-caller act-as, Cloud Deploy service-agent act-as, and Cloud Build service-agent token-creator relationships.

Google’s cross-project procedure also requires an organization-policy decision allowing cross-project service-account usage in the project that owns the execution identity. This module does not relax that organization policy. The customer foundation owner must approve and scope it; otherwise use a same-project pipeline topology.

Set `artifact_consumers` on the project that owns Artifact Registry. The module grants repository-level Reader to each target's standard deploy identity and Cloud Run service agent, which Google requires when Cloud Run deploys an image from another project.

## Official evidence

- [Cloud Foundation Fabric v57.0.0 project module](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/v57.0.0/modules/project)
- [Artifact Registry Terraform resources](https://docs.cloud.google.com/artifact-registry/docs/repositories/terraform)
- [Enable Artifact Analysis automatic scanning](https://docs.cloud.google.com/artifact-analysis/docs/enable-automatic-scanning)
- [Shared VPC provisioning with Terraform](https://docs.cloud.google.com/vpc/docs/provisioning-shared-vpc)
- [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity)
- [Firestore transactions](https://docs.cloud.google.com/firestore/native/docs/best-practices)
- [Monitoring alert policies with Terraform](https://docs.cloud.google.com/monitoring/alerts/terraform)
- [Workload Identity Federation for deployment pipelines](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines)
- [Service-account practices for deployment pipelines](https://docs.cloud.google.com/iam/docs/best-practices-for-using-service-accounts-in-deployment-pipelines)
- [Cloud Deploy execution service accounts and cross-project requirements](https://docs.cloud.google.com/deploy/docs/cloud-deploy-service-account)
- [Deploy Cloud Run images from another project](https://docs.cloud.google.com/run/docs/deploying#other-projects)
