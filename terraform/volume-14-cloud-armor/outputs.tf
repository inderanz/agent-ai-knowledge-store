output "security_policy_id" {
  description = "Policy ID to attach explicitly to the intended backend service."
  value       = google_compute_security_policy.this.id
}

output "security_policy_self_link" {
  description = "Policy self link for attachment and post-deploy verification."
  value       = google_compute_security_policy.this.self_link
}
