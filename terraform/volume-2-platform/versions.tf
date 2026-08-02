terraform {
  required_version = "= 1.15.8"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "= 7.42.0"
    }
  }
}

provider "google" {
  region = var.region

  default_labels = {
    environment = var.environment
    managed-by  = "terraform"
    platform    = "enterprise-agent-platform"
  }
}

