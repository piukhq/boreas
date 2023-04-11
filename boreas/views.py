from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.models import APIKey
from kombu import Connection
from starlette.responses import JSONResponse

from boreas import message_queue
from boreas.exceptions import InvalidTokenError
from boreas.models import RetailTransaction
from boreas.security import get_api_key
from boreas.settings import settings

app = FastAPI(title="Retail Transactions API")


@app.exception_handler(InvalidTokenError)
async def invalid_token_exc_handler(request, exc: InvalidTokenError):
    return JSONResponse(status_code=exc.status_code, content=exc.content)


@app.exception_handler(RequestValidationError)
async def unprocessable_entity_handler(request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error_message": "Invalid JSON", "error_slug": "MALFORMED_REQUEST"})


@app.post("/retailers/{retailer_id}/transactions")
async def transactions(
    retailer_id: str,
    transactions: list[RetailTransaction],
    api_key: APIKey = Depends(get_api_key),
) -> None:
    with Connection(settings.rabbitmq_dsn, connect_timeout=3) as conn:
        for transaction in transactions:
            message_queue.add(transaction.dict(), retailer_id=retailer_id, connection=conn)
