from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.optimization_job import OptimizationJob
from app.db.models.optimization_recommendation import OptimizationRecommendation
from app.repositories.optimization import OptimizationRepository
from app.repositories.trip import TripRepository
from app.schemas.optimization import OptimizationJobCreate


class OptimizationTripNotFoundError(Exception):
    pass


class OptimizationService:
    ENERGY_THRESHOLD_PERCENT = 10.0
    DISTANCE_THRESHOLD_PERCENT = 10.0

    def __init__(self, db: Session):
        self.db = db
        self.jobs = OptimizationRepository(db)
        self.trips = TripRepository(db)

    def create_job(self, data: OptimizationJobCreate) -> OptimizationJob:
        trip = self.trips.get(data.trip_id)
        if trip is None:
            raise OptimizationTripNotFoundError("Trip not found")

        minimum_soc = (
            data.minimum_soc_percent
            if data.minimum_soc_percent is not None
            else trip.vehicle.minimum_soc_percent
        )
        job = OptimizationJob(
            trip_id=trip.id,
            status="completed",
            energy_variance_threshold_percent=self.ENERGY_THRESHOLD_PERCENT,
            distance_variance_threshold_percent=self.DISTANCE_THRESHOLD_PERCENT,
            minimum_soc_percent=minimum_soc,
            created_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )

        if trip.actual_energy_kwh is not None and trip.planned_energy_kwh > 0:
            energy_variance = (
                (trip.actual_energy_kwh - trip.planned_energy_kwh)
                / trip.planned_energy_kwh
                * 100
            )
            if energy_variance > self.ENERGY_THRESHOLD_PERCENT:
                job.recommendations.append(
                    OptimizationRecommendation(
                        rule_code="ENERGY_OVER_PLAN",
                        severity="warning",
                        message="Actual energy use exceeds the plan by more than 10%.",
                        observed_value=energy_variance,
                        threshold_value=self.ENERGY_THRESHOLD_PERCENT,
                    )
                )

        if trip.ending_soc_percent is not None and trip.ending_soc_percent < minimum_soc:
            job.recommendations.append(
                OptimizationRecommendation(
                    rule_code="LOW_ENDING_SOC",
                    severity="warning",
                    message="Ending state of charge is below the minimum; schedule charging.",
                    observed_value=trip.ending_soc_percent,
                    threshold_value=minimum_soc,
                )
            )

        if trip.actual_distance_km is not None and trip.planned_distance_km > 0:
            distance_variance = (
                (trip.actual_distance_km - trip.planned_distance_km)
                / trip.planned_distance_km
                * 100
            )
            if distance_variance > self.DISTANCE_THRESHOLD_PERCENT:
                job.recommendations.append(
                    OptimizationRecommendation(
                        rule_code="ROUTE_VARIANCE",
                        severity="warning",
                        message="Actual distance exceeds the planned route by more than 10%.",
                        observed_value=distance_variance,
                        threshold_value=self.DISTANCE_THRESHOLD_PERCENT,
                    )
                )

        return self.jobs.add(job)

    def get_job(self, job_id: int) -> OptimizationJob | None:
        return self.jobs.get(job_id)
