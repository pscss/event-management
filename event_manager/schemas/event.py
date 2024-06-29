from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field
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

    def to_db_format(self):
        return {
            "name": self.name,
            "event_date": self.event_date,
            "event_time": self.event_time.time(),  # Convert to time
            "venue": self.venue,
            "location_lat": self.location_lat,
            "location_long": self.location_long,
            "available_tickets": self.available_tickets,
            "base_price": self.base_price,
        }


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


class Event(EventBase):
    id: int

    class Config:
        from_attributes = True
