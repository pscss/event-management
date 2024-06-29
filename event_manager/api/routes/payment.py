from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.core.database import with_session
from event_manager.dal.booking import booking_manager
from event_manager.dal.payment import payment_manager
from event_manager.schemas.payment import Payment, PaymentCreate

router = APIRouter()


@router.post("/", response_model=Payment)
async def create_payment(
    payment_in: PaymentCreate, db: AsyncSession = Depends(with_session)
):
    try:
        booking = await booking_manager.get(db, payment_in.booking_id)
        if not booking:
            raise RuntimeError(f"Event with id: {payment_in.event_id} not found")
        return await payment_manager.create_payment(db, payment_in, booking)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
