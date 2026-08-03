from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json
from typing import List

from app.database.database import get_db
from app.models.prediction_history import PredictionHistory
from app.schemas.model_management import PredictionHistoryResponse, ModelMetadataResponse, ModelStatisticsResponse
from app.ml.model_loader import ml_models

router = APIRouter()

@router.get("/metadata", response_model=ModelMetadataResponse)
def get_model_metadata():
    """
    Returns the metadata of the currently active ML model.
    """
    if not ml_models.model:
        raise HTTPException(status_code=404, detail="Model not loaded.")
        
    return ModelMetadataResponse(
        version=ml_models.model_version,
        last_trained=datetime.utcnow(), # Placeholder, ideally from model artifact
        accuracy=0.87, # Placeholder for current production accuracy metric
        features_used=[
            "weight_kg", 
            "shipping_cost", 
            "carrier_encoded", 
            "origin_encoded", 
            "destination_encoded", 
            "transport_mode_encoded"
        ]
    )

@router.get("/version")
def get_model_version():
    """
    Returns the current model version string.
    """
    return {"version": ml_models.model_version}

@router.get("/history", response_model=List[PredictionHistoryResponse])
def get_prediction_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves the prediction history.
    """
    history = db.query(PredictionHistory).order_by(PredictionHistory.created_at.desc()).offset(skip).limit(limit).all()
    return history

@router.get("/statistics", response_model=ModelStatisticsResponse)
def get_model_statistics(db: Session = Depends(get_db)):
    """
    Retrieves statistics about the model predictions and feedback loop.
    """
    total_preds = db.query(PredictionHistory).count()
    
    # Calculate avg predicted delay
    from sqlalchemy import func
    avg_delay = db.query(func.avg(PredictionHistory.predicted_delay_days)).scalar() or 0.0
    
    # Check retraining flags in decisions
    from app.models.decision import Decision
    retraining_flags = db.query(Decision).filter(Decision.needs_retraining == True).count()
    
    return ModelStatisticsResponse(
        total_predictions=total_preds,
        avg_delay_predicted=avg_delay,
        retraining_flags_raised=retraining_flags
    )
