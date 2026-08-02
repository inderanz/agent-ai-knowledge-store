locals {
  priorities = concat(
    [for rule in values(var.preconfigured_waf_rules) : rule.priority],
    [for rule in values(var.source_rules) : rule.priority],
    [for rule in values(var.custom_cel_rules) : rule.priority],
    [for rule in values(var.threat_intelligence_rules) : rule.priority],
  )
  has_enforced_rule = anytrue(concat(
    [for rule in values(var.preconfigured_waf_rules) : !rule.preview],
    [for rule in values(var.source_rules) : !rule.preview],
    [for rule in values(var.custom_cel_rules) : !rule.preview],
    [for rule in values(var.threat_intelligence_rules) : !rule.preview],
  ))
}

resource "terraform_data" "policy_gate" {
  input = {
    enforcement_approved = var.enforcement_approved
    priorities           = local.priorities
  }

  lifecycle {
    precondition {
      condition     = length(local.priorities) == length(distinct(local.priorities))
      error_message = "Cloud Armor rule priorities must be unique across every rule class."
    }
    precondition {
      condition     = !local.has_enforced_rule || var.enforcement_approved
      error_message = "Set enforcement_approved only after preview-log analysis, false-positive review, and a recorded production change approval."
    }
  }
}

module "cloud_armor" {
  source  = "GoogleCloudPlatform/cloud-armor/google"
  version = "8.1.1"

  project_id                           = var.project_id
  name                                 = var.name
  description                          = var.description
  labels                               = var.labels
  default_rule_action                  = var.default_rule_action
  type                                 = "CLOUD_ARMOR"
  pre_configured_rules                 = var.preconfigured_waf_rules
  security_rules                       = var.source_rules
  custom_rules                         = var.custom_cel_rules
  threat_intelligence_rules            = var.threat_intelligence_rules
  layer_7_ddos_defense_enable          = var.layer_7_ddos_defense_enable
  layer_7_ddos_defense_rule_visibility = "STANDARD"
  adaptive_protection_auto_deploy      = { enable = false }
  json_parsing                         = var.json_parsing
  log_level                            = "NORMAL"
  request_body_inspection_size         = var.request_body_inspection_size

  depends_on = [terraform_data.policy_gate]
}
