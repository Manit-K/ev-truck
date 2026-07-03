from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OptimizationJobCreate(BaseModel):
    trip_id: int
    minimum_soc_percent: float | None = Field(default=None, ge=0, le=100)


class OptimizationRecommendationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rule_code: str
    severity: str
    message: str
    observed_value: float | None
    threshold_value: float | None
    created_at: datetime


class OptimizationJobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trip_id: int
    status: str
    energy_variance_threshold_percent: float
    distance_variance_threshold_percent: float
    minimum_soc_percent: float | None
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None
    recommendations: list[OptimizationRecommendationRead]
