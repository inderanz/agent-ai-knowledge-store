# Volume 14 implementation evidence ledger

**Verified:** 2 August 2026. **Status:** Terraform source rules format locally and
Python rule tests pass; no policy was planned/applied/attached to a backend.

| Decision | Official evidence | Implemented artifact |
|---|---|---|
| Protect only supported load-balancer/backend boundaries | [policy overview](https://docs.cloud.google.com/armor/docs/security-policy-overview) | attachment/topology qualification gate |
| Roll WAF through labeled preview and narrow tuning | [WAF rules](https://docs.cloud.google.com/armor/docs/waf-rules) | lab/test matrix |
| Distinguish throttle and rate-based ban | [rate limiting](https://docs.cloud.google.com/armor/docs/rate-limiting-overview) | policy design checklist |
| Review Adaptive suggestions before enforcement | [Adaptive Protection](https://docs.cloud.google.com/armor/docs/adaptive-protection-overview) | incident/rollout runbook |
| Enable backend request logging and monitor preview/enforced outcomes | [monitoring](https://docs.cloud.google.com/armor/docs/monitoring), [policy logging](https://docs.cloud.google.com/armor/docs/security-policy-overview) | logging gate and operations pack |
| Pin/review Google-owned Terraform patterns | [official module reviewed commit](https://github.com/GoogleCloudPlatform/terraform-google-cloud-armor/tree/0757d7ca6ccc4b530337f79050f715ca14677c5a) | narrow local Terraform module |

Production evidence still required: live feature/load-balancer compatibility,
provider plan, backend attachment and origin-block test, WAF/rate/bot preview
corpus, false-positive/load/attack results, logs/metrics/alerts, incident and exact
rollback.
