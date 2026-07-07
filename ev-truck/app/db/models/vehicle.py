from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.trip import Trip
    from app.db.models.vehicle_reading import VehicleReading


class Vehicle(TimestampMixin, Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    license_plate: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    battery_capacity_kwh: Mapped[float] = mapped_column(Float)
    minimum_soc_percent: Mapped[float] = mapped_column(Float, default=20.0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    trips: Mapped[list["Trip"]] = relationship(back_populates="vehicle")
    readings: Mapped[list["VehicleReading"]] = relationship(back_populates="vehicle")
