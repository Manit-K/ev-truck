from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.trip import PlanVsActual, TripCreate, TripRead, TripUpdate
from app.services.trip import TripConflictError, TripReferenceError, TripService


router = APIRouter(prefix="/trips")


@router.post("", response_model=TripRead, status_code=status.HTTP_201_CREATED)
def create_trip(data: TripCreate, db: Session = Depends(get_db)):
    try:
        return TripService(db).create(data)
    except TripReferenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except TripConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("", response_model=list[TripRead])
def list_trips(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return TripService(db).list(offset, limit)


@router.get("/{trip_id}", response_model=TripRead)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = TripService(db).get(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.patch("/{trip_id}", response_model=TripRead)
def update_trip(trip_id: int, data: TripUpdate, db: Session = Depends(get_db)):
    service = TripService(db)
    trip = service.get(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    try:
        return service.update(trip, data)
    except TripReferenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except TripConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: int, db: Session = Depends(get_db)) -> Response:
    service = TripService(db)
    trip = service.get(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    service.delete(trip)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{trip_id}/plan-vs-actual", response_model=PlanVsActual)
def plan_vs_actual(trip_id: int, db: Session = Depends(get_db)):
    service = TripService(db)
    trip = service.get(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return service.plan_vs_actual(trip)
