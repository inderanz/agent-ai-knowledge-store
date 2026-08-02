# Volumes 4–10 delivery gates

This validation build runs the dependency-free production qualification toolkit,
the shared qualification-record validator, repository integrity, and source
freshness metadata. It intentionally performs no cloud deployment or IAM change.

Each volume supplies a customer-owned qualification record. `--production`
requires every named gate to be explicitly `true`, an exact environment, project,
location, source revision, and accountable owners. A boolean is only an index to
external immutable evidence; it must never replace the report, test output, plan,
approval, or incident exercise itself.
