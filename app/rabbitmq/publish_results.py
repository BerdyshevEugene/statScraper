import json

from aio_pika import (
    connect_robust,
    Message,
    DeliveryMode,
    RobustConnection,
    RobustChannel,
)

from logger.logger import setup_logger
from app.config import settings

logger = setup_logger(module_name=__name__)

RABBITMQ_URL = settings.rabbitmq_url
QUEUE_NAME = settings.queue_name

_connection: RobustConnection | None = None
_channel: RobustChannel | None = None


async def publish_results(data: dict):
    global _connection, _channel

    try:
        if _connection is None or _connection.is_closed:
            logger.debug("🔌 connecting to RabbitMQ...")
            _connection = await connect_robust(RABBITMQ_URL)
            _channel = await _connection.channel()
            await _channel.declare_queue(QUEUE_NAME, durable=True)
            logger.success("📡 rabbitMQ connection established")

        message = Message(
            body=json.dumps(data).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        await _channel.default_exchange.publish(message, routing_key=QUEUE_NAME)
        logger.success(f"✅ published to queue '{QUEUE_NAME}': {data}")

    except Exception as e:
        logger.error(f"❌ failed to publish message: {e}")
