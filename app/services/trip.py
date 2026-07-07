from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.trip import Trip
from app.repositories.trip import TripRepository
from app.repositories.vehicle import VehicleRepository
from app.repositories.vehicle_reading import VehicleReadingRepository
from app.schemas.trip import (
    PlanVsActual,
    TripActual,
    TripCreate,
    TripPlan,
    TripUpdate,
    TripVariance,
)


class TripConflictError(Exception):
    pass


class TripReferenceError(Exception):
    pass


class TripService:
    def __init__(self, db: Session):
        self.repository = TripRepository(db)
        self.vehicles = VehicleRepository(db)
        self.readings = VehicleReadingRepository(db)
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
        readings = self.readings.list_by_trip(trip.id)
        distances = [reading.distance_km for reading in readings if reading.distance_km is not None]
        soc_values = [reading.soc_percent for reading in readings if reading.soc_percent is not None]

        actual_distance = distances[-1] if distances else trip.actual_distance_km

        battery_start = trip.starting_soc_percent
        if battery_start is None and soc_values:
            battery_start = soc_values[0]
        battery_end = trip.ending_soc_percent
        if battery_end is None and soc_values:
            battery_end = soc_values[-1]

        actual_start = trip.actual_start
        if actual_start is None and readings:
            actual_start = readings[0].recorded_at
        actual_end = trip.actual_end
        if actual_end is None and readings:
            actual_end = readings[-1].recorded_at

        return PlanVsActual(
            trip_id=trip.id,
            vehicle_id=trip.vehicle_id,
            planned=TripPlan(
                planned_distance_km=trip.planned_distance_km,
                planned_start_time=trip.scheduled_start,
                planned_end_time=None,
            ),
            actual=TripActual(
                actual_distance_km=actual_distance,
                actual_start_time=actual_start,
                actual_end_time=actual_end,
                battery_start_percent=battery_start,
                battery_end_percent=battery_end,
                odometer_start_km=None,
                odometer_end_km=None,
            ),
            variance=TripVariance(
                distance_variance_km=(
                    None
                    if actual_distance is None
                    else actual_distance - trip.planned_distance_km
                ),
                battery_used_percent=(
                    None
                    if battery_start is None or battery_end is None
                    else battery_start - battery_end
                ),
            ),
        )

    def _validate_vehicle(self, vehicle_id: int) -> None:
        if self.vehicles.get(vehicle_id) is None:
            raise TripReferenceError("Vehicle not found")
