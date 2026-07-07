from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.optimization_job import OptimizationJob
    from app.db.models.vehicle import Vehicle
    from app.db.models.vehicle_reading import VehicleReading


class Trip(TimestampMixin, Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), index=True)
    driver_id: Mapped[int | None] = mapped_column(ForeignKey("drivers.id"), index=True)
    external_id: Mapped[str | None] = mapped_column(String(100), unique=True, index=True)
    origin: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), default="planned")
    planned_distance_km: Mapped[float] = mapped_column(Float)
    actual_distance_km: Mapped[float | None] = mapped_column(Float)
    planned_energy_kwh: Mapped[float] = mapped_column(Float)
    actual_energy_kwh: Mapped[float | None] = mapped_column(Float)
    starting_soc_percent: Mapped[float | None] = mapped_column(Float)
    ending_soc_percent: Mapped[float | None] = mapped_column(Float)
    scheduled_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    vehicle: Mapped["Vehicle"] = relationship(back_populates="trips")
    readings: Mapped[list["VehicleReading"]] = relationship(back_populates="trip")
    optimization_jobs: Mapped[list["OptimizationJob"]] = relationship(back_populates="trip")
