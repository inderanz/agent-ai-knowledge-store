"""Fail-closed authorization and risk policy."""

from __future__ import annotations

from dataclasses import dataclass

from .models import ChangeRequest, Principal, Risk


@dataclass(frozen=True, slots=True)
class Policy:
    tenant_id: str
    allowed_actions: frozenset[str]
    executor_group: str
    approval_group: str
    force_approval_actions: frozenset[str] = frozenset()
    deny_all: bool = True

    def authorize_request(self, principal: Principal, request: ChangeRequest) -> Risk:
        if self.deny_all:
            raise PermissionError("policy is deny-all")
        if request.tenant_id != self.tenant_id:
            raise PermissionError("cross-tenant request denied")
        if principal.subject != request.requested_by:
            raise PermissionError("authenticated principal does not match requested_by")
        if self.executor_group not in principal.groups:
            raise PermissionError("principal lacks the executor group")
        if request.action not in self.allowed_actions:
            raise PermissionError("action is not allowlisted")
        return Risk.HIGH if request.action in self.force_approval_actions else request.risk

    def authorize_approver(self, principal: Principal, request: ChangeRequest) -> None:
        if request.tenant_id != self.tenant_id:
            raise PermissionError("cross-tenant approval denied")
        if self.approval_group not in principal.groups:
            raise PermissionError("principal lacks the approval group")
