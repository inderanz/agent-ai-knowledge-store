variable "project_id" { type = string }
variable "agent_location" { type = string }

variable "labels" {
  type = map(string)
  validation {
    condition     = alltrue([for key in ["environment", "owner", "data-classification", "cost-centre"] : contains(keys(var.labels), key)])
    error_message = "labels must include environment, owner, data-classification, and cost-centre."
  }
}

variable "registry_services" {
  type = map(object({
    kind         = string
    display_name = string
    description  = string
    interfaces = list(object({
      url              = string
      protocol_binding = string
    }))
    spec_type       = string
    spec_content    = optional(string)
    deletion_policy = optional(string)
  }))
  default = {}
}

variable "registry_bindings" {
  type = map(object({
    display_name    = string
    description     = string
    source_urn      = string
    target_urn      = string
    auth_provider   = string
    scopes          = optional(list(string), [])
    continue_uri    = optional(string)
    deletion_policy = optional(string)
  }))
  default = {}
}

variable "gateway" {
  type = object({
    name                 = string
    description          = string
    governed_access_path = string
    iam_enforcement_mode = optional(string, "ENFORCED")
    network_config = optional(object({
      network_attachment = string
      dns = optional(object({
        domains        = list(string)
        target_project = string
        target_network = string
      }))
    }))
    mcp_egress_grants = optional(map(object({
      mcp_server_id         = string
      agent_principal       = string
      condition_title       = string
      condition_expression  = string
      condition_description = optional(string)
    })), {})
    agent_egress_grants = optional(map(object({
      agent_id              = string
      source_principal      = string
      condition_title       = string
      condition_expression  = string
      condition_description = optional(string)
    })), {})
    endpoint_egress_grants = optional(map(object({
      endpoint_id           = string
      agent_principal       = string
      condition_title       = string
      condition_expression  = string
      condition_description = optional(string)
    })), {})
  })
}

variable "identity_providers" {
  type = map(object({
    mode                  = string
    description           = optional(string)
    labels                = optional(map(string), {})
    workload_ids          = set(string)
    allowed_scopes        = set(string)
    blocked_scopes        = optional(set(string), [])
    client_id             = string
    authorization_url     = optional(string)
    token_url             = string
    default_continue_uri  = optional(string)
    enable_pkce           = optional(bool, true)
    client_secret_version = string
    deletion_policy       = optional(string, "PREVENT")
  }))
  default = {}
}

variable "oauth_client_secrets" {
  type        = map(string)
  sensitive   = true
  ephemeral   = true
  default     = {}
  description = "Apply-time OAuth secrets. Do not put these in tfvars or state."
}

variable "cloud_armor" {
  type = object({
    name                = string
    description         = string
    default_rule_action = optional(string, "deny(403)")
    preconfigured_waf_rules = optional(map(object({
      action                  = string
      priority                = number
      description             = string
      preview                 = optional(bool, true)
      target_rule_set         = string
      sensitivity_level       = optional(number, 2)
      include_target_rule_ids = optional(list(string), [])
      exclude_target_rule_ids = optional(list(string), [])
    })), {})
    source_rules = optional(map(object({
      action        = string
      priority      = number
      description   = string
      preview       = optional(bool, true)
      src_ip_ranges = list(string)
      rate_limit_options = optional(object({
        enforce_on_key                       = optional(string)
        enforce_on_key_name                  = optional(string)
        exceed_action                        = optional(string)
        rate_limit_http_request_count        = optional(number)
        rate_limit_http_request_interval_sec = optional(number)
        ban_duration_sec                     = optional(number)
        ban_http_request_count               = optional(number)
        ban_http_request_interval_sec        = optional(number)
      }), {})
    })), {})
    custom_cel_rules = optional(map(object({
      action      = string
      priority    = number
      description = string
      preview     = optional(bool, true)
      expression  = string
      rate_limit_options = optional(object({
        enforce_on_key                       = optional(string)
        enforce_on_key_name                  = optional(string)
        exceed_action                        = optional(string)
        rate_limit_http_request_count        = optional(number)
        rate_limit_http_request_interval_sec = optional(number)
        ban_duration_sec                     = optional(number)
        ban_http_request_count               = optional(number)
        ban_http_request_interval_sec        = optional(number)
      }), {})
    })), {})
    threat_intelligence_rules = optional(map(object({
      action      = string
      priority    = number
      description = string
      preview     = optional(bool, true)
      feed        = string
      exclude_ip  = optional(string)
    })), {})
    enforcement_approved         = optional(bool, false)
    layer_7_ddos_defense_enable  = optional(bool, true)
    json_parsing                 = optional(string, "STANDARD")
    request_body_inspection_size = optional(string, "16KB")
  })
}

variable "gemini_enterprise" {
  type = object({
    location      = optional(string, "global")
    collection_id = optional(string, "default_collection")
    engine_id     = string
    display_name  = string
    company_name  = string
    data_stores = map(object({
      display_name      = string
      content_config    = optional(string, "CONTENT_REQUIRED")
      industry_vertical = optional(string, "GENERIC")
    }))
    subscription_tier = optional(string, "SUBSCRIPTION_TIER_ENTERPRISE")
    features          = optional(map(string), {})
    app_users         = set(string)
    cmek = optional(object({
      cmek_config_id     = optional(string, "default_cmek_config")
      kms_key            = string
      single_region_keys = optional(list(string), [])
    }))
    acl_config = optional(object({
      idp_type            = string
      workforce_pool_name = optional(string)
    }))
  })
}
