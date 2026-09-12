# FDE customer adoption delivery kit

This kit turns the [customer adoption playbook](../../docs/FDE_CUSTOMER_ADOPTION_PLAYBOOK.md)
and [Google FDE operating model](../../docs/GOOGLE_FDE_OPERATING_MODEL.md) into a
machine-checkable engagement record. Keep real customer records in the
customer-approved system; do not commit confidential information here.

Start from `customer-engagement.example.json`, replace every synthetic value, and
validate the record:

```bash
python3 delivery/fde-adoption/validate_engagement.py customer-record.json
```

Before claiming production readiness:

```bash
python3 delivery/fde-adoption/validate_engagement.py customer-record.json --production
```

Production mode requires Level 4 or higher, non-synthetic evidence, all six gates,
customer sign-offs, outcome evidence, rollback and runbook artifacts, and passed
handover competency. The validator proves record completeness, not the truth of
customer evidence.
