"""Command-line entry points for validation, ADK execution, and draft application."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import uuid
from pathlib import Path

from .policy import load_manifest, validate_manifest
from .repository_tools import apply_candidate_for_draft


async def run_agent(signal: Path, output: Path) -> None:
    from google.adk.runners import InMemoryRunner
    from google.genai import types

    from .agent import root_agent

    payload = json.loads(signal.read_text(encoding="utf-8"))
    runner = InMemoryRunner(agent=root_agent, app_name="fde-handbook-maintainer")
    session_id = str(uuid.uuid4())
    await runner.session_service.create_session(app_name="fde-handbook-maintainer", user_id="github-actions", session_id=session_id)
    message = types.Content(role="user", parts=[types.Part.from_text(text=json.dumps(payload, sort_keys=True))])
    final = ""
    async for event in runner.run_async(user_id="github-actions", session_id=session_id, new_message=message):
        if event.is_final_response() and event.content and event.content.parts:
            final = "".join(part.text or "" for part in event.content.parts)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(final + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--candidate", type=Path, required=True)
    apply = subparsers.add_parser("apply")
    apply.add_argument("--candidate", type=Path, required=True)
    apply.add_argument("--repository", type=Path, required=True)
    apply.add_argument("--for-draft-pr", action="store_true", required=True)
    execute = subparsers.add_parser("run-agent")
    execute.add_argument("--signal", type=Path, required=True)
    execute.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "run-agent":
        if not os.environ.get("MODEL_NAME"):
            parser.error("MODEL_NAME must be explicitly configured")
        asyncio.run(run_agent(args.signal, args.output))
        return 0
    manifest = load_manifest(args.candidate / "proposal.json")
    errors = validate_manifest(manifest, args.candidate)
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    if args.command == "validate":
        return 0
    changed = apply_candidate_for_draft(args.repository.resolve(), args.candidate.resolve())
    print("\n".join(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
