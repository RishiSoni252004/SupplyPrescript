from pydantic import BaseModel
from typing import List, Optional

class PredictionRequest(BaseModel):
    supplier: str
    origin: str
    destination: str
    transport_mode: str
    distance_km: float
    shipping_cost: float
    weather_condition: str
    traffic_level: str
    order_priority: str
    expected_delivery_days: int

class PredictionResponse(BaseModel):
    prediction: str
    delay_probability: float
    confidence: str

class ModelInfoResponse(BaseModel):
    model_name: str
    algorithm: str
    features_used: List[str]
    status: str
