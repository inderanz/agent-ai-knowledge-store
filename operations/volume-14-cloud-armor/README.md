# Cloud Armor operations pack

Record policy/backend attachment, rule priority/action/preview/version, WAF rule
set and exclusions, rate keys/thresholds, bot configuration, log sampling, owner
and rollback. Dashboards separate enforced from preview matches and segment by
backend, outcome, rule and response. Alert on DDoS/WAF/rate anomalies, allow or
deny shifts, false-positive business impact, policy detachment and logging loss.

During an event, confirm traffic actually traverses the protected load balancer;
identify the first matched rule; preserve load-balancer/Armor logs; mitigate with
the smallest reviewed rule; use preview when time and threat permit; notify app,
Gateway and identity owners; and validate recovery. Never copy Adaptive
Protection suggestions directly to enforce. Keep an emergency rollback and a
bounded, expiring exception path. Test direct-origin blocking and backend
attachment drift—the strongest policy is ineffective when bypassed or unattached.
