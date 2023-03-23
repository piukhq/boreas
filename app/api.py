from fastapi import FastAPI

from app.views import api_router, root_app


def create_app() -> FastAPI:
    root_app.include_router(
        api_router,
        prefix="/retailers",
    )
    return root_app
