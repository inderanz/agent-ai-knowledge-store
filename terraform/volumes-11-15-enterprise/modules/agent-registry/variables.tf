variable "project_id" {
  description = "Project that owns the project-scoped Agent Registry."
  type        = string
}

variable "location" {
  description = "Supported Agent Registry location. Gateway-bound registries should align with the Gateway location."
  type        = string
}

variable "manage_project_service" {
  description = "Enable agentregistry.googleapis.com in this module. Set false when a bootstrap stack owns APIs."
  type        = bool
  default     = true
}

variable "deletion_policy" {
  description = "PREVENT in production; DELETE is intended only for disposable environments."
  type        = string
  default     = "PREVENT"
  validation {
    condition     = contains(["PREVENT", "ABANDON", "DELETE"], var.deletion_policy)
    error_message = "deletion_policy must be PREVENT, ABANDON, or DELETE."
  }
}

variable "services" {
  description = "Owned manual Registry services. Exactly one spec block is selected from kind."
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

  validation {
    condition     = alltrue([for service in values(var.services) : contains(["AGENT", "MCP_SERVER", "ENDPOINT"], service.kind)])
    error_message = "kind must be AGENT, MCP_SERVER, or ENDPOINT."
  }
  validation {
    condition     = alltrue(flatten([for service in values(var.services) : [for interface in service.interfaces : startswith(interface.url, "https://")]]))
    error_message = "Every Registry interface must use an absolute HTTPS URL."
  }
  validation {
    condition     = alltrue(flatten([for service in values(var.services) : [for interface in service.interfaces : contains(["JSONRPC", "GRPC", "HTTP_JSON"], interface.protocol_binding)]]))
    error_message = "protocol_binding must be JSONRPC, GRPC, or HTTP_JSON."
  }
}

variable "bindings" {
  description = "Agent-to-agent/MCP/endpoint Auth Provider bindings using Registry URNs."
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

  validation {
    condition     = alltrue([for binding in values(var.bindings) : startswith(binding.source_urn, "urn:agent:")])
    error_message = "Every binding source must be an urn:agent URN."
  }
  validation {
    condition     = alltrue([for binding in values(var.bindings) : can(regex("^urn:(agent|mcp|endpoint):", binding.target_urn))])
    error_message = "Every target must be an agent, mcp, or endpoint URN."
  }
}
