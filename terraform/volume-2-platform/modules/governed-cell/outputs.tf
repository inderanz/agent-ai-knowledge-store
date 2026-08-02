output "artifact_repository" {
  value = google_artifact_registry_repository.containers.name
}

output "runtime_service_account" {
  value = google_service_account.identity["runtime"].email
}

output "runtime_identity_member" {
  value = google_service_account.identity["runtime"].member
}

output "build_service_account" {
  value = google_service_account.identity["build"].email
}

output "deploy_service_account" {
  value = google_service_account.identity["deploy"].email
}

output "plan_service_account" {
  value = google_service_account.identity["plan"].email
}

output "apply_service_account" {
  value = google_service_account.identity["apply"].email
}

output "subject_hash_secret" {
  value = google_secret_manager_secret.subject_hash.id
}
