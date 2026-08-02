"""Agent Gateway ingress/egress policy qualification."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class GatewayMode(StrEnum):
    INGRESS = "client-to-agent"
    EGRESS = "agent-to-anywhere"


@dataclass(frozen=True, slots=True)
class GatewayRoute:
    name: str
    mode: GatewayMode
    source: str
    destination: str
    destination_registered: bool
    agent_identity: bool
    request_authorization: bool
    content_authorization: bool
    audit_logging: bool
    fail_open: bool = False
    dry_run: bool = True


def qualify_route(route: GatewayRoute, *, production: bool) -> list[str]:
    errors: list[str] = []
    if not route.destination_registered:
        errors.append("destination is not registered")
    if not route.agent_identity:
        errors.append("route is not bound to Agent Identity")
    if not route.request_authorization:
        errors.append("request authorization is missing")
    if route.mode is GatewayMode.EGRESS and not route.content_authorization:
        errors.append("egress content authorization is missing")
    if not route.audit_logging:
        errors.append("gateway audit/traffic logging is missing")
    if production and route.fail_open:
        errors.append("production protected action cannot fail open without an exception")
    if production and route.dry_run:
        errors.append("production route is still dry-run only")
    return errors
