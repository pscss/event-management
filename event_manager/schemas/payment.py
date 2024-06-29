from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from event_manager.models.payment import PaymentStatus


class PaymentBase(BaseModel):
    booking_id: int
    payment_time: datetime


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    pass


class Payment(PaymentBase):
    id: int
    status: PaymentStatus
    transaction_id: UUID
    amount: float

    class Config:
        from_attributes = True
