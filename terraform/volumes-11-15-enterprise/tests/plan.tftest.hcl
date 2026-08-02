mock_provider "google" {}
mock_provider "google-beta" {}

run "enterprise_baseline_plans" {
  command = apply

  variables {
    project_id           = "customer-agent-platform-prod"
    agent_location       = "us-central1"
    oauth_client_secrets = { crm-oauth = "unit-test-placeholder" }
    labels = {
      environment         = "production"
      owner               = "agent-platform"
      data-classification = "confidential"
      cost-centre         = "cc-1234"
    }
    gateway = {
      name                 = "enterprise-agent-egress"
      description          = "Fail-closed governed egress"
      governed_access_path = "AGENT_TO_ANYWHERE"
    }
    registry_services = {
      orchestrator = {
        kind         = "AGENT"
        display_name = "Orchestrator"
        description  = "Test agent"
        interfaces   = [{ url = "https://agent.example.com", protocol_binding = "HTTP_JSON" }]
        spec_type    = "NO_SPEC"
      }
      crm-mcp = {
        kind         = "MCP_SERVER"
        display_name = "CRM MCP"
        description  = "Test MCP server"
        interfaces   = [{ url = "https://mcp.example.com", protocol_binding = "JSONRPC" }]
        spec_type    = "TOOL_SPEC"
        spec_content = jsonencode({ tools = [] })
      }
    }
    identity_providers = {
      crm-oauth = {
        mode                  = "TWO_LEGGED_OAUTH"
        workload_ids          = ["principal://agents.example.test/orchestrator"]
        allowed_scopes        = ["crm.read"]
        client_id             = "unit-test-client"
        token_url             = "https://oauth.example.com/token"
        client_secret_version = "1"
      }
    }
    cloud_armor = {
      name        = "agent-app-edge"
      description = "Customer agent application edge"
      preconfigured_waf_rules = {
        sqli = {
          action            = "deny(403)"
          priority          = 1000
          description       = "SQL injection preview"
          preview           = true
          target_rule_set   = "sqli-v33-stable"
          sensitivity_level = 2
        }
      }
    }
    gemini_enterprise = {
      engine_id    = "enterprise-search"
      display_name = "Enterprise Search"
      company_name = "Customer"
      data_stores = {
        docs = { display_name = "Enterprise documents" }
      }
      app_users = ["group:enterprise-users@example.com"]
    }
  }

  assert {
    condition     = module.agent_gateway.iap_authz_extension_id != null
    error_message = "Gateway must include its fail-closed IAP authorization extension."
  }

  assert {
    condition     = module.gemini_enterprise.observability_handoff_required
    error_message = "Gemini Enterprise observability handoff must remain explicit."
  }
}
