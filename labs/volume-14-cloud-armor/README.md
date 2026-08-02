# Volume 14 lab — edge protection without agent authorization confusion

Attach a policy to a sandbox load-balancer backend that fronts an agent-facing
HTTP application. Enable backend request logging, deploy IP/WAF/rate rules in
preview, replay a synthetic benign/malicious corpus, tune false positives, obtain
approval and enforce incrementally. Prove policy attachment, first-match priority,
rate-key behavior, preview telemetry, alerting and rollback. Test direct-backend
bypass separately; Cloud Armor does not replace Gateway tool authorization,
Agent Identity or application business rules.

Use no real attack traffic or customer payload. Remove load generators and lab
resources after exporting redacted evidence. The example must fail production.
