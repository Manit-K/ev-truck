from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.optimization_job import OptimizationJob


class OptimizationRecommendation(TimestampMixin, Base):
    __tablename__ = "optimization_recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("optimization_jobs.id"), index=True)
    rule_code: Mapped[str] = mapped_column(String(80))
    severity: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)
    observed_value: Mapped[float | None] = mapped_column(Float)
    threshold_value: Mapped[float | None] = mapped_column(Float)

    job: Mapped["OptimizationJob"] = relationship(back_populates="recommendations")
