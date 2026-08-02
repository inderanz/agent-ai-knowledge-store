# Volume 2 executable field labs

These labs are safe locally: they do not create cloud resources. Cloud application is a separate customer-authorized activity.

## Lab contract

| Lab | Objective | Prerequisites | Expected time | Cost and region |
|---|---|---|---:|---|
| 1 | Prove deterministic, fail-closed workload admission | Python 3.12 | 10 minutes | no cloud cost; region independent |
| 2 | Prove Terraform syntax and destructive/public-IAM guardrails | Terraform 1.15.8, Python 3.12 | 15 minutes | local checks are free; provider-backed CI needs network only |
| 3 | Render a non-injectable two-target delivery configuration | Python 3.12; customer placeholder values | 15 minutes | no cloud cost; choose only customer-approved target regions |
| 4 | Record current Agent Platform topology and maturity acceptance | Python 3.12; security/privacy/legal/product/operations owners | 30–60 minutes | no local cost; verify product region and commercial eligibility live |
| 5 | Exercise the end-to-end customer sandbox | approved GCP projects, billing, identities, quotas, network, IAP and on-call | 1–2 days | billable Cloud Run, Firestore, Artifact Analysis, logging, build/deploy and selected Agent Platform services |

Use an isolated sandbox and the exact project IDs named in the approved change. The local labs write only to explicit `/tmp` paths shown below. Do not run a cloud apply from a workstation until the saved plan and authority are approved.

## Lab 1 — Prove deterministic admission

~~~bash
python3 -m unittest discover -s examples/python/platform-admission/tests -v
python3 -m compileall -q examples/python/platform-admission/src examples/python/platform-admission/tests examples/python/platform-admission/main.py
~~~

Exit criterion: policy, identity, and idempotency tests pass, and a production request selecting Managed Agents is denied.

## Lab 2 — Prove infrastructure guardrails

~~~bash
terraform fmt -check -recursive terraform/volume-2-platform
python3 -m unittest discover -s terraform/volume-2-platform/policies -v
~~~

In a CI worker with approved network access and disk, also run `terraform init -backend=false` and `terraform validate`. A successful local syntax check is not a successful customer plan.

## Lab 3 — Render a customer delivery pipeline

~~~bash
cp delivery/volume-2-platform/customer.env.example /tmp/customer.env
# Replace every example value in /tmp/customer.env.
python3 delivery/volume-2-platform/render_config.py \
  --environment-file /tmp/customer.env \
  --output /tmp/volume-2-clouddeploy.yaml
python3 delivery/volume-2-platform/validate_delivery.py \
  /tmp/volume-2-clouddeploy.yaml \
  delivery/volume-2-platform/service.yaml \
  delivery/volume-2-platform/cloudbuild.yaml \
  delivery/volume-2-platform/release.yaml
python3 -m unittest discover -s delivery/volume-2-platform -p 'test_*.py' -v
~~~

Exit criterion: no public IAM, unresolved customer token, mutable container tag in the release path, missing ingress boundary, absent Binary Authorization, or missing production approval is accepted. The supply-chain unit tests also prove that pending scanning, missing matching provenance, and High/Critical findings fail closed.

## Lab 4 — Qualify Agent Platform dependencies

Copy `qualification.example.json` to the customer evidence store and replace the example decisions. Then run:

~~~bash
python3 validate_qualification.py /secure/path/customer-qualification.json
~~~

The validator enforces the current same-project and same-region Gateway topology for Runtime agents and refuses Managed Agents in production. It cannot decide contractual acceptance or regional availability; the named customer owners must do that from current official pages.

## Lab 5 — Execute in a customer sandbox

After customer authorization:

1. plan two governed-cell stacks, one development and one production;
2. review the JSON plans with the supplied policy gate;
3. apply only the approved saved plans;
4. create the Secret Manager secret version through the customer's secret process;
5. configure the IAP-protected load balancer and exact JWT audience;
6. apply the rendered Cloud Deploy configuration;
7. deploy to development and execute positive and negative journey tests;
8. test rollback, alerts, Firestore recovery, and incident ownership; and
9. collect evidence before requesting production approval.

The official product procedures are linked in the [implementation evidence ledger](../../references/implementation/volume-2-platform.md).

## Failure injection

- reuse an idempotency key with a different body and expect HTTP 409/domain conflict;
- request an unapproved region or Managed Agents in production and expect denial;
- add `allUsers`, remove production approval, or inject a YAML token and expect the delivery gate to fail;
- feed a pending discovery occurrence, missing build provenance, or High vulnerability into the supply-chain gate and expect failure;
- mismatch Runtime/Gateway/Registry regions or omit Preview acceptance and expect qualification failure; and
- in the authorized sandbox, roll back a revision, revoke the release caller's act-as grant, deny repository access, and exercise Firestore recovery one condition at a time.

## Cleanup

Local cleanup is limited to files created by the commands:

~~~bash
find /tmp -maxdepth 1 -type f -name 'volume-2-clouddeploy.yaml' -delete
find /tmp -maxdepth 1 -type f -name 'customer.env' -delete
~~~

For Lab 5, use the approved Terraform destroy plan only for the exact non-production stack and retain required audit evidence. Do not delete production, a state bucket, a shared network, a folder, or a project through a generic cleanup command.

## Troubleshooting

- a deny-all policy response is expected until a reviewed policy is built into the image;
- a release gate with no discovery occurrence means scanning has not completed or is not enabled—never interpret it as zero vulnerabilities;
- a cross-project deploy failure commonly indicates missing Cloud Deploy/Cloud Build service-agent impersonation, repository Reader, Cloud Run service-agent access, or the cross-project service-account organization-policy decision;
- an IAP denial commonly indicates the wrong backend-service audience or an unsigned header; and
- Terraform provider/module errors must be resolved in the pinned CI environment before interpreting a plan.
