# Volume 12 lab — ingress/egress default-deny enforcement

Build one Client-to-Agent and one Agent-to-Anywhere route in an authorized
sandbox. Register every destination, bind Agent Identity, start authorization in
dry-run, generate known-good and known-bad requests, review logs, then promote a
reviewed policy. Test unknown destination, missing IAP permission, identity
mismatch, denied MCP method/tool, injected payload, authorization-extension
timeout and downstream 5xx. Protected actions must not succeed during an
authorization outage. Export dashboard/alert evidence and exercise rollback.

The example record remains false until topology, policy, load, failure and
rollback evidence is independently accepted. Remove routes/extensions and prove
default-deny behavior after cleanup.
