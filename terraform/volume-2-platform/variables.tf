variable "billing_account" {
  description = "Billing account ID used by the project and budget."
  type        = string
  sensitive   = true
}

variable "folder_id" {
  description = "Existing landing-zone folder in folders/NUMBER form."
  type        = string
  validation {
    condition     = can(regex("^folders/[0-9]+$", var.folder_id))
    error_message = "folder_id must use folders/NUMBER."
  }
}

variable "project_id" {
  description = "Globally unique governed-cell project ID."
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "project_id must satisfy the Google Cloud project ID form."
  }
}

variable "environment" {
  description = "Lifecycle boundary."
  type        = string
  validation {
    condition     = contains(["dev", "test", "stage", "prod"], var.environment)
    error_message = "environment must be dev, test, stage, or prod."
  }
}

variable "region" {
  description = "Customer-approved region."
  type        = string
}

variable "approved_regions" {
  description = "Regions approved by product, security, privacy, legal, data, and operations."
  type        = set(string)
}

variable "owner_label" {
  description = "Lowercase owner label."
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9_-]{2,62}$", var.owner_label))
    error_message = "owner_label has an unsupported form."
  }
}

variable "cost_centre" {
  description = "Customer cost allocation label."
  type        = string
}

variable "budget_amount" {
  description = "Monthly project budget in billing-account currency."
  type        = number
  validation {
    condition     = var.budget_amount > 0
    error_message = "budget_amount must be positive."
  }
}

variable "budget_currency" {
  description = "ISO 4217 currency code used by the billing account budget."
  type        = string
  validation {
    condition     = can(regex("^[A-Z]{3}$", var.budget_currency))
    error_message = "budget_currency must be a three-letter uppercase ISO 4217 code."
  }
}

variable "notification_channels" {
  description = "Existing Monitoring notification channel resource names."
  type        = list(string)
  default     = []
}

variable "network_host_project_id" {
  description = "Shared VPC host project ID; null disables attachment."
  type        = string
  default     = null
}

variable "runtime_subnetwork" {
  description = "Subnetwork name in the host project; required for Shared VPC."
  type        = string
  default     = null
}

variable "create_firestore_database" {
  description = "Create the default Firestore Native database."
  type        = bool
  default     = false
}

variable "plan_project_roles" {
  description = "Customer-reviewed project roles for the Terraform plan identity."
  type        = set(string)
  default     = []
  validation {
    condition = alltrue([
      for role in var.plan_project_roles :
      !contains(["roles/owner", "roles/editor"], role)
    ])
    error_message = "Primitive Owner and Editor roles are prohibited."
  }
}

variable "apply_project_roles" {
  description = "Customer-reviewed project roles for the Terraform apply identity."
  type        = set(string)
  default     = []
  validation {
    condition = alltrue([
      for role in var.apply_project_roles :
      !contains(["roles/owner", "roles/editor"], role)
    ])
    error_message = "Primitive Owner and Editor roles are prohibited."
  }
}

variable "github_wif" {
  description = "Optional GitHub OIDC provider restricted by immutable repository ID."
  type = object({
    enabled                  = bool
    identity_project_id      = optional(string)
    identity_project_number  = optional(string)
    pool_id                  = optional(string, "agent-platform-ci")
    provider_id              = optional(string, "github")
    repository_id            = optional(string)
    apply_ref                = optional(string, "refs/heads/main")
    apply_environment_suffix = optional(string, "-apply")
  })
  default = {
    enabled = false
  }
  validation {
    condition = !var.github_wif.enabled || alltrue([
      var.github_wif.identity_project_id != null,
      can(regex("^[0-9]+$", coalesce(var.github_wif.identity_project_number, ""))),
      can(regex("^[0-9]+$", coalesce(var.github_wif.repository_id, ""))),
    ])
    error_message = "Enabled GitHub WIF requires identity project ID/number and immutable repository ID."
  }
}

variable "cloud_deploy_control_plane" {
  description = "Optional external Cloud Deploy project for cross-project promotion."
  type = object({
    project_id              = string
    project_number          = string
    release_service_account = string
  })
  default = null
  validation {
    condition = var.cloud_deploy_control_plane == null || (
      can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.cloud_deploy_control_plane.project_id)) &&
      can(regex("^[0-9]+$", var.cloud_deploy_control_plane.project_number)) &&
      can(regex("^[^@]+@[^@]+\\.iam\\.gserviceaccount\\.com$", var.cloud_deploy_control_plane.release_service_account))
    )
    error_message = "cloud_deploy_control_plane values are malformed."
  }
}

variable "artifact_consumers" {
  description = "Cloud Run target projects allowed to deploy images from this cell's repository."
  type = set(object({
    project_id     = string
    project_number = string
  }))
  default = []
  validation {
    condition = alltrue([
      for consumer in var.artifact_consumers :
      can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", consumer.project_id)) &&
      can(regex("^[0-9]+$", consumer.project_number))
    ])
    error_message = "artifact consumer project IDs or numbers are malformed."
  }
}
