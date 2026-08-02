variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "environment" {
  type = string
}

variable "labels" {
  type = map(string)
}

variable "billing_account" {
  type      = string
  sensitive = true
}

variable "budget_amount" {
  type = number
}

variable "budget_currency" {
  description = "ISO 4217 currency code accepted by Cloud Billing Budgets."
  type        = string
}

variable "notification_channels" {
  type    = list(string)
  default = []
}

variable "create_firestore_database" {
  type    = bool
  default = false
}

variable "plan_project_roles" {
  type    = set(string)
  default = []
}

variable "apply_project_roles" {
  type    = set(string)
  default = []
}

variable "cloud_deploy_control_plane" {
  description = "Cross-project Cloud Deploy project and release caller; null means this governed-cell project."
  type = object({
    project_id              = string
    project_number          = string
    release_service_account = string
  })
  default = null
}

variable "artifact_consumers" {
  description = "Cross-project Cloud Run consumers of the Artifact Registry repository."
  type = set(object({
    project_id     = string
    project_number = string
  }))
  default = []
}
