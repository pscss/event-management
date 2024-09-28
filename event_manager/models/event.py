from datetime import date, time

from sqlalchemy import (
    Column,
    Date,
    Float,
    Index,
    Integer,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, relationship

from event_manager.models.base import Base
from event_manager.models.booking import Booking


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        Index("location_lat", "location_long"),
        UniqueConstraint(
            "name", "location_lat", "location_long", name="name_lat_long_uix"
        ),
    )

    name: str = Column(String, nullable=False, index=True)
    event_date: date = Column(Date, nullable=False, index=True)
    event_time: time = Column(Time(timezone=True), nullable=False, index=True)
    venue: str = Column(String, nullable=False)
    location_lat: float = Column(Float, nullable=False)
    location_long: float = Column(Float, nullable=False)
    available_tickets: int = Column(Integer, nullable=False)
    base_price: float = Column(Float, nullable=False)
    surge_price: float = Column(Float, nullable=False, default=0)
    surge_threshold: float = Column(Float, nullable=False, default=0)
    version: int = Column(Integer, nullable=False, default=0)

    __mapper_args__ = {
        "version_id_col": version,  # SQLAlchemy uses this column for versioning
        "version_id_generator": False,  # We'll manually increment the version
    }

    bookings: Mapped[list[Booking]] = relationship(
        "Booking", back_populates="event", lazy="selectin"
    )
