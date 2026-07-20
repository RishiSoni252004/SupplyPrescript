"""
SupplyPrescript FastAPI application entry-point.

Configures CORS, registers API routers, creates database tables on
startup, and exposes a health-check endpoint.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.router import api_router
from app.database.database import Base, engine

# Import all models so SQLAlchemy registers them with Base.metadata
# before `create_all` is called.
import app.models.shipment  # noqa: F401

# Initialize standard logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan handler.

    On startup: creates all database tables that don't already exist.
    On shutdown: (no cleanup required yet).
    """
    # Create tables defined in Base.metadata (safe to call repeatedly —
    # existing tables are left untouched).
    Base.metadata.create_all(bind=engine)
    yield


# Create FastAPI application with metadata from config
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, restrict this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Register all routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint to verify the service is running.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }
