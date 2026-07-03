from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.vehicle_reading import VehicleReading


class VehicleReadingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_source_record(self, source: str, record_id: str) -> VehicleReading | None:
        return self.db.scalar(
            select(VehicleReading).where(
                VehicleReading.source == source,
                VehicleReading.source_record_id == record_id,
            )
        )

    def upsert(self, values: dict) -> tuple[VehicleReading, bool]:
        reading = self.get_by_source_record(values["source"], values["source_record_id"])
        created = reading is None
        if reading is None:
            reading = VehicleReading(**values)
            self.db.add(reading)
        else:
            for field, value in values.items():
                setattr(reading, field, value)
        self.db.flush()
        return reading, created
