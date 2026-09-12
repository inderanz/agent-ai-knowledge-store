# Evidence contract

## Allowed authorities

| Claim | Primary authorities |
|---|---|
| Google product capability | `docs.cloud.google.com`, `cloud.google.com`, `adk.dev`, `developers.google.com` |
| Google implementation | `github.com/google`, `github.com/GoogleCloudPlatform`, `github.com/googleapis` |
| Google FDE role or field practice | `google.com/about/careers`, `cloud.google.com/blog` |
| OpenAI delivery practice | `openai.com`, `platform.openai.com`, `github.com/openai` |
| Anthropic delivery practice | `anthropic.com`, `docs.anthropic.com`, `github.com/anthropics`, or an Anthropic job linked through `job-boards.greenhouse.io/anthropic/` |

For this repository, current public Google FDE material is primary for the field
role contract. OpenAI and Anthropic evidence can inform a secondary cross-industry
comparison. It cannot establish a Gemini Enterprise Agent Platform capability,
support status, configuration, quota, location, security control, or API contract.

## Required evidence item

```json
{
  "source_id": "stable-kebab-id",
  "vendor": "google",
  "url": "https://docs.cloud.google.com/...",
  "locator": "heading, release tag, or repository path@commit",
  "retrieved_at": "YYYY-MM-DD",
  "tier": 1,
  "maturity": "GA|Preview|Experimental|Not applicable",
  "supports": "One narrowly scoped paraphrased claim",
  "content_sha256": "64 lowercase hexadecimal characters"
}
```

Tier 1 is official product documentation or release notes. Tier 2 is tagged official source. Tier 3 is an official sample. Tier 4 is official architecture or delivery guidance. Tier 5 is official role or engineering-practice material.

## Research packet

The packet must contain `schema_version`, `question`, `as_of`, `evidence`, `facts`, `inferences`, `unknowns`, and `affected_paths`. Preserve source wording in notes only when necessary and keep quotations short.
