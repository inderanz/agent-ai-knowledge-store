resource "google_project_service" "agent_identity" {
  count = var.manage_project_service ? 1 : 0

  project            = var.project_id
  service            = "agentidentity.googleapis.com"
  disable_on_destroy = false
}

resource "google_agent_identity_auth_provider" "this" {
  for_each = var.auth_providers

  project          = var.project_id
  location         = var.location
  auth_provider_id = each.key
  description      = each.value.description
  labels           = each.value.labels
  workload_ids     = sort(tolist(each.value.workload_ids))
  allowed_scopes   = sort(tolist(each.value.allowed_scopes))
  blocked_scopes   = sort(tolist(each.value.blocked_scopes))
  deletion_policy  = each.value.deletion_policy

  auth_provider_type_params {
    dynamic "three_legged_oauth" {
      for_each = each.value.mode == "THREE_LEGGED_OAUTH" ? [each.value] : []
      content {
        client_id                = three_legged_oauth.value.client_id
        client_secret_wo         = lookup(var.oauth_client_secrets, each.key, null)
        client_secret_wo_version = three_legged_oauth.value.client_secret_version
        authorization_url        = three_legged_oauth.value.authorization_url
        token_url                = three_legged_oauth.value.token_url
        default_continue_uri     = three_legged_oauth.value.default_continue_uri
        enable_pkce              = three_legged_oauth.value.enable_pkce
      }
    }

    dynamic "two_legged_oauth" {
      for_each = each.value.mode == "TWO_LEGGED_OAUTH" ? [each.value] : []
      content {
        client_id                = two_legged_oauth.value.client_id
        client_secret_wo         = lookup(var.oauth_client_secrets, each.key, null)
        client_secret_wo_version = two_legged_oauth.value.client_secret_version
        token_url                = two_legged_oauth.value.token_url
      }
    }
  }

  lifecycle {
    precondition {
      condition     = contains(keys(var.oauth_client_secrets), each.key)
      error_message = "oauth_client_secrets must contain an apply-time secret for every auth provider."
    }
    precondition {
      condition     = each.value.mode != "THREE_LEGGED_OAUTH" || (each.value.authorization_url != null && each.value.enable_pkce)
      error_message = "Three-legged OAuth requires authorization_url and PKCE enabled in this enterprise module."
    }
  }

  depends_on = [google_project_service.agent_identity]
}
