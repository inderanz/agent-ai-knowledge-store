# Python example standard

Reference implementations target Python 3.12 or later and pin the qualified ADK minor/patch version.

Each example includes typed public interfaces, structured logging, configuration validation, timeouts, bounded retries, idempotency for side effects, OpenTelemetry instrumentation, unit tests, integration-test boundaries, a dependency lock, and a README describing how to run it safely.

Model output is untrusted input. Validate structured output before routing or executing a tool. Never log secrets, credentials, raw regulated data, or chain-of-thought. Examples that cannot be compiled or executed against the stated baseline must be labeled pseudocode.
