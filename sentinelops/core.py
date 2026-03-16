from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import threading
import psutil
import time
import sys

SENTINEL_ENDPOINT = "app.sentinelops.page:4317"

def init(api_key: str, service_name: str = "my-service", endpoint: str = SENTINEL_ENDPOINT):
    resource = Resource(attributes={
        "service.name": service_name,
        "sentinelops.api_key": api_key
    })

    exporter = OTLPSpanExporter(
        endpoint=endpoint,
        insecure=True,
        headers={"api-key": api_key}
    )

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # Auto-instrument Flask
    try:
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
        FlaskInstrumentor().instrument()
        print("[SentinelOps] Flask instrumented")
    except Exception:
        pass

    # Auto-instrument FastAPI
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        FastAPIInstrumentor().instrument()
        print("[SentinelOps] FastAPI instrumented")
    except Exception:
        pass

    # Auto-instrument Django
    try:
        from opentelemetry.instrumentation.django import DjangoInstrumentor
        DjangoInstrumentor().instrument()
        print("[SentinelOps] Django instrumented")
    except Exception:
        pass

    # Auto-instrument SQLAlchemy
    try:
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
        SQLAlchemyInstrumentor().instrument()
        print("[SentinelOps] SQLAlchemy instrumented")
    except Exception:
        pass

    # Auto-instrument Psycopg2
    try:
        from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
        Psycopg2Instrumentor().instrument()
        print("[SentinelOps] Psycopg2 instrumented")
    except Exception:
        pass

    # Auto-instrument Redis
    try:
        from opentelemetry.instrumentation.redis import RedisInstrumentor
        RedisInstrumentor().instrument()
        print("[SentinelOps] Redis instrumented")
    except Exception:
        pass

    # Auto-instrument Requests
    try:
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        RequestsInstrumentor().instrument()
        print("[SentinelOps] Requests instrumented")
    except Exception:
        pass

    # Auto-instrument Celery
    try:
        from opentelemetry.instrumentation.celery import CeleryInstrumentor
        CeleryInstrumentor().instrument()
        print("[SentinelOps] Celery instrumented")
    except Exception:
        pass

    # Exception hook
    _setup_exception_hook()

    # Background threads
    threading.Thread(target=_collect_metrics, args=(api_key,), daemon=True).start()

    print(f"[SentinelOps] Initialized for service '{service_name}'")


def _setup_exception_hook():
    original_excepthook = sys.excepthook

    def custom_excepthook(exc_type, exc_value, exc_traceback):
        tracer = trace.get_tracer("sentinelops.exceptions")
        with tracer.start_as_current_span("sentinelops.exception") as span:
            span.set_attribute("exception.type", exc_type.__name__)
            span.set_attribute("exception.message", str(exc_value))
            span.set_attribute("sentinelops.metric_type", "exception")
            span.record_exception(exc_value)
        original_excepthook(exc_type, exc_value, exc_traceback)

    sys.excepthook = custom_excepthook


def _collect_metrics(api_key: str):
    tracer = trace.get_tracer("sentinelops.metrics")
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            with tracer.start_as_current_span("sentinelops.infra.metrics") as span:
                span.set_attribute("metric.cpu_percent", cpu)
                span.set_attribute("metric.memory_percent", memory)
                span.set_attribute("metric.disk_percent", disk)
                span.set_attribute("sentinelops.metric_type", "infra")

            if cpu > 90:
                print(f"[SentinelOps] WARNING — CPU at {cpu}%")
            if memory > 90:
                print(f"[SentinelOps] WARNING — Memory at {memory}%")
            if disk > 90:
                print(f"[SentinelOps] WARNING — Disk at {disk}%")

        except Exception:
            pass
        time.sleep(30)