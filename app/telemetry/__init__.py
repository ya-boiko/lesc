from .metrics import metrics
from .traces import configure_traces, trace, current_trace_context, extract_trace_context, TRACE_CONTEXT_KEY


def configure(database_engine):
    """Telemetry configuration."""
    # Temporarily disabled as we use Jaeger which doesn't support metrics
    # configure_metrics()

    configure_traces(database_engine)


__all__ = [
    "TRACE_CONTEXT_KEY",
    "configure",
    "metrics",
    "trace",
    "current_trace_context",
    "extract_trace_context",
]
