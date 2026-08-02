from __future__ import annotations

from datetime import UTC, datetime
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from platform_admission.repository import (  # noqa: E402
    DecisionRecord,
    IdempotencyConflict,
    InMemoryDecisionRepository,
)


def record(request_hash: str) -> DecisionRecord:
    return DecisionRecord(
        idempotency_key="52c00f16-c9e6-46d0-89dd-cb0ab7fd1748",
        request_hash=request_hash,
        actor_pseudonym="actor-hash",
        placement={"governed_cell": "australia-southeast1-prod"},
        created_at=datetime.now(UTC),
    )


class RepositoryTests(unittest.TestCase):
    def test_replay_returns_original_record(self) -> None:
        repository = InMemoryDecisionRepository()
        _, first_created = repository.create_or_get(record("hash-a"))
        _, replay_created = repository.create_or_get(record("hash-a"))
        self.assertTrue(first_created)
        self.assertFalse(replay_created)

    def test_key_reuse_with_different_payload_conflicts(self) -> None:
        repository = InMemoryDecisionRepository()
        repository.create_or_get(record("hash-a"))
        with self.assertRaises(IdempotencyConflict):
            repository.create_or_get(record("hash-b"))


if __name__ == "__main__":
    unittest.main()
