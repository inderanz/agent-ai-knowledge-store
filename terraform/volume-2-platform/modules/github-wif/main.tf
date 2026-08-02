locals {
  modes = {
    plan = {
      condition = "assertion.repository_id == \"${var.repository_id}\""
    }
    apply = {
      condition = "assertion.repository_id == \"${var.repository_id}\" && assertion.ref == \"${var.apply_ref}\" && assertion.environment.endsWith(\"${var.apply_environment_suffix}\")"
    }
  }
}

resource "google_iam_workload_identity_pool" "github" {
  for_each = local.modes

  project                   = var.identity_project_id
  workload_identity_pool_id = "${var.pool_id}-${each.key}"
  display_name              = "Agent platform GitHub ${each.key}"
  description               = "OIDC trust for the ${each.key} identity, restricted by immutable repository ID."
}

resource "google_iam_workload_identity_pool_provider" "github" {
  for_each = local.modes

  project                            = var.identity_project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github[each.key].workload_identity_pool_id
  workload_identity_pool_provider_id = "${var.provider_id}-${each.key}"
  display_name                       = "GitHub Actions ${each.key}"

  attribute_mapping = merge(
    {
      "google.subject"          = "assertion.sub"
      "attribute.repository_id" = "assertion.repository_id"
      "attribute.ref"           = "assertion.ref"
    },
    each.key == "apply" ? { "attribute.environment" = "assertion.environment" } : {}
  )

  attribute_condition = each.value.condition

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com/"
  }
}

locals {
  repository_principals = {
    for mode, pool in google_iam_workload_identity_pool.github :
    mode => "principalSet://iam.googleapis.com/projects/${var.identity_project_number}/locations/global/workloadIdentityPools/${pool.workload_identity_pool_id}/attribute.repository_id/${var.repository_id}"
  }
}

resource "google_service_account_iam_member" "plan" {
  service_account_id = "projects/-/serviceAccounts/${var.plan_service_account}"
  role               = "roles/iam.workloadIdentityUser"
  member             = local.repository_principals["plan"]
}

resource "google_service_account_iam_member" "apply" {
  service_account_id = "projects/-/serviceAccounts/${var.apply_service_account}"
  role               = "roles/iam.workloadIdentityUser"
  member             = local.repository_principals["apply"]
}
