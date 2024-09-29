from typing import TYPE_CHECKING

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError

from event_manager.dal.crud_manager import CRUD
from event_manager.errors.all_errors import InsufficientTickets
from event_manager.models.booking import Booking
from event_manager.schemas.booking import BookingCreate, BookingUpdate

if TYPE_CHECKING:
    from event_manager.models.event import Event


class BookingManager(CRUD[Booking, BookingCreate, BookingUpdate]):
    def calculate_total_cost(self, event: "Event", quantity: int) -> int:

        if event.available_tickets > event.surge_threshold:
            # No surge pricing if tickets are above the threshold
            return quantity * event.base_price

        total_cost = 0
        remaining_tickets = event.available_tickets
        remaining_quantity = quantity
        surge_level = 1  # Start with one surge level

        while remaining_quantity > 0:
            if remaining_tickets % 5 == 0:
                tickets_in_tier = 5
            else:
                tickets_in_tier = remaining_tickets % 5

            tier_price = event.base_price + ((surge_level) * event.surge_price)
            total_cost += tickets_in_tier * tier_price
            remaining_quantity -= tickets_in_tier
            remaining_tickets -= tickets_in_tier
            surge_level += 1  # Increase surge level for the next tier

        return total_cost

    async def create_booking(
        self, db: AsyncSession, booking_in: BookingCreate, event: "Event"
    ) -> Booking:
        try:
            if event.available_tickets < booking_in.quantity:
                raise InsufficientTickets

            booking = Booking(**booking_in.model_dump())

            db.add(booking)
            event.available_tickets -= booking_in.quantity
            await db.commit()
            await db.refresh(booking)
        except Exception as e:
            await db.rollback()
            raise e

        return booking

    async def create_booking_optimistic(
        self, db: AsyncSession, booking_in: BookingCreate, event: "Event"
    ) -> Booking:
        try:
            # Check ticket availability
            if event.available_tickets < booking_in.quantity:
                raise InsufficientTickets

            # Decrease available tickets
            event.available_tickets -= booking_in.quantity

            # Manually increment the version to detect changes
            event.version += 1

            booking = Booking(**booking_in.model_dump())

            db.add(booking)
            db.add(event)

            # Flush changes to the database
            await db.flush()
            await db.refresh(booking)

        except StaleDataError:
            await db.rollback()
            raise RuntimeError("The event was modified by another transaction.")
        except Exception as e:
            await db.rollback()
            raise e

        return booking

    async def create_booking_pessimistic(
        self, db: AsyncSession, booking_in: BookingCreate, event: "Event"
    ) -> Booking:
        try:
            # Check ticket availability
            if event.available_tickets < booking_in.quantity:
                raise InsufficientTickets

            # Decrease available tickets
            event.available_tickets -= booking_in.quantity

            # # Calculate total cost
            # total_cost = self.calculate_total_cost(event, booking_in.quantity)

            # Create booking
            booking = Booking(**booking_in.model_dump())

            db.add(booking)
            db.add(event)

            # Flush changes to the database
            await db.flush()
            await db.refresh(booking)

        except OperationalError as e:
            # Handle deadlocks or lock timeouts
            if "deadlock detected" in str(e):
                await db.rollback()
                raise RuntimeError("Booking conflict occurred. Please try again.")
            else:
                await db.rollback()
                raise e
        except Exception as e:
            await db.rollback()
            raise e

        return booking


booking_manager = BookingManager(Booking)
