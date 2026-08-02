"""Audit envelopes that exclude request payloads and secrets by construction."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from typing import Any


_FORBIDDEN = {"authorization", "cookie", "prompt", "parameters", "secret", "token"}


def _detail_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = {str(key).lower() for key in value}
        for child in value.values():
            keys.update(_detail_keys(child))
        return keys
    if isinstance(value, (list, tuple)):
        keys: set[str] = set()
        for child in value:
            keys.update(_detail_keys(child))
        return keys
    return set()


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_type: str
    request_id: str
    tenant_hash: str
    status: str
    workflow_version: str
    timestamp: str
    details: dict[str, Any]

    def to_json(self) -> str:
        keys = _detail_keys(self.details)
        if keys & _FORBIDDEN:
            raise ValueError("audit details contain a forbidden sensitive field")
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))


def make_audit_event(*, event_type: str, request_id: str, tenant_id: str,
                     status: str, workflow_version: str,
                     details: dict[str, Any] | None = None) -> AuditEvent:
    return AuditEvent(
        event_type=event_type,
        request_id=request_id,
        tenant_hash=hashlib.sha256(tenant_id.encode()).hexdigest()[:16],
        status=status,
        workflow_version=workflow_version,
        timestamp=datetime.now(timezone.utc).isoformat(),
        details=details or {},
    )
