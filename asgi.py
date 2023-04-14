from fastapi import FastAPI

from boreas import healthcheck, prometheus, views
from boreas.exceptions import InvalidTokenError
from boreas.views import invalid_token_exc_handler

app = FastAPI(title="Retail Transactions API")
app.include_router(views.router)
app.include_router(healthcheck.router)
app.include_router(prometheus.router)
app.add_exception_handler(InvalidTokenError, invalid_token_exc_handler)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
