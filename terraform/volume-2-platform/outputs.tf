output "project_id" {
  description = "Governed-cell project ID."
  value       = module.project.id
}

output "project_number" {
  description = "Governed-cell project number."
  value       = module.project.number
}

output "artifact_repository" {
  description = "Regional immutable Docker repository."
  value       = module.governed_cell.artifact_repository
}

output "runtime_service_account" {
  description = "Cloud Run service identity."
  value       = module.governed_cell.runtime_service_account
}

output "build_service_account" {
  description = "Cloud Build user-specified service account."
  value       = module.governed_cell.build_service_account
}

output "deploy_service_account" {
  description = "Cloud Deploy execution service account."
  value       = module.governed_cell.deploy_service_account
}

output "terraform_plan_service_account" {
  description = "Federatable Terraform plan identity."
  value       = module.governed_cell.plan_service_account
}

output "terraform_apply_service_account" {
  description = "Separately federatable Terraform apply identity."
  value       = module.governed_cell.apply_service_account
}

output "subject_hash_secret" {
  description = "Secret resource awaiting customer-managed secret versions."
  value       = module.governed_cell.subject_hash_secret
}

output "workload_identity_provider" {
  description = "GitHub WIF provider and restricted principal when enabled."
  value       = var.github_wif.enabled ? module.github_wif[0].provider : null
}

