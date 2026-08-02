# Volume 13 lab — per-agent identity and credential containment

Create two sandbox agents with Agent Identity, grant each a different minimal
resource role, and prove cross-agent/cross-resource denial. Verify SPIFFE/effective
identity in supported logs, certificate-bound token behavior from the intended
runtime, and rejection outside it. Where an approved preview is in scope, create
an Auth Manager provider with test-only credentials and prove the agent never
receives the raw secret. Exercise token/certificate expiry, role revocation,
auth-provider disablement and recovery. Do not opt out of Context-Aware Access.

The example is deliberately rejected for production. Retain only redacted audit
evidence; delete providers, grants, agents and test credentials during cleanup.
