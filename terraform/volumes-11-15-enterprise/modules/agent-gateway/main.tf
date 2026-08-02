locals {
  services = toset([
    "agentregistry.googleapis.com",
    "iap.googleapis.com",
    "networksecurity.googleapis.com",
    "networkservices.googleapis.com",
    "serviceextensions.googleapis.com",
  ])
}

resource "google_project_service" "required" {
  for_each = var.manage_project_services ? local.services : toset([])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_network_services_agent_gateway" "this" {
  project         = var.project_id
  location        = var.location
  name            = var.name
  description     = var.description
  labels          = var.labels
  registries      = var.registries
  deletion_policy = var.deletion_policy

  google_managed {
    governed_access_path = var.governed_access_path
  }

  dynamic "network_config" {
    for_each = var.network_config == null ? [] : [var.network_config]
    content {
      egress {
        network_attachment = network_config.value.network_attachment
      }
      dynamic "dns_peering_config" {
        for_each = network_config.value.dns == null ? [] : [network_config.value.dns]
        content {
          domains        = dns_peering_config.value.domains
          target_project = dns_peering_config.value.target_project
          target_network = dns_peering_config.value.target_network
        }
      }
    }
  }

  lifecycle {
    precondition {
      condition     = var.network_config == null || alltrue([for domain in var.network_config.dns == null ? [] : var.network_config.dns.domains : endswith(domain, ".")])
      error_message = "Every DNS peering domain must be a fully qualified name ending with a dot."
    }
  }

  depends_on = [google_project_service.required]
}

resource "google_network_services_authz_extension" "iap" {
  project     = var.project_id
  location    = var.location
  name        = "${var.name}-iap"
  description = "Fail-closed IAP request authorization for ${var.name}."
  service     = "iap.googleapis.com"
  timeout     = var.iap_extension_timeout
  fail_open   = var.iam_enforcement_mode == "DRY_RUN"
  labels      = var.labels
  metadata = merge(
    { iapPolicyVersion = "V1" },
    var.iam_enforcement_mode == "DRY_RUN" ? { iamEnforcementMode = "DRY_RUN" } : {},
  )
  deletion_policy = var.deletion_policy

  depends_on = [google_project_service.required]
}

resource "google_network_security_authz_policy" "iap" {
  project         = var.project_id
  location        = var.location
  name            = "${var.name}-iap"
  description     = "IAP request authorization attached to Agent Gateway ${var.name}."
  action          = "CUSTOM"
  policy_profile  = "REQUEST_AUTHZ"
  labels          = var.labels
  deletion_policy = var.deletion_policy

  target {
    resources = [google_network_services_agent_gateway.this.id]
  }
  custom_provider {
    authz_extension {
      resources = [google_network_services_authz_extension.iap.id]
    }
  }
}

resource "google_iap_agent_registry_mcp_server_iam_member" "egress" {
  for_each = var.mcp_egress_grants

  project       = var.project_id
  location      = var.location
  mcp_server_id = each.value.mcp_server_id
  role          = "roles/iap.egressor"
  member        = each.value.agent_principal

  condition {
    title       = each.value.condition_title
    description = each.value.condition_description
    expression  = each.value.condition_expression
  }
}

resource "google_iap_agent_registry_agent_iam_member" "egress" {
  for_each = var.agent_egress_grants

  project  = var.project_id
  location = var.location
  agent_id = each.value.agent_id
  role     = "roles/iap.egressor"
  member   = each.value.source_principal

  condition {
    title       = each.value.condition_title
    description = each.value.condition_description
    expression  = each.value.condition_expression
  }
}

resource "google_iap_agent_registry_endpoint_iam_member" "egress" {
  for_each = var.endpoint_egress_grants

  project     = var.project_id
  location    = var.location
  endpoint_id = each.value.endpoint_id
  role        = "roles/iap.egressor"
  member      = each.value.agent_principal

  condition {
    title       = each.value.condition_title
    description = each.value.condition_description
    expression  = each.value.condition_expression
  }
}
