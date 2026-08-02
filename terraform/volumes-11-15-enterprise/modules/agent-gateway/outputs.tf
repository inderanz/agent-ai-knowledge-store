output "gateway_id" { value = google_network_services_agent_gateway.this.id }
output "gateway_mtls_endpoint" { value = try(google_network_services_agent_gateway.this.agent_gateway_card[0].mtls_endpoint, null) }
output "gateway_root_certificates" { value = try(google_network_services_agent_gateway.this.agent_gateway_card[0].root_certificates, []) }
output "iap_authz_policy_id" { value = google_network_security_authz_policy.iap.id }
output "iap_authz_extension_id" { value = google_network_services_authz_extension.iap.id }
