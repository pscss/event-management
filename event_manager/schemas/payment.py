from datetime import datetime

from pydantic import BaseModel, ConfigDict

from event_manager.models.payment import PaymentStatus


class PaymentBase(BaseModel):
    booking_id: int
    payment_time: datetime
    transaction_id: str
    amount: float
    status: PaymentStatus


class PaymentCreate(PaymentBase):
    idempotency_key: str


class PaymentUpdate(BaseModel):
    pass


class Payment(PaymentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
