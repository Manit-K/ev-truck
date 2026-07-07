from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.trip import Trip
from app.schemas.trip import TripCreate, TripUpdate


class TripRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, offset: int = 0, limit: int = 100) -> list[Trip]:
        return list(self.db.scalars(select(Trip).offset(offset).limit(limit)))

    def get(self, trip_id: int) -> Trip | None:
        return self.db.get(Trip, trip_id)

    def create(self, data: TripCreate) -> Trip:
        trip = Trip(**data.model_dump())
        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def update(self, trip: Trip, data: TripUpdate) -> Trip:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(trip, field, value)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def delete(self, trip: Trip) -> None:
        self.db.delete(trip)
        self.db.commit()
