# Source registry

`sources.json` records authoritative sources, ownership, evidence tier, verification date, and review interval. `versions.json` records dated tool and platform baselines. `BASELINE.md` explains the current human-readable baseline and product naming caveats.

Update the registry in the same pull request as any claim or baseline change. Run `python3 scripts/check_sources.py` to check reachability and freshness.
