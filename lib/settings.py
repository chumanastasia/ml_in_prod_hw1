from pydantic import AmqpDsn, PositiveInt
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    metric_log_path: Path = Path("logs/metric_log.csv")
    time_step: PositiveInt = 4
    random_seed: PositiveInt = 43
    rabbit_mq_dsn: AmqpDsn = "amqp://guest:guest@rabbitmq:5672/"


settings = Settings()