from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, offset: int = 0, limit: int = 100) -> list[Vehicle]:
        return list(self.db.scalars(select(Vehicle).offset(offset).limit(limit)))

    def get(self, vehicle_id: int) -> Vehicle | None:
        return self.db.get(Vehicle, vehicle_id)

    def get_by_external_id(self, external_id: str) -> Vehicle | None:
        return self.db.scalar(select(Vehicle).where(Vehicle.external_id == external_id))

    def create(self, data: VehicleCreate) -> Vehicle:
        vehicle = Vehicle(**data.model_dump())
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def update(self, vehicle: Vehicle, data: VehicleUpdate) -> Vehicle:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(vehicle, field, value)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self.db.delete(vehicle)
        self.db.commit()
