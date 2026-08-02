# Volumes 11–15 delivery gates

This pack validates the five control-plane/app handbooks without deploying cloud
resources. Every `true` value in a production record is an index to immutable,
customer-owned evidence—not a substitute for a report, test, approval or drill.

Run `python3 -m unittest discover -s delivery/volumes-11-15 -p 'test_*.py' -v`.
Run a record with `python3 delivery/volumes-11-15/validate_qualification.py
labs/volume-11-agent-registry/qualification.example.json --production`; the
example must fail because it contains placeholders and false evidence.
