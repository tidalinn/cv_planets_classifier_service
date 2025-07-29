import time
from typing import Any

from fastapi import Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

request_count = Counter(
    'app_request_count',
    'Total number of requests',
    ['method', 'endpoint', 'http_status']
)

request_latency = Histogram(
    'app_request_latency_seconds',
    'Request latency',
    ['method', 'endpoint']
)


async def metrics_middleware(request: Request, call_next) -> Any:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    endpoint = request.url.path
    request_count.labels(request.method, endpoint, str(response.status_code)).inc()
    request_latency.labels(request.method, endpoint).observe(process_time)

    return response


def metrics_handler() -> Response:
    metrics = generate_latest()
    return Response(content=metrics, media_type=CONTENT_TYPE_LATEST)
