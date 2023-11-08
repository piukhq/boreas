"""Message queue module."""
import logging

from kombu import Connection, Queue

from boreas.settings import settings

log = logging.getLogger(__name__)


def _on_error(exc: Exception, interval: int) -> None:
    log.warning("Failed to connect to RabbitMQ", extra={"err": exc, "retry_in": interval})


def add(message: dict, *, retailer_id: str, connection: Connection) -> None:
    """Add a message to the queue."""
    queue_name = f"tx-{retailer_id}-harmonia"
    transactions_queue = Queue(queue_name)
    connection.ensure_connection(
        errback=_on_error,
        max_retries=3,
        interval_start=0.2,
        interval_step=0.4,
        interval_max=1,
        timeout=3,
    )
    producer = connection.Producer(serializer="json")
    producer.publish(
        message,
        headers={"x-provider": retailer_id},
        routing_key=queue_name,
        declare=[transactions_queue],
    )


def is_available() -> bool:
    """Check if the message queue is available."""
    status = False
    try:
        with Connection(str(settings.rabbitmq_dsn), connect_timeout=3) as conn:
            conn.connect()
            status = True
    except Exception as err:
        log.exception("Failed to connect to queue", extra={"err": err})
    return status
