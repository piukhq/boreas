"""Settings for Boreas."""

from pydantic import AmqpDsn, HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for Boreas."""

    keyvault_uri: HttpUrl = "https://uksouth-prod-qj46.vault.azure.net/"
    rabbitmq_dsn: AmqpDsn = "amqp://guest:guest@localhost:5672"
    sentry_dsn: HttpUrl = "https://3da15a03d0ceedea0c4b0f5c862e711e@o503751.ingest.sentry.io/4506190606041088"
    sentry_environment: str = "production"


settings = Settings()
