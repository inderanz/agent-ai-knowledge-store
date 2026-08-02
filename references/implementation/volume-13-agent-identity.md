# Volume 13 implementation evidence ledger

**Verified:** 2 August 2026. **Status:** admission policy is tested locally; no
customer identity, role, auth provider, consent or credential was created.

| Decision | Official evidence | Implemented artifact |
|---|---|---|
| Use lifecycle-bound SPIFFE/X.509 agent principal | [Identity overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-identity-overview) | `fde_kit.identity`, identity contract |
| Provision Runtime with `AGENT_IDENTITY` | [Runtime identity](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-identity) | provisioning gates/lab |
| Keep default certificate-bound CAA | [Runtime identity](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-identity) | explicit opt-out rejection |
| Gate exact external/delegated mode maturity | [Identity overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-identity-overview) | Preview exception validator |
| Preserve Gateway credential non-disclosure | [Identity overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-identity-overview) | raw-secret rejection and lab |

Production evidence still required: effective principal/trust domain, target IAM
allow/deny/PAB/perimeter support, certificate/token behavior, current maturity and
terms, provider/consent/scopes, secret non-disclosure, dual audit attribution,
negative tests, revoke/offboard/rotate and recovery.
