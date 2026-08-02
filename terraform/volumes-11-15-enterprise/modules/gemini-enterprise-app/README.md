# Gemini Enterprise application module

Creates a protected Gemini Enterprise intranet application (`APP_TYPE_INTRANET`), one enterprise-search datastore, LLM add-on, optional document-level ACL configuration, optional CMEK, and app-scoped end-user IAM.

Enterprise controls built into the module:

- `PREVENT` deletion on the datastore, CMEK registration, and app;
- CMEK service-agent grants and registration occur before data creation;
- CMEK is rejected in `global`, where it is unsupported;
- `PUBLIC_WEBSITE` datastores are rejected for this Gemini Enterprise app path;
- users receive `roles/discoveryengine.agentspaceUser` on the app, never at project scope;
- broad `allUsers`/`allAuthenticatedUsers` grants are rejected.

Provider `7.42.0` does not expose the Gemini Enterprise observability configuration as a first-class Terraform resource. Configure it through Google's supported API/console flow, retain the change record, and validate telemetry before go-live; the output `observability_handoff_required` makes that handoff explicit.

Official references: [create a Gemini Enterprise app](https://cloud.google.com/gemini/enterprise/docs/create-app), [control access to apps](https://cloud.google.com/gemini/enterprise/docs/iam-policy-for-apps), [CMEK](https://cloud.google.com/gemini/enterprise/docs/cmek), [configure the identity provider](https://cloud.google.com/gemini/enterprise/docs/configure-identity-provider), and provider `7.42.0` resources for [search engine](https://github.com/hashicorp/terraform-provider-google/blob/v7.42.0/website/docs/r/discovery_engine_search_engine.html.markdown), [datastore](https://github.com/hashicorp/terraform-provider-google/blob/v7.42.0/website/docs/r/discovery_engine_data_store.html.markdown), and [CMEK config](https://github.com/hashicorp/terraform-provider-google/blob/v7.42.0/website/docs/r/discovery_engine_cmek_config.html.markdown).
