# Automated upstream status

**Generated:** 2026-08-03 UTC by the scheduled documentation-maintenance workflow.

> [!IMPORTANT]
> This is an observation report, not the qualified repository baseline. Automation never
> changes `references/versions.json`, chapter claims, maturity labels, or `verified_at`
> dates. A human reviewer must compare official documentation and code, update affected
> material, and pass the repository review gates before a new baseline is accepted.

## Summary

| Check | Count |
|---|---:|
| Tracked release baselines | 7 |
| Release drifts requiring review | 0 |
| Release-query errors | 0 |
| Registered sources within review interval | 84 |
| Registered sources overdue | 0 |
| Invalid source records | 0 |

## Release comparison

| Dependency | Qualified baseline | Latest observed official release | State |
|---|---:|---:|---|
| `google-adk-python` | `2.6.1` | [`2.6.1`](https://github.com/google/adk-python/releases/tag/v2.6.1) | CURRENT |
| `google-cloud-aiplatform` | `1.163.0` | [`1.163.0`](https://github.com/googleapis/python-aiplatform/releases/tag/v1.163.0) | CURRENT |
| `googlecloudplatform-agent-starter-pack` | `0.41.3` | [`0.41.3`](https://github.com/GoogleCloudPlatform/agent-starter-pack/releases/tag/v0.41.3) | CURRENT |
| `googlecloudplatform-cloud-foundation-fabric` | `57.0.0` | [`57.0.0`](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/releases/tag/v57.0.0) | CURRENT |
| `terraform` | `1.15.8` | [`1.15.8`](https://github.com/hashicorp/terraform/releases/tag/v1.15.8) | CURRENT |
| `terraform-provider-google` | `7.42.0` | [`7.42.0`](https://github.com/hashicorp/terraform-provider-google/releases/tag/v7.42.0) | CURRENT |
| `googlecloudplatform-terraform-google-cloud-armor` | `8.1.1` | [`8.1.1`](https://github.com/GoogleCloudPlatform/terraform-google-cloud-armor/releases/tag/v8.1.1) | CURRENT |

## Sources requiring semantic re-verification

No registered source is overdue as of this report date.

## Required maintainer action

1. Open the official release, documentation, source tag, samples, and release notes.
2. Identify affected volumes, Terraform modules, examples, labs, runbooks, and claims.
3. Update code and prose together; preserve capability/recommendation/field-pattern labels.
4. Update `references/versions.json` only after implementation qualification.
5. Update a source's `verified_at` only after semantic review, not merely reachability.
6. Run all local and component CI gates and obtain required independent reviews.

See [the repository workflow](../README.md#how-documentation-stays-current) and [research policy](../docs/RESEARCH_AND_REVIEW.md).
