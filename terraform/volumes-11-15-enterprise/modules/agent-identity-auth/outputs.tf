output "auth_providers" {
  description = "Non-secret auth-provider identifiers and runtime metadata."
  value = {
    for key, provider in google_agent_identity_auth_provider.this : key => {
      id    = provider.id
      name  = provider.name
      state = provider.state
    }
  }
}

output "three_legged_oauth_redirect_urls" {
  description = "Register these deterministic callback URLs with the upstream OAuth providers."
  value = {
    for key, provider in google_agent_identity_auth_provider.this :
    key => try(provider.auth_provider_type_params[0].three_legged_oauth[0].redirect_url, null)
    if var.auth_providers[key].mode == "THREE_LEGGED_OAUTH"
  }
}
