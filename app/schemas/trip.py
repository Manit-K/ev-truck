from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TripBase(BaseModel):
    vehicle_id: int
    driver_id: int | None = None
    external_id: str | None = Field(default=None, max_length=100)
    origin: str = Field(min_length=1, max_length=255)
    destination: str = Field(min_length=1, max_length=255)
    status: str = Field(default="planned", max_length=30)
    planned_distance_km: float = Field(ge=0)
    actual_distance_km: float | None = Field(default=None, ge=0)
    planned_energy_kwh: float = Field(ge=0)
    actual_energy_kwh: float | None = Field(default=None, ge=0)
    starting_soc_percent: float | None = Field(default=None, ge=0, le=100)
    ending_soc_percent: float | None = Field(default=None, ge=0, le=100)
    scheduled_start: datetime | None = None
    actual_start: datetime | None = None
    actual_end: datetime | None = None


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    vehicle_id: int | None = None
    driver_id: int | None = None
    external_id: str | None = Field(default=None, max_length=100)
    origin: str | None = Field(default=None, min_length=1, max_length=255)
    destination: str | None = Field(default=None, min_length=1, max_length=255)
    status: str | None = Field(default=None, max_length=30)
    planned_distance_km: float | None = Field(default=None, ge=0)
    actual_distance_km: float | None = Field(default=None, ge=0)
    planned_energy_kwh: float | None = Field(default=None, ge=0)
    actual_energy_kwh: float | None = Field(default=None, ge=0)
    starting_soc_percent: float | None = Field(default=None, ge=0, le=100)
    ending_soc_percent: float | None = Field(default=None, ge=0, le=100)
    scheduled_start: datetime | None = None
    actual_start: datetime | None = None
    actual_end: datetime | None = None


class TripRead(TripBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class MetricComparison(BaseModel):
    planned: float
    actual: float | None
    variance: float | None
    variance_percent: float | None


class PlanVsActual(BaseModel):
    trip_id: int
    distance_km: MetricComparison
    energy_kwh: MetricComparison
    planned_ending_soc_percent: float | None
    actual_ending_soc_percent: float | None
