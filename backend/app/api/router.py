"""
Main API router that aggregates all endpoint sub-routers.

Each feature area (shipments, predictions, etc.) has its own router
in `app/api/endpoints/`. This module wires them together under a
common prefix defined in `app/core/config.py`.
"""

from fastapi import APIRouter

from app.api.endpoints import dashboard, shipments

# Main API router that groups all sub-routers
api_router = APIRouter()

# --- Shipment endpoints ---
api_router.include_router(
    shipments.router,
    prefix="/shipments",
    tags=["shipments"],
)

# --- Dashboard endpoints ---
api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["dashboard"],
)

# Future routers will be registered here, e.g.:
# from app.api.endpoints import predictions
# api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
