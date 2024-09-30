from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.core.database import with_session
from event_manager.dal.event import event_manager
from event_manager.schemas.event import Event, EventCreate, EventUpdate

router = APIRouter()


@router.post("/", response_model=Event)
async def create_event(event_in: EventCreate, db: AsyncSession = Depends(with_session)):
    try:
        return await event_manager.create(db, event_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{event_id}", response_model=Event)
async def read_event(event_id: int, db: AsyncSession = Depends(with_session)):
    try:
        event = await event_manager.get(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{event_id}", response_model=Event)
async def update_event(
    event_id: int,
    event_in: EventUpdate,
    db: AsyncSession = Depends(with_session),
):
    try:
        db_event = await event_manager.get(db, event_id)
        if not db_event:
            raise HTTPException(status_code=404, detail="Event not found")
        return await event_manager.update(db, db_event, event_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{event_id}", response_model=None)
async def delete_event(event_id: int, db: AsyncSession = Depends(with_session)):
    try:
        await event_manager.remove(db, event_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[Event])
async def get_all_events(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(with_session)
):
    try:
        return await event_manager.get_all(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/", response_model=list[Event])
async def search_events(
    name: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    venue: Optional[str] = None,
    location_lat: Optional[float] = None,
    location_long: Optional[float] = None,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(with_session),
):
    try:
        return await event_manager.search(
            db,
            name=name,
            date=date,
            time=time,
            venue=venue,
            location_lat=location_lat,
            location_long=location_long,
            skip=skip,
            limit=limit,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/{event_id}/map", response_model=str)
async def get_event_map(event_id: int, db: AsyncSession = Depends(with_session)):
    try:
        return await event_manager.get_event_location_map(event_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
