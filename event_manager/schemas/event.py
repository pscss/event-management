from datetime import date, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class EventBase(BaseModel):
    name: str
    event_date: date
    event_time: time
    venue: str
    location_lat: Annotated[float, Field(strict=True, gt=-90, lt=90)]
    location_long: Annotated[float, Field(strict=True, gt=-180, lt=180)]
    available_tickets: int
    base_price: Annotated[float, Field(strict=True, gt=0)]
    surge_price: float | None = 0
    surge_threshold: float | None = 0


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    name: Optional[str] = None
    event_date: Optional[date] = None
    event_time: Optional[time] = None
    venue: Optional[str] = None
    location_lat: Optional[float] = None
    location_long: Optional[float] = None
    available_tickets: Optional[int] = None
    base_price: Optional[float] = None
    surge_price: Optional[float] = None
    surge_threshold: Optional[float] = None


class Event(EventBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
