from enum import StrEnum
from datetime import datetime

from pydantic import BaseModel, Field


class Queues(StrEnum):
    y_true = "y_true"
    y_pred = "y_pred"
    features = "features"
    metrics = "metrics"

class FeaturesEvent(BaseModel):
    event_id: float = Field(default_factory=lambda: datetime.timestamp(datetime.now()))
    teacher: float
    features: list[float]
    created_at: datetime = Field(default_factory=datetime.now)
    timestamp: float = Field(default_factory=lambda: datetime.timestamp(datetime.now()))


class ModelResponseEvent(BaseModel):
    event_id: float = Field(default_factory=lambda: datetime.timestamp(datetime.now()))
    parent_id: float
    teacher: float
    prediction: float
    created_at: datetime
    timestamp: float = Field(default_factory=lambda: datetime.timestamp(datetime.now()))


class MetricEvent(BaseModel):
    id: float
    y_true: float
    y_pred: float
    absolute_error: float
