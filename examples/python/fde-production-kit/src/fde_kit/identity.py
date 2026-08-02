"""Per-agent identity and Auth Manager qualification."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AuthMode(StrEnum):
    GOOGLE_CLOUD = "agent-identity"
    OAUTH_3LO = "oauth-3lo"
    OAUTH_2LO = "oauth-2lo"
    API_KEY = "api-key"
    BASIC = "http-basic"


PREVIEW_MODES = frozenset({AuthMode.OAUTH_3LO, AuthMode.OAUTH_2LO, AuthMode.API_KEY})


@dataclass(frozen=True, slots=True)
class IdentityBinding:
    agent_resource: str
    mode: AuthMode
    target: str
    agent_identity_enabled: bool
    caa_enforced: bool
    least_privilege_reviewed: bool
    raw_secret_visible_to_agent: bool = False
    preview_exception: str | None = None


def qualify_identity(binding: IdentityBinding, *, production: bool) -> list[str]:
    errors: list[str] = []
    if not binding.agent_resource or not binding.target:
        errors.append("agent resource and target are required")
    if not binding.agent_identity_enabled:
        errors.append("per-agent identity is not enabled")
    if not binding.caa_enforced:
        errors.append("default certificate-bound Context-Aware Access is disabled")
    if not binding.least_privilege_reviewed:
        errors.append("least-privilege IAM/auth-provider review is missing")
    if binding.raw_secret_visible_to_agent:
        errors.append("agent can observe a raw downstream credential")
    if binding.mode is AuthMode.BASIC:
        errors.append("HTTP basic authentication is not accepted")
    if production and binding.mode in PREVIEW_MODES and not binding.preview_exception:
        errors.append(f"preview auth mode requires an accepted exception: {binding.mode.value}")
    return errors
