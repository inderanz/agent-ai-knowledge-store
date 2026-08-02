# Cloud Armor source-rule reference module

This narrow module creates a backend Cloud Armor policy with reviewed source-CIDR
rules and an explicit default. It intentionally does not pretend one abstraction
can safely cover every WAF, rate, bot, edge or hierarchical feature. Build those
against the exact current provider/service schema and their own preview tests.

The module does **not** attach the policy. The consuming load-balancer stack must
attach `security_policy_self_link` to the intended supported backend, enable
backend request logging and verify deployed attachment/direct-origin controls.

Versions match [`references/versions.json`](../../references/versions.json).
Initialize/validate in an environment with provider access, save the exact plan,
run policy/preview tests, and apply only through the customer-approved workflow.
