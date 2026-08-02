from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from threading import Lock
from typing import Any, Mapping, Protocol


class IdempotencyConflict(ValueError):
    """An idempotency key was reused with a different request."""


@dataclass(frozen=True)
class DecisionRecord:
    idempotency_key: str
    request_hash: str
    actor_pseudonym: str
    placement: Mapping[str, Any]
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "idempotency_key": self.idempotency_key,
            "request_hash": self.request_hash,
            "actor_pseudonym": self.actor_pseudonym,
            "placement": dict(self.placement),
            "created_at": self.created_at,
        }


class DecisionRepository(Protocol):
    def create_or_get(self, record: DecisionRecord) -> tuple[DecisionRecord, bool]:
        """Return the record and whether it was newly created."""


class InMemoryDecisionRepository:
    def __init__(self) -> None:
        self._records: dict[str, DecisionRecord] = {}
        self._lock = Lock()

    def create_or_get(self, record: DecisionRecord) -> tuple[DecisionRecord, bool]:
        with self._lock:
            existing = self._records.get(record.idempotency_key)
            if existing is None:
                self._records[record.idempotency_key] = record
                return record, True
            if existing.request_hash != record.request_hash:
                raise IdempotencyConflict(
                    "idempotency key already represents another request"
                )
            return existing, False


class FirestoreDecisionRepository:
    def __init__(self, project: str, collection: str) -> None:
        from google.cloud import firestore

        self._firestore = firestore
        self._client = firestore.Client(project=project)
        self._collection = self._client.collection(collection)

    def create_or_get(self, record: DecisionRecord) -> tuple[DecisionRecord, bool]:
        transaction = self._client.transaction(max_attempts=5)
        reference = self._collection.document(record.idempotency_key)
        firestore = self._firestore

        @firestore.transactional
        def persist(txn: Any) -> tuple[Mapping[str, Any], bool]:
            snapshot = reference.get(transaction=txn)
            if snapshot.exists:
                value = snapshot.to_dict()
                if value["request_hash"] != record.request_hash:
                    raise IdempotencyConflict(
                        "idempotency key already represents another request"
                    )
                return value, False
            value = record.to_dict()
            txn.set(reference, value)
            return value, True

        value, created = persist(transaction)
        stored = DecisionRecord(
            idempotency_key=str(value["idempotency_key"]),
            request_hash=str(value["request_hash"]),
            actor_pseudonym=str(value["actor_pseudonym"]),
            placement=value["placement"],
            created_at=(
                value["created_at"]
                if isinstance(value["created_at"], datetime)
                else datetime.now(UTC)
            ),
        )
        return stored, created

