from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sentinelops",
    version="0.1.1",
    description="Observability SDK for SentinelOps - instrument your app in 2 lines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nathanael Fetue",
    packages=find_packages(),
    install_requires=[
        "opentelemetry-api>=1.20.0",
        "opentelemetry-sdk>=1.20.0",
        "opentelemetry-exporter-otlp-proto-grpc>=1.20.0",
        "opentelemetry-instrumentation-flask>=0.41b0",
        "opentelemetry-instrumentation-fastapi>=0.41b0",
        "psutil>=5.9.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "django": ["opentelemetry-instrumentation-django>=0.41b0"],
        "sqlalchemy": ["opentelemetry-instrumentation-sqlalchemy>=0.41b0"],
    },
    python_requires=">=3.8",
)