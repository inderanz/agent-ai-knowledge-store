from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
import hashlib
import json
import re
from typing import Any, Mapping

NAME = re.compile(r"^[a-z][a-z0-9-]{2,39}$")
OWNER = re.compile(r"^[a-z][a-z0-9-]{2,62}$")
ALLOWED_REQUEST_FIELDS = frozenset(
    {
        "name",
        "owner_group",
        "environment",
        "region",
        "risk_tier",
        "tenant_model",
        "writes_business_data",
        "uses_sensitive_data",
        "requires_agent_gateway",
        "requires_agent_identity",
        "requires_managed_agents",
    }
)


class RequestValidationError(ValueError):
    """The request does not conform to the public contract."""


class RiskTier(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    REGULATED = "regulated"


class TenantModel(StrEnum):
    POOLED = "pooled"
    DOMAIN = "domain"
    DEDICATED_PROJECT = "dedicated-project"


@dataclass(frozen=True)
class Principal:
    subject: str
    email: str
    access_levels: frozenset[str]


@dataclass(frozen=True)
class WorkloadRequest:
    name: str
    owner_group: str
    environment: str
    region: str
    risk_tier: RiskTier
    tenant_model: TenantModel
    writes_business_data: bool
    uses_sensitive_data: bool
    requires_agent_gateway: bool
    requires_agent_identity: bool
    requires_managed_agents: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> WorkloadRequest:
        unknown = set(value) - ALLOWED_REQUEST_FIELDS
        missing = ALLOWED_REQUEST_FIELDS - set(value)
        if unknown:
            raise RequestValidationError(f"unknown request fields: {sorted(unknown)}")
        if missing:
            raise RequestValidationError(f"missing request fields: {sorted(missing)}")

        for field in (
            "writes_business_data",
            "uses_sensitive_data",
            "requires_agent_gateway",
            "requires_agent_identity",
            "requires_managed_agents",
        ):
            if type(value[field]) is not bool:
                raise RequestValidationError(f"{field} must be a boolean")

        try:
            request = cls(
                name=str(value["name"]),
                owner_group=str(value["owner_group"]),
                environment=str(value["environment"]),
                region=str(value["region"]),
                risk_tier=RiskTier(str(value["risk_tier"])),
                tenant_model=TenantModel(str(value["tenant_model"])),
                writes_business_data=value["writes_business_data"],
                uses_sensitive_data=value["uses_sensitive_data"],
                requires_agent_gateway=value["requires_agent_gateway"],
                requires_agent_identity=value["requires_agent_identity"],
                requires_managed_agents=value["requires_managed_agents"],
            )
        except ValueError as exc:
            raise RequestValidationError(f"unsupported enum value: {exc}") from exc
        request.validate()
        return request

    def validate(self) -> None:
        if not NAME.fullmatch(self.name):
            raise RequestValidationError("name must match ^[a-z][a-z0-9-]{2,39}$")
        if not OWNER.fullmatch(self.owner_group):
            raise RequestValidationError(
                "owner_group must match ^[a-z][a-z0-9-]{2,62}$"
            )
        if self.environment not in {"dev", "test", "stage", "prod"}:
            raise RequestValidationError("unsupported environment")
        if not re.fullmatch(r"^[a-z]+-[a-z]+[0-9]+$", self.region):
            raise RequestValidationError("region must use a Google Cloud region form")

    def canonical_hash(self) -> str:
        payload = asdict(self)
        payload["risk_tier"] = self.risk_tier.value
        payload["tenant_model"] = self.tenant_model.value
        encoded = json.dumps(
            payload, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class Placement:
    folder: str
    project_profile: str
    governed_cell: str
    requires_human_approval: bool
    required_controls: tuple[str, ...]
    maturity_acceptances: tuple[str, ...]
    policy_version: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "folder": self.folder,
            "project_profile": self.project_profile,
            "governed_cell": self.governed_cell,
            "requires_human_approval": self.requires_human_approval,
            "required_controls": list(self.required_controls),
            "maturity_acceptances": list(self.maturity_acceptances),
            "policy_version": self.policy_version,
        }

