from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.trip import Trip
from app.repositories.trip import TripRepository
from app.repositories.vehicle import VehicleRepository
from app.schemas.trip import MetricComparison, PlanVsActual, TripCreate, TripUpdate


class TripConflictError(Exception):
    pass


class TripReferenceError(Exception):
    pass


class TripService:
    def __init__(self, db: Session):
        self.repository = TripRepository(db)
        self.vehicles = VehicleRepository(db)
        self.db = db

    def list(self, offset: int, limit: int) -> list[Trip]:
        return self.repository.list(offset, limit)

    def get(self, trip_id: int) -> Trip | None:
        return self.repository.get(trip_id)

    def create(self, data: TripCreate) -> Trip:
        self._validate_vehicle(data.vehicle_id)
        try:
            return self.repository.create(data)
        except IntegrityError as exc:
            self.db.rollback()
            raise TripConflictError("Trip external ID already exists or a reference is invalid") from exc

    def update(self, trip: Trip, data: TripUpdate) -> Trip:
        if data.vehicle_id is not None:
            self._validate_vehicle(data.vehicle_id)
        try:
            return self.repository.update(trip, data)
        except IntegrityError as exc:
            self.db.rollback()
            raise TripConflictError("Trip external ID already exists or a reference is invalid") from exc

    def delete(self, trip: Trip) -> None:
        self.repository.delete(trip)

    def plan_vs_actual(self, trip: Trip) -> PlanVsActual:
        distance = self._compare(trip.planned_distance_km, trip.actual_distance_km)
        energy = self._compare(trip.planned_energy_kwh, trip.actual_energy_kwh)
        planned_soc = None
        if trip.starting_soc_percent is not None and trip.vehicle.battery_capacity_kwh > 0:
            planned_soc = max(
                0.0,
                trip.starting_soc_percent
                - (trip.planned_energy_kwh / trip.vehicle.battery_capacity_kwh * 100),
            )
        return PlanVsActual(
            trip_id=trip.id,
            distance_km=distance,
            energy_kwh=energy,
            planned_ending_soc_percent=planned_soc,
            actual_ending_soc_percent=trip.ending_soc_percent,
        )

    def _validate_vehicle(self, vehicle_id: int) -> None:
        if self.vehicles.get(vehicle_id) is None:
            raise TripReferenceError("Vehicle not found")

    @staticmethod
    def _compare(planned: float, actual: float | None) -> MetricComparison:
        variance = None if actual is None else actual - planned
        variance_percent = None
        if variance is not None and planned != 0:
            variance_percent = variance / planned * 100
        return MetricComparison(
            planned=planned,
            actual=actual,
            variance=variance,
            variance_percent=variance_percent,
        )
