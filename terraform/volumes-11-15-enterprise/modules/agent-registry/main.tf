resource "google_project_service" "agent_registry" {
  count = var.manage_project_service ? 1 : 0

  project            = var.project_id
  service            = "agentregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_agent_registry_service" "this" {
  for_each = var.services

  project         = var.project_id
  location        = var.location
  service_id      = each.key
  display_name    = each.value.display_name
  description     = each.value.description
  deletion_policy = coalesce(each.value.deletion_policy, var.deletion_policy)

  dynamic "interfaces" {
    for_each = each.value.interfaces
    content {
      url              = interfaces.value.url
      protocol_binding = interfaces.value.protocol_binding
    }
  }

  dynamic "agent_spec" {
    for_each = each.value.kind == "AGENT" ? [each.value] : []
    content {
      type    = agent_spec.value.spec_type
      content = agent_spec.value.spec_content
    }
  }

  dynamic "mcp_server_spec" {
    for_each = each.value.kind == "MCP_SERVER" ? [each.value] : []
    content {
      type    = mcp_server_spec.value.spec_type
      content = mcp_server_spec.value.spec_content
    }
  }

  dynamic "endpoint_spec" {
    for_each = each.value.kind == "ENDPOINT" ? [each.value] : []
    content {
      type = endpoint_spec.value.spec_type
    }
  }

  lifecycle {
    precondition {
      condition     = length(each.value.interfaces) > 0
      error_message = "A Registry service needs at least one qualified interface."
    }
    precondition {
      condition = (
        (each.value.kind == "AGENT" && contains(["NO_SPEC", "A2A_AGENT_CARD"], each.value.spec_type)) ||
        (each.value.kind == "MCP_SERVER" && contains(["NO_SPEC", "TOOL_SPEC"], each.value.spec_type)) ||
        (each.value.kind == "ENDPOINT" && each.value.spec_type == "NO_SPEC")
      )
      error_message = "spec_type is incompatible with the selected Registry service kind."
    }
    precondition {
      condition     = each.value.kind != "ENDPOINT" || !contains(["us", "eu"], var.location)
      error_message = "Agent Registry endpoints are not supported in us/eu multi-regions; choose a supported region or global."
    }
  }

  depends_on = [google_project_service.agent_registry]
}

resource "google_agent_registry_binding" "this" {
  for_each = var.bindings

  project         = var.project_id
  location        = var.location
  binding_id      = each.key
  display_name    = each.value.display_name
  description     = each.value.description
  deletion_policy = coalesce(each.value.deletion_policy, var.deletion_policy)

  source {
    identifier = each.value.source_urn
  }
  target {
    identifier = each.value.target_urn
  }
  auth_provider_binding {
    auth_provider = each.value.auth_provider
    scopes        = each.value.scopes
    continue_uri  = each.value.continue_uri
  }

  lifecycle {
    precondition {
      condition     = !contains(["us", "eu"], var.location)
      error_message = "Agent Registry bindings are not supported in us/eu multi-regions."
    }
  }

  depends_on = [google_project_service.agent_registry]
}
