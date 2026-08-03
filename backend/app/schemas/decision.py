from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DecisionBase(BaseModel):
    shipment_id: int = Field(..., description="Foreign key to the shipment this decision applies to")
    selected_option: str = Field(..., description="The option selected by the user/system")
    predicted_cost: float = Field(..., description="Predicted cost of the selected option")
    predicted_delay: float = Field(..., description="Predicted delay (days) of the selected option")
    status: Optional[str] = Field("executed", description="Status of the decision")

class DecisionCreate(DecisionBase):
    pass

class DecisionResponse(DecisionBase):
    id: int
    execution_time: datetime
    needs_retraining: bool

    class Config:
        orm_mode = True
        from_attributes = True

class AnalyticsSummary(BaseModel):
    total_decisions: int = Field(0, description="Total number of decisions executed")
    successful_recommendations: int = Field(0, description="Decisions where actual outcome met or beat predicted outcome")
    failed_recommendations: int = Field(0, description="Decisions where actual outcome was worse than predicted")
    average_savings: float = Field(0.0, description="Average cost savings across successful decisions")
    decision_roi: float = Field(0.0, description="Overall Return on Investment based on decisions")
    accuracy_percentage: float = Field(0.0, description="Percentage of successful recommendations")

class FeedbackLog(BaseModel):
    decision_id: int
    shipment_id: int
    cost_variance: float
    delay_variance: float
    marked_for_retraining: bool
    status_updated_to: str
