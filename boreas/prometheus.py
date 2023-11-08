"""Prometheus metrics for Boreas."""

from os import getenv

from fastapi import APIRouter
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, CollectorRegistry, Counter, generate_latest, multiprocess
from starlette.responses import Response
from starlette.status import HTTP_200_OK

counter = Counter("transactions_total", "Total requests", ["merchant_slug"])

router = APIRouter()


@router.get("/metrics")
async def metrics() -> None:
    """Return Prometheus metrics."""
    registry = REGISTRY

    if getenv("PROMETHEUS_MULTIPROC_DIR"):
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
    return Response(
        headers={"Content-Type": CONTENT_TYPE_LATEST},
        content=generate_latest(registry),
        status_code=HTTP_200_OK,
    )
