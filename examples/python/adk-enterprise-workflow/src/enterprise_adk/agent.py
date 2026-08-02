"""ADK v2.6.1 graph entry point.

The graph verifies and stages a command. It deliberately does not make the
irreversible write: a customer-owned command handler must call
EnterpriseWorkflow with a durable ToolGateway and authenticated principals.
"""

from __future__ import annotations

from typing import Any

from google.adk import Context, Event, Workflow
from google.adk.events import RequestInput
from google.adk.workflow import JoinNode, node


def normalize(node_input: dict[str, Any]) -> dict[str, Any]:
    required = {
        "request_id", "tenant_id", "action", "target", "justification",
        "risk", "parameters", "requested_by", "principal_subject",
    }
    if not isinstance(node_input, dict):
        raise ValueError("workflow input must be an object")
    missing = required - set(node_input)
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")
    return {key: node_input[key] for key in sorted(required)}


def verify_identity(node_input: dict[str, Any]) -> dict[str, Any]:
    return {
        "check": "identity_binding",
        "passed": node_input["principal_subject"] == node_input["requested_by"],
    }


def verify_contract(node_input: dict[str, Any]) -> dict[str, Any]:
    return {
        "check": "contract",
        "passed": (
            node_input["risk"] in {"low", "high"}
            and isinstance(node_input["parameters"], dict)
            and bool(str(node_input["justification"]).strip())
        ),
    }


join_checks = JoinNode(name="join_checks")


def route_checks(node_input: dict[str, dict[str, Any]]) -> Event:
    passed = all(result.get("passed") is True for result in node_input.values())
    return Event(route="accepted" if passed else "denied")


def stage_command(node_input: dict[str, dict[str, Any]]) -> Event:
    return Event(
        output={
            "status": "READY_FOR_POLICY_AND_APPROVAL",
            "checks": node_input,
            "boundary": "no external side effect executed",
        }
    )


def deny(node_input: dict[str, dict[str, Any]]) -> Event:
    return Event(output={"status": "DENIED", "checks": node_input})


@node(rerun_on_resume=True, timeout=30)
async def bounded_dynamic_checks(ctx: Context, node_input: list[dict[str, Any]]) -> list[Any]:
    """Example dynamic section with explicit fan-out and a hard task bound."""
    if len(node_input) > 10:
        raise ValueError("dynamic task budget exceeds 10")
    results: list[Any] = []
    for index, item in enumerate(node_input):
        result = await ctx.run_node(
            verify_contract,
            node_input=item,
            run_id=f"contract-{index}",
            use_sub_branch=True,
        )
        results.append(result)
    return results


def request_non_authoritative_input() -> RequestInput:
    """UX interrupt example only; never treat its response as enterprise authz."""
    return RequestInput(
        interrupt_id="clarification",
        message="Provide the missing non-sensitive request clarification.",
        response_schema=str,
    )


root_agent = Workflow(
    name="enterprise_change_workflow",
    max_concurrency=4,
    edges=[
        ("START", normalize, (verify_identity, verify_contract), join_checks, route_checks),
        (route_checks, {"accepted": stage_command, "denied": deny}),
    ],
)
