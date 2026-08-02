resource "google_compute_security_policy" "this" {
  project     = var.project_id
  name        = var.name
  description = var.description
  type        = "CLOUD_ARMOR"

  dynamic "rule" {
    for_each = var.source_rules
    content {
      action      = rule.value.action
      priority    = rule.value.priority
      preview     = rule.value.preview
      description = rule.value.description
      match {
        versioned_expr = "SRC_IPS_V1"
        config {
          src_ip_ranges = sort(tolist(rule.value.source_ranges))
        }
      }
    }
  }

  rule {
    action      = var.default_action
    priority    = 2147483647
    preview     = false
    description = "Explicit default rule"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
  }

  lifecycle {
    precondition {
      condition     = alltrue([for rule in values(var.source_rules) : rule.priority >= 0 && rule.priority < 2147483647])
      error_message = "Custom priorities must be between 0 and 2147483646."
    }
  }
}
