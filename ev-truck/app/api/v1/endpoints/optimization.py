from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.optimization import OptimizationJobCreate, OptimizationJobRead
from app.services.optimization import OptimizationService, OptimizationTripNotFoundError


router = APIRouter(prefix="/optimization/jobs")


@router.post("", response_model=OptimizationJobRead, status_code=status.HTTP_201_CREATED)
def create_optimization_job(data: OptimizationJobCreate, db: Session = Depends(get_db)):
    try:
        return OptimizationService(db).create_job(data)
    except OptimizationTripNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{job_id}", response_model=OptimizationJobRead)
def get_optimization_job(job_id: int, db: Session = Depends(get_db)):
    job = OptimizationService(db).get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Optimization job not found")
    return job
