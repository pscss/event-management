from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookingBase(BaseModel):
    event_id: int
    user_id: int
    booking_time: datetime
    quantity: int
    total_cost: float


class BookingCreate(BaseModel):
    event_id: int
    user_id: int
    booking_time: datetime
    quantity: int


class BookingUpdate(BookingBase):
    event_id: Optional[int] = None
    user_id: Optional[int] = None
    booking_time: Optional[datetime] = None
    quantity: Optional[int] = None


class Booking(BookingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
