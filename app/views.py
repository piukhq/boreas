from typing import Dict, List

from fastapi import APIRouter, Depends, FastAPI, Response
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.models import APIKey
from kombu import Connection
from starlette.responses import JSONResponse

import settings
from app import message_queue
from app.exceptions import InvalidTokenError
from app.security import get_api_key

root_app = FastAPI(title="Harmonia Transactions API", openapi_url="/openapi.json")

api_router = APIRouter()


@root_app.exception_handler(InvalidTokenError)
async def invalid_token_exc_handler(request, exc: InvalidTokenError):
    return JSONResponse(status_code=exc.status_code, content=exc.content)


@root_app.exception_handler(RequestValidationError)
async def unprocessable_entity_handler(request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error_message": "Invalid JSON", "error_slug": "MALFORMED_REQUEST"})


@api_router.post("/{merchant_id}/transactions")
async def transactions(
    merchant_id: str,
    body: List[Dict],
    response: Response,
    api_key: APIKey = Depends(get_api_key),
) -> dict:
    with Connection(settings.RABBITMQ_DSN, connect_timeout=3) as conn:
        for transaction in body:
            message_queue.add(transaction, merchant_id=merchant_id, connection=conn)
    response.status_code = 200
    return response
