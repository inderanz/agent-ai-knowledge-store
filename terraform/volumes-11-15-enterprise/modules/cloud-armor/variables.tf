variable "project_id" { type = string }
variable "name" { type = string }
variable "description" { type = string }
variable "labels" { type = map(string) }

variable "default_rule_action" {
  type        = string
  description = "Explicit lowest-priority action. Default-deny is the enterprise baseline."
  default     = "deny(403)"
  validation {
    condition     = contains(["allow", "deny(403)", "deny(404)", "deny(502)"], var.default_rule_action)
    error_message = "Use a Cloud Armor supported explicit default action."
  }
}

variable "preconfigured_waf_rules" {
  description = "Google preconfigured WAF rules. Begin in preview and graduate using enforcement_approved."
  type = map(object({
    action                  = string
    priority                = number
    description             = string
    preview                 = optional(bool, true)
    target_rule_set         = string
    sensitivity_level       = optional(number, 2)
    include_target_rule_ids = optional(list(string), [])
    exclude_target_rule_ids = optional(list(string), [])
  }))
  default = {}
}

variable "source_rules" {
  type = map(object({
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
  }))
  default = {}
}

variable "custom_cel_rules" {
  type = map(object({
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
  }))
  default = {}
}

variable "threat_intelligence_rules" {
  description = "Cloud Armor Threat Intelligence feeds; Managed Protection Plus may be required."
  type = map(object({
    action      = string
    priority    = number
    description = string
    preview     = optional(bool, true)
    feed        = string
    exclude_ip  = optional(string)
  }))
  default = {}
}

variable "enforcement_approved" {
  type        = bool
  description = "Explicit production change approval gate for any non-preview rule."
  default     = false
}

variable "layer_7_ddos_defense_enable" {
  type    = bool
  default = true
}

variable "json_parsing" {
  type    = string
  default = "STANDARD"
  validation {
    condition     = contains(["DISABLED", "STANDARD"], var.json_parsing)
    error_message = "json_parsing must be DISABLED or STANDARD."
  }
}

variable "request_body_inspection_size" {
  type    = string
  default = "16KB"
}
