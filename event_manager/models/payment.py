import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from event_manager.models.base import Base

if TYPE_CHECKING:
    from event_manager.models.booking import Booking


class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (Index("transaction_id_idx", "transaction_id"),)

    booking_id: int = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    amount: float = Column(Float, nullable=False)
    status: PaymentStatus = Column(Enum(PaymentStatus), nullable=False)
    transaction_id: str = Column(String, nullable=False, unique=True)
    payment_time: datetime = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    idempotency_key: str = Column(String, nullable=False, unique=True)

    booking: Mapped["Booking"] = relationship("Booking", back_populates="payments")
