data "google_project" "this" {
  project_id = var.project_id
}

data "google_storage_project_service_account" "this" {
  count   = var.cmek == null ? 0 : 1
  project = var.project_id

  depends_on = [google_project_service.storage]
}

resource "google_project_service" "discovery_engine" {
  count = var.manage_project_service ? 1 : 0

  project            = var.project_id
  service            = "discoveryengine.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "storage" {
  count = var.manage_project_service && var.cmek != null ? 1 : 0

  project            = var.project_id
  service            = "storage.googleapis.com"
  disable_on_destroy = false
}

locals {
  discovery_engine_service_agent = "serviceAccount:service-${data.google_project.this.number}@gcp-sa-discoveryengine.iam.gserviceaccount.com"
  storage_service_agent          = var.cmek == null ? null : "serviceAccount:${data.google_storage_project_service_account.this[0].email_address}"
  cmek_members = var.cmek == null ? toset([]) : toset([
    local.discovery_engine_service_agent,
    local.storage_service_agent,
  ])
  cmek_keys = var.cmek == null ? toset([]) : toset(concat([var.cmek.kms_key], var.cmek.single_region_keys))
  cmek_grants = {
    for pair in setproduct(local.cmek_keys, local.cmek_members) : "${pair[0]}|${pair[1]}" => {
      key    = pair[0]
      member = pair[1]
    }
  }
}

resource "google_kms_crypto_key_iam_member" "cmek" {
  for_each = local.cmek_grants

  crypto_key_id = each.value.key
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = each.value.member
}

resource "google_discovery_engine_cmek_config" "this" {
  count = var.cmek == null ? 0 : 1

  project         = var.project_id
  location        = var.location
  cmek_config_id  = var.cmek.cmek_config_id
  kms_key         = var.cmek.kms_key
  set_default     = true
  deletion_policy = var.deletion_policy

  dynamic "single_region_keys" {
    for_each = var.cmek.single_region_keys
    content {
      kms_key = single_region_keys.value
    }
  }

  lifecycle {
    precondition {
      condition     = contains(["us", "eu"], var.location)
      error_message = "Discovery Engine CMEK is supported only in the us and eu multi-regions, not global."
    }
  }

  depends_on = [google_project_service.discovery_engine, google_kms_crypto_key_iam_member.cmek]
}

resource "google_discovery_engine_acl_config" "this" {
  count = var.acl_config == null ? 0 : 1

  project  = var.project_id
  location = var.location

  idp_config {
    idp_type = var.acl_config.idp_type
    dynamic "external_idp_config" {
      for_each = var.acl_config.idp_type == "THIRD_PARTY" ? [1] : []
      content {
        workforce_pool_name = var.acl_config.workforce_pool_name
      }
    }
  }

  lifecycle {
    precondition {
      condition     = var.acl_config.idp_type != "THIRD_PARTY" || var.acl_config.workforce_pool_name != null
      error_message = "THIRD_PARTY ACL configuration requires workforce_pool_name."
    }
  }

  depends_on = [google_project_service.discovery_engine]
}

resource "google_discovery_engine_data_store" "this" {
  for_each = var.data_stores

  project           = var.project_id
  location          = var.location
  data_store_id     = each.key
  display_name      = each.value.display_name
  industry_vertical = each.value.industry_vertical
  content_config    = each.value.content_config
  solution_types    = ["SOLUTION_TYPE_SEARCH"]
  kms_key_name      = var.cmek == null ? null : var.cmek.kms_key
  deletion_policy   = var.deletion_policy

  depends_on = [google_discovery_engine_cmek_config.this]
}

resource "google_discovery_engine_search_engine" "this" {
  project           = var.project_id
  location          = var.location
  collection_id     = var.collection_id
  engine_id         = var.engine_id
  display_name      = var.display_name
  industry_vertical = "GENERIC"
  app_type          = "APP_TYPE_INTRANET"
  data_store_ids    = sort(keys(google_discovery_engine_data_store.this))
  kms_key_name      = var.cmek == null ? null : var.cmek.kms_key
  features          = var.features
  deletion_policy   = var.deletion_policy

  common_config {
    company_name = var.company_name
  }

  search_engine_config {
    search_tier                = "SEARCH_TIER_ENTERPRISE"
    search_add_ons             = ["SEARCH_ADD_ON_LLM"]
    required_subscription_tier = var.subscription_tier
  }

  depends_on = [google_discovery_engine_cmek_config.this]
}

resource "google_discovery_engine_search_engine_iam_member" "app_user" {
  for_each = var.app_users

  project       = var.project_id
  location      = var.location
  collection_id = var.collection_id
  engine_id     = google_discovery_engine_search_engine.this.engine_id
  role          = "roles/discoveryengine.agentspaceUser"
  member        = each.value
}
