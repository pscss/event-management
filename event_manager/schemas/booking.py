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


class BookingUpdate(BaseModel):
    pass


class Booking(BookingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
