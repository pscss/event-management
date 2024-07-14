import logging
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from event_manager.api.routes import api_router
from event_manager.core.config import settings

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG to capture all types of log messages
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Set the log message format
    handlers=[logging.StreamHandler(sys.stdout)],  # Log to standard output
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.POSTGRES_APPLICATION_NAME,
    description="Manager for managing events, bookings, and payments",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    ssl_keyfile=settings.SSL_KEY_FILE,
    ssl_certfile=settings.SSL_CERT_FILE,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
