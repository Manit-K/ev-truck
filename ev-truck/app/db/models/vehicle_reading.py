from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.import_batch import ImportBatch
    from app.db.models.trip import Trip
    from app.db.models.vehicle import Vehicle


class VehicleReading(Base):
    __tablename__ = "vehicle_readings"
    __table_args__ = (
        UniqueConstraint("source", "source_record_id", name="uq_reading_source_record"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), index=True)
    trip_id: Mapped[int | None] = mapped_column(ForeignKey("trips.id"), index=True)
    import_batch_id: Mapped[int] = mapped_column(ForeignKey("import_batches.id"), index=True)
    source: Mapped[str] = mapped_column(String(50), default="google_sheet")
    source_record_id: Mapped[str] = mapped_column(String(128))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    soc_percent: Mapped[float | None] = mapped_column(Float)
    energy_used_kwh: Mapped[float | None] = mapped_column(Float)
    distance_km: Mapped[float | None] = mapped_column(Float)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSONB)

    vehicle: Mapped["Vehicle"] = relationship(back_populates="readings")
    trip: Mapped["Trip | None"] = relationship(back_populates="readings")
    import_batch: Mapped["ImportBatch"] = relationship(back_populates="readings")
