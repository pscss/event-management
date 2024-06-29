from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.dal.crud_manager import CRUD
from event_manager.models.booking import Booking
from event_manager.schemas.booking import BookingCreate, BookingUpdate

if TYPE_CHECKING:
    from event_manager.models.event import Event


class BookingManager(CRUD[Booking, BookingCreate, BookingUpdate]):
    async def create_booking(
        self, db: AsyncSession, booking_in: BookingCreate, event: "Event"
    ) -> Booking:
        try:
            if not event or event.available_tickets < booking_in.quantity:
                raise HTTPException(
                    status_code=400, detail="Insufficient tickets available"
                )

            total_cost = booking_in.quantity * event.base_price
            booking = Booking(**booking_in.model_dump(), total_cost=total_cost)

            db.add(booking)
            event.available_tickets -= booking_in.quantity
            await db.commit()
            await db.refresh(booking)
        except Exception as e:
            await db.rollback()
            raise e

        return booking


booking_manager = BookingManager(Booking)
