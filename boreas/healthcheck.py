"""Healthcheck endpoints for the Boreas API."""

from fastapi import APIRouter
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR

from boreas.message_queue import is_available

router = APIRouter()


@router.get("/readyz")
async def readyz() -> None:
    """Healthcheck: Return a HTTP 200 OK response if the message queue is available."""
    queue_available = is_available()
    if not queue_available:
        return Response(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=HTTP_200_OK)


@router.get("/livez")
async def livez() -> None:
    """Healthcheck: Immediately return a HTTP 204 No Content response."""
    Response(status_code=HTTP_204_NO_CONTENT)
