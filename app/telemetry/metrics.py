"""
Metrics module.

Environment variables:
- OTLP_ENDPOINT - OTLP endpoint
- OTLP_SERVICE_NAME - OTLP service name
"""

import os

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

otlp_service_name = os.getenv("OTLP_SERVICE_NAME", __name__)
otlp_endpoint = os.getenv("OTLP_ENDPOINT", None)


def configure_metrics():
    """Configuration of telemetry metrics."""
    if not otlp_endpoint:
        return

    exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
    reader = PeriodicExportingMetricReader(exporter)
    resource = Resource(attributes={SERVICE_NAME: otlp_service_name})
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)
