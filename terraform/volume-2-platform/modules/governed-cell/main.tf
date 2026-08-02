locals {
  service_accounts = {
    runtime = {
      id   = "agent-admission-runtime"
      name = "Agent platform admission runtime"
    }
    build = {
      id   = "agent-platform-build"
      name = "Agent platform build pipeline"
    }
    deploy = {
      id   = "agent-platform-deploy"
      name = "Agent platform deployment pipeline"
    }
    plan = {
      id   = "agent-platform-tf-plan"
      name = "Agent platform Terraform plan"
    }
    apply = {
      id   = "agent-platform-tf-apply"
      name = "Agent platform Terraform apply"
    }
  }

  runtime_roles = toset([
    "roles/datastore.user",
    "roles/serviceusage.serviceUsageConsumer",
    "roles/telemetry.tracesWriter",
  ])

  build_roles = toset([
    "roles/artifactregistry.writer",
    "roles/containeranalysis.occurrences.viewer",
    "roles/logging.logWriter",
  ])

  deploy_roles = toset([
    "roles/artifactregistry.reader",
    "roles/logging.logWriter",
    "roles/run.developer",
  ])

  delivery_project_id = var.cloud_deploy_control_plane == null ? var.project_id : var.cloud_deploy_control_plane.project_id
  release_caller      = var.cloud_deploy_control_plane == null ? google_service_account.identity["build"].member : "serviceAccount:${var.cloud_deploy_control_plane.release_service_account}"

  artifact_reader_members = merge([
    for consumer in var.artifact_consumers : {
      "${consumer.project_id}-deployer"  = "serviceAccount:agent-platform-deploy@${consumer.project_id}.iam.gserviceaccount.com"
      "${consumer.project_id}-run-agent" = "serviceAccount:service-${consumer.project_number}@serverless-robot-prod.iam.gserviceaccount.com"
    }
  ]...)
}

resource "google_service_account" "identity" {
  for_each = local.service_accounts

  project      = var.project_id
  account_id   = each.value.id
  display_name = each.value.name
  description  = "Managed by the Volume 2 governed-cell Terraform module."
}

resource "google_project_iam_member" "runtime" {
  for_each = local.runtime_roles

  project = var.project_id
  role    = each.value
  member  = google_service_account.identity["runtime"].member
}

resource "google_project_iam_member" "build" {
  for_each = local.build_roles

  project = var.project_id
  role    = each.value
  member  = google_service_account.identity["build"].member
}

resource "google_project_iam_member" "deploy" {
  for_each = local.deploy_roles

  project = var.project_id
  role    = each.value
  member  = google_service_account.identity["deploy"].member
}

resource "google_project_iam_member" "deploy_job_runner" {
  project = local.delivery_project_id
  role    = "roles/clouddeploy.jobRunner"
  member  = google_service_account.identity["deploy"].member
}

resource "google_project_iam_member" "release_caller" {
  project = local.delivery_project_id
  role    = "roles/clouddeploy.releaser"
  member  = local.release_caller
}

resource "google_project_iam_member" "plan" {
  for_each = var.plan_project_roles

  project = var.project_id
  role    = each.value
  member  = google_service_account.identity["plan"].member
}

resource "google_project_iam_member" "apply" {
  for_each = var.apply_project_roles

  project = var.project_id
  role    = each.value
  member  = google_service_account.identity["apply"].member
}

resource "google_service_account_iam_member" "deploy_acts_as_runtime" {
  service_account_id = google_service_account.identity["runtime"].name
  role               = "roles/iam.serviceAccountUser"
  member             = google_service_account.identity["deploy"].member
}

resource "google_service_account_iam_member" "release_caller_acts_as_deploy" {
  service_account_id = google_service_account.identity["deploy"].name
  role               = "roles/iam.serviceAccountUser"
  member             = local.release_caller
}

resource "google_service_account_iam_member" "cross_project_cloud_deploy" {
  count = var.cloud_deploy_control_plane == null ? 0 : 1

  service_account_id = google_service_account.identity["deploy"].name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:service-${var.cloud_deploy_control_plane.project_number}@gcp-sa-clouddeploy.iam.gserviceaccount.com"
}

