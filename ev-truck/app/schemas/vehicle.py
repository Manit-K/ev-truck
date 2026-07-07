from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VehicleBase(BaseModel):
    external_id: str | None = Field(default=None, max_length=100)
    name: str = Field(min_length=1, max_length=150)
    license_plate: str = Field(min_length=1, max_length=50)
    battery_capacity_kwh: float = Field(gt=0)
    minimum_soc_percent: float = Field(default=20.0, ge=0, le=100)
    active: bool = True


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    external_id: str | None = Field(default=None, max_length=100)
    name: str | None = Field(default=None, min_length=1, max_length=150)
    license_plate: str | None = Field(default=None, min_length=1, max_length=50)
    battery_capacity_kwh: float | None = Field(default=None, gt=0)
    minimum_soc_percent: float | None = Field(default=None, ge=0, le=100)
    active: bool | None = None


class VehicleRead(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
