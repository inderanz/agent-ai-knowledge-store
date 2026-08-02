# Cloud Armor enterprise wrapper

This wrapper pins Google's official Cloud Armor module to `8.1.1` and the Google providers to `7.42.0`. It establishes default-deny, WAF/source/CEL/rate-limit/Threat Intelligence rule support, Adaptive Protection detection without automatic deployment, normal request logging, unique priorities, and a hard approval gate before any rule leaves preview. Threat Intelligence feeds can require Managed Protection Plus; confirm the customer's subscription before enabling them.

The consuming load-balancer stack **must** attach `policy.self_link` to every internet-facing backend service and enable load-balancer logging. This module intentionally does not own those backends. Treat `backend_attachment_required = true` as a deployment handoff control and verify it with an integration test against the customer environment.

Recommended rollout: preview, inspect sampled logs and false positives, tune exclusions narrowly, obtain change approval, set only the reviewed rules to `preview = false`, then set `enforcement_approved = true` for the approved plan.

Official references: [Google Cloud Armor Terraform module v8.1.1](https://github.com/GoogleCloudPlatform/terraform-google-cloud-armor/tree/v8.1.1), [module inputs and attachment example](https://github.com/GoogleCloudPlatform/terraform-google-cloud-armor/blob/v8.1.1/README.md), [rule tuning](https://cloud.google.com/armor/docs/rule-tuning), and [request logging](https://cloud.google.com/armor/docs/request-logging).
