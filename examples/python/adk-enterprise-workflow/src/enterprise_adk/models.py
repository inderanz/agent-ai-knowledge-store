"""Strict domain contracts. Model output is never accepted directly as authority."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
import hashlib
import json
import re
from typing import Any


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class Risk(StrEnum):
    LOW = "low"
    HIGH = "high"


class Status(StrEnum):
    DENIED = "DENIED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    READY = "READY"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _clean_text(value: str, field_name: str, maximum: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    value = value.strip()
    if not value or len(value) > maximum or "\x00" in value:
        raise ValueError(f"{field_name} must contain 1..{maximum} safe characters")
    return value


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    groups: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not _ID.fullmatch(self.subject):
            raise ValueError("subject has an invalid identifier")
        if any(not _ID.fullmatch(group) for group in self.groups):
            raise ValueError("group has an invalid identifier")


@dataclass(frozen=True, slots=True)
class ChangeRequest:
    request_id: str
    tenant_id: str
    action: str
    target: str
    justification: str
    risk: Risk
    parameters: dict[str, Any]
    requested_by: str
    workflow_version: str = "3.1.0"

    def __post_init__(self) -> None:
        for name in ("request_id", "tenant_id", "action", "target", "requested_by"):
            if not _ID.fullmatch(getattr(self, name)):
                raise ValueError(f"{name} has an invalid identifier")
        object.__setattr__(self, "justification", _clean_text(self.justification, "justification", 2000))
        if not isinstance(self.risk, Risk):
            object.__setattr__(self, "risk", Risk(self.risk))
        if not isinstance(self.parameters, dict):
            raise ValueError("parameters must be an object")
        encoded = json.dumps(self.parameters, sort_keys=True, separators=(",", ":"), allow_nan=False)
        if len(encoded.encode("utf-8")) > 16_384:
            raise ValueError("parameters exceed the 16 KiB contract limit")

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ChangeRequest:
        allowed = {
            "request_id", "tenant_id", "action", "target", "justification",
            "risk", "parameters", "requested_by", "workflow_version",
        }
        unknown = set(value) - allowed
        missing = allowed - {"workflow_version"} - set(value)
        if unknown or missing:
            raise ValueError(f"request fields invalid; missing={sorted(missing)}, unknown={sorted(unknown)}")
        return cls(**value)

    def approval_digest(self) -> str:
        payload = {
            "action": self.action,
            "parameters": self.parameters,
            "request_id": self.request_id,
            "target": self.target,
            "tenant_id": self.tenant_id,
            "workflow_version": self.workflow_version,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def idempotency_key(self) -> str:
        material = f"{self.tenant_id}\n{self.request_id}\n{self.action}\n{self.target}\n{self.approval_digest()}"
        return hashlib.sha256(material.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class ApprovalDecision:
    request_id: str
    tenant_id: str
    action_digest: str
    approver: str
    approved: bool
    issued_at: datetime
    expires_at: datetime
    decision_id: str

    def __post_init__(self) -> None:
        for name in ("request_id", "tenant_id", "approver", "decision_id"):
            if not _ID.fullmatch(getattr(self, name)):
                raise ValueError(f"{name} has an invalid identifier")
        if not re.fullmatch(r"[0-9a-f]{64}", self.action_digest):
            raise ValueError("action_digest must be a lowercase SHA-256 digest")
        if self.issued_at.tzinfo is None or self.expires_at.tzinfo is None:
            raise ValueError("approval timestamps must be timezone aware")
        if self.expires_at <= self.issued_at:
            raise ValueError("approval expiry must follow issue time")

    def validate_for(self, request: ChangeRequest, now: datetime) -> None:
        if not self.approved:
            raise PermissionError("approval decision rejected the action")
        if now < self.issued_at or now >= self.expires_at:
            raise PermissionError("approval is outside its validity window")
        if self.request_id != request.request_id or self.tenant_id != request.tenant_id:
            raise PermissionError("approval is bound to another request or tenant")
        if self.action_digest != request.approval_digest():
            raise PermissionError("approved action differs from the requested action")
        if self.approver == request.requested_by:
            raise PermissionError("requester cannot approve their own high-risk action")
