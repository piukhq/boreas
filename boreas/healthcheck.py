from fastapi import APIRouter
from kombu import Connection
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR

from boreas.settings import settings

router = APIRouter()


@router.get("/readyz")
async def readyz() -> None:
    try:
        with Connection(settings.rabbitmq_dsn, connect_timeout=3) as conn:
            conn.connect()
            return Response(status_code=HTTP_200_OK)
    except ConnectionRefusedError:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": [
                    {
                        "msg": "Cannot connect to AMQP",
                        "type": "Internal Server Error",
                    }
                ]
            },
        )


@router.get("/livez")
async def livez() -> None:
    Response(status_code=HTTP_204_NO_CONTENT)
