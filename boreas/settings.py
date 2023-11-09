from pydantic import AmqpDsn, HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    keyvault_uri: str | None = None
    rabbitmq_dsn: AmqpDsn = "amqp://guest:guest@localhost:5672"
    sentry_dsn: HttpUrl | None = None
    sentry_environment: str = "local"


settings = Settings()


ACTIVE_RETAILERS = ["costa", "test-retailer"]
