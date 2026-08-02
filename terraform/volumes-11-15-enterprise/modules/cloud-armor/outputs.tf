output "policy" {
  description = "Cloud Armor policy object; attach policy.self_link in the load-balancer owner stack."
  value       = module.cloud_armor.policy
}

output "backend_attachment_required" {
  value       = true
  description = "A policy without a backend-service attachment does not protect traffic."
}
