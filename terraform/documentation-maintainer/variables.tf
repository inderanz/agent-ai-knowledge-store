variable "project_id" {
  description = "Dedicated Google Cloud project used only for documentation-maintainer model invocation."
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "project_id must be a valid Google Cloud project ID."
  }
}

variable "project_number" {
  description = "Numeric project number for the workload identity principal URI."
  type        = string
  validation {
    condition     = can(regex("^[0-9]+$", var.project_number))
    error_message = "project_number must contain digits only."
  }
}

variable "region" {
  description = "Approved Vertex AI location passed to the GitHub workflow."
  type        = string
}

variable "repository" {
  description = "Case-sensitive GitHub owner/repository claim, for example inderanz/agent-ai-knowledge-store."
  type        = string
  validation {
    condition     = can(regex("^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", var.repository))
    error_message = "repository must use owner/name form."
  }
}

variable "repository_id" {
  description = "Immutable numeric GitHub repository ID from the repository API."
  type        = string
  validation {
    condition     = can(regex("^[0-9]+$", var.repository_id))
    error_message = "repository_id must contain digits only."
  }
}

variable "repository_owner_id" {
  description = "Immutable numeric GitHub owner ID from the repository API."
  type        = string
  validation {
    condition     = can(regex("^[0-9]+$", var.repository_owner_id))
    error_message = "repository_owner_id must contain digits only."
  }
}

variable "workflow_ref" {
  description = "Exact OIDC workflow_ref allowed to exchange a token."
  type        = string
  validation {
    condition = var.workflow_ref == format(
      "%s/.github/workflows/agentic-handbook-maintenance.yml@refs/heads/main",
      var.repository,
    )
    error_message = "workflow_ref must identify agentic-handbook-maintenance.yml on refs/heads/main in repository."
  }
}

variable "service_account_id" {
  description = "Account ID for the model-invocation-only workload identity."
  type        = string
  default     = "fde-doc-maintainer"
}

variable "workload_identity_pool_id" {
  type    = string
  default = "fde-doc-maintainer"
}

variable "workload_identity_provider_id" {
  type    = string
  default = "github"
}
