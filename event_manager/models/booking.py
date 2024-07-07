from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from event_manager.models.base import Base
from event_manager.models.payment import Payment

if TYPE_CHECKING:
    from event_manager.models.event import Event
    from event_manager.models.user import User


class Booking(Base):
    __tablename__ = "bookings"

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    booking_time = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    quantity = Column(Integer, nullable=False)
    total_cost = Column(Float, nullable=False)

    event: Mapped["Event"] = relationship("Event", back_populates="bookings")
    user: Mapped["User"] = relationship("User", back_populates="bookings")
    payments: Mapped[list[Payment]] = relationship("Payment", back_populates="booking")
