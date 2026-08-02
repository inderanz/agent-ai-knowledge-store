output "service_names" {
  description = "Writable Service resource names keyed by service ID."
  value       = { for key, service in google_agent_registry_service.this : key => service.name }
}

output "registry_resources" {
  description = "Resulting read-only Agent/MCP Server/Endpoint resource names."
  value       = { for key, service in google_agent_registry_service.this : key => service.registry_resource }
}

output "binding_names" {
  description = "Binding resource names keyed by binding ID."
  value       = { for key, binding in google_agent_registry_binding.this : key => binding.name }
}
