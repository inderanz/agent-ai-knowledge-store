# Mermaid diagram standard

Mermaid source is the canonical diagram format. Keep diagrams reviewable in Git and accessible without proprietary tools.

## Required conventions

- Give every node a stable, meaningful identifier.
- Label trust boundaries, projects, regions, networks, and execution environments.
- Use solid arrows for synchronous calls, dashed arrows for asynchronous delivery, and dotted arrows for control or telemetry.
- Label protocol and identity on security-sensitive edges.
- Do not imply high availability, ordering, exactly-once behavior, or private connectivity unless cited and explained.
- Include failure routes, retry ownership, and terminal states when they affect the design.
- Keep one diagram focused on one concern; split unreadable diagrams.

## Diagram types

Every completed chapter includes or explicitly justifies omission of logical, physical, sequence, security, identity, deployment, network, component, lifecycle, state, failure, and data-flow diagrams.

Run repository validation to catch unbalanced Mermaid fences. Visual review remains mandatory.
