# Contributing

The repository accepts evidence-led changes that preserve the boundary between Google product capability and handbook recommendation.

## Required workflow

1. Open or select one chapter issue.
2. Create a feature branch named `chapter/<volume>-<chapter>-<slug>` or `maintenance/<slug>`.
3. Complete the research record before drafting prose.
4. Cite primary sources next to the claims they support.
5. Implement examples against the pinned baseline.
6. Run local quality checks.
7. Open a pull request and complete all six review gates.
8. Mark a chapter Approved only after all gates pass.

Research must precede writing. A contributor may update an existing draft only after comparing it with current upstream documentation, source, samples, and release notes.

## Local checks

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
python3 scripts/check_sources.py --offline
python3 scripts/validate_skills.py skills
PYTHONPATH=automation/fde-doc-maintainer/src \
  python3 -m unittest discover -s automation/fde-doc-maintainer/tests -v
```

Run `python3 scripts/check_sources.py` when network access is available.

## Pull request scope

A chapter pull request should contain one chapter, its diagrams, its runnable code or Terraform, its lab, its ADR, and its source-registry changes. Do not combine unrelated volume work.

## Agent-generated proposals

Agentic maintenance opens Draft pull requests only. Treat the author output and
the independent-agent verdict as untrusted proposal evidence. A human reviewer
must verify official sources, inspect the complete diff, confirm component tests,
resolve material findings and apply the normal six gates. Never approve because
the manifest, model summary or generated citations appear internally consistent.

Do not place customer confidential data, credentials, production traces, private
support material or non-public product information in a maintenance signal,
prompt, skill, candidate, pull request or workflow artifact.

## Review gates

- **Research review:** claims are current, sourced, and maturity-scoped.
- **Architecture review:** boundaries, failure modes, alternatives, and customer decisions are explicit.
- **Implementation review:** code is typed, tested, configurable, observable, and version-pinned.
- **Security review:** identity, authorization, data handling, abuse cases, audit, and supply chain are addressed.
- **Operations review:** telemetry, SLOs, runbooks, recovery, DR, capacity, and cost are actionable.
- **Customer delivery review:** discovery questions, workshop artifacts, decisions, and acceptance criteria are usable by an FDE.

## Unsupported claims

If an official source cannot be found, remove the claim or label it as a recommendation/field pattern. Do not infer undocumented API behavior, service guarantees, regional availability, or support status.
