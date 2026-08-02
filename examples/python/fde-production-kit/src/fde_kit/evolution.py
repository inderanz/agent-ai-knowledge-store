"""Upstream change impact and in-flight compatibility gates."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True, slots=True)
class UpstreamChange:
    source_id: str
    old_version: str
    new_version: str
    changed_surfaces: frozenset[str]
    security: bool = False
    removed: bool = False


HIGH_SURFACES = frozenset({"event-schema", "session", "resume", "auth", "tool-contract", "runtime-api"})


def classify(change: UpstreamChange) -> Severity:
    if change.security or change.removed:
        return Severity.CRITICAL
    if change.changed_surfaces & HIGH_SURFACES:
        return Severity.HIGH
    if change.changed_surfaces:
        return Severity.MEDIUM
    return Severity.LOW


def affected_assets(change: UpstreamChange, dependency_map: dict[str, set[str]]) -> list[str]:
    assets: set[str] = set(dependency_map.get(change.source_id, set()))
    for surface in change.changed_surfaces:
        assets.update(dependency_map.get(f"surface:{surface}", set()))
    return sorted(assets)


@dataclass(frozen=True, slots=True)
class VersionEnvelope:
    workflow: int
    event: int
    state: int
    tool: int
    approval_digest: int


def compatible(old: VersionEnvelope, new: VersionEnvelope) -> tuple[bool, tuple[str, ...]]:
    blockers: list[str] = []
    if new.event < old.event or new.state < old.state:
        blockers.append("schema versions cannot move backwards")
    if new.workflow != old.workflow and new.event == old.event:
        blockers.append("workflow topology changed without an event-version boundary")
    if new.tool != old.tool and new.approval_digest == old.approval_digest:
        blockers.append("tool contract changed without approval-digest version change")
    return not blockers, tuple(blockers)
