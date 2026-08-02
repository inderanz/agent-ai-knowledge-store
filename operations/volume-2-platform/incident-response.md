# Incident response: platform admission service

## Trigger and roles

Declare an incident for sustained 5xx responses, unauthorized admission, policy divergence, unavailable decision storage, suspected credential or subject-hash-key compromise, or an SLO burn that meets the customer paging rule. Assign an incident commander, operations lead, communications lead, and scribe. Preserve evidence before changing resources.

## First 15 minutes

1. Record incident time, affected projects/regions, Cloud Run revision, image digest, last Cloud Deploy rollout, and last Terraform apply.
2. Determine whether impact is authentication, policy, storage, runtime, telemetry, networking, quota, or an upstream Agent Platform capability.
3. Stop production promotion and freeze policy or infrastructure changes.
4. If an unauthorized decision is possible, disable the ingress path or set Cloud Run maximum instances to zero through the customer emergency procedure. Do not weaken IAP or grant public access as a workaround.
5. Query by correlation ID, revision, outcome, and trace. Do not paste JWTs, raw principals, request bodies, secrets, or customer content into the incident channel.

## Containment branches

- **Bad revision:** route traffic to the last known-good Cloud Run revision and verify its image digest.
- **Bad policy:** restore the last reviewed policy artifact and replay the policy test corpus before routing traffic.
- **IAP validation failure:** verify the signed assertion audience and load-balancer backend ID. Never switch to unsigned `X-Goog-Authenticated-User-*` headers.
- **Firestore contention/outage:** preserve idempotency keys, stop automated retries that exceed the client transaction policy, and follow the customer recovery runbook.
- **Subject-hash-key exposure:** restrict access, create a new secret version, deploy it, invalidate the exposed material, and document whether pseudonym correlation is intentionally broken.
- **Preview product issue:** collect product/region/resource identifiers, check current release notes and known issues, open the contracted support path, and activate the documented fallback.

## Recovery

Run synthetic health, signed-IAP, invalid-IAP, admission, replay, idempotency-conflict, denial, trace, and alert tests. Observe at least one customer-approved stability window. The incident commander—not the implementer alone—authorizes restoration.

## Closure

Retain the timeline, contributing conditions, customer impact, evidence links, corrective owners, and due dates. Update the test, control, or runbook that would have prevented or shortened the incident. Avoid naming an individual as the root cause.

Official procedures: [IAP signed headers](https://docs.cloud.google.com/iap/docs/signed-headers-howto), [Cloud Run rollback](https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration), and [Google SRE incident response](https://sre.google/workbook/incident-response/).

