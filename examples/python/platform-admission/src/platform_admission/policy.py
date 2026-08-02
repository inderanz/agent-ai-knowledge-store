from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Mapping

from .models import Placement, Principal, RiskTier, TenantModel, WorkloadRequest


class AdmissionError(ValueError):
    """A valid request is not allowed by the active platform policy."""


@dataclass(frozen=True)
class ProfilePolicy:
    allowed_risk_tiers: frozenset[RiskTier]
    required_controls: tuple[str, ...]


@dataclass(frozen=True)
class PlatformPolicy:
    schema_version: int
    policy_version: str
    deny_all: bool
    approved_regions: frozenset[str]
    allowed_subjects: frozenset[str]
    required_access_level: str | None
    production_folder: str
    nonproduction_folder: str
    profiles: Mapping[TenantModel, ProfilePolicy]

    @classmethod
    def load(cls, path: Path) -> PlatformPolicy:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise AdmissionError("policy root must be an object")
        return cls.from_mapping(value)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> PlatformPolicy:
        expected = {
            "schema_version",
            "policy_version",
            "deny_all",
            "approved_regions",
            "allowed_subjects",
            "required_access_level",
            "production_folder",
            "nonproduction_folder",
            "profiles",
        }
        if set(value) != expected:
            raise AdmissionError("policy fields do not match schema version 1")
        if value["schema_version"] != 1:
            raise AdmissionError("unsupported policy schema_version")

        profiles: dict[TenantModel, ProfilePolicy] = {}
        raw_profiles = value["profiles"]
        if not isinstance(raw_profiles, dict):
            raise AdmissionError("profiles must be an object")
        for name, raw in raw_profiles.items():
            try:
                model = TenantModel(name)
                profiles[model] = ProfilePolicy(
                    allowed_risk_tiers=frozenset(
                        RiskTier(item) for item in raw["allowed_risk_tiers"]
                    ),
                    required_controls=tuple(
                        sorted(set(str(item) for item in raw["required_controls"]))
                    ),
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise AdmissionError(f"invalid profile {name}: {exc}") from exc
        if set(profiles) != set(TenantModel):
            raise AdmissionError("policy must define every tenant model")

        policy = cls(
            schema_version=1,
            policy_version=str(value["policy_version"]),
            deny_all=value["deny_all"],
            approved_regions=frozenset(str(x) for x in value["approved_regions"]),
            allowed_subjects=frozenset(str(x) for x in value["allowed_subjects"]),
            required_access_level=(
                str(value["required_access_level"])
                if value["required_access_level"] is not None
                else None
            ),
            production_folder=str(value["production_folder"]),
            nonproduction_folder=str(value["nonproduction_folder"]),
            profiles=profiles,
        )
        policy.validate()
        return policy

    def validate(self) -> None:
        if type(self.deny_all) is not bool:
            raise AdmissionError("deny_all must be a boolean")
        if not re.fullmatch(
            r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]+$", self.policy_version
        ):
            raise AdmissionError("policy_version must use YYYY-MM-DD.N")
        if not self.approved_regions:
            raise AdmissionError("approved_regions cannot be empty")
        if (
            not self.deny_all
            and not self.allowed_subjects
            and self.required_access_level is None
        ):
            raise AdmissionError("policy requires subjects or an access level")
        for folder in (self.production_folder, self.nonproduction_folder):
            if not re.fullmatch(r"^folders/[0-9]+$", folder):
                raise AdmissionError("folder names must use folders/NUMBER")

    def admit(self, principal: Principal, request: WorkloadRequest) -> Placement:
        if self.deny_all:
            raise AdmissionError("platform policy is in deny-all bootstrap mode")
        subject_allowed = principal.subject in self.allowed_subjects
        access_allowed = (
            self.required_access_level is not None
            and self.required_access_level in principal.access_levels
        )
        if not (subject_allowed or access_allowed):
            raise AdmissionError("principal is not authorized by platform policy")
        if request.region not in self.approved_regions:
            raise AdmissionError("region is not approved by platform policy")

        profile = self.profiles[request.tenant_model]
        if request.risk_tier not in profile.allowed_risk_tiers:
            raise AdmissionError("risk tier is not permitted for tenant model")
        if (
            request.risk_tier is RiskTier.REGULATED
            and request.tenant_model is not TenantModel.DEDICATED_PROJECT
        ):
            raise AdmissionError("regulated workloads require dedicated-project")
        if request.uses_sensitive_data and request.tenant_model is TenantModel.POOLED:
            raise AdmissionError("sensitive data is not permitted in pooled profile")

        controls = set(profile.required_controls)
        controls.update(
            {
                "budget-and-quota-alerts",
                "immutable-release",
                "source-and-evaluation-evidence",
            }
        )
        if request.writes_business_data:
            controls.update(
                {"human-approval-policy", "idempotent-tool-contract", "reconciliation"}
            )

        maturity = []
        if request.requires_agent_gateway:
            maturity.append("agent-gateway-preview")
        if request.requires_agent_identity:
            maturity.append("agent-identity-preview")
        if request.requires_managed_agents:
            maturity.append("managed-agents-pre-ga-non-production-only")

        production = request.environment == "prod"
        if production and request.requires_managed_agents:
            raise AdmissionError(
                "current Managed Agents Pre-GA terms prohibit production use"
            )

        return Placement(
            folder=(
                self.production_folder if production else self.nonproduction_folder
            ),
            project_profile=request.tenant_model.value,
            governed_cell=f"{request.region}-{'prod' if production else 'nonprod'}",
            requires_human_approval=(
                request.writes_business_data
                or request.risk_tier in {RiskTier.HIGH, RiskTier.REGULATED}
            ),
            required_controls=tuple(sorted(controls)),
            maturity_acceptances=tuple(sorted(maturity)),
            policy_version=self.policy_version,
        )
