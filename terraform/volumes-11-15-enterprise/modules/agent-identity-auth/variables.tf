variable "project_id" {
  type        = string
  description = "Project that owns the Agent Identity auth providers."
}

variable "location" {
  type        = string
  description = "Agent Identity location."
}

variable "manage_project_service" {
  type        = bool
  description = "Whether this module enables agentidentity.googleapis.com."
  default     = true
}

variable "oauth_client_secrets" {
  type        = map(string)
  description = "Ephemeral OAuth secrets keyed exactly like auth_providers. Supply at apply time from an approved secret broker."
  sensitive   = true
  ephemeral   = true
  default     = {}
}

variable "auth_providers" {
  description = "OAuth providers. API-key authentication is deliberately unsupported because its provider argument is state-persistent."
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

  validation {
    condition     = alltrue([for p in values(var.auth_providers) : contains(["THREE_LEGGED_OAUTH", "TWO_LEGGED_OAUTH"], p.mode)])
    error_message = "mode must be THREE_LEGGED_OAUTH or TWO_LEGGED_OAUTH."
  }

  validation {
    condition     = alltrue([for id in keys(var.auth_providers) : can(regex("^[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?$", id))])
    error_message = "Auth-provider keys must satisfy the Google resource ID rules (1-63 lowercase letters, digits, and hyphens)."
  }

  validation {
    condition     = alltrue([for p in values(var.auth_providers) : length(p.workload_ids) > 0 && alltrue([for id in p.workload_ids : startswith(id, "principal://")])])
    error_message = "Every provider needs at least one principal:// workload identity."
  }

  validation {
    condition     = alltrue([for p in values(var.auth_providers) : length(p.allowed_scopes) > 0 && length(p.allowed_scopes) <= 200 && length(p.blocked_scopes) <= 200])
    error_message = "Use a non-empty allowlist; Google treats an empty allowed_scopes list as all scopes. Each list is limited to 200 entries."
  }

  validation {
    condition     = alltrue([for p in values(var.auth_providers) : p.deletion_policy == "PREVENT"])
    error_message = "Enterprise auth providers must use deletion_policy PREVENT."
  }
}
