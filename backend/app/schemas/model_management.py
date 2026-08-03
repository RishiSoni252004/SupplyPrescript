from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class PredictionHistoryBase(BaseModel):
    shipment_id: int
    predicted_delay_days: float
    model_version: str
    features_json: Optional[str] = None

class PredictionHistoryResponse(PredictionHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ModelMetadataResponse(BaseModel):
    version: str
    last_trained: datetime
    accuracy: float
    features_used: List[str]

class ModelStatisticsResponse(BaseModel):
    total_predictions: int
    avg_delay_predicted: float
    retraining_flags_raised: int
