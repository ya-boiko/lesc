"""
Traces instrumentation module.

Environment variables:
- OTLP_ENDPOINT - OTLP endpoint
- OTLP_SERVICE_NAME - OTLP service name
"""

import os
from contextvars import ContextVar
from typing import List, Optional

from opentelemetry import trace
from opentelemetry.context import Context
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


OTLP_SERVICE_NAME = os.getenv("OTLP_SERVICE_NAME", __name__)
OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", None)

TRACE_CONTEXT_KEY = "x-source-trace-context"


def configure_traces(database_engine):
    """Configures telemetry collection."""
    if not OTLP_ENDPOINT:
        return

    resource = Resource(attributes={SERVICE_NAME: OTLP_SERVICE_NAME})
    exporter = OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True)
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    RequestsInstrumentor().instrument()

    SQLAlchemyInstrumentor().instrument(enable_commenter=True, engine=database_engine)


def current_trace_context() -> dict:
    """
    Provide trace context of the current span.
    """

    carrier = {}

    # Write the current context into the carrier.
    # A TextMapPropagator works with any dict-like object as its Carrier by default.
    TraceContextTextMapPropagator().inject(carrier)

    return carrier


def extract_trace_context(carrier: dict | None = None) -> Context | None:
    """Provide trace context of the current span."""
    if carrier is None:
        return None

    return TraceContextTextMapPropagator().extract(carrier=carrier)


# Used for storing links to the span contexts.
span_context_links: ContextVar[Optional[List[trace.Link]]] = ContextVar("span_context_links", default=None)
