# Volume 5 security qualification lab

Use synthetic tenants, records, identities and secrets. The local stage mutates
nothing in Google Cloud.

## Local preflight

~~~bash
PYTHONPATH=examples/python/fde-production-kit/src \
  python3 -m unittest examples/python/fde-production-kit/tests/test_security.py -v
python3 delivery/volumes-4-10/validate_qualification.py \
  labs/volume-5-security/qualification.example.json --production
~~~

The example is intentionally incomplete and must fail production validation.
Copy it into the customer-controlled evidence store and replace all placeholders.

## Authorized sandbox exercise

1. Inventory business actions and mark read/propose/approve/execute authority.
2. Draw the deployed DFD; name every principal, credential, data class and owner.
3. Select exact Agent Identity/Gateway/Registry/Model Armor modes and recheck
   maturity, region, terms, IAM, quotas and support from official pages.
4. Build method-and-parameter policies and run wrong-user, wrong-agent,
   cross-tenant, extra-field, mutated-approval, replay and policy-outage tests.
5. Register a synthetic tool, attempt unauthorized publication/discovery/use,
   then revoke it and measure propagation through caches and sessions.
6. Run direct/indirect prompt injection, obfuscation, malicious URL, synthetic
   secret/PII exfiltration and safe-content regression against approved controls.
7. Test forbidden egress, redirects, DNS/IP changes, metadata endpoints and
   direct endpoint bypass. Prove target authentication remains mandatory.
8. Rotate and revoke a synthetic secret/identity during traffic; scan telemetry,
   builds, state and evidence for canary secret values.
9. Reject an altered/unsigned artifact or policy and preserve the verdict.
10. Run the SOC incident: detect, contain agent/tool/egress, preserve evidence,
    reconcile an ambiguous write, recover, validate, and obtain customer sign-off.

Do not run adversarial techniques outside written scope. Cleanup is an approved
exact-resource plan; never generically delete shared projects, perimeters,
gateways, registries, templates, sinks, keys, evidence, or business data.
