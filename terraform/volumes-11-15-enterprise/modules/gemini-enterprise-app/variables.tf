variable "project_id" { type = string }

variable "location" {
  type    = string
  default = "global"
  validation {
    condition     = contains(["global", "us", "eu"], var.location)
    error_message = "Gemini Enterprise supports global, us, or eu."
  }
}

variable "collection_id" {
  type    = string
  default = "default_collection"
}

variable "engine_id" { type = string }
variable "display_name" { type = string }
variable "company_name" { type = string }

variable "manage_project_service" {
  type    = bool
  default = true
}

variable "deletion_policy" {
  type    = string
  default = "PREVENT"
  validation {
    condition     = var.deletion_policy == "PREVENT"
    error_message = "Enterprise applications and data stores must use deletion_policy PREVENT."
  }
}

variable "data_stores" {
  description = "A single enterprise content datastore for the current Terraform search-engine API contract."
  type = map(object({
    display_name      = string
    content_config    = optional(string, "CONTENT_REQUIRED")
    industry_vertical = optional(string, "GENERIC")
  }))
  validation {
    condition     = length(var.data_stores) == 1
    error_message = "google_discovery_engine_search_engine currently supports at most one datastore for SOLUTION_TYPE_SEARCH."
  }
  validation {
    condition     = alltrue([for ds in values(var.data_stores) : contains(["CONTENT_REQUIRED", "NO_CONTENT"], ds.content_config)])
    error_message = "Gemini Enterprise app datastores cannot use PUBLIC_WEBSITE content configuration."
  }
}

variable "subscription_tier" {
  type    = string
  default = "SUBSCRIPTION_TIER_ENTERPRISE"
}

variable "features" {
  type    = map(string)
  default = {}
}

variable "app_users" {
  type        = set(string)
  description = "Users or groups granted roles/discoveryengine.agentspaceUser on this app only."
  validation {
    condition     = length(var.app_users) > 0 && alltrue([for member in var.app_users : can(regex("^(user|group):", member))])
    error_message = "Provide at least one explicit user: or group: principal; do not use allUsers or project-wide grants."
  }
}

variable "cmek" {
  description = "Optional multi-region CMEK registration. Supported only for us/eu, not global."
  type = object({
    cmek_config_id     = optional(string, "default_cmek_config")
    kms_key            = string
    single_region_keys = optional(list(string), [])
  })
  default = null
}

variable "acl_config" {
  description = "Optional document-level ACL identity provider."
  type = object({
    idp_type            = string
    workforce_pool_name = optional(string)
  })
  default = null
  validation {
    condition     = var.acl_config == null || contains(["GSUITE", "THIRD_PARTY"], var.acl_config.idp_type)
    error_message = "idp_type must be GSUITE or THIRD_PARTY."
  }
}
