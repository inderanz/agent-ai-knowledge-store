# Agentic documentation-maintenance operations

## Purpose and authority boundary

The maintainer detects upstream review obligations, uses Google ADK agents and
repository skills to prepare candidate updates, runs an independent agent review,
and opens a draft pull request. It has no authority to merge, approve a customer
risk, change production Google Cloud resources, or write outside its proposal
branch.

## Required GitHub and Google Cloud configuration

Set these repository variables only after creating a dedicated documentation
project and least-privilege Workload Identity Federation binding:

Use the reviewed root stack at
[`terraform/documentation-maintainer`](../../terraform/documentation-maintainer/README.md)
to create that binding and model-invocation identity. It restricts token exchange
to immutable repository and owner IDs, this exact workflow on `main`, and only
scheduled or manually dispatched executions.

| Variable | Purpose |
|---|---|
| `ENABLE_AGENTIC_DOC_PROPOSALS` | Must equal `true` to enable proposal generation |
| `DOC_MAINTAINER_WIF_PROVIDER` | GitHub OIDC workload identity provider |
| `DOC_MAINTAINER_SERVICE_ACCOUNT` | Model-invocation-only service account |
| `DOC_MAINTAINER_PROJECT` | Dedicated project for proposal generation |
| `DOC_MAINTAINER_LOCATION` | Approved Vertex AI location |
| `DOC_MAINTAINER_MODEL` | Explicitly qualified model resource or version |

Do not grant the service account project Editor, repository write, deployment,
customer data, production logging, Secret Manager administration, or service
account impersonation privileges. GitHub's scoped token creates only the proposal
branch and draft PR.

Authorize model processing only after the repository owner has classified the
repository content and approved the selected project, location, model, logging,
retention and provider terms. The read allowlist excludes hidden files and common
credential/configuration surfaces, but it is not a substitute for repository data
classification or secret scanning.

## Normal run

1. `detect-and-validate` validates skills and maintainer policy and builds a
   bounded signal from release drift and overdue semantic reviews.
2. The signal is retained as an artifact even when proposal generation is disabled.
3. When enabled and actionable, the ADK author loads relevant skills, fetches
   allowlisted evidence and stages candidate files outside the checkout.
4. The reviewer independently records `approve-draft` or `reject`.
5. Policy validates source authority, path allowlist, file hashes, risk gates,
   reviewer separation and unresolved findings.
6. Candidate files are copied to a proposal branch; repository gates run; a draft
   PR is opened or updated.
7. Normal path-based CI and human CODEOWNER reviews decide publication.

## Alert and incident conditions

- **No proposal job:** check the actionable signal, enable variable and event mode.
- **Authentication failure:** do not add a key; repair the WIF subject/audience and
  service-account binding.
- **Unsupported source:** add no broad domain; verify the exact official authority
  and update policy through a separately reviewed human PR.
- **Manifest failure:** reject the candidate. Do not manually bypass hashes or path
  protection.
- **Agent loop or cost spike:** cancel the workflow, disable proposals, preserve the
  signal/artifacts and review model/tool traces.
- **Unsafe or irrelevant proposal:** close the PR, retain findings as evaluation
  cases, and improve skills/policy before re-enabling.
- **Unauthorized branch content:** revoke the workflow token permission, disable
  proposals, preserve audit logs, rotate/revoke affected identity bindings and
  follow the repository security process.

## Rollback

Set `ENABLE_AGENTIC_DOC_PROPOSALS=false`. Scheduled detection continues without
model invocation or repository writes. Close the draft PR and delete only its
automation branch through normal repository administration. Revert maintainer
code through a reviewed PR; never weaken `main` protection.

## Service objectives

- Detection completes weekly without credentials for customer systems.
- A proposal changes only manifest-declared paths.
- Every candidate byte matches its recorded SHA-256.
- Every semantic proposal remains Draft until human review.
- No proposal path causes customer cloud mutation.
- Failures retain the signal and evidence needed for diagnosis.
