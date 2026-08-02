from __future__ import annotations

from contextlib import nullcontext
import logging
from typing import Any

from .configuration import Settings

LOGGER = logging.getLogger(__name__)


class Telemetry:
    def __init__(self, tracer: Any = None) -> None:
        self._tracer = tracer

    def span(self, name: str, attributes: dict[str, str] | None = None) -> Any:
        if self._tracer is None:
            return nullcontext()
        return self._tracer.start_as_current_span(name, attributes=attributes or {})


def configure_telemetry(settings: Settings) -> Telemetry:
    if not settings.otel_enabled:
        return Telemetry()
    try:
        import google.auth
        import google.auth.transport.grpc
        import google.auth.transport.requests
        import grpc
        from google.auth.transport.grpc import AuthMetadataPlugin
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import SERVICE_NAME, Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased

        credentials, _ = google.auth.default()
        request = google.auth.transport.requests.Request()
        plugin = AuthMetadataPlugin(credentials=credentials, request=request)
        channel_credentials = grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(),
            grpc.metadata_call_credentials(plugin),
        )
        provider = TracerProvider(
            resource=Resource.create({SERVICE_NAME: "platform-admission"}),
            sampler=ParentBased(TraceIdRatioBased(settings.trace_sample_ratio)),
        )
        provider.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporter(
                    credentials=channel_credentials,
                    endpoint=settings.otlp_endpoint,
                )
            )
        )
        trace.set_tracer_provider(provider)
        return Telemetry(trace.get_tracer("platform.admission"))
    except Exception:
        LOGGER.exception("OpenTelemetry initialization failed")
        if settings.otel_required:
            raise
        return Telemetry()

