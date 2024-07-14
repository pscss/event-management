from logging import getLogger
from typing import Any, Dict

import stripe
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.core.config import settings
from event_manager.dal.payment import payment_manager
from event_manager.models.payment import PaymentStatus
from event_manager.payment_gateway.abstract_payment_gateway import PaymentGateway

logger = getLogger(__name__)
stripe.api_key = settings.STRIPE_API_KEY


class StripePaymentGateway(PaymentGateway):
    def create_payment_intent(
        self,
        amount: float,
        idempotency_key: str,
        currency: str | None = "INR",
        metadata: Dict[str, Any] = {},
    ) -> Dict[str, Any]:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata=metadata,
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
            idempotency_key=idempotency_key,
        )
        return {
            "id": intent["id"],
            "client_secret": intent["client_secret"],
            "idempotency_key": idempotency_key,
        }

    async def handle_webhook_event(
        self, event: Dict[str, Any], db: AsyncSession
    ) -> None:
        if event["type"] == "payment_intent.succeeded":
            intent = event["data"]["object"]
            logger.info("Payment SUCCESS!!!")
            await self._handle_payment_intent_succeeded(intent, db)
        elif event["type"] == "payment_intent.payment_failed":
            intent = event["data"]["object"]
            logger.info("Payment FAILURE!!!")
            await self._handle_payment_intent_failed(intent, db)
        else:
            logger.info(f"UNKNOWN Intent Type!!! --> {event['type']}")

    async def _handle_payment_intent_succeeded(
        self, intent: Dict[str, Any], db: AsyncSession
    ) -> None:
        db_payment = await payment_manager.get_payment_by_transaction_id(
            db, intent["id"]
        )
        if db_payment:
            db_payment.status = PaymentStatus.COMPLETED
            await db.commit()
            await db.refresh(db_payment)

    async def _handle_payment_intent_failed(
        self, intent: Dict[str, Any], db: AsyncSession
    ) -> None:
        db_payment = await payment_manager.get_payment_by_transaction_id(
            db, intent["id"]
        )
        if db_payment:
            db_payment.status = PaymentStatus.FAILED
            db_payment.booking.event.available_tickets += db_payment.booking.quantity
            db.add(db_payment)
            db.add(db_payment.booking.event)
            db.commit()
            db.refresh(db_payment)


stripe_payment_gateway = StripePaymentGateway()
