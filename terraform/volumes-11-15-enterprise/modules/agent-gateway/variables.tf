variable "project_id" { type = string }
variable "location" { type = string }
variable "name" { type = string }
variable "description" { type = string }
variable "labels" { type = map(string) }

variable "governed_access_path" {
  description = "AGENT_TO_ANYWHERE or CLIENT_TO_AGENT. Gemini Enterprise supports egress, not Client-to-Agent Gateway mode."
  type        = string
  validation {
    condition     = contains(["AGENT_TO_ANYWHERE", "CLIENT_TO_AGENT"], var.governed_access_path)
    error_message = "governed_access_path must be AGENT_TO_ANYWHERE or CLIENT_TO_AGENT."
  }
}

variable "registries" {
  description = "Project-scoped Registry URIs governed by this Gateway."
  type        = list(string)
  validation {
    condition     = length(var.registries) > 0 && alltrue([for value in var.registries : startswith(value, "//agentregistry.googleapis.com/projects/")])
    error_message = "At least one project-scoped //agentregistry.googleapis.com/projects/... Registry URI is required."
  }
}

variable "network_config" {
  description = "Optional PSC-interface attachment and optional private DNS peering for private VPC destinations."
  type = object({
    network_attachment = string
    dns = optional(object({
      domains        = list(string)
      target_project = string
      target_network = string
    }))
  })
  default = null
}

variable "manage_project_services" {
  type    = bool
  default = true
}

variable "deletion_policy" {
  type    = string
  default = "PREVENT"
  validation {
    condition     = contains(["PREVENT", "ABANDON", "DELETE"], var.deletion_policy)
    error_message = "deletion_policy must be PREVENT, ABANDON, or DELETE."
  }
}

variable "iap_extension_timeout" {
  description = "Per-message IAP authorization extension timeout. Provider permits 10-10000 ms."
  type        = string
  default     = "0.1s"
}

variable "iam_enforcement_mode" {
  description = "ENFORCED for production, or DRY_RUN for Google's recommended audit-only qualification phase."
  type        = string
  default     = "ENFORCED"
  validation {
    condition     = contains(["ENFORCED", "DRY_RUN"], var.iam_enforcement_mode)
    error_message = "iam_enforcement_mode must be ENFORCED or DRY_RUN."
  }
}

variable "mcp_egress_grants" {
  description = "Least-privilege IAP egress grants on registered MCP servers."
  type = map(object({
    mcp_server_id         = string
    agent_principal       = string
    condition_title       = string
    condition_expression  = string
    condition_description = optional(string)
  }))
  default = {}
}

variable "agent_egress_grants" {
  description = "Least-privilege IAP egress grants on registered target agents."
  type = map(object({
    agent_id              = string
    source_principal      = string
    condition_title       = string
    condition_expression  = string
    condition_description = optional(string)
  }))
  default = {}
}

variable "endpoint_egress_grants" {
  description = "Least-privilege IAP egress grants on registered HTTPS endpoints."
  type = map(object({
    endpoint_id           = string
    agent_principal       = string
    condition_title       = string
    condition_expression  = string
    condition_description = optional(string)
  }))
  default = {}
}
