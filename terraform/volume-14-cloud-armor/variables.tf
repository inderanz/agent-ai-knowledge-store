variable "project_id" {
  description = "Project that owns the Cloud Armor policy."
  type        = string
}

variable "name" {
  description = "Stable security-policy name."
  type        = string
}

variable "description" {
  description = "Owner, purpose and change reference; do not include secrets."
  type        = string
}

variable "source_rules" {
  description = "Reviewed source-CIDR rules. WAF/rate/bot rules require separate exact-feature modules and tests."
  type = map(object({
    action        = string
    priority      = number
    source_ranges = set(string)
    preview       = bool
    description   = string
  }))

  validation {
    condition     = length(distinct([for rule in values(var.source_rules) : rule.priority])) == length(var.source_rules)
    error_message = "Every rule priority must be unique."
  }

  validation {
    condition     = alltrue([for rule in values(var.source_rules) : contains(["allow", "deny(403)", "deny(404)", "deny(502)"], rule.action)])
    error_message = "Source rules support only explicit allow/deny actions."
  }
}

variable "default_action" {
  description = "Explicit default action. Choose from the customer ingress contract."
  type        = string
  validation {
    condition     = contains(["allow", "deny(403)", "deny(404)", "deny(502)"], var.default_action)
    error_message = "default_action must be an explicit supported allow/deny action."
  }
}