resource "google_service_account_iam_member" "cross_project_cloud_build" {
  count = var.cloud_deploy_control_plane == null ? 0 : 1

  service_account_id = google_service_account.identity["deploy"].name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:service-${var.cloud_deploy_control_plane.project_number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"
}

resource "google_artifact_registry_repository" "containers" {
  project       = var.project_id
  location      = var.region
  repository_id = "agent-platform"
  description   = "Immutable release artifacts for the governed cell."
  format        = "DOCKER"
  labels        = var.labels

  docker_config {
    immutable_tags = true
  }

  vulnerability_scanning_config {
    enablement_config = "INHERITED"
  }

  cleanup_policy_dry_run = true
  cleanup_policies {
    id     = "candidate-expiry-dry-run"
    action = "DELETE"
    condition {
      tag_state  = "UNTAGGED"
      older_than = "2592000s"
    }
  }
}

resource "google_artifact_registry_repository_iam_member" "cross_project_reader" {
  for_each = local.artifact_reader_members

  project    = var.project_id
  location   = google_artifact_registry_repository.containers.location
  repository = google_artifact_registry_repository.containers.repository_id
  role       = "roles/artifactregistry.reader"
  member     = each.value
}

resource "google_firestore_database" "admission" {
  count = var.create_firestore_database ? 1 : 0

  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  delete_protection_state = var.environment == "prod" ? "DELETE_PROTECTION_ENABLED" : "DELETE_PROTECTION_DISABLED"
  deletion_policy         = var.environment == "prod" ? "ABANDON" : "DELETE"
}

resource "google_secret_manager_secret" "subject_hash" {
  project   = var.project_id
  secret_id = "platform-admission-subject-hash-key"
  labels    = var.labels

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_iam_member" "runtime" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.subject_hash.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = google_service_account.identity["runtime"].member
}

resource "google_logging_metric" "admission_denied" {
  project = var.project_id
  name    = "platform_admission_denied"
  filter = join(" AND ", [
    "resource.type=\"cloud_run_revision\"",
    "jsonPayload.outcome=\"denied\"",
  ])

  metric_descriptor {
    metric_kind = "DELTA"
    value_type  = "INT64"
    unit        = "1"
  }
}

resource "google_monitoring_alert_policy" "admission_denied" {
  project               = var.project_id
  display_name          = "Platform admission denials elevated"
  combiner              = "OR"
  notification_channels = var.notification_channels

  conditions {
    display_name = "Five or more denied admissions in five minutes"
    condition_threshold {
      filter          = "metric.type=\"logging.googleapis.com/user/${google_logging_metric.admission_denied.name}\" AND resource.type=\"cloud_run_revision\""
      comparison      = "COMPARISON_GT"
      threshold_value = 4
      duration        = "0s"

      aggregations {
        alignment_period   = "300s"
        per_series_aligner = "ALIGN_SUM"
      }
    }
  }

  alert_strategy {
    auto_close = "1800s"
  }
}

resource "google_monitoring_dashboard" "platform" {
  project = var.project_id
  dashboard_json = jsonencode({
    displayName = "Enterprise Agent Platform - Governed Cell"
    mosaicLayout = {
      columns = 12
      tiles = [
        {
          height = 4
          width  = 6
          widget = {
            title = "Cloud Run request count"
            xyChart = {
              dataSets = [{
                plotType = "LINE"
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "metric.type=\"run.googleapis.com/request_count\" resource.type=\"cloud_run_revision\""
                    aggregation = {
                      alignmentPeriod  = "60s"
                      perSeriesAligner = "ALIGN_RATE"
                    }
                  }
                }
              }]
            }
          }
        },
        {
          height = 4
          width  = 6
          xPos   = 6
          widget = {
            title = "Admission denials"
            xyChart = {
              dataSets = [{
                plotType = "STACKED_BAR"
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "metric.type=\"logging.googleapis.com/user/platform_admission_denied\" resource.type=\"cloud_run_revision\""
                    aggregation = {
                      alignmentPeriod  = "300s"
                      perSeriesAligner = "ALIGN_SUM"
                    }
                  }
                }
              }]
            }
          }
        },
      ]
    }
  })
}

resource "google_billing_budget" "cell" {
  billing_account = var.billing_account
  display_name    = "${var.project_id} monthly budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = var.budget_currency
      units         = tostring(floor(var.budget_amount))
    }
  }

  dynamic "threshold_rules" {
    for_each = toset([0.5, 0.8, 1.0])
    content {
      threshold_percent = threshold_rules.value
      spend_basis       = "CURRENT_SPEND"
    }
  }
}
