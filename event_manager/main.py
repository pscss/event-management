from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from event_manager.api.routes import api_router
from event_manager.core.config import settings

app = FastAPI(
    title=settings.POSTGRES_APPLICATION_NAME,
    description="Manager for managing events, bookings, and payments",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return HTTPException(
        status_code=422,
        detail=exc.errors(),
    )


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


app.include_router(api_router)
