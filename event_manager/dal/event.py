from typing import List, Optional

import googlemaps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import and_, or_

from event_manager.core.config import settings
from event_manager.dal.crud_manager import CRUD
from event_manager.models.event import Event
from event_manager.schemas.event import EventCreate, EventUpdate


class EventManager(CRUD[Event, EventCreate, EventUpdate]):
    async def search(
        self,
        db: AsyncSession,
        name: Optional[str] = None,
        date: Optional[str] = None,
        time: Optional[str] = None,
        venue: Optional[str] = None,
        location_lat: Optional[float] = None,
        location_long: Optional[float] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Event]:
        query = select(Event)
        filters = []
        if name:
            filters.append(Event.name.ilike(f"%{name}%"))
        if date:
            filters.append(Event.event_date == date)
        if time:
            filters.append(Event.event_time == time)
        if venue:
            filters.append(Event.venue.ilike(f"%{venue}%"))
        if location_lat and location_long:
            filters.append(
                and_(
                    Event.location_lat == location_lat,
                    Event.location_long == location_long,
                )
            )

        if filters:
            query = query.where(or_(*filters))

        query = query.offset(skip).limit(limit).order_by(Event.name)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_event_location_map(self, event_id: int, db: AsyncSession):
        event = await event_manager.get(db, event_id)
        if not event:
            raise ValueError("Event not found")

        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        geocode_result = gmaps.geocode(event.venue)
        if geocode_result:
            location = geocode_result[0]["geometry"]["location"]
            lat = location["lat"]
            lng = location["lng"]
        else:
            lat = event.location_lat
            lng = event.location_long

        # Construct the Google Maps URL
        map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"

        return map_url

    async def get_pessimistic_event(self, event_id: int, db: AsyncSession):
        # Acquire a lock on the event row using with_for_update()
        result = await db.execute(
            select(Event).where(Event.id == event_id).with_for_update()
        )
        event = result.scalar_one_or_none()
        return event

    async def update_event_after_payment_failure(
        self, event_id: int, db: AsyncSession, booking_quantity: int
    ):
        event = await self.get(db, event_id)
        event.available_tickets += booking_quantity
        db.add(event)
        await db.commit()


event_manager = EventManager(Event)
