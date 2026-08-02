variable "identity_project_id" {
  type = string
}

variable "identity_project_number" {
  type = string
}

variable "pool_id" {
  type = string
}

variable "provider_id" {
  type = string
}

variable "repository_id" {
  type = string
}

variable "plan_service_account" {
  type = string
}

variable "apply_service_account" {
  type = string
}

variable "apply_ref" {
  description = "Only this Git ref can exchange a token through the apply provider."
  type        = string
}

variable "apply_environment_suffix" {
  description = "GitHub apply environments must end with this suffix."
  type        = string
}
