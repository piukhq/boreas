"""Views for the Boreas API."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from kombu import Connection
from starlette.responses import JSONResponse

from boreas import message_queue
from boreas.exceptions import InvalidTokenError
from boreas.models import RetailTransaction
from boreas.prometheus import counter
from boreas.security import get_api_key
from boreas.settings import settings

router = APIRouter(
    prefix="/retailers",
    dependencies=[Depends(get_api_key)],
)


async def invalid_token_exc_handler(exc: InvalidTokenError) -> JSONResponse:
    """Response for exceptions raised by the API Key security dependency."""
    # This is returning an exception as a response, which is not ideal, consider better messaging.
    return JSONResponse(status_code=exc.status_code, content=exc.content)


@router.post("/{retailer_id}/transactions")
async def transactions(
    retailer_id: str,
    transactions: list[RetailTransaction],
) -> None:
    """Receive a list of transactions from a retailer."""
    counter.labels(merchant_slug=retailer_id).inc()
    with Connection(settings.rabbitmq_dsn, connect_timeout=3) as conn:
        for transaction in transactions:
            message_queue.add(transaction.dict(), retailer_id=retailer_id, connection=conn)
