from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import hmac
import logging
import uuid
from typing import Any

from .configuration import Settings
from .identity import IapJwtVerifier, IdentityError
from .logging_json import configure_logging
from .models import RequestValidationError, WorkloadRequest
from .policy import AdmissionError, PlatformPolicy
from .repository import (
    DecisionRecord,
    FirestoreDecisionRepository,
    IdempotencyConflict,
    InMemoryDecisionRepository,
)
from .telemetry import Telemetry, configure_telemetry

LOGGER = logging.getLogger(__name__)


def _uuid_header(value: str | None, *, required: bool) -> str:
    if not value:
        if required:
            raise RequestValidationError("missing Idempotency-Key")
        return str(uuid.uuid4())
    try:
        return str(uuid.UUID(value))
    except ValueError as exc:
        raise RequestValidationError("identifier header must contain a UUID") from exc


def _pseudonym(subject: str, key: bytes) -> str:
    return hmac.new(key, subject.encode("utf-8"), hashlib.sha256).hexdigest()


def _trace_name(project: str, header: str | None) -> str | None:
    if not header:
        return None
    trace_id = header.split("/", 1)[0]
    if len(trace_id) != 32 or any(c not in "0123456789abcdefABCDEF" for c in trace_id):
        return None
    return f"projects/{project}/traces/{trace_id}"


def create_app(
    settings: Settings | None = None,
    policy: PlatformPolicy | None = None,
    repository: Any = None,
    verifier: IapJwtVerifier | None = None,
    telemetry: Telemetry | None = None,
) -> Any:
    from flask import Flask, jsonify, request

    configure_logging()
    active_settings = settings or Settings.from_environment()
    active_policy = policy or PlatformPolicy.load(active_settings.policy_path)
    active_repository = repository
    if active_repository is None:
        if active_settings.repository_backend == "firestore":
            active_repository = FirestoreDecisionRepository(
                active_settings.project_id,
                active_settings.firestore_collection,
            )
        else:
            active_repository = InMemoryDecisionRepository()
    active_verifier = verifier or IapJwtVerifier(active_settings.iap_expected_audience)
    active_telemetry = telemetry or configure_telemetry(active_settings)

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 32 * 1024

    @app.get("/healthz")
    def health() -> Any:
        return {"status": "ok"}, 200

    @app.get("/readyz")
    def ready() -> Any:
        return {"status": "ready", "policy_version": active_policy.policy_version}, 200

    @app.post("/v1/admissions")
    def admit() -> Any:
        correlation_id = "unassigned"
        cloud_trace = _trace_name(
            active_settings.project_id,
            request.headers.get("X-Cloud-Trace-Context"),
        )
        try:
            correlation_id = _uuid_header(
                request.headers.get("X-Request-Id"), required=False
            )
            idempotency_key = _uuid_header(
                request.headers.get("Idempotency-Key"), required=True
            )
            principal = active_verifier.verify(
                request.headers.get("X-Goog-IAP-JWT-Assertion")
            )
            raw = request.get_json(silent=False)
            if not isinstance(raw, dict):
                raise RequestValidationError("JSON body must be an object")
            workload = WorkloadRequest.from_mapping(raw)
            with active_telemetry.span(
                "platform.admission.evaluate",
                {
                    "platform.workload": workload.name,
                    "platform.environment": workload.environment,
                    "platform.region": workload.region,
                },
            ):
                placement = active_policy.admit(principal, workload)
                record = DecisionRecord(
                    idempotency_key=idempotency_key,
                    request_hash=workload.canonical_hash(),
                    actor_pseudonym=_pseudonym(
                        principal.subject, active_settings.subject_hash_key
                    ),
                    placement=placement.to_dict(),
                    created_at=datetime.now(UTC),
                )
                stored, created = active_repository.create_or_get(record)
            LOGGER.info(
                "platform admission completed",
                extra={
                    "correlation_id": correlation_id,
                    "cloud_trace": cloud_trace,
                    "workload": workload.name,
                    "environment": workload.environment,
                    "governed_cell": placement.governed_cell,
                    "policy_version": placement.policy_version,
                    "outcome": "created" if created else "replayed",
                },
            )
            return (
                jsonify(
                    {
                        "correlation_id": correlation_id,
                        "idempotency_key": idempotency_key,
                        "created": created,
                        "placement": dict(stored.placement),
                    }
                ),
                201 if created else 200,
            )
        except (IdentityError, AdmissionError) as exc:
            LOGGER.warning(
                "platform admission denied",
                extra={
                    "correlation_id": correlation_id,
                    "cloud_trace": cloud_trace,
                    "outcome": "denied",
                },
            )
            return {"error": "request_denied", "message": str(exc)}, 403
        except RequestValidationError as exc:
            return {"error": "invalid_request", "message": str(exc)}, 400
        except IdempotencyConflict as exc:
            return {"error": "idempotency_conflict", "message": str(exc)}, 409
        except Exception:
            LOGGER.exception(
                "platform admission failed",
                extra={
                    "correlation_id": correlation_id,
                    "cloud_trace": cloud_trace,
                    "outcome": "error",
                },
            )
            return {"error": "internal_error"}, 500

    return app

