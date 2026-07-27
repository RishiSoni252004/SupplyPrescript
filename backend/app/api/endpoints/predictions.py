from fastapi import APIRouter, HTTPException
from typing import Any

from app.schemas.prediction import PredictionRequest, PredictionResponse, ModelInfoResponse
from app.ml.predict import PredictionService
from app.ml.model_loader import ml_models

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_shipment_delay(request: PredictionRequest) -> Any:
    """
    Predict whether a shipment will be delayed.
    """
    if not ml_models.is_loaded:
        raise HTTPException(status_code=503, detail="ML model is not loaded yet")
        
    try:
        # Convert request to dict and pass to prediction service
        features = request.model_dump()
        prediction = PredictionService.predict_delay(features)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {e}")

@router.get("/model/info", response_model=ModelInfoResponse)
def get_model_info() -> Any:
    """
    Get metadata about the loaded ML model.
    """
    if not ml_models.is_loaded:
        raise HTTPException(status_code=503, detail="ML model is not loaded yet")
        
    info = ml_models.get_model_info()
    return info
