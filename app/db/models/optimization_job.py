from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.optimization_recommendation import OptimizationRecommendation
    from app.db.models.trip import Trip


class OptimizationJob(Base):
    __tablename__ = "optimization_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), index=True)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    energy_variance_threshold_percent: Mapped[float] = mapped_column(Float, default=10.0)
    distance_variance_threshold_percent: Mapped[float] = mapped_column(Float, default=10.0)
    minimum_soc_percent: Mapped[float | None] = mapped_column(Float)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    trip: Mapped["Trip"] = relationship(back_populates="optimization_jobs")
    recommendations: Mapped[list["OptimizationRecommendation"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )
