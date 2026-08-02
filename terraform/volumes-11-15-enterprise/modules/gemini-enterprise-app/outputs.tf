output "engine" {
  value = {
    id   = google_discovery_engine_search_engine.this.id
    name = google_discovery_engine_search_engine.this.name
  }
}

output "data_stores" {
  value = { for key, ds in google_discovery_engine_data_store.this : key => ds.name }
}

output "observability_handoff_required" {
  value       = true
  description = "Configure Gemini Enterprise observability through the supported API/console workflow; provider 7.42.0 has no first-class observability-config resource."
}
