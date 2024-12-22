import asyncio

import numpy as np
from faststream.rabbit import RabbitBroker
from loguru import logger
from sklearn.datasets import load_diabetes

from lib.types import Queues, FeaturesEvent
from lib.settings import settings


async def main():
    np.random.seed(settings.random_seed)
    train_set, target_set = load_diabetes(return_X_y=True)
    async with RabbitBroker(str(settings.rabbit_mq_dsn)) as broker:
        while True:

            random_row = np.random.randint(0, train_set.shape[0] - 1)
            features_message = FeaturesEvent(
                teacher=target_set[random_row],
                features=train_set[random_row].tolist(),
            )

            await broker.publish(
                message=features_message,
                queue=Queues.features,
            )
            logger.info(f"Published message: {features_message}")

            await asyncio.sleep(settings.time_step)


if __name__ == "__main__":
    logger.add("logs/features_app.log")
    logger.info("Starting features producer...")
    asyncio.run(main())