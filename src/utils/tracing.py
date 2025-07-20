import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src.constants import PROJECT_NAME


def setup_tracer(app):
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: 'model-inference'})
        )
    )

    host = os.getenv('JAEGER_NAME', 'jaeger')
    port = os.getenv('JAEGER_PORT', '4317')

    tracer_provider = trace.get_tracer_provider()
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=f'http://{host}:{port}',
                insecure=True
            )
        )
    )

    FastAPIInstrumentor.instrument_app(app)


TRACER = trace.get_tracer(PROJECT_NAME)
