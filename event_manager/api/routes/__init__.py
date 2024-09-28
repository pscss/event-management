from fastapi import APIRouter

from event_manager.api.routes import booking, event, payment, user

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(event.router, prefix="/events", tags=["events"])
api_router.include_router(booking.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(payment.router, prefix="/payments", tags=["payments"])
