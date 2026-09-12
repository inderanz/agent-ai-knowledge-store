output "workload_identity_provider" {
  description = "Set as DOC_MAINTAINER_WIF_PROVIDER."
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "service_account" {
  description = "Set as DOC_MAINTAINER_SERVICE_ACCOUNT."
  value       = google_service_account.maintainer.email
}

output "project_id" {
  description = "Set as DOC_MAINTAINER_PROJECT."
  value       = var.project_id
}

output "region" {
  description = "Set as DOC_MAINTAINER_LOCATION."
  value       = var.region
}
