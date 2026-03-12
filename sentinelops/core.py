from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import threading
import psutil
import time

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

    # Auto-instrument Flask if present
    try:
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
        FlaskInstrumentor().instrument()
        print("[SentinelOps] Flask instrumented")
    except Exception:
        pass

    # Auto-instrument FastAPI if present
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        FastAPIInstrumentor().instrument()
        print("[SentinelOps] FastAPI instrumented")
    except Exception:
        pass

    threading.Thread(target=_collect_metrics, args=(api_key,), daemon=True).start()
    print(f"[SentinelOps] Initialized for service '{service_name}'")


def _collect_metrics(api_key: str):
    while True:
        try:
            metrics = {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent
            }
        except Exception:
            pass
        time.sleep(30)