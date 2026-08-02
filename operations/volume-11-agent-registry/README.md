# Agent Registry operations pack

**Service owner:** platform catalog team. **Security owner:** agent governance.
**Escalation:** resource owner → registry platform → security/incident command.

Monitor registration/create/update/delete audit activity, lookup/search errors,
resolution latency, duplicate/ownerless resources, endpoint health, metadata and
tool-annotation drift, bindings, location mismatch and gateway resolution failure.
Alert on unauthorized editor/admin changes, destructive metadata change, bulk
deletion and sustained lookup failure. The catalog is control-plane discovery,
not live health proof: invocation health remains a separate signal.

Incident order: freeze writes; export resource/IAM/binding state; disable or
remove unsafe bindings/routes; identify affected agents and cached consumers;
revoke unsafe destination access; restore reviewed metadata from source control;
test resolution and denial; reconcile audit evidence; reopen writes. Recovery
objectives and drift intervals are customer decisions. Never silently recreate a
registry in another project/location—the official setup guide says data is not
migrated when projects change.
