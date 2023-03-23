import logging

import kombu
from kombu import Connection, Exchange, Queue

log = logging.getLogger(__name__)


def _on_error(exc, interval):
    log.warning(f"Failed to connect to RabbitMQ: {exc}. Will retry after {interval:.1f}s...")


def add(message: dict, *, merchant_id: str, connection: Connection) -> None:
    queue_name = f"{merchant_id}-transactions"
    dl_exchange_name = f"{merchant_id}-dl-exchange"
    dl_queue_name = f"{merchant_id}-dl-queue"
    dl_exchange = Exchange(dl_exchange_name, type="fanout")
    transactions_queue = Queue(
        queue_name,
        queue_arguments={
            "x-max-length": 1,
            "x-dead-letter-routing-key": dl_queue_name,
            "x-dead-letter-exchange": dl_exchange_name,
        },
    )
    dl_queue = kombu.Queue(f"{merchant_id}-dl-queue", exchange=dl_exchange)

    connection.ensure_connection(
        errback=_on_error, max_retries=3, interval_start=0.2, interval_step=0.4, interval_max=1, timeout=3
    )
    producer = connection.Producer(serializer="json")
    producer.publish(
        message,
        headers={"x-provider": merchant_id},
        routing_key=queue_name,
        declare=[dl_exchange, dl_queue, transactions_queue],
    )
