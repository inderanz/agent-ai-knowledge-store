provider "google" {
  project = var.project_id
  default_labels = merge(var.labels, {
    managed-by = "terraform"
    stack      = "gemini-agent-platform"
  })
}

provider "google-beta" {
  project = var.project_id
  default_labels = merge(var.labels, {
    managed-by = "terraform"
    stack      = "gemini-agent-platform"
  })
}
