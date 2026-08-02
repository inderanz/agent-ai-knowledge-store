"""Fail-closed Agent Registry catalog and binding qualification."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import urlparse


class ResourceKind(StrEnum):
    AGENT = "agent"
    MCP_SERVER = "mcp-server"
    ENDPOINT = "endpoint"
    SKILL = "skill"


@dataclass(frozen=True, slots=True)
class CatalogEntry:
    name: str
    kind: ResourceKind
    uri: str
    location: str
    owner: str
    protocol: str
    maturity: str = "GA"
    destructive_capabilities: bool = False


def validate_catalog(entries: tuple[CatalogEntry, ...], *, production: bool) -> list[str]:
    """Reject ambiguous, unowned, insecure, or unqualified catalog entries."""
    errors: list[str] = []
    names: set[str] = set()
    for entry in entries:
        if entry.name in names:
            errors.append(f"duplicate registry name: {entry.name}")
        names.add(entry.name)
        if not entry.owner:
            errors.append(f"missing owner: {entry.name}")
        parsed = urlparse(entry.uri)
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"endpoint must use an absolute HTTPS URI: {entry.name}")
        if entry.kind is ResourceKind.AGENT and entry.protocol != "a2a":
            errors.append(f"agent must declare A2A protocol: {entry.name}")
        if entry.kind is ResourceKind.MCP_SERVER and entry.protocol != "mcp":
            errors.append(f"MCP server must declare MCP protocol: {entry.name}")
        if production and entry.maturity.lower() != "ga":
            errors.append(f"non-GA registry capability needs an accepted exception: {entry.name}")
    return errors


def validate_binding(source: CatalogEntry, target: CatalogEntry, *, gateway_location: str) -> list[str]:
    errors: list[str] = []
    if source.location in {"us", "eu"} or target.location in {"us", "eu"}:
        errors.append("registry bindings/endpoints do not support us/eu multi-regions")
    if target.location not in {gateway_location, "global"}:
        errors.append("target and gateway placement have not been qualified together")
    if source.name == target.name:
        errors.append("self-binding is not allowed")
    return errors
