# FDE documentation maintainer

This package provides the governed automation boundary for AI-assisted handbook
maintenance. It loads the repository skills through Google ADK, lets an author
agent research and stage candidate files in an isolated directory, requires a
separate reviewer agent, validates a signed-by-content manifest, and permits a
GitHub workflow to apply only declared files to a draft pull-request branch.

It never pushes to `main`, merges a pull request, changes customer cloud state,
or treats an agent review as customer risk acceptance.

## Local deterministic tests

```bash
PYTHONPATH=automation/fde-doc-maintainer/src \
  python3 -m unittest discover -s automation/fde-doc-maintainer/tests -v
```

## Runtime configuration

The ADK execution path requires `google-adk==2.6.1`, Vertex AI authentication,
an explicitly configured `MODEL_NAME`, and `FDE_REPOSITORY_ROOT` and
`FDE_CANDIDATE_DIR`. See the GitHub workflow and the operating guide under
`operations/fde-documentation-maintainer/`.
