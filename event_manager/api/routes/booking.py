from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.core.database import with_session
from event_manager.dal.booking import booking_manager
from event_manager.dal.event import event_manager
from event_manager.dal.user import user_manager
from event_manager.schemas.booking import Booking, BookingCreate

router = APIRouter()


@router.post("/", response_model=Booking)
async def create_booking(
    booking_in: BookingCreate, db: AsyncSession = Depends(with_session)
):
    try:
        event = await event_manager.get(db, booking_in.event_id)
        if not event:
            raise RuntimeError(f"Event with id: {booking_in.event_id} not found")
        user = await user_manager.get(db, booking_in.user_id)
        if not user:
            raise RuntimeError(f"User with id: {booking_in.user_id} not found")
        return await booking_manager.create_booking(db, booking_in, event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{booking_id}", response_model=Booking)
async def read_booking(booking_id: int, db: AsyncSession = Depends(with_session)):
    try:
        booking = await booking_manager.get(db, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{booking_id}", response_model=Booking)
async def delete_booking(booking_id: int, db: AsyncSession = Depends(with_session)):
    try:
        booking = await booking_manager.remove(db, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[Booking])
async def get_all_bookings(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(with_session)
):
    try:
        return await booking_manager.get_all(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
