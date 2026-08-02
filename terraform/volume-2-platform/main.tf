locals {
  required_services = [
    "artifactregistry.googleapis.com",
    "billingbudgets.googleapis.com",
    "binaryauthorization.googleapis.com",
    "cloudbuild.googleapis.com",
    "clouddeploy.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "containeranalysis.googleapis.com",
    "containerscanning.googleapis.com",
    "firestore.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "iap.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "serviceusage.googleapis.com",
    "sts.googleapis.com",
    "telemetry.googleapis.com",
  ]

  labels = {
    cost-centre = var.cost_centre
    environment = var.environment
    owner       = var.owner_label
    platform    = "enterprise-agent-platform"
  }
}

check "region_is_approved" {
  assert {
    condition     = contains(var.approved_regions, var.region)
    error_message = "The selected region is not in approved_regions."
  }
}

check "shared_vpc_inputs_are_complete" {
  assert {
    condition = (
      var.network_host_project_id == null && var.runtime_subnetwork == null
      ) || (
      var.network_host_project_id != null && var.runtime_subnetwork != null
    )
    error_message = "Shared VPC host and runtime subnetwork must be set together."
  }
}

module "project" {
  source = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/project?ref=v57.0.0"

  billing_account = var.billing_account
  deletion_policy = var.environment == "prod" ? "PREVENT" : "DELETE"
  labels          = local.labels
  lien_reason     = var.environment == "prod" ? "Protect production agent-platform governed cell." : null
  name            = var.project_id
  parent          = var.folder_id
  services        = local.required_services

  service_config = {
    disable_dependent_services = false
    disable_on_destroy         = false
  }
}

module "governed_cell" {
  source = "./modules/governed-cell"

  project_id                 = module.project.id
  region                     = var.region
  environment                = var.environment
  labels                     = local.labels
  budget_amount              = var.budget_amount
  budget_currency            = var.budget_currency
  billing_account            = var.billing_account
  notification_channels      = var.notification_channels
  create_firestore_database  = var.create_firestore_database
  plan_project_roles         = var.plan_project_roles
  apply_project_roles        = var.apply_project_roles
  cloud_deploy_control_plane = var.cloud_deploy_control_plane
  artifact_consumers         = var.artifact_consumers
}

resource "google_compute_shared_vpc_service_project" "cell" {
  count = var.network_host_project_id == null ? 0 : 1

  host_project    = var.network_host_project_id
  service_project = module.project.id
}

resource "google_compute_subnetwork_iam_member" "runtime" {
  count = var.network_host_project_id == null ? 0 : 1

  project    = var.network_host_project_id
  region     = var.region
  subnetwork = var.runtime_subnetwork
  role       = "roles/compute.networkUser"
  member     = module.governed_cell.runtime_identity_member
}

module "github_wif" {
  count  = var.github_wif.enabled ? 1 : 0
  source = "./modules/github-wif"

  identity_project_id      = var.github_wif.identity_project_id
  identity_project_number  = var.github_wif.identity_project_number
  pool_id                  = var.github_wif.pool_id
  provider_id              = var.github_wif.provider_id
  repository_id            = var.github_wif.repository_id
  plan_service_account     = module.governed_cell.plan_service_account
  apply_service_account    = module.governed_cell.apply_service_account
  apply_ref                = var.github_wif.apply_ref
  apply_environment_suffix = var.github_wif.apply_environment_suffix
}
