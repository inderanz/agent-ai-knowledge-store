from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fde_doc_maintainer.repository_tools import list_repository_files, read_repository_file, stage_candidate_file


class RepositoryToolTests(unittest.TestCase):
    def test_staging_is_isolated_from_repository(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as candidate:
            repo = Path(repository)
            (repo / ".git").mkdir()
            (repo / "docs").mkdir()
            (repo / "docs/original.md").write_text("original", encoding="utf-8")
            with patch.dict(os.environ, {"FDE_REPOSITORY_ROOT": repository, "FDE_CANDIDATE_DIR": candidate}):
                staged = stage_candidate_file("docs/original.md", "candidate")
                self.assertEqual((repo / "docs/original.md").read_text(encoding="utf-8"), "original")
                self.assertEqual((Path(candidate) / "docs/original.md").read_text(encoding="utf-8"), "candidate")
                self.assertEqual(staged["bytes"], 9)

    def test_read_rejects_dot_github(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as candidate:
            repo = Path(repository)
            (repo / ".git").mkdir()
            (repo / ".github").mkdir()
            (repo / ".github/workflow.yml").write_text("secret", encoding="utf-8")
            with patch.dict(os.environ, {"FDE_REPOSITORY_ROOT": repository, "FDE_CANDIDATE_DIR": candidate}):
                with self.assertRaises(ValueError):
                    read_repository_file(".github/workflow.yml")

    def test_nested_credentials_are_neither_listed_nor_readable(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as candidate:
            repo = Path(repository)
            (repo / ".git").mkdir()
            (repo / "examples/.secrets").mkdir(parents=True)
            (repo / "examples/agent.py").write_text("safe", encoding="utf-8")
            (repo / "examples/customer.tfvars").write_text("secret", encoding="utf-8")
            (repo / "examples/.secrets/key.pem").write_text("secret", encoding="utf-8")
            with patch.dict(os.environ, {"FDE_REPOSITORY_ROOT": repository, "FDE_CANDIDATE_DIR": candidate}):
                self.assertEqual(list_repository_files("examples"), ["examples/agent.py"])
                for path in ("examples/customer.tfvars", "examples/.secrets/key.pem"):
                    with self.assertRaises(ValueError):
                        read_repository_file(path)

    def test_root_prefix_collision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as candidate:
            repo = Path(repository)
            (repo / ".git").mkdir()
            (repo / "README.md.credentials").write_text("secret", encoding="utf-8")
            with patch.dict(os.environ, {"FDE_REPOSITORY_ROOT": repository, "FDE_CANDIDATE_DIR": candidate}):
                with self.assertRaises(ValueError):
                    read_repository_file("README.md.credentials")

    def test_candidate_directory_inside_checkout_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as repository:
            repo = Path(repository)
            (repo / ".git").mkdir()
            candidate = repo / "candidate"
            with patch.dict(os.environ, {"FDE_REPOSITORY_ROOT": repository, "FDE_CANDIDATE_DIR": str(candidate)}):
                with self.assertRaises(ValueError):
                    stage_candidate_file("docs/example.md", "candidate")
