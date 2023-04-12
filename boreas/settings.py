from pydantic import BaseSettings


class Settings(BaseSettings):
    keyvault_uri: str | None = None
    rabbitmq_user: str = "guest"
    rabbitmq_pass: str = "guest"
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672

    @property
    def rabbitmq_dsn(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_pass}@{self.rabbitmq_host}:{self.rabbitmq_port}//"


settings = Settings()


ACTIVE_RETAILERS = ["costa", "test-retailer"]
