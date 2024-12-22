import asyncio
import csv
from pathlib import Path

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from loguru import logger

from lib.types import ModelResponseEvent, Queues, MetricEvent
from lib.settings import settings

metric_log_path = Path("logs/metric_log.csv")
filed_names = ['id', 'y_true','y_pred','absolute_error']

broker = RabbitBroker(str(settings.rabbit_mq_dsn))
app = FastStream(broker)


@broker.subscriber(Queues.y_pred)
@broker.publisher(Queues.metrics)
async def handle(event: ModelResponseEvent) -> MetricEvent:
    logger.info(f"Received event: {event}")

    abs_error = abs(event.prediction - event.teacher)
    with open(metric_log_path, mode='a', newline='\n') as file:
        writer = csv.DictWriter(file, fieldnames=filed_names)
        log_row = MetricEvent(
            id=event.event_id,
            y_true=event.teacher,
            y_pred=round(event.prediction, 3),
            absolute_error=round(abs_error, 3)
        )
        writer.writerow(log_row.model_dump())

        logger.info(f"Logged event: {log_row}")

    return log_row


if __name__ == "__main__":
    if not metric_log_path.exists():
        raise FileNotFoundError(f"File {metric_log_path} not found")

    logger.add("logs/metric_app.log")
    logger.info("Starting evaluation consumer...")
    asyncio.run(app.run())
