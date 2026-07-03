from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.vehicle import Vehicle
from app.repositories.vehicle import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleConflictError(Exception):
    pass


class VehicleService:
    def __init__(self, db: Session):
        self.repository = VehicleRepository(db)
        self.db = db

    def list(self, offset: int, limit: int) -> list[Vehicle]:
        return self.repository.list(offset, limit)

    def get(self, vehicle_id: int) -> Vehicle | None:
        return self.repository.get(vehicle_id)

    def create(self, data: VehicleCreate) -> Vehicle:
        try:
            return self.repository.create(data)
        except IntegrityError as exc:
            self.db.rollback()
            raise VehicleConflictError("Vehicle external ID or license plate already exists") from exc

    def update(self, vehicle: Vehicle, data: VehicleUpdate) -> Vehicle:
        try:
            return self.repository.update(vehicle, data)
        except IntegrityError as exc:
            self.db.rollback()
            raise VehicleConflictError("Vehicle external ID or license plate already exists") from exc

    def delete(self, vehicle: Vehicle) -> None:
        self.repository.delete(vehicle)
