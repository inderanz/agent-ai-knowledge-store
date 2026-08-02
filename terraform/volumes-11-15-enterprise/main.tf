locals {
  required_services = toset([
    "agentidentity.googleapis.com",
    "agentregistry.googleapis.com",
    "compute.googleapis.com",
    "discoveryengine.googleapis.com",
    "iap.googleapis.com",
    "networksecurity.googleapis.com",
    "networkservices.googleapis.com",
    "serviceextensions.googleapis.com",
    "storage.googleapis.com",
  ])

  registry_uri = "//agentregistry.googleapis.com/projects/${var.project_id}/locations/${var.agent_location}"
}

resource "google_project_service" "required" {
  for_each = local.required_services

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

module "agent_identity_auth" {
  source = "./modules/agent-identity-auth"

  project_id             = var.project_id
  location               = var.agent_location
  manage_project_service = false
  auth_providers         = var.identity_providers
  oauth_client_secrets   = var.oauth_client_secrets

  depends_on = [google_project_service.required]
}

module "agent_registry" {
  source = "./modules/agent-registry"

  project_id             = var.project_id
  location               = var.agent_location
  manage_project_service = false
  deletion_policy        = "PREVENT"
  services               = var.registry_services
  bindings               = var.registry_bindings

  depends_on = [module.agent_identity_auth]
}

module "agent_gateway" {
  source = "./modules/agent-gateway"

  project_id              = var.project_id
  location                = var.agent_location
  name                    = var.gateway.name
  description             = var.gateway.description
  labels                  = var.labels
  governed_access_path    = var.gateway.governed_access_path
  iam_enforcement_mode    = var.gateway.iam_enforcement_mode
  registries              = [local.registry_uri]
  network_config          = var.gateway.network_config
  manage_project_services = false
  deletion_policy         = "PREVENT"
  mcp_egress_grants       = var.gateway.mcp_egress_grants
  agent_egress_grants     = var.gateway.agent_egress_grants
  endpoint_egress_grants  = var.gateway.endpoint_egress_grants

  depends_on = [module.agent_registry]
}

module "cloud_armor" {
  source = "./modules/cloud-armor"

  project_id                   = var.project_id
  name                         = var.cloud_armor.name
  description                  = var.cloud_armor.description
  labels                       = var.labels
  default_rule_action          = var.cloud_armor.default_rule_action
  preconfigured_waf_rules      = var.cloud_armor.preconfigured_waf_rules
  source_rules                 = var.cloud_armor.source_rules
  custom_cel_rules             = var.cloud_armor.custom_cel_rules
  threat_intelligence_rules    = var.cloud_armor.threat_intelligence_rules
  enforcement_approved         = var.cloud_armor.enforcement_approved
  layer_7_ddos_defense_enable  = var.cloud_armor.layer_7_ddos_defense_enable
  json_parsing                 = var.cloud_armor.json_parsing
  request_body_inspection_size = var.cloud_armor.request_body_inspection_size

  depends_on = [google_project_service.required]
}

module "gemini_enterprise" {
  source = "./modules/gemini-enterprise-app"

  project_id             = var.project_id
  location               = var.gemini_enterprise.location
  collection_id          = var.gemini_enterprise.collection_id
  engine_id              = var.gemini_enterprise.engine_id
  display_name           = var.gemini_enterprise.display_name
  company_name           = var.gemini_enterprise.company_name
  manage_project_service = false
  deletion_policy        = "PREVENT"
  data_stores            = var.gemini_enterprise.data_stores
  subscription_tier      = var.gemini_enterprise.subscription_tier
  features               = var.gemini_enterprise.features
  app_users              = var.gemini_enterprise.app_users
  cmek                   = var.gemini_enterprise.cmek
  acl_config             = var.gemini_enterprise.acl_config

  depends_on = [google_project_service.required]
}
