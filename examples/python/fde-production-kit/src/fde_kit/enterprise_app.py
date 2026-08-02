"""Gemini Enterprise app configuration qualification."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DataStore:
    name: str
    location: str
    cmek_key: str | None
    access_controlled: bool
    source_domain: str


@dataclass(frozen=True, slots=True)
class EnterpriseApp:
    app_id: str
    location: str
    data_stores: tuple[DataStore, ...]
    app_level_iam: bool
    broad_project_role_removed: bool
    registry_imports: tuple[str, ...] = ()
    gateway_governed: bool = False
    cross_domain_drive_approved: bool = False
    observability_enabled: bool = False


def qualify_app(app: EnterpriseApp, *, production: bool) -> list[str]:
    errors: list[str] = []
    if not app.app_id or app.app_id.startswith("REPLACE"):
        errors.append("immutable app ID is missing")
    if not app.data_stores:
        errors.append("app has no qualified data store")
    if len(app.data_stores) > 50:
        errors.append("app exceeds the documented 50 data-store limit")
    keys = {store.cmek_key for store in app.data_stores}
    if len(keys) > 1:
        errors.append("connected data stores do not use one consistent CMEK posture")
    for store in app.data_stores:
        if store.location != app.location:
            errors.append(f"data-store location mismatch: {store.name}")
        if not store.access_controlled:
            errors.append(f"source access control is not enforced: {store.name}")
        if store.source_domain == "cross-domain-drive" and not app.cross_domain_drive_approved:
            errors.append(f"cross-domain Drive risk not approved: {store.name}")
    if not app.app_level_iam or not app.broad_project_role_removed:
        errors.append("app-level IAM is undermined by broad project-level access")
    if app.registry_imports and not app.gateway_governed:
        errors.append("imported Registry resources are not governed by Agent Gateway")
    if production and not app.observability_enabled:
        errors.append("production app observability is not enabled")
    return errors
