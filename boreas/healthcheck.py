from fastapi import APIRouter
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR

from boreas.message_queue import is_available

router = APIRouter()


@router.get("/readyz")
async def readyz() -> None:
    queue_available = is_available()
    if queue_available[0]:
        return Response(status_code=HTTP_200_OK)
    else:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": [
                    {
                        "msg": queue_available[1],
                        "type": "Internal Server Error",
                    }
                ]
            },
        )


@router.get("/livez")
async def livez() -> None:
    Response(status_code=HTTP_204_NO_CONTENT)
