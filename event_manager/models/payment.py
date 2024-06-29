import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from event_manager.models.base import Base


class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Payment(Base):
    __tablename__ = "payments"

    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    transaction_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
    )
    payment_time = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    booking = relationship("Booking", back_populates="payments")
