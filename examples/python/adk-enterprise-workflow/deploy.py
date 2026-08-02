#!/usr/bin/env python3
"""Guarded Agent Runtime deployment using the current official AdkApp route."""

from __future__ import annotations

import argparse
import json
import re
import sys


ADK_VERSION = "2.6.1"
AIPLATFORM_VERSION = "1.163.0"
_PROJECT = re.compile(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$")
_LOCATION = re.compile(r"^[a-z]+-[a-z]+[0-9]+$")
_BUCKET = re.compile(r"^gs://[a-z0-9][a-z0-9._-]{1,220}[a-z0-9]$")


def build_config(project: str, location: str, staging_bucket: str,
                 service_account: str | None) -> dict:
    if not _PROJECT.fullmatch(project):
        raise ValueError("invalid Google Cloud project ID")
    if not _LOCATION.fullmatch(location):
        raise ValueError("invalid Google Cloud location")
    if not _BUCKET.fullmatch(staging_bucket):
        raise ValueError("staging bucket must be an explicit gs:// URI")
    if service_account and not service_account.endswith(f"@{project}.iam.gserviceaccount.com"):
        raise ValueError("service account must belong to the target project")
    config = {
        "display_name": "enterprise-adk-workflow",
        "description": "Governed ADK graph workflow qualification deployment",
        "requirements": [
            f"google-adk=={ADK_VERSION}",
            f"google-cloud-aiplatform[agent_engines,adk]=={AIPLATFORM_VERSION}",
        ],
        "staging_bucket": staging_bucket,
        "labels": {"volume": "3", "managed-by": "customer-delivery-pipeline"},
    }
    if service_account:
        config["service_account"] = service_account
    return {"project": project, "location": location, "config": config}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument("--staging-bucket", required=True)
    parser.add_argument("--service-account")
    parser.add_argument("--execute", action="store_true",
                        help="create the billable remote Agent Runtime resource")
    parser.add_argument("--confirm-project",
                        help="must exactly match --project when --execute is used")
    args = parser.parse_args()
    deployment = build_config(args.project, args.location, args.staging_bucket,
                              args.service_account)
    if not args.execute:
        print(json.dumps(deployment, indent=2, sort_keys=True))
        return 0
    if args.confirm_project != args.project:
        parser.error("--execute requires --confirm-project to exactly match --project")

    from vertexai import Client, agent_engines, types
    from enterprise_adk.agent import root_agent

    config = dict(deployment["config"])
    config["identity_type"] = types.IdentityType.AGENT_IDENTITY
    app = agent_engines.AdkApp(agent=root_agent)
    client = Client(project=args.project, location=args.location)
    remote_agent = client.agent_engines.create(agent=app, config=config)
    print(remote_agent.api_resource.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
