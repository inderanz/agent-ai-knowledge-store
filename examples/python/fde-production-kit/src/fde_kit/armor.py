"""Cloud Armor policy safety checks and deterministic rule evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from ipaddress import ip_address, ip_network


class ArmorAction(StrEnum):
    ALLOW = "allow"
    DENY = "deny-403"
    THROTTLE = "throttle"


@dataclass(frozen=True, slots=True)
class ArmorRule:
    priority: int
    action: ArmorAction
    source_ranges: tuple[str, ...] = ()
    preview: bool = True
    description: str = ""


def validate_policy(rules: tuple[ArmorRule, ...], *, logging_enabled: bool,
                    attached_backend: bool, production: bool) -> list[str]:
    errors: list[str] = []
    priorities = [rule.priority for rule in rules]
    if len(priorities) != len(set(priorities)):
        errors.append("Cloud Armor rule priorities must be unique")
    if not logging_enabled:
        errors.append("backend request logging is not enabled")
    if not attached_backend:
        errors.append("security policy is not attached to the intended backend")
    for rule in rules:
        if not 0 <= rule.priority <= 2_147_483_647:
            errors.append(f"invalid priority: {rule.priority}")
        for network in rule.source_ranges:
            try:
                ip_network(network)
            except ValueError:
                errors.append(f"invalid source range: {network}")
        if production and rule.preview and rule.action is ArmorAction.ALLOW:
            errors.append(f"production allow rule remains preview-only: {rule.priority}")
    return errors


def evaluate_ip(rules: tuple[ArmorRule, ...], address: str) -> ArmorAction | None:
    candidate = ip_address(address)
    for rule in sorted(rules, key=lambda value: value.priority):
        if rule.preview:
            continue
        if not rule.source_ranges or any(candidate in ip_network(value) for value in rule.source_ranges):
            return rule.action
    return None
