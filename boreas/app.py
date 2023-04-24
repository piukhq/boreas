from fastapi import FastAPI

from boreas import healthcheck, prometheus, views
from boreas.exceptions import InvalidTokenError
from boreas.views import invalid_token_exc_handler


def create_app() -> FastAPI:
    app = FastAPI(title="Retail Transactions API")

    app.include_router(views.router)
    app.include_router(healthcheck.router)
    app.include_router(prometheus.router)
    app.add_exception_handler(InvalidTokenError, invalid_token_exc_handler)

    return app
