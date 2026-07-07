from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Driver(TimestampMixin, Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    license_number: Mapped[str | None] = mapped_column(String(100), unique=True)
