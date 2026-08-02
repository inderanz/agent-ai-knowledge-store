from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


class ConfigurationError(ValueError):
    """Runtime configuration is incomplete or unsafe."""


def _boolean(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized not in {"true", "false"}:
        raise ConfigurationError(f"{name} must be true or false")
    return normalized == "true"


@dataclass(frozen=True)
class Settings:
    project_id: str
    iap_expected_audience: str
    policy_path: Path
    subject_hash_key: bytes
    firestore_collection: str
    repository_backend: str
    otel_enabled: bool
    otel_required: bool
    trace_sample_ratio: float
    otlp_endpoint: str

    @classmethod
    def from_environment(cls) -> Settings:
        required = {
            name: os.getenv(name, "").strip()
            for name in (
                "GOOGLE_CLOUD_PROJECT",
                "IAP_EXPECTED_AUDIENCE",
                "POLICY_PATH",
                "SUBJECT_HASH_KEY",
            )
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ConfigurationError(
                f"missing required environment variables: {sorted(missing)}"
            )
        if len(required["SUBJECT_HASH_KEY"]) < 32:
            raise ConfigurationError("SUBJECT_HASH_KEY must contain at least 32 characters")
        backend = os.getenv("REPOSITORY_BACKEND", "firestore").strip()
        if backend not in {"firestore", "memory"}:
            raise ConfigurationError("REPOSITORY_BACKEND must be firestore or memory")
        ratio = float(os.getenv("OTEL_TRACE_SAMPLE_RATIO", "0.05"))
        if not 0.0 <= ratio <= 1.0:
            raise ConfigurationError("OTEL_TRACE_SAMPLE_RATIO must be between 0 and 1")
        return cls(
            project_id=required["GOOGLE_CLOUD_PROJECT"],
            iap_expected_audience=required["IAP_EXPECTED_AUDIENCE"],
            policy_path=Path(required["POLICY_PATH"]),
            subject_hash_key=required["SUBJECT_HASH_KEY"].encode("utf-8"),
            firestore_collection=os.getenv(
                "FIRESTORE_COLLECTION", "platform-admission-decisions"
            ),
            repository_backend=backend,
            otel_enabled=_boolean("OTEL_ENABLED", True),
            otel_required=_boolean("OTEL_REQUIRED", True),
            trace_sample_ratio=ratio,
            otlp_endpoint=os.getenv(
                "OTEL_EXPORTER_OTLP_ENDPOINT",
                "https://telemetry.googleapis.com:443/v1/traces",
            ),
        )

