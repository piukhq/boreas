import logging
from typing import Tuple

from kombu import Connection, Queue

from boreas.settings import settings

log = logging.getLogger(__name__)


_conn: Connection | None = None


async def queue_connection() -> Connection:
    global _conn
    if _conn is None:
        _conn = Connection(str(settings.rabbitmq_dsn), connect_timeout=3)
    return _conn


def _on_error(exc, interval):
    log.warning(f"Failed to connect to RabbitMQ: {exc}. Will retry after {interval:.1f}s...")


def add(message: dict, *, retailer_id: str, connection: Connection) -> None:
    queue_name = f"tx-{retailer_id}-harmonia"
    transactions_queue = Queue(queue_name)
    connection.ensure_connection(
        errback=_on_error, max_retries=3, interval_start=0.2, interval_step=0.4, interval_max=1, timeout=3
    )
    producer = connection.Producer(serializer="json")
    producer.publish(
        message,
        headers={"x-provider": retailer_id},
        routing_key=queue_name,
        declare=[transactions_queue],
    )


def is_available() -> Tuple[bool, str]:
    status, error_msg = True, ""

    try:
        with Connection(str(settings.rabbitmq_dsn), connect_timeout=3) as conn:
            conn.connect()
            assert conn.connected
    except Exception as err:
        status = False
        error_msg = f"Failed to connect to queue, err: {err}"

    return status, error_msg
