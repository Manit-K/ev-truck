from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.import_batch import ImportBatch
    from app.db.models.trip import Trip
    from app.db.models.vehicle import Vehicle


class VehicleReading(Base):
    __tablename__ = "vehicle_readings"

    __table_args__ = (
        UniqueConstraint("source", "source_record_id", name="uq_vehicle_readings_source_record"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    vehicle_id: Mapped[int | None] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=True,
        index=True,
    )

    trip_id: Mapped[int | None] = mapped_column(
        ForeignKey("trips.id"),
        nullable=True,
        index=True,
    )

    import_batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("import_batches.id"),
        nullable=True,
        index=True,
    )

    source: Mapped[str] = mapped_column(String(50), nullable=False, default="google_sheet")
    source_record_id: Mapped[str | None] = mapped_column(String(128), nullable=True)

    sheet_row_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sheet_title: Mapped[str | None] = mapped_column(String(255), nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    battery_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    odometer_km: Mapped[float | None] = mapped_column(Float, nullable=True)
    trip_km: Mapped[float | None] = mapped_column(Float, nullable=True)
    range_km: Mapped[float | None] = mapped_column(Float, nullable=True)

    front_pressure_bar: Mapped[float | None] = mapped_column(Float, nullable=True)
    rear_pressure_bar: Mapped[float | None] = mapped_column(Float, nullable=True)

    energy_used_kwh: Mapped[float | None] = mapped_column(Float, nullable=True)
    distance_km: Mapped[float | None] = mapped_column(Float, nullable=True)

    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    raw_ocr_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    sync_batch_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sync_status: Mapped[str] = mapped_column(String(30), nullable=False, default="synced")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    vehicle: Mapped["Vehicle | None"] = relationship(back_populates="readings")
    trip: Mapped["Trip | None"] = relationship(back_populates="readings")
    import_batch: Mapped["ImportBatch | None"] = relationship(back_populates="readings")