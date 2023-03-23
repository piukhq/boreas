import logging
from typing import Any, Type

import kombu
import settings
from kombu.mixins import ConsumerMixin

MAX_RESEND = 3

log = logging.getLogger("harmonia-transactions-dead-letter-consumer")


class DeadLetterConsumer(ConsumerMixin):
    @staticmethod
    def make_queues():
        return [kombu.Queue(name=f"{merchant_id}-dl-queue") for merchant_id in settings.ACTIVE_MERCHANTS]

    def __init__(self, connection: kombu.Connection) -> None:
        self.connection = connection

    def get_consumers(self, Consumer: Type[kombu.Consumer], channel: Any) -> list[kombu.Consumer]:  # pragma: no cover
        return [Consumer(queues=self.make_queues(), callbacks=[self.on_message])]

    def on_message(self, body: dict, message: kombu.Message) -> None:  # pragma: no cover
        headers = message.headers
        resend_count = headers["x-death"][0]["count"]
        merchant_id = headers["x-provider"]
        if resend_count > MAX_RESEND:
            log.debug(
                f"Message for transaction {body['transaction_id']} not delivered to Harmonia "
                f"after {MAX_RESEND} attempts."
            )
            message.reject()
        else:
            delay = 300 * resend_count
            log.debug(
                f"Resending message for transaction {body['transaction_id']} to Harmonia. "
                f"Next attempt {resend_count} in {delay/60} minutes"
            )
            producer = self.connection.Producer(serializer="json")
            producer.publish(
                body, headers=message.headers, routing_key=f"{merchant_id}-transactions", properties={"x-delay": delay}
            )


def main():
    with kombu.Connection(settings.RABBITMQ_DSN) as conn:
        consumer = DeadLetterConsumer(conn)
        consumer.run()


if __name__ == "__main__":
    main()
