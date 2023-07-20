from pydantic import BaseSettings, AmqpDsn


class Settings(BaseSettings):
    keyvault_uri: str | None = None
    rabbitmq_dsn: AmqpDsn = "amqp://guest:guest@localhost:5672"


settings = Settings()


ACTIVE_RETAILERS = ["costa", "test-retailer"]
