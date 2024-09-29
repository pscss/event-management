from logging import getLogger

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.core.config import settings
from event_manager.core.database import with_session
from event_manager.dal.booking import booking_manager
from event_manager.dal.event import event_manager
from event_manager.dal.payment import payment_manager
from event_manager.dal.user import user_manager
from event_manager.errors.all_errors import ResourceNotFound
from event_manager.models.payment import PaymentStatus
from event_manager.payment_gateway import get_idempotency_key, get_payment_gateway
from event_manager.payment_gateway.abstract_payment_gateway import PaymentGateway
from event_manager.schemas.booking import BookingCreate
from event_manager.schemas.payment import Payment, PaymentCreate

logger = getLogger(__name__)
router = APIRouter()


@router.get("/{payment_id}", response_model=Payment)
async def read_payment(payment_id: int, db: AsyncSession = Depends(with_session)):
    try:
        payment = await payment_manager.get(db, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[Payment])
async def get_all_payments(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(with_session)
):
    try:
        return await payment_manager.get_all(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/book_and_pay", response_model=dict)
async def book_and_pay(
    booking_in: BookingCreate,
    optimistic: bool,
    db: AsyncSession = Depends(with_session),
    payment_gateway: PaymentGateway = Depends(get_payment_gateway),
    idempotency_key: str = Depends(get_idempotency_key),
):

    try:
        user = await user_manager.get(db, booking_in.user_id)
        if not user:
            raise RuntimeError(f"User with id: {booking_in.user_id} not found")
        if optimistic:
            logger.info("OPtimistic Booking!!")
            event = await event_manager.get(db, booking_in.event_id)
            if not event:
                raise RuntimeError(f"Event with id: {booking_in.event_id} not found")
            db_booking = await booking_manager.create_booking_optimistic(
                db, booking_in, event
            )
        else:
            logger.info("Pessimistic Booking!!")
            event = await event_manager.get_pessimistic_event(booking_in.event_id, db)
            if not event:
                raise RuntimeError(f"Event with id: {booking_in.event_id} not found")
            db_booking = await booking_manager.create_booking_pessimistic(
                db, booking_in, event
            )

        logger.info(
            f"COST {int(db_booking.total_cost)}",
        )
        payment_intent = payment_gateway.create_payment_intent(
            amount=int(db_booking.total_cost),
            metadata={"booking_id": db_booking.id},
            idempotency_key=idempotency_key,
        )

        payment_data = PaymentCreate(
            booking_id=db_booking.id,
            transaction_id=payment_intent["id"],
            amount=db_booking.total_cost,
            status=PaymentStatus.PENDING,
            payment_time=booking_in.booking_time,
            idempotency_key=idempotency_key,
        )
        await payment_manager.create(db, payment_data)
        logger.info(f"Payment Intent --> {payment_intent}")
        return {
            "payment_intent_id": payment_intent["id"],
            "client_secret": payment_intent["client_secret"],
        }
    except Exception as e:
        logger.exception(f"Error creating PaymentIntent: {e}")
        raise HTTPException(status_code=500, detail="Failed to create payment intent")


@router.post("/success")
async def payment_success(
    payment_intent_id: str,
    db: AsyncSession = Depends(with_session),
):
    try:
        payment = await payment_manager.get_payment_by_transaction_id(
            db=db, transaction_id=payment_intent_id
        )
        if not payment:
            raise ResourceNotFound(
                f"Payment with intent id {payment_intent_id} not found"
            )
        if payment.status == PaymentStatus.COMPLETED:
            return {"status": "success"}

        stripe.PaymentIntent.confirm(
            payment_intent_id,
            payment_method="pm_card_visa",
        )
        return {"status": "success"}
    except Exception as e:
        logger.exception(f"Error confirming PaymentIntent: {e}")
        raise HTTPException(status_code=500, detail="Failed to confirm payment intent")


@router.post("/failure")
async def payment_failure(
    payment_intent_id: str,
    db: AsyncSession = Depends(with_session),
):
    try:
        payment = await payment_manager.get_payment_by_transaction_id(
            db=db, transaction_id=payment_intent_id
        )
        if not payment:
            raise ResourceNotFound(
                f"Payment with intent id {payment_intent_id} not found"
            )
        if payment.status == PaymentStatus.FAILED:
            return {"status": "failure"}

        stripe.PaymentIntent.cancel(payment_intent_id)
        await event_manager.update_event_after_payment_failure(
            event_id=payment.booking.event_id,
            db=db,
            booking_quantity=payment.booking.quantity,
        )
        return {"status": "failure"}
    except Exception as e:
        logger.exception(f"Error failing PaymentIntent: {e}")
        raise HTTPException(status_code=500, detail="Failed to fail payment intent")


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(with_session),
    payment_gateway: PaymentGateway = Depends(get_payment_gateway),
):
    payload = await request.body()
    # logger.info(f"webhook payload --> {payload}")
    sig_header = request.headers.get("stripe-signature")
    logger.info(f"webhook sig_header --> {sig_header}")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        logger.info(f"webhook event --> {event}")
    except ValueError as e:
        logger.exception(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.exception.SignatureVerificationError as e:
        logger.exception(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    logger.info("Handling webhook event...")
    await payment_gateway.handle_webhook_event(event, db)
    logger.info("RETURNING!!!")
    return {"status": "success"}
