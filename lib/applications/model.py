import asyncio
import pickle

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from loguru import logger

from lib.settings import settings
from lib.types import FeaturesEvent, ModelResponseEvent, Queues

broker = RabbitBroker(str(settings.rabbit_mq_dsn))
app = FastStream(broker)

with open('lib/model.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)


@broker.subscriber(Queues.features)
@broker.publisher(Queues.y_pred)
async def handle(event: FeaturesEvent) -> ModelResponseEvent:
    prediction = regressor.predict([event.features])[0]
    logger.info(f"Received event: {event}, predicted: {prediction}")

    predict_mess = ModelResponseEvent(
        parent_id=event.event_id,
        teacher=event.teacher,
        prediction=prediction,
        created_at=event.created_at
    )
    logger.info(f"Published event: {predict_mess}")
    return predict_mess


if __name__ == "__main__":
    logger.add("logs/predictions_app.log")
    logger.info("Starting predictions consumer...")
    asyncio.run(app.run())
