import uuid
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.dal.crud_manager import CRUD
from event_manager.models.payment import Payment, PaymentStatus
from event_manager.schemas.payment import PaymentCreate, PaymentUpdate

if TYPE_CHECKING:
    from event_manager.models.booking import Booking


class PaymentManager(CRUD[Payment, PaymentCreate, PaymentUpdate]):
    async def create_payment(
        self, db: AsyncSession, payment_in: PaymentCreate, booking: "Booking"
    ) -> Payment:
        try:
            payment = Payment(
                **payment_in.model_dump(),
                status=PaymentStatus.COMPLETED,
                transaction_id=uuid.uuid4(),
                amount=booking.total_cost
            )
            db.add(payment)
            await db.commit()
            await db.refresh(payment)
            if payment.status == PaymentStatus.FAILED:
                db.delete(booking)
                await db.commit()
        except Exception as e:
            await db.rollback()
            raise e

        return payment


payment_manager = PaymentManager(Payment)
