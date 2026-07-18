from fastapi import APIRouter

# Main API router that groups all sub-routers
api_router = APIRouter()

# Example of including sub-routers in the future:
# from app.api.endpoints import predictions
# api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
