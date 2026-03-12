# SentinelOps Python SDK

Instrument your Python app in 2 lines.

## Installation

pip install sentinelops

## Usage

from sentinelops import init
init(api_key="your-api-key", service_name="your-service")

That's it. SentinelOps will automatically:
- Instrument Flask, FastAPI, or Django
- Collect traces and send them to your dashboard
- Monitor CPU, memory, and disk in the background

## Supported frameworks

- Flask
- FastAPI
- Django (pip install sentinelops[django])
- Any Python app

## Dashboard

View your traces and anomalies at https://app.sentinelops.page