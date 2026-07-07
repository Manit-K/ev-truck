from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class GoogleSheetSyncRequest(BaseModel):
    sheet_id: str | None = None
    sheet_range: str | None = None


class VehicleReadingImport(BaseModel):
    source_record_id: str | None = None
    vehicle_id: int | None = None
    vehicle_external_id: str | None = None
    trip_id: int | None = None
    recorded_at: datetime
    soc_percent: float | None = Field(default=None, ge=0, le=100)
    energy_used_kwh: float | None = Field(default=None, ge=0)
    distance_km: float | None = Field(default=None, ge=0)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @model_validator(mode="after")
    def vehicle_reference_required(self) -> "VehicleReadingImport":
        if self.vehicle_id is None and not self.vehicle_external_id:
            raise ValueError("vehicle_id or vehicle_external_id is required")
        return self


class ImportBatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    status: str
    sheet_id: str | None
    sheet_range: str | None
    total_rows: int
    imported_rows: int
    updated_rows: int
    skipped_rows: int
    failed_rows: int
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None


def normalize_sheet_row(headers: list[str], values: list[Any]) -> dict[str, Any]:
    return {
        header.strip(): values[index] if index < len(values) and values[index] != "" else None
        for index, header in enumerate(headers)
        if header.strip()
    }
