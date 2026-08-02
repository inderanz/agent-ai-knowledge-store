# Agent Identity operations pack

Inventory immutable agent resource, effective SPIFFE principal, trust domain,
runtime, IAM grants, deny policies, auth providers, target, owner, maturity and
expiry/review date. Alert on identity creation/deletion, broad role grant, CAA
opt-out, unusual target access, auth-provider change, repeated token failures and
user/agent audit-correlation loss. Raw credentials and tokens never enter logs.

For suspected compromise: stop routes/actions, disable provider or revoke grants,
preserve agent/user/effective-identity logs, identify replay attempts, rotate
external credentials, recreate only when lifecycle semantics are understood, and
reconcile actions. Certificate rotation is Google-managed; a 24-hour certificate
validity is not a substitute for immediate authorization revocation. Exercise
revocation, provider outage, consent withdrawal, certificate/token expiry and
break-glass denial before launch.
