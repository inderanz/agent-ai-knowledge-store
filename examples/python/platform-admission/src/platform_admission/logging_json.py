from __future__ import annotations

import json
import logging
import sys
from typing import Any


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        for name in (
            "correlation_id",
            "workload",
            "environment",
            "governed_cell",
            "policy_version",
            "outcome",
        ):
            value = getattr(record, name, None)
            if value is not None:
                payload[name] = value
        trace = getattr(record, "cloud_trace", None)
        if trace:
            payload["logging.googleapis.com/trace"] = trace
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=True)


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)

