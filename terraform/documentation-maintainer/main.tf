locals {
  required_services = toset([
    "aiplatform.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "serviceusage.googleapis.com",
    "sts.googleapis.com",
  ])

  repository_principal = "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github.workload_identity_pool_id}/attribute.repository_id/${var.repository_id}"
}

resource "google_project_service" "required" {
  for_each = local.required_services

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_service_account" "maintainer" {
  project      = var.project_id
  account_id   = var.service_account_id
  display_name = "FDE documentation maintainer"
  description  = "Keyless identity restricted to bounded Vertex AI model invocation from the approved GitHub workflow."

  depends_on = [google_project_service.required]
}

resource "google_project_iam_custom_role" "model_invoker" {
  project     = var.project_id
  role_id     = "fdeDocumentationModelInvoker"
  title       = "FDE documentation model invoker"
  description = "Minimum project permissions for Vertex AI inference from the documentation maintainer."
  permissions = [
    "aiplatform.endpoints.predict",
    "serviceusage.services.use",
  ]

  depends_on = [google_project_service.required]
}

resource "google_project_iam_member" "model_invoker" {
  project = var.project_id
  role    = google_project_iam_custom_role.model_invoker.name
  member  = "serviceAccount:${google_service_account.maintainer.email}"
}

resource "google_iam_workload_identity_pool" "github" {
  project                   = var.project_id
  workload_identity_pool_id = var.workload_identity_pool_id
  display_name              = "FDE docs GitHub"
  description               = "OIDC trust dedicated to the FDE documentation maintainer."

  depends_on = [google_project_service.required]
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = var.workload_identity_provider_id
  display_name                       = "FDE docs workflow"

  attribute_mapping = {
    "google.subject"                = "assertion.sub"
    "attribute.repository"          = "assertion.repository"
    "attribute.repository_id"       = "assertion.repository_id"
    "attribute.repository_owner_id" = "assertion.repository_owner_id"
    "attribute.workflow_ref"        = "assertion.workflow_ref"
    "attribute.ref"                 = "assertion.ref"
    "attribute.event_name"          = "assertion.event_name"
  }

  attribute_condition = join(" && ", [
    "attribute.repository == '${var.repository}'",
    "attribute.repository_id == '${var.repository_id}'",
    "attribute.repository_owner_id == '${var.repository_owner_id}'",
    "attribute.workflow_ref == '${var.workflow_ref}'",
    "attribute.ref == 'refs/heads/main'",
    "(attribute.event_name == 'schedule' || attribute.event_name == 'workflow_dispatch')",
  ])

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com/"
  }
}

resource "google_service_account_iam_member" "github" {
  service_account_id = google_service_account.maintainer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = local.repository_principal
}
