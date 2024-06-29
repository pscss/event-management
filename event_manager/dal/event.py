from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import and_, or_

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


event_manager = EventManager(Event)
