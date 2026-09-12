#!/usr/bin/env python3
"""Build an evidence-constrained research report from a WhatsApp link archive."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


AS_OF = date(2026, 8, 4)
USER_AGENT = "agent-ai-knowledge-store-link-research/1.0"
GITHUB_FIELDS = (
    "nameWithOwner,description,homepageUrl,stargazerCount,forkCount,issues,"
    "pullRequests,latestRelease,licenseInfo,primaryLanguage,isArchived,isPrivate,"
    "pushedAt,updatedAt,url,isSecurityPolicyEnabled"
)


@dataclass
class LinkRecord:
    url: str
    first_seen: str
    message: str
    occurrences: int = 1
    seen_dates: list[str] = field(default_factory=list)


@dataclass
class Probe:
    requested_url: str
    final_url: str = ""
    status: str = ""
    content_type: str = ""
    title: str = ""
    evidence: str = "Not fetched"


def run(command: list[str], *, cwd: Path | None = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def parse_archive(path: Path) -> list[LinkRecord]:
    text = path.read_text(encoding="utf-8")
    records: dict[str, LinkRecord] = {}
    for block in re.split(r"\n(?=## \d+\.)", text):
        heading = re.search(r"^## \d+\. (\d{4}-\d{2}-\d{2})", block)
        if not heading:
            continue
        seen = heading.group(1)
        message_match = re.search(r"Message:\s*\n\n```\n(.*?)\n```", block, flags=re.S)
        message = message_match.group(1).strip() if message_match else ""
        for raw_url in re.findall(r"^  - <([^>]+)>$", block, flags=re.M):
            url = raw_url if raw_url.startswith(("http://", "https://")) else f"https://{raw_url}"
            if url in records:
                records[url].occurrences += 1
                records[url].seen_dates.append(seen)
            else:
                records[url] = LinkRecord(url, seen, message, seen_dates=[seen])
    return list(records.values())


def github_repo(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.hostname != "github.com":
        return None
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2 or parts[0] in {"features", "issues", "marketplace", "orgs", "topics"}:
        return None
    return "/".join(parts[:2])


def repository_metadata(repo: str) -> dict[str, Any]:
    result = run(["gh", "repo", "view", repo, "--json", GITHUB_FIELDS], timeout=45)
    if result.returncode:
        return {"nameWithOwner": repo, "error": result.stderr.strip() or "gh query failed"}
    return json.loads(result.stdout)


def probe_page(url: str) -> Probe:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if host in {"share.google", "lnkd.in"}:
        return Probe(url, evidence="Restricted short link; destination not independently verified")
    if host in {"drive.usercontent.google.com"}:
        return Probe(url, evidence="Direct download intentionally not fetched")
    if host == "github.com":
        return Probe(url, final_url=url, status="API", evidence="GitHub API and local clone")
    target = url
    if host == "arxiv.org" and parsed.path.startswith("/pdf/"):
        target = url.replace("/pdf/", "/abs/", 1)
    command = [
        "curl",
        "--location",
        "--silent",
        "--show-error",
        "--connect-timeout",
        "5",
        "--max-time",
        "15",
        "--max-filesize",
        "524288",
        "--range",
        "0-262143",
        "--user-agent",
        USER_AGENT,
        "--write-out",
        "\n__LINK_META__%{http_code}\t%{url_effective}\t%{content_type}",
        target,
    ]
    try:
        result = run(command, timeout=18)
    except (subprocess.TimeoutExpired, OSError):
        return Probe(url, evidence="Fetch timed out")
    output = result.stdout
    marker = output.rfind("\n__LINK_META__")
    body = output[:marker] if marker >= 0 else output
    metadata = output[marker + len("\n__LINK_META__") :] if marker >= 0 else ""
    fields = metadata.split("\t", 2)
    status = fields[0] if fields else ""
    final_url = fields[1] if len(fields) > 1 else ""
    content_type = fields[2] if len(fields) > 2 else ""
    title = ""
    if "html" in content_type.lower() or "<title" in body[:200000].lower():
        candidates = (
            re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)', body, re.I),
            re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']', body, re.I),
            re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S),
        )
        for candidate in candidates:
            if candidate:
                title = re.sub(
                    r"\s+", " ", html.unescape(html.unescape(candidate.group(1)))
                ).strip()
                break
    if title:
        evidence = "Live page metadata"
    elif status and status not in {"000", "403", "401", "404", "410"}:
        evidence = "Reachable page; title unavailable"
    elif status:
        evidence = f"HTTP {status}; content not independently readable"
    else:
        evidence = "Page fetch failed"
    return Probe(url, final_url=final_url, status=status, content_type=content_type, title=title, evidence=evidence)


def fallback_label(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "unknown").removeprefix("www.")
    path = unquote(parsed.path).strip("/")
    if not path:
        return host
    leaf = path.split("/")[-1]
    leaf = re.sub(r"[-_]+", " ", leaf)
    leaf = re.sub(r"\s+", " ", leaf).strip()
    if leaf.lower() in {"viewform", "mobilebasic", "edit", "information"} and len(path.split("/")) > 1:
        leaf = f"{host} shared resource"
    return leaf[:140] or host


def useful_title(title: str) -> bool:
    normalized = re.sub(r"\s+", " ", title).strip().lower()
    return normalized not in {
        "",
        "just a moment...",
        "linkedin",
        "sign in - google accounts",
        "error",
        "not found",
    }


def github_identification(url: str, metadata: dict[str, Any]) -> tuple[str, str]:
    """Return a link label and detail for a repository or exact GitHub sub-resource."""
    repo = github_repo(url) or str(metadata.get("nameWithOwner", "GitHub repository"))
    parts = urlparse(url).path.strip("/").split("/")
    suffix = parts[2:]
    description = metadata.get("description") or "No repository description supplied"
    if not suffix:
        return repo, description
    if len(suffix) >= 2 and suffix[0] == "issues" and suffix[1].isdigit():
        result = run(
            ["gh", "issue", "view", suffix[1], "--repo", repo, "--json", "title,state,updatedAt"],
            timeout=30,
        )
        if result.returncode == 0:
            issue = json.loads(result.stdout)
            detail = f"GitHub issue ({issue.get('state', 'state unknown')}): {issue.get('title', '')}"
            return f"{repo} issue #{suffix[1]}", detail
        return f"{repo} issue #{suffix[1]}", "Issue details were not independently readable"
    if len(suffix) >= 3 and suffix[0] in {"blob", "tree"}:
        item = "/".join(suffix[2:])
        noun = "file" if suffix[0] == "blob" else "directory"
        return f"{repo} — {item}", f"Repository {noun}; parent repository: {description}"
    return f"{repo} — {'/'.join(suffix)}", description


def link_kind(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path = parsed.path.lower()
    if github_repo(url):
        if any(segment in path for segment in ("/blob/", "/tree/", "/issues/")):
            return "Repository sub-resource"
        return "Repository"
    if "linkedin.com/jobs" in f"{host}{path}" or any(
        token in f"{host}{path}" for token in ("myworkdayjobs", "/careers/", "greenhouse.io", "/job/")
    ):
        return "Job/role"
    if host == "www.linkedin.com" and "/in/" in path:
        return "Professional profile"
    if host == "www.linkedin.com" and ("/posts/" in path or "/pulse/" in path):
        return "Social/article"
    if host == "arxiv.org":
        return "Research paper"
    if "youtube" in host or host == "youtu.be":
        return "Video/playlist"
    if host in {"bit.ly", "lnkd.in", "share.google", "goo.gle"}:
        return "Short link"
    if host in {"docs.google.com", "drive.google.com", "drive.usercontent.google.com", "chatgpt.com", "claude.ai"}:
        return "Shared/private resource"
    if any(token in host for token in ("kaggle.com", "codelabs.developers.google.com", "deeplearning.ai", "skills.google")):
        return "Course/lab"
    if host == "pypi.org":
        return "Package"
    if any(token in host for token in ("medium.com", "substack.com", "blog", "thenewstack.io", "seroter.com", "glaforge.dev", "intoai.pub", "towardsdatascience.com")):
        return "Article"
    if any(token in host for token in ("docs.", "developer.", "developers.", "compliance-framework.github.io", "sre.google")):
        return "Documentation/guide"
    if any(token in host for token in ("bestinbeds", "snooze.com.au", "vicway.com.au", "maps.app.goo.gl")):
        return "Non-AI/personal"
    if host in {"www.apra.gov.au", "www.digital.nsw.gov.au"}:
        return "Policy/regulation"
    return "Website/resource"


def fde_use(kind: str, text: str, url: str) -> str:
    haystack = f"{text} {url}".lower()
    if kind == "Non-AI/personal":
        return "No direct agentic-AI/FDE use verified; keep outside the technical learning backlog."
    if kind in {"Job/role", "Professional profile"}:
        return "Extract role expectations and customer-facing competencies; verify that the listing/profile is still current."
    if kind == "Policy/regulation":
        return "Use as a dated governance input when designing controls for Australian customer deployments."
    if kind == "Shared/private resource" or kind == "Short link":
        return "Open and verify access/content before adding it to a learning or delivery plan."
    if kind == "Research paper":
        return "Read the methods and reproduce relevant claims in a small benchmark before adopting the approach."
    if kind in {"Course/lab", "Video/playlist"}:
        return "Use as a hands-on learning module; save the resulting code and an evaluation note as portfolio evidence."
    if any(word in haystack for word in ("security", "secure", "policy", "guardrail", "sandbox", "threat", "compliance")):
        return "Use to design least-privilege tools, approval gates, isolation, audit trails, and security tests."
    if any(word in haystack for word in ("eval", "quality", "benchmark", "test")):
        return "Use to build task datasets, graders, regression gates, and trace-based quality reviews."
    if any(word in haystack for word in ("memory", "context", "rag", "retrieval", "embedding", "knowledge graph", "ontology")):
        return "Use in a context/retrieval prototype; measure relevance, freshness, tenant isolation, latency, and cost."
    if any(word in haystack for word in ("mcp", "a2a", "protocol", "tool", "interoperab")):
        return "Use to prototype governed tool/data interoperability and document auth, schemas, failure modes, and auditability."
    if any(word in haystack for word in ("cost", "token", "inference", "cache", "efficient")):
        return "Use in a cost/performance experiment and record quality, latency, token, and infrastructure trade-offs."
    if any(word in haystack for word in ("sre", "incident", "slo", "reliable", "observab", "production")):
        return "Use to define production SLOs, traces, runbooks, rollback paths, and operational readiness checks."
    if any(word in haystack for word in ("scrap", "crawl", "document", "pdf", "data")):
        return "Use as an ingestion/data-preparation option; test permission boundaries, extraction quality, and provenance."
    if kind.startswith("Repository"):
        return "Evaluate in an isolated proof of concept against a concrete customer requirement; inspect licence, tests, releases, and security posture first."
    if kind in {"Article", "Documentation/guide", "Social/article"}:
        return "Treat as a dated learning input; extract one testable practice and validate it against primary documentation or code."
    return "Use only after confirming the resource solves a specific customer-delivery or agent-engineering gap."


def local_repo_dir(root: Path, repo: str) -> Path:
    owner, name = repo.split("/", 1)
    return root / "knowledge-repos" / f"{owner}--{name}"


def tree_entries(repo_dir: Path) -> set[str]:
    result = run(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=repo_dir)
    return {line.strip().lower() for line in result.stdout.splitlines() if line.strip()}


def days_since(raw: str | None) -> int | None:
    if not raw:
        return None
    parsed = datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
    return (AS_OF - parsed).days


def repo_kind(metadata: dict[str, Any]) -> str:
    text = f"{metadata.get('nameWithOwner', '')} {metadata.get('description', '')}".lower()
    if any(word in text for word in ("tutorial", "workshop", "roadmap", "sample", "awesome", "learn it")):
        return "Learning/reference"
    if "specification" in text or "standard specification" in text:
        return "Specification"
    if "framework" in text or "toolkit" in text:
        return "Framework/toolkit"
    return "Product/tool"


def maturity(metadata: dict[str, Any], entries: set[str]) -> dict[str, int | str]:
    if metadata.get("error"):
        return {"activity": 0, "adoption": 0, "release": 0, "docs": 0, "quality": 0, "governance": 0, "total": 0, "band": "Unverified"}
    pushed_days = days_since(metadata.get("pushedAt"))
    if metadata.get("isArchived"):
        activity = 0
    elif pushed_days is None:
        activity = 0
    elif pushed_days <= 30:
        activity = 20
    elif pushed_days <= 90:
        activity = 16
    elif pushed_days <= 180:
        activity = 12
    elif pushed_days <= 365:
        activity = 8
    else:
        activity = 3
    stars = int(metadata.get("stargazerCount") or 0)
    adoption = 20 if stars >= 10000 else 16 if stars >= 3000 else 12 if stars >= 1000 else 8 if stars >= 100 else 4 if stars >= 10 else 1
    latest = metadata.get("latestRelease") or {}
    release_days = days_since(latest.get("publishedAt"))
    release = 4 if release_days is None else 20 if release_days <= 90 else 16 if release_days <= 180 else 12 if release_days <= 365 else 8
    has_readme = any(Path(item).name.startswith("readme") for item in entries)
    has_docs = any(item.startswith(("docs/", "documentation/")) for item in entries)
    has_examples = any(item.startswith(("examples/", "example/", "samples/")) for item in entries)
    docs = (8 if has_readme else 0) + (4 if has_docs else 0) + (3 if has_examples else 0)
    has_tests = any(item.startswith(("tests/", "test/")) or "/tests/" in item for item in entries)
    has_ci = any(item.startswith(".github/workflows/") for item in entries)
    has_build = any(Path(item).name in {"pyproject.toml", "package.json", "go.mod", "cargo.toml", "build.gradle", "pom.xml"} for item in entries)
    quality = (8 if has_tests else 0) + (4 if has_ci else 0) + (3 if has_build else 0)
    has_license = bool(metadata.get("licenseInfo")) or any(Path(item).name.startswith(("license", "copying")) for item in entries)
    has_security = bool(metadata.get("isSecurityPolicyEnabled")) or any(Path(item).name.startswith("security") for item in entries)
    has_contributing = any(Path(item).name.startswith("contributing") for item in entries)
    has_community = any(Path(item).name in {"code_of_conduct.md", "codeowners"} for item in entries)
    governance = (4 if has_license else 0) + (3 if has_security else 0) + (2 if has_contributing else 0) + (1 if has_community else 0)
    total = activity + adoption + release + docs + quality + governance
    band = "Very strong public repo signals" if total >= 85 else "Established public repo signals" if total >= 70 else "Growing public repo signals" if total >= 55 else "Early public repo signals" if total >= 40 else "Experimental/resource-level signals"
    return {"activity": activity, "adoption": adoption, "release": release, "docs": docs, "quality": quality, "governance": governance, "total": total, "band": band}


def clean_cell(value: Any, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    text = text.replace("|", "\\|").replace("\n", " ")
    return text[:limit]


def md_link(label: str, url: str) -> str:
    return f"[{clean_cell(label, 140)}](<{url}>)"


def build_report(source: Path, output: Path, workspace: Path, workers: int) -> None:
    links = parse_archive(source)
    repos: list[str] = []
    for record in links:
        repo = github_repo(record.url)
        if repo and repo not in repos:
            repos.append(repo)

    repo_metadata: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=min(workers, 8)) as executor:
        futures = {executor.submit(repository_metadata, repo): repo for repo in repos}
        for future in as_completed(futures):
            repo_metadata[futures[future]] = future.result()

    probes: dict[str, Probe] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(probe_page, record.url): record.url for record in links}
        for future in as_completed(futures):
            probes[futures[future]] = future.result()

    score_rows: list[tuple[str, dict[str, Any], dict[str, int | str], set[str]]] = []
    for repo in repos:
        metadata = repo_metadata[repo]
        clone = local_repo_dir(workspace, repo)
        entries = tree_entries(clone) if (clone / ".git").is_dir() else set()
        score_rows.append((repo, metadata, maturity(metadata, entries), entries))
    score_rows.sort(key=lambda row: (-int(row[2]["total"]), row[0].lower()))

    category_counts = Counter(link_kind(record.url) for record in links)
    live_count = sum(probe.evidence in {"Live page metadata", "GitHub API and local clone"} for probe in probes.values())
    restricted_count = sum("not independently" in probe.evidence.lower() or "failed" in probe.evidence.lower() or "timed out" in probe.evidence.lower() for probe in probes.values())

    lines: list[str] = []
    lines.extend(
        [
            "# WhatsApp Links Research: Agentic AI FDE Knowledge Map",
            "",
            "- **Start here:** [Agentic AI FDE Navigator](START_HERE.md)",
            "- Browse cloned projects: [Knowledge Repositories Index](knowledge-repos/README.md)",
            f"- Source archive: [{source.name}]({source.name})",
            f"- Research as of: `{AS_OF.isoformat()}` (Australia/Melbourne)",
            f"- Coverage: **{len(links)} unique links** from **{sum(record.occurrences for record in links)} URL occurrences**",
            f"- GitHub coverage: **{len(repos)} distinct repositories cloned** into [`knowledge-repos/`](knowledge-repos/)",
            f"- Direct verification: **{live_count}** links via live page metadata or GitHub API/local clone; **{restricted_count}** links explicitly marked restricted/unresolved",
            "",
            "## Evidence and no-hallucination policy",
            "",
            "A literal zero-error guarantee is not possible for changing web content. This report instead applies a strict evidence rule: factual descriptions come from the linked page metadata, official GitHub repository metadata, or the cloned repository; inaccessible, private, expired, or opaque short links are marked as such. FDE-use recommendations and maturity scores are explicitly assessments, not vendor claims. Dates and availability states must be rechecked before a customer decision.",
            "",
            "Repository star, fork, release, licence, issue, and activity data were queried from GitHub on the research date. Clones are shallow and blob-filtered, with a sparse review checkout containing top-level documentation, governance files, manifests, and workflows.",
            "",
            "## Executive recommendation for your FDE journey",
            "",
            "1. **Learn the operating model:** start with the agent architecture, context-engineering, evaluation, and prototype-to-production resources in the archive. Turn each into a one-page decision record, not just reading notes.",
            "2. **Build one vertical slice:** use Google ADK or Pydantic AI Harness for an agent, connect one governed MCP/data tool, add retrieval only if the task requires it, and deploy in a sandboxed runtime.",
            "3. **Make quality observable:** create task datasets, deterministic checks, model graders where needed, traces, latency/cost budgets, and failure taxonomies before expanding autonomy.",
            "4. **Practise FDE delivery:** frame the customer problem, map systems and policy constraints, ship a measurable pilot, run adoption workshops, and leave a production/readiness handover.",
            "5. **Build a portfolio from evidence:** retain architecture decisions, eval results, threat model, SLOs, cost analysis, and a short customer-outcome narrative for each project.",
            "",
            "## Time-sensitive platform findings",
            "",
            "| Platform/topic | Verified status on the research date | FDE implication | Primary source |",
            "|---|---|---|---|",
            "| Google-managed MCP servers | Platform-level availability became GA on 2026-05-01; Google states individual servers can be Preview or GA. | Check the supported-product status for every server and design IAM/audit controls per tool. | [Official release notes](https://docs.cloud.google.com/mcp/release-notes) |",
            "| Cloud Run sandboxes | Preview/Pre-GA. Google documents isolated execution for untrusted code and agent tools. | Good for experiments and controlled pilots; apply Pre-GA risk treatment before customer production. | [Official documentation](https://docs.cloud.google.com/run/docs/configuring/services/sandboxes) |",
            "| Vertex AI Agent Engine | Managed runtime and observability are documented as GA; several context/evaluation capabilities are Preview. | Treat each sub-service independently in architecture and risk reviews. | [Official overview](https://cloud.google.com/vertex-ai/generative-ai/docs/reasoning-engine/overview) |",
            "| Gemini CLI / Antigravity CLI | Google’s repository announcement states that individual-account Gemini CLI service ended on 2026-06-18 and transitioned to Antigravity CLI; enterprise licences and API-key authentication were stated as unaffected. | Do not build a new individual learning workflow around old Gemini CLI assumptions without checking the current path. | [Official GitHub announcement](https://github.com/google-gemini/gemini-cli/discussions/28017) |",
            "| Agent evaluation | Anthropic recommends moving beyond ad-hoc testing to tasks, repeated trials, graders, and transcripts/traces for multi-turn agents. | Make evals a delivery workstream from the pilot, not a final QA step. | [Anthropic engineering](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) |",
            "",
            "## Product/repository maturity scorecard",
            "",
            "This is a **public-repository evidence score**, not a security certification or guarantee of product fitness. Maximum 100: activity 20, adoption 20, release discipline 20, documentation/examples 15, tests/CI/build signals 15, and governance/security/licence signals 10. Resource collections, workshops, tutorials, and specifications are identified so they are not mistaken for deployable products.",
            "",
            "| Repository | Kind | Score | Evidence band | Activity | Adoption | Releases | Docs | Quality | Governance | Stars | Latest release | Last push |",
            "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|",
        ]
    )
    for repo, metadata, score, _entries in score_rows:
        release = metadata.get("latestRelease") or {}
        lines.append(
            "| "
            + " | ".join(
                [
                    md_link(repo, metadata.get("url") or f"https://github.com/{repo}"),
                    repo_kind(metadata),
                    f"**{score['total']}**",
                    str(score["band"]),
                    str(score["activity"]),
                    str(score["adoption"]),
                    str(score["release"]),
                    str(score["docs"]),
                    str(score["quality"]),
                    str(score["governance"]),
                    str(metadata.get("stargazerCount", "?")),
                    clean_cell(f"{release.get('tagName', 'none')} {str(release.get('publishedAt', ''))[:10]}"),
                    clean_cell(str(metadata.get("pushedAt", ""))[:10]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "### How to read the score",
            "",
            "- A high score means the public repository shows stronger maintenance, adoption, release, documentation, engineering, and governance signals. It does **not** prove enterprise security, support, data residency, or suitability for a customer workload.",
            "- A low score can be appropriate for a tutorial, specification, workshop, or focused utility. Assess those artifacts by learning value or standards fit rather than treating the number as a product verdict.",
            "- Before customer use, add licence compatibility, dependency/SBOM review, vulnerability scanning, maintainer/bus-factor review, performance tests, privacy review, and support/exit planning.",
            "",
            "## Products that are similar or overlap",
            "",
            "| Capability cluster | Similar/overlapping products | Where they overlap | Important distinction to test |",
            "|---|---|---|---|",
            "| Web and document ingestion | Scrapling; ScrapeGraphAI; MinerU; RAG-Anything | Acquire or transform external/unstructured content for agents. | Scrapling/ScrapeGraphAI focus on web acquisition; MinerU converts complex documents; RAG-Anything adds multimodal RAG. Test provenance, extraction fidelity, permissions, and update handling. |",
            "| Knowledge and code context | Graphify; gortex; AWS Context Ontology Accelerator; Google Knowledge Catalog samples | Make structured context discoverable/queryable for agents. | Graphify/gortex centre on code intelligence; ontology/catalog approaches centre on semantic enterprise context. Test incremental updates, explainability, tenancy, and retrieval quality. |",
            "| Agent frameworks and meta-harnesses | Google ADK; Pydantic AI Harness; Omnigent; atlas-agents; exxperts; Aiden | Build or operate agents with tools, state, and orchestration. | ADK/Pydantic are developer toolkits; Omnigent abstracts multiple harnesses; exxperts emphasizes governed local memory; Aiden emphasizes computer operation. Choose from workload and control requirements, not feature count. |",
            "| Memory and long-horizon work | MemMachine; Hivemind; Beads; exxperts | Preserve useful state beyond one model turn/session. | MemMachine is an agent memory layer; Hivemind turns traces into shared skills; Beads persists dependency-aware work; exxperts gates what is remembered. Evaluate privacy, deletion, freshness, conflict handling, and retrieval precision. |",
            "| Agent skills and harness optimization | addyosmani/agent-skills; Bright Data skills; ECC; loop-engineering; Pydantic AI Harness | Package repeatable agent behavior and improve harness performance. | Some are reusable instructions, some are domain integrations, and some are full optimization/tooling systems. Test portability and measure outcomes on your own tasks. |",
            "| Evaluation, security, and operations | OpenAI Evals; Uber ADR; Specula; cctop; agent-flow | Observe, test, or secure agent behavior. | Evals measures behavior; ADR focuses on security/observability; Specula targets deep system bugs; cctop monitors sessions; agent-flow visualizes orchestration. They are complementary more often than substitutes. |",
            "| Token/context efficiency | RTK; gortex; Graphify; loop-engineering | Reduce irrelevant context or make agent loops more efficient. | RTK compresses command output; gortex/Graphify retrieve code context; loop-engineering shapes orchestration. Benchmark total task success, not token reduction alone. |",
            "| FDE/career enablement | Awesome FDE Roadmap; career-ops; ai-assisted-job-search; ai-engineering-from-scratch | Build skills, portfolio evidence, and job-search workflow. | These are learning/career resources, not production agent platforms. Validate advice against current role descriptions and your target market. |",
            "",
            "## Suggested build sequence from this collection",
            "",
            "| Stage | Build artifact | Best-fit resources from the collection | Exit evidence |",
            "|---|---|---|---|",
            "| 1. Problem framing | Customer workflow map, baseline, risk constraints, success metric | FDE roadmap and role links; agent architecture/policy articles | Signed problem statement and measurable baseline |",
            "| 2. Thin agent | One bounded workflow with explicit tools and human checkpoints | Google ADK or Pydantic AI Harness; Anthropic agent-pattern guidance | Reproducible demo and architecture decision record |",
            "| 3. Context/data | One permissioned data source with citations/provenance | Managed MCP, Context Forge, MinerU/RAG-Anything, Graphify, MemMachine as needed | Retrieval/extraction eval and tenant-isolation test |",
            "| 4. Quality/security | Task suite, graders, traces, threat model, approval gates | OpenAI Evals, Uber ADR, Specula, Cloud Run sandboxes, compliance resources | Regression gate, security test results, incident/rollback plan |",
            "| 5. Production/adoption | Deployment, SLOs, cost budget, training and handover | Agent Engine/Cloud Run/SRE resources; FDE adoption practices | SLO dashboard, runbook, cost report, adoption metric |",
            "",
            "## Clone manifest",
            "",
            "| Repository | Local review path | HEAD | Clone status |",
            "|---|---|---|---|",
        ]
    )
    for repo in sorted(repos, key=str.lower):
        clone = local_repo_dir(workspace, repo)
        result = run(["git", "rev-parse", "--short=12", "HEAD"], cwd=clone) if (clone / ".git").is_dir() else None
        head = result.stdout.strip() if result and result.returncode == 0 else "—"
        status = "Shallow, blob-filtered, sparse review checkout" if head != "—" else "Clone unavailable"
        relative = clone.relative_to(workspace).as_posix()
        lines.append(f"| {md_link(repo, f'https://github.com/{repo}')} | [`{relative}/`]({relative}/) | `{head}` | {status} |")

    lines.extend(
        [
            "",
            "## Link-by-link research catalogue",
            "",
            "The catalogue preserves every unique link. “URL/context only” means the page itself was not independently readable; the label may come from the URL slug or the surrounding WhatsApp message and is not treated as a verified page title.",
            "",
            "| # | First seen | Link and verified identification | Type | FDE use | Verification |",
            "|---:|---|---|---|---|---|",
        ]
    )
    for index, record in enumerate(links, start=1):
        probe = probes[record.url]
        repo = github_repo(record.url)
        if repo and repo in repo_metadata:
            metadata = repo_metadata[repo]
            title, description = github_identification(record.url, metadata)
            identification = f"{md_link(title, record.url)} — {clean_cell(description)}"
            recommendation_text = f"{title} {description}"
        elif useful_title(probe.title):
            identification = md_link(probe.title, record.url)
            recommendation_text = probe.title
        else:
            source_match = re.fullmatch(r"Source:\s*([^\n]+?)\s+https?://\S+", record.message.strip())
            source_hint = f"Source: {source_match.group(1).strip()}" if source_match else ""
            redirect_label = fallback_label(probe.final_url) if probe.final_url and probe.final_url != record.url else ""
            label = source_hint or redirect_label or fallback_label(record.url)
            identification = f"{md_link(label or fallback_label(record.url), record.url)} — title not independently verified"
            recommendation_text = f"{label} {fallback_label(record.url)}"
        kind = link_kind(record.url)
        recommendation_kind = kind
        if probe.final_url and probe.final_url != record.url and kind == "Short link":
            destination_kind = link_kind(probe.final_url)
            if destination_kind != kind:
                kind = f"Short link → {destination_kind}"
                recommendation_kind = destination_kind
        verification = probe.evidence
        if probe.final_url and probe.final_url != record.url and urlparse(record.url).hostname in {"bit.ly", "goo.gle", "maps.app.goo.gl"}:
            verification += f"; resolved to {md_link(fallback_label(probe.final_url), probe.final_url)}"
        if record.occurrences > 1:
            verification += f"; {record.occurrences} occurrences"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    record.first_seen,
                    clean_cell(identification, 4000),
                    kind,
                    clean_cell(
                        fde_use(
                            recommendation_kind,
                            recommendation_text,
                            f"{record.url} {probe.final_url}",
                        ),
                        300,
                    ),
                    clean_cell(verification, 3000),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Coverage summary",
            "",
            "| Link type | Unique links |",
            "|---|---:|",
        ]
    )
    for kind, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {kind} | {count} |")
    lines.extend(
        [
            "",
            "## Revalidation checklist",
            "",
            "- Recheck all Preview/Pre-GA and role/job links before relying on them.",
            "- Manually open restricted `share.google`, `lnkd.in`, private Drive/Docs, ChatGPT share, and Claude artifact links; do not infer their content from this report.",
            "- Refresh GitHub metadata and rerun dependency/security review before selecting a repository for customer work.",
            "- For every pilot, validate product claims with a task-specific benchmark, threat model, cost model, and operational readiness review.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    build_report(args.source.resolve(), args.output.resolve(), args.workspace.resolve(), max(1, args.workers))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
