from fastapi import APIRouter, HTTPException
import logging

from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.optimization.recommendation_engine import get_recommendations

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=RecommendationResponse)
async def create_recommendation(request: RecommendationRequest):
    """
    Generates business recommendations based on predicted shipment delay,
    budget, priority, and inventory level.
    """
    try:
        response = get_recommendations(request)
        return response
    except Exception as e:
        logger.error(f"Error generating recommendation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while generating recommendations.")

@router.get("/sample", response_model=RecommendationResponse)
async def get_sample_recommendation():
    """
    Returns a sample recommendation response for frontend testing.
    """
    sample_request = RecommendationRequest(
        predicted_delay_days=7,
        budget=20000.0,
        priority="High",
        inventory_level=30
    )
    
    try:
        response = get_recommendations(sample_request)
        return response
    except Exception as e:
        logger.error(f"Error generating sample recommendation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while generating sample.")
