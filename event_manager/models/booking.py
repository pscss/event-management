from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from event_manager.models.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    booking_time = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    quantity = Column(Integer, nullable=False)
    total_cost = Column(Float, nullable=False)

    event = relationship("Event", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking")
