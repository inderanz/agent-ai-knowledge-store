# Agent Gateway operations pack

Own Gateway as an authorization service, not a transparent proxy. Dashboard by
gateway/mode/source/destination/policy: request rate, allow/deny, auth failures,
extension latency/error/timeout, downstream latency/status, MCP method/tool,
unregistered-destination denies and policy version. Preserve correlation IDs
without logging credentials or sensitive bodies.

Page on broad authorization bypass, fail-open protected action, unexplained deny
spike, extension saturation, logging loss or gateway availability breach. First
contain with default deny or route disable; preserve config/logs; distinguish IAP,
IAM, Registry, Identity, policy, extension, network and downstream failures; use a
reviewed rollback; reconcile any potentially executed actions. Run quarterly
policy-deny, extension-outage, load and rollback exercises. Customer SLOs must
measure successful authorized outcomes, not proxy 2xx alone.
