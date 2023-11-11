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

conn = Connection(str(settings.rabbitmq_dsn), connect_timeout=3)


async def invalid_token_exc_handler(request, exc: InvalidTokenError):
    return JSONResponse(status_code=exc.status_code, content=exc.content)


@router.post("/{retailer_id}/transactions")
async def transactions(
    retailer_id: str,
    transactions: list[RetailTransaction],
) -> None:
    counter.labels(merchant_slug=retailer_id).inc()
    for transaction in transactions:
        message_queue.add(transaction.model_dump(), retailer_id=retailer_id, connection=conn)
