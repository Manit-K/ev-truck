from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate
from app.services.vehicle import VehicleConflictError, VehicleService


router = APIRouter(prefix="/vehicles")


@router.post("", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
def create_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
    try:
        return VehicleService(db).create(data)
    except VehicleConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("", response_model=list[VehicleRead])
def list_vehicles(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return VehicleService(db).list(offset, limit)


@router.get("/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = VehicleService(db).get(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.patch("/{vehicle_id}", response_model=VehicleRead)
def update_vehicle(vehicle_id: int, data: VehicleUpdate, db: Session = Depends(get_db)):
    service = VehicleService(db)
    vehicle = service.get(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    try:
        return service.update(vehicle, data)
    except VehicleConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)) -> Response:
    service = VehicleService(db)
    vehicle = service.get(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    service.delete(vehicle)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
