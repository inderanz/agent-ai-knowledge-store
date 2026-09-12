terraform {
  required_version = "= 1.15.8"

  backend "gcs" {}

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "= 7.42.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region

  default_labels = {
    managed-by = "terraform"
    system     = "fde-documentation-maintainer"
  }
}
