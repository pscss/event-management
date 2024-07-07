from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.dal.crud_manager import CRUD
from event_manager.models.payment import Payment
from event_manager.schemas.payment import PaymentCreate, PaymentUpdate


class PaymentManager(CRUD[Payment, PaymentCreate, PaymentUpdate]):
    async def get_payment_by_transaction_id(
        self, db: AsyncSession, transaction_id: str
    ) -> Payment | None:
        payments = await self.get_all(
            db=db, additional_where_clause=[Payment.transaction_id == transaction_id]
        )
        if payments:
            return payments[0]
        else:
            return None


payment_manager = PaymentManager(Payment)
