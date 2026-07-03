from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models.optimization_job import OptimizationJob


class OptimizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, job_id: int) -> OptimizationJob | None:
        return self.db.scalar(
            select(OptimizationJob)
            .options(selectinload(OptimizationJob.recommendations))
            .where(OptimizationJob.id == job_id)
        )

    def add(self, job: OptimizationJob) -> OptimizationJob:
        self.db.add(job)
        self.db.commit()
        return self.get(job.id)  # type: ignore[return-value]
