"""Business-action authorization and security control coverage."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class Decision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


@dataclass(frozen=True, slots=True)
class ActionContext:
    user: str
    agent: str
    tenant: str
    tool: str
    method: str
    environment: str
    risk: str
    parameters: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ActionPolicy:
    tenant: str
    allowed_agents: frozenset[str]
    allowed_methods: frozenset[tuple[str, str]]
    production_users: frozenset[str]
    high_risk_methods: frozenset[tuple[str, str]]
    maximum_parameter_bytes: int = 16_384


def authorize(policy: ActionPolicy, action: ActionContext) -> Decision:
    import json

    if action.tenant != policy.tenant or action.agent not in policy.allowed_agents:
        return Decision.DENY
    method = (action.tool, action.method)
    if method not in policy.allowed_methods:
        return Decision.DENY
    if action.environment == "production" and action.user not in policy.production_users:
        return Decision.DENY
    encoded = json.dumps(action.parameters, sort_keys=True, allow_nan=False).encode()
    if len(encoded) > policy.maximum_parameter_bytes:
        return Decision.DENY
    if action.risk == "high" or method in policy.high_risk_methods:
        return Decision.REQUIRE_APPROVAL
    return Decision.ALLOW


REQUIRED_THREAT_CONTROLS = frozenset({
    "prompt-injection", "confused-deputy", "cross-tenant-leakage",
    "credential-exfiltration", "ssrf-egress", "tool-poisoning",
    "replay-duplicate-write", "supply-chain", "excessive-agency",
    "audit-tampering",
})


def missing_threat_controls(evidence: dict[str, bool]) -> list[str]:
    return sorted(control for control in REQUIRED_THREAT_CONTROLS if evidence.get(control) is not True)
