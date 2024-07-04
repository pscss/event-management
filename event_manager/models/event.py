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
from sqlalchemy.orm import relationship

from event_manager.models.base import Base


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        Index("location_lat", "location_long"),
        UniqueConstraint(
            "name", "location_lat", "location_long", name="name_lat_long_uix"
        ),
    )

    name = Column(String, nullable=False, index=True)
    event_date = Column(Date, nullable=False, index=True)
    event_time = Column(Time(timezone=True), nullable=False, index=True)
    venue = Column(String, nullable=False)
    location_lat = Column(Float, nullable=False)
    location_long = Column(Float, nullable=False)
    available_tickets = Column(Integer, nullable=False)
    base_price = Column(Float, nullable=False)
    surge_price = Column(Float, nullable=False, default=0)
    surge_threshold = Column(Float, nullable=False, default=0)

    bookings = relationship("Booking", back_populates="event")
