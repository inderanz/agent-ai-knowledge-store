output "agent_registry_services" { value = module.agent_registry.service_names }
output "agent_gateway" {
  value = {
    id            = module.agent_gateway.gateway_id
    mtls_endpoint = module.agent_gateway.gateway_mtls_endpoint
  }
}
output "identity_auth_providers" { value = module.agent_identity_auth.auth_providers }
output "cloud_armor_policy" { value = module.cloud_armor.policy }
output "gemini_enterprise_engine" { value = module.gemini_enterprise.engine }

output "mandatory_handoffs" {
  value = {
    cloud_armor_backend_attachment = module.cloud_armor.backend_attachment_required
    gemini_observability           = module.gemini_enterprise.observability_handoff_required
  }
}
